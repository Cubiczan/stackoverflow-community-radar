"""Parse Ramanujan notebook PDFs with LlamaParse (llama-cloud SDK)."""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

from dotenv import load_dotenv
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, TimeElapsedColumn

ROOT = Path(__file__).resolve().parents[1]
load_dotenv(ROOT / ".env")

console = Console()

# Map local PDFs -> stable volume ids (Berndt Springer edition)
NOTEBOOKS = [
    {
        "id": "part-1",
        "title": "Ramanujan's Notebooks, Part I (Berndt, 1985)",
        "glob": "pdfcoffee.com_ramanujanx27s-notebooks-part-1-of-5*.pdf",
    },
    {
        "id": "part-2",
        "title": "Ramanujan's Notebooks, Part II",
        "glob": "pdfcoffee.com_ramanujanx27s-notebooks-part-2-of-5*.pdf",
    },
    {
        "id": "part-3",
        "title": "Ramanujan's Notebooks, Part III",
        "glob": "dokumen.pub_ramanujans-notebooks-part-iii*.pdf",
    },
    {
        "id": "part-4",
        "title": "Ramanujan's Notebooks, Part IV",
        "glob": "pdfcoffee.com_ramanujanx27s-notebooks-part-4-of-5*.pdf",
    },
    {
        "id": "part-5",
        "title": "Ramanujan's Notebooks, Part V",
        "glob": "pdfcoffee.com_ramanujanx27s-notebooks-part-5-of-5*.pdf",
    },
]


def resolve_pdf(spec: dict) -> Path:
    matches = sorted(ROOT.glob(spec["glob"]))
    if not matches:
        raise FileNotFoundError(f"No PDF for {spec['id']}: {spec['glob']}")
    return matches[0]


def out_dir(volume_id: str) -> Path:
    d = ROOT / "data" / "parsed" / volume_id
    d.mkdir(parents=True, exist_ok=True)
    return d


def already_done(volume_id: str) -> bool:
    meta = out_dir(volume_id) / "job.json"
    md = out_dir(volume_id) / "full.md"
    return meta.exists() and md.exists() and md.stat().st_size > 0


def write_markdown(result, path: Path) -> int:
    """Concatenate page markdown; return page count."""
    pages = []
    md_view = getattr(result, "markdown", None)
    if md_view is not None and getattr(md_view, "pages", None):
        for i, page in enumerate(md_view.pages, start=1):
            text = getattr(page, "markdown", None) or getattr(page, "text", None) or ""
            pages.append(f"\n\n<!-- page {i} -->\n\n{text}")
    elif isinstance(result, dict):
        for i, page in enumerate(result.get("markdown", {}).get("pages", []), start=1):
            pages.append(f"\n\n<!-- page {i} -->\n\n{page.get('markdown', '')}")
    else:
        # Fallback: stringify
        pages.append(str(result))

    path.write_text("".join(pages).lstrip() + "\n", encoding="utf-8")
    return max(len(pages), 1)


def parse_one(client, volume: dict, *, force: bool, tier: str) -> dict:
    volume_id = volume["id"]
    dest = out_dir(volume_id)

    if already_done(volume_id) and not force:
        console.print(f"[yellow]skip[/yellow] {volume_id} (already parsed)")
        return {"id": volume_id, "status": "skipped"}

    pdf = resolve_pdf(volume)
    console.print(f"[bold]Parsing[/bold] {volume_id}: {pdf.name} ({pdf.stat().st_size / 1e6:.1f} MB)")

    t0 = time.time()
    file_obj = client.files.create(file=pdf, purpose="parse")
    file_id = file_obj.id if hasattr(file_obj, "id") else file_obj["id"]

    # Prefer high-quality parse for math-heavy scanned books
    result = client.parsing.parse(
        file_id=file_id,
        tier=tier,
        version="latest",
        expand=["markdown", "text", "metadata"],
    )

    page_count = write_markdown(result, dest / "full.md")

    # Persist raw-ish metadata for resume / KG linking
    job_id = getattr(result, "id", None) or getattr(result, "job_id", None)
    meta = {
        "volume_id": volume_id,
        "title": volume["title"],
        "source_pdf": pdf.name,
        "source_bytes": pdf.stat().st_size,
        "file_id": file_id,
        "job_id": job_id,
        "tier": tier,
        "page_count_written": page_count,
        "parsed_at": datetime.now(timezone.utc).isoformat(),
        "elapsed_sec": round(time.time() - t0, 1),
    }
    (dest / "job.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")

    # Optional: dump text view if present
    text_view = getattr(result, "text", None)
    if text_view is not None and getattr(text_view, "pages", None):
        chunks = []
        for i, page in enumerate(text_view.pages, start=1):
            chunks.append(f"\n\n<!-- page {i} -->\n\n{getattr(page, 'text', '')}")
        (dest / "full.txt").write_text("".join(chunks).lstrip() + "\n", encoding="utf-8")

    console.print(
        f"[green]done[/green] {volume_id}: {page_count} pages in {meta['elapsed_sec']}s -> {dest}"
    )
    return {"id": volume_id, "status": "ok", **meta}


def main() -> int:
    parser = argparse.ArgumentParser(description="Parse Ramanujan notebooks via LlamaParse")
    parser.add_argument("--only", nargs="*", help="Volume ids to parse, e.g. part-1 part-3")
    parser.add_argument("--force", action="store_true", help="Re-parse even if output exists")
    parser.add_argument(
        "--tier",
        default=os.getenv("LLAMA_PARSE_TIER", "agentic"),
        help="Parse tier (default: agentic — best for math OCR)",
    )
    args = parser.parse_args()

    api_key = os.getenv("LLAMA_CLOUD_API_KEY")
    if not api_key:
        console.print("[red]Missing LLAMA_CLOUD_API_KEY in .env[/red]")
        return 1

    try:
        from llama_cloud import LlamaCloud
    except ImportError:
        console.print("[red]Install deps: pip install -r requirements.txt[/red]")
        return 1

    client = LlamaCloud(api_key=api_key)

    volumes = NOTEBOOKS
    if args.only:
        wanted = set(args.only)
        volumes = [v for v in NOTEBOOKS if v["id"] in wanted]
        missing = wanted - {v["id"] for v in volumes}
        if missing:
            console.print(f"[red]Unknown volume ids: {sorted(missing)}[/red]")
            return 1

    summary = []
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        TimeElapsedColumn(),
        console=console,
    ) as progress:
        task = progress.add_task("LlamaParse batch", total=len(volumes))
        for volume in volumes:
            progress.update(task, description=f"Parsing {volume['id']}…")
            try:
                summary.append(parse_one(client, volume, force=args.force, tier=args.tier))
            except Exception as exc:  # noqa: BLE001 — surface API errors, continue batch
                console.print(f"[red]FAIL[/red] {volume['id']}: {exc}")
                summary.append({"id": volume["id"], "status": "error", "error": str(exc)})
            progress.advance(task)

    manifest_path = ROOT / "data" / "parsed" / "manifest.json"
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(
        json.dumps(
            {
                "generated_at": datetime.now(timezone.utc).isoformat(),
                "volumes": summary,
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    console.print(f"\nManifest -> {manifest_path}")
    ok = sum(1 for s in summary if s.get("status") in {"ok", "skipped"})
    console.print(f"Completed {ok}/{len(summary)} volumes")
    return 0 if ok == len(summary) else 2


if __name__ == "__main__":
    sys.exit(main())
