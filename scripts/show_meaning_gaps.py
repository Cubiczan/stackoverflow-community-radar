import json
from pathlib import Path

hits = json.loads(Path("data/kg/mined_hits.json").read_text(encoding="utf-8"))
mg = [h for h in hits if h.get("priority") == "meaning_gap"]
print(f"meaning_gap {len(mg)} / total {len(hits)}")
for h in mg:
    span = h["span"][:280].replace("\n", " ")
    print(f"{h['volume_id']} p{h.get('page')}: [{h['cue']}] {span}...")
