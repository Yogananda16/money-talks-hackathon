import json

with open("../security_profile.json") as f:
    profile = json.load(f)

with open("../questions.json") as f:
    questions = {str(q["id"]): {"text": q["question"], "topic": q["topic"]} for q in json.load(f)}

lines = ["# Security Questionnaire — Completed Report\n"]
lines.append("**Legend:** ✅ Verified (from documents) | 💬 Confirmed (employee) | ❓ Unknown\n")

current_topic = None
for qid in sorted(profile.keys(), key=int):
    q = questions[qid]
    p = profile[qid]

    if q["topic"] != current_topic:
        current_topic = q["topic"]
        lines.append(f"\n## {current_topic}\n")

    icon = {"verified": "✅", "confirmed": "💬", "unknown": "❓"}.get(p["status"], "❓")
    lines.append(f"**Q{qid}. {q['text']}**")
    lines.append(f"{icon} {p['status'].upper()}")
    if p.get("answer"):
        lines.append(f"> {p['answer']}")
    if p.get("source"):
        lines.append(f"*Source: {p['source']}*")
    lines.append("")

lines.append("\n## ⚠️ Conflicts Detected\n")
lines.append("**Business Continuity & Disaster Recovery (Q41/Q42)**")
lines.append("The approved BC/DR Policy states backups are **not** replicated to a second geographic region and that **no recovery test has ever been performed**. The SOC 2 report, however, claims automated backups **with cross-region replication** and implies completed recovery testing via AWS multi-AZ architecture.")
lines.append("")
lines.append("*Recommended action: verify actual AWS backup configuration and reconcile the BC/DR Policy with the SOC 2 report before submitting either as authoritative.*")
lines.append("")

with open("../FINAL_REPORT.md", "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

verified = sum(1 for p in profile.values() if p["status"] == "verified")
confirmed = sum(1 for p in profile.values() if p["status"] == "confirmed")
unknown = sum(1 for p in profile.values() if p["status"] == "unknown")
print(f"Report generated: {verified} verified, {confirmed} confirmed, {unknown} unknown")
print("Saved to FINAL_REPORT.md")