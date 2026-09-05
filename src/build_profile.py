import json

with open("../profile.json") as f:
    raw = json.load(f)

profile = {}
for item in raw:
    profile[item["id"]] = {
        "question_id": item["id"],
        "answer": item["answer"] if item["found"] else None,
        "status": "verified" if item["found"] else "unknown",
        "evidence": item.get("evidence") or None,
        "source": item.get("source") or None,
        "confidence": "high" if item["found"] else None
    }

unknowns = [pid for pid, p in profile.items() if p["status"] == "unknown"]

with open("../security_profile.json", "w") as f:
    json.dump(profile, f, indent=2)

print(f"Profile built. {len(profile) - len(unknowns)} verified, {len(unknowns)} unknown.")
print(f"Unknown IDs: {unknowns}")