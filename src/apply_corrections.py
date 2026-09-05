import json

with open("../security_profile.json") as f:
    profile = json.load(f)

profile["3"]["answer"] = "No — Regodit's information security policies are internally classified 'Internal/Confidential,' not public."
profile["3"]["evidence"] = "Document Control tables classify all policies as Internal / Confidential."
profile["3"]["source"] = "Regodit_information_security_policy_v1.0.docx (Document Control table)"
profile["3"]["status"] = "verified"

profile["37"]["answer"] = "Yes, developers follow secure coding practices including peer pull-request review before merge."
profile["37"]["evidence"] = "Source code is managed in a version-control platform, and changes require peer pull-request review before merge; developers follow secure coding practices."
profile["37"]["source"] = "Regodit_information_security_policy_v1.0.docx (Section 13)"
profile["37"]["status"] = "verified"

profile["38"]["answer"] = "No automated internal scanning program — relies on annual third-party penetration testing, AWS GuardDuty findings, and manual review."
profile["38"]["evidence"] = "The company does not currently operate automated vulnerability scanning or an automated patch-management platform."
profile["38"]["source"] = "Regodit_vulnerability_and_patch_management_policy_v1.0.docx (Section 3-4)"
profile["38"]["status"] = "verified"

for qid in ["27", "44", "52"]:
    profile[qid]["answer"] = None
    profile[qid]["status"] = "unknown"
    profile[qid]["evidence"] = None
    profile[qid]["source"] = None
    profile[qid]["confidence"] = None

with open("../security_profile.json", "w") as f:
    json.dump(profile, f, indent=2)

print("Corrections applied to Q3, Q37, Q38. Q27, Q44, Q52 reset to unknown.")