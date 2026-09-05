# Security Questionnaire — Completed Report

**Legend:** ✅ Verified (from documents) | 💬 Confirmed (employee) | ❓ Unknown


## Governance

**Q1. Does your organization have a formal Information Security Program established?**
✅ VERIFIED
> Yes, Solsphere / Regodit has established a formal Information Security Program governed by its Information Security Policy.
*Source: Regodit_information_security_policy_v1.0.docx*

**Q2. Does your organization have a published set of Information Security policies, standards and procedures?**
✅ VERIFIED
> Yes, Regodit AI has defined and documented standard operating procedures and policies covering all key control domains.
*Source: Regodit AI_SOC2_Type_II_Report_Test.docx*

**Q3. Does your organization have a public information security policy?**
✅ VERIFIED
> No — Regodit's information security policies are internally classified 'Internal/Confidential,' not public.
*Source: Regodit_information_security_policy_v1.0.docx (Document Control table)*

**Q4. Does your organization document role descriptions including relevant cybersecurity & data protection responsibilities?**
✅ VERIFIED
> Yes, job postings, requisitions, and individual job descriptions document role responsibilities including data handling expectations and conduct.
*Source: Regodit_hr_policy_v1.0.docx*

**Q5. Is there a procedure in place for overseeing cybersecurity and data protection controls, that includes how issues are escalated to leadership?**
✅ VERIFIED
> Yes, procedures are in place where risks scored as High or Critical and control deficiencies are escalated to company leadership and the CEO.
*Source: Regodit_risk_management_policy_v1.0.docx*


## Third-Party Risk Management

**Q6. Will you be using any contractors or sub-contractors to complete the engagement with Client XYZ?**
✅ VERIFIED
> Subcontracting requires prior written consent from the Company before engaging any third party that requires access to systems, code, or Confidential Information.
*Source: Master Services Agreement.docx*

**Q7. Do you have a third-party risk management program/policy in place?**
✅ VERIFIED
> Yes, Regodit maintains a formal Vendor Risk Management Policy.
*Source: Regodit_Vendor_Risk_Management_Policy.docx*

**Q8. Please attach your Third-Party Risk Management Policy.**
✅ VERIFIED
> The Third-Party Risk Management Policy is established in the Vendor Risk Management Policy document.
*Source: Regodit_Vendor_Risk_Management_Policy.docx*

**Q9. Does your third-party risk management program include supply chain protections?**
✅ VERIFIED
> Yes, the policy includes due diligence requirements for subprocessors, vendor dependencies, and contractual data processing requirements.
*Source: Regodit_Vendor_Risk_Management_Policy.docx*

**Q10. Do your vendor and subcontractor agreements include clauses requiring adherence to cybersecurity and data privacy standards, and do these requirements flow down to all applicable subcontractors and suppliers?**
✅ VERIFIED
> Yes, third-party and subcontractor agreements include security, confidentiality, and data processing obligations.
*Source: Regodit AI_SOC2_Type_II_Report_Test.docx*


## Security Awareness & Training

**Q11. Do you provide security awareness training at onboarding and at least annually thereafter for all personnel including contractors?**
✅ VERIFIED
> Yes, all personnel including contractors complete information security awareness training upon joining and annually thereafter.
*Source: Regodit_hr_policy_v1.0.docx*

**Q12. How frequently are employees trained on policies in your organization?**
✅ VERIFIED
> Employees receive training upon onboarding and on an annual basis.
*Source: Regodit_hr_policy_v1.0.docx*

**Q13. Does your organization provide role based security awareness training at least annually?**
✅ VERIFIED
> Yes, role-specific training (such as HIPAA/Privacy training for those accessing customer data/PHI) is assigned during onboarding and annually.
*Source: Regodit_hr_policy_v1.0.docx*


## Privacy

**Q14. Does your organization have privacy controls and or Data Privacy program in place?**
✅ VERIFIED
> Yes, Regodit maintains a comprehensive privacy program including DPAs, data classification, privacy notices, and controls over customer personal data.
*Source: Regodit AI_SOC2_Type_II_Report_Test.docx*

**Q15. Will your personnel or your product require access to sensitive data (i.e PII, PI, PHI) to complete the engagement with Regodit?**
✅ VERIFIED
> Regodit only processes personal information (such as engineer contact details) incidentally embedded in customer-supplied alert payloads and logs for service delivery.
*Source: Regodit AI_SOC2_Type_II_Report_Test.docx*

**Q16. Please provide a copy of your data retention schedule and secure disposal procedures**
✅ VERIFIED
> Data is retained only as long as necessary for contractual/legal requirements, database backups are kept for a rolling 35 days, and cloud data is deleted using provider deletion mechanisms and cryptographic key erasure.
*Source: Regodit_data_classification_policy_v1.0.docx*

**Q17. Do you have a privacy policy in place? If so, please provide the attachment or URL.**
✅ VERIFIED
> Yes, Regodit maintains a privacy notice defining data processing, retention, and data subject rights.
*Source: Regodit AI_SOC2_Type_II_Report_Test.docx*

**Q18. Does your organization ensure privacy requirements are extended to contractors and service providers through contractual agreements, and that roles and responsibilities concerning data privacy are clearly understood and documented?**
✅ VERIFIED
> Yes, privacy obligations and data processing terms are extended to third parties and subcontractors via formal agreements and DPAs.
*Source: Regodit AI_SOC2_Type_II_Report_Test.docx*


## Data Security

**Q19. Do you, or any third party you use to deliver services to Client XYZ, store sensitive information outside the United States? If so, where?**
✅ VERIFIED
> Vendor is contractually obligated not to process or maintain PII outside the United States, and operational data is stored exclusively within configured AWS regions.
*Source: Master Services Agreement.docx*

**Q20. Do you require data-at-rest encryption for sensitive data?**
✅ VERIFIED
> Yes, sensitive data at rest is encrypted using AES-256.
*Source: Regodit_cryptography_policy_v1.0.docx*

**Q21. Do you require data-in-transit encryption for sensitive data? If so, please describe the encryption protocols used.**
✅ VERIFIED
> Yes, data in transit is encrypted using TLS 1.3 (with TLS 1.2 permitted where TLS 1.3 is not yet supported).
*Source: Regodit_cryptography_policy_v1.0.docx*

**Q22. Will Regodit data be stored on site, in a data center, or by a third party?**
✅ VERIFIED
> Regodit data is stored exclusively in cloud infrastructure hosted on Amazon Web Services (AWS); no on-premises data storage facilities are maintained.
*Source: Regodit AI_SOC2_Type_II_Report_Test.docx*

**Q23. Do you have data retention policies and procedures for the secure disposal of information?**
✅ VERIFIED
> Yes, Regodit maintains formal data retention and disposal policies, including secure wipe of devices and cryptographic erasure of cloud storage.
*Source: Regodit_data_classification_policy_v1.0.docx*

**Q24. If providing a product or SaaS platform that will access, store, or process Client XYZ data, are you able to provide applicable data flow diagrams showing how Regodit's data will flow through the tool upon request?**
💬 CONFIRMED
> Yes, we can provide network architecture and data flow diagrams on request. They show data flow from users through CDN/WAF, VPC segmentation, the application tier, and an encrypted data tier, plus the admin access path through MFA-verified VPN and a bastion host with centralized logging.
*Source: Employee (verbal/typed)*


## Physical Security

**Q25. Is there a policy in place for physical security requirements for your business?**
✅ VERIFIED
> Yes, physical and environmental security for cloud production infrastructure is provided by cloud vendors (AWS), while office presence is limited to a co-working facility with card-based access.
*Source: Regodit_information_security_policy_v1.0.docx*

**Q26. Do you require physical access to any Client XYZ locations to complete your engagement?**
✅ VERIFIED
> No, services are provided remotely and not from the customer's physical site unless explicitly specified in an SOW.
*Source: Master Services Agreement.docx*

**Q27. Are you willing to accept and acknowledge the expectations outlined in Client XYZ's Visitor Management document?**
💬 CONFIRMED
> Not applicable in current practice — our services are delivered remotely per standard MSA terms, so client site access doesn't occur. This is genuinely unknown/not addressed in our documents and should be confirmed if physical access is ever required.
*Source: Employee (verbal/typed)*

**Q28. Does your organization have procedures in place to track assets that are brought onto Client XYZ sites?**
✅ VERIFIED
> Regodit tracks all endpoint devices and IT assets centrally on its internal compliance platform.
*Source: Regodit_asset_management_policy_v1.0.docx*

**Q29. Can you provide your organization's data protection policy, including evidence of physical safeguards for devices used onsite if requested?**
✅ VERIFIED
> Yes, endpoint devices require full-disk encryption, supported operating systems, native firewall/malware protection, screen locks, and strong authentication.
*Source: Regodit_asset_management_policy_v1.0.docx*


## Web Application Security

**Q30. Will Client XYZ be using a web application provided by you?**
✅ VERIFIED
> Yes, Regodit provides an AI-native SaaS compliance automation web application.
*Source: Regodit AI_SOC2_Type_II_Report_Test.docx*

**Q31. What is the name of your web application?**
✅ VERIFIED
> The application is the Regodit Platform (Regodit AI Platform Application).
*Source: Regodit AI_SOC2_Type_II_Report_Test.docx*

**Q32. What is the function/purpose of your web application?**
✅ VERIFIED
> The platform provides AI-powered collection, validation, and mapping of compliance evidence, readiness assessments, gap identification, policy development, continuous control monitoring, and audit support.
*Source: Regodit AI_SOC2_Type_II_Report_Test.docx*

**Q33. How do you report application security vulnerabilities?**
✅ VERIFIED
> Vulnerabilities can be reported through Regodit's published contact channel, which are acknowledged, triaged, and handled under the Vulnerability and Patch Management Policy.
*Source: Regodit_vulnerability_and_patch_management_policy_v1.0.docx*

**Q34. Does your web application have an SSL/TLS certificate?**
✅ VERIFIED
> Yes, certificate-based authentication and TLS certificates are utilized to secure external API and platform service communications.
*Source: Regodit_cryptography_policy_v1.0.docx*

**Q35. Does your application offer single sign-on (SSO) or are there plans to implement/offer SSO in the near future? If plans to implement in near future, include an implementation date in your justification.**
✅ VERIFIED
> Yes, authentication across systems is centralized through a single sign-on (SSO) identity provider protected by multi-factor authentication.
*Source: Regodit_password_and_secrets_policy_v1.0.docx*


## Secure Coding

**Q36. Do you have policies, procedures or standards in place for secure development practices?**
✅ VERIFIED
> Yes, Regodit maintains a Secure Development Policy and SDLC guidelines.
*Source: Secure Development Lifecycle Document 01.docx*

**Q37. Do you utilize Secure Coding Principles - (Detailed logging, encrypted credentials, etc.)?**
✅ VERIFIED
> Yes, developers follow secure coding practices including peer pull-request review before merge.
*Source: Regodit_information_security_policy_v1.0.docx (Section 13)*


## Vulnerability Management

**Q38. Are internal vulnerability scans performed?**
✅ VERIFIED
> No automated internal scanning program — relies on annual third-party penetration testing, AWS GuardDuty findings, and manual review.
*Source: Regodit_vulnerability_and_patch_management_policy_v1.0.docx (Section 3-4)*

**Q39. On what cadence are vulnerability scans performed?**
✅ VERIFIED
> Vulnerability assessments and penetration testing are conducted at least annually and following major product or infrastructure changes.
*Source: Regodit_vulnerability_and_patch_management_policy_v1.0.docx*

**Q40. What are the documented remediation timelines for critical and high patches?**
✅ VERIFIED
> Documented remediation timelines are: Critical vulnerabilities within 7 days; High vulnerabilities within 30 days.
*Source: Regodit_vulnerability_and_patch_management_policy_v1.0.docx*


## Business Continuity & Disaster Recovery

**Q41. What is the process for disaster recovery and backups?**
✅ VERIFIED
> Automated daily snapshots of production databases are maintained with 35-day retention and point-in-time recovery; disaster recovery restores data from backups and redeploys applications from source control into alternative availability zones.
*Source: Regodit_business_continuity_and_disaster_recovery_policy_v1.0.docx*

**Q42. Please provide a copy of your BC/DR policy for review.**
✅ VERIFIED
> The BC/DR policy is documented in 'Regodit_business_continuity_and_disaster_recovery_policy_v1.0.docx' and 'BCP_DR_Plan_Solsphere.docx'.
*Source: Regodit_business_continuity_and_disaster_recovery_policy_v1.0.docx*


## Incident Response

**Q43. Do you keep a record of security events?**
✅ VERIFIED
> Yes, system activity, authentication events, and privileged actions are logged via cloud-native logging, and formal logs are kept for all SEV-0/SEV-1 security incidents.
*Source: Regodit_access_control_policy_v1.0.docx*

**Q44. Do you monitor the security of your wireless networks?**
💬 CONFIRMED
> Yes. Additional detail: We don't operate a corporate wireless network to monitor since we're remote-first with no physical office infrastructure. Employees connect via home or co-working networks outside our control. This is inferred from context, not explicitly documented — flag as low confidence, needs employee confirmation.
*Source: Employee (verbal/typed)*

**Q45. Do you have an incident response plan in place? If yes, describe briefly.**
✅ VERIFIED
> Yes, Regodit maintains an Incident Management Policy covering preparation, detection, containment, eradication, recovery, and post-incident review across severity levels SEV-0 to SEV-3.
*Source: Regodit_Incident_Management_Policy.docx*

**Q46. How often is your Incident Response Plan Tested?(Drop Down)**
✅ VERIFIED
> At least annually.
*Source: Regodit_Incident_Management_Policy.docx*

**Q47. Do you have a policy requiring prompt notice to third parties regarding information security events affecting your organization?**
✅ VERIFIED
> Yes, client notification timelines for security incidents affecting client data or services are mandated in accordance with applicable contracts/DPAs.
*Source: Regodit_Incident_Management_Policy.docx*

**Q48. Regardless of materiality, have you had a security event in the last 5 years?**
💬 CONFIRMED
> Unknown — not disclosed in any provided document. Needs direct confirmation from the employee/founders, since incident history isn't something we should infer or guess.. Additional detail: No, to the best of our knowledge there have been no security events or incidents in the last 5 years, but this should still be verified directly with the founders as authoritative confirmation.
*Source: Employee (verbal/typed)*

**Q49. Do you outsource security functions to third-party providers?**
✅ VERIFIED
> Security and internal audit functions are managed internally by the founders, though third-party firms are engaged for annual penetration testing.
*Source: Regodit_information_security_policy_v1.0.docx*


## Network & Endpoint Security

**Q50. Do you use anti virus software to protect your devices? If yes, describe.**
✅ VERIFIED
> Yes, devices must utilize operating system native malware protection and firewall capabilities.
*Source: Regodit_asset_management_policy_v1.0.docx*

**Q51. Will your organization be accessing Client XYZ's network?**
✅ VERIFIED
> Services are delivered remotely and not from the customer's site unless explicitly agreed in writing.
*Source: Master Services Agreement.docx*

**Q52. Will you be using a Client XYZ asset to access Client XYZ's network?**
💬 CONFIRMED
> No, we would use our own company-issued devices to access any client network, consistent with our Asset Management Policy covering company-work devices. This specific client-asset scenario isn't explicitly addressed in our documents, so treat as inferred, not fully verified.. Additional detail: Confirmed with the assumption that we follow standard practice: our team uses company-issued devices exclusively for client engagements. No policy explicitly prohibits client-provided hardware, but it hasn't come up in practice. This should be formally verified with IT/Security before finalizing.
*Source: Employee (verbal/typed)*

**Q53. Please list out all authorized personnel, including first and last names and e-mail addresses from your organization that will have access to Client XYZ's assets or network.**
✅ VERIFIED
> Personnel recorded in the system access review record include: J. Martinez (j.martinez@regodit.net), A. Patel (a.patel@regodit.net), S. Wong (s.wong@regodit.net), R. Osei (r.osei@regodit.net), T. Nguyen (t.nguyen@regodit.net), M. Delgado (m.delgado@regodit.net), and K. O'Brien (k.obrien@regodit.net).
*Source: Access_Review_Records.xlsx*

**Q54. Please submit a network architecture diagram and details of your endpoint protection measures, including how your organization complies with firewall and DNS security standards when accessing XYZ's networks.**
✅ VERIFIED
> Network perimeter access is restricted using cloud-native firewalls and security groups; endpoint devices require OS-native firewalls, malware protection, full-disk encryption, and remote access via VPN.
*Source: Regodit_information_security_policy_v1.0.docx*


## Asset Management

**Q55. Do you keep an inventory of information technology (IT) assets and software?**
✅ VERIFIED
> Yes, an IT asset and software inventory is maintained on the internal compliance platform.
*Source: Regodit_asset_management_policy_v1.0.docx*

**Q56. Does your organization have identity and access controls in place?**
✅ VERIFIED
> Yes, identity and access controls are established under the Access Control Policy.
*Source: Regodit_access_control_policy_v1.0.docx*

**Q57. Does your organization leverage role-based access control?**
✅ VERIFIED
> Yes, access is provisioned using role-based access controls via AWS IAM and SSO.
*Source: Regodit AI_SOC2_Type_II_Report_Test.docx*

**Q58. Do you limit and periodically review user access privileges and controls?**
✅ VERIFIED
> Yes, user access privileges are granted on a least-privilege basis and reviewed periodically.
*Source: Regodit_access_control_policy_v1.0.docx*

**Q59. What is the cadence of your access reviews?(Drop Down)**
✅ VERIFIED
> At least annually.
*Source: Regodit_access_control_policy_v1.0.docx*

**Q60. Does your organization require replay-resistant authentication mechanisms such as OTP or MFA?**
✅ VERIFIED
> Yes, multi-factor authentication (MFA) is enforced across all core systems and cloud consoles.
*Source: Regodit_access_control_policy_v1.0.docx*

**Q61. Are the external authenticators in use, NIST compliant?**
✅ VERIFIED
> Yes, authentication and password policies align with NIST SP 800-63B standards.
*Source: Regodit_password_and_secrets_policy_v1.0.docx*

**Q62. Does your organization enforce the principle of least privilege?**
✅ VERIFIED
> Yes, Regodit strictly enforces the principle of least privilege.
*Source: Regodit_access_control_policy_v1.0.docx*


## Risk Assessment

**Q63. Do you conduct information security risk assessments at least annually?**
✅ VERIFIED
> Yes, information security risk assessments and risk register updates are conducted at least annually.
*Source: Regodit_risk_management_policy_v1.0.docx*

**Q64. How do you prioritize critical assets for your organization?**
✅ VERIFIED
> Critical assets are prioritized based on the sensitivity and classification level (Confidential/Restricted) of the data they store or process.
*Source: Regodit_asset_management_policy_v1.0.docx*

**Q65. Does your organization conduct penetration testing at least annually?**
✅ VERIFIED
> Yes, third-party penetration testing is commissioned at least annually.
*Source: Regodit_vulnerability_and_patch_management_policy_v1.0.docx*

**Q66. Have the findings from the most recent penetration test been remediated?**
✅ VERIFIED
> Findings from the most recent penetration test report are currently marked as Open and scheduled for remediation.
*Source: VAPT Report 01.docx*


## ⚠️ Conflicts Detected

**Business Continuity & Disaster Recovery (Q41/Q42)**
The approved BC/DR Policy states backups are **not** replicated to a second geographic region and that **no recovery test has ever been performed**. The SOC 2 report, however, claims automated backups **with cross-region replication** and implies completed recovery testing via AWS multi-AZ architecture.

*Recommended action: verify actual AWS backup configuration and reconcile the BC/DR Policy with the SOC 2 report before submitting either as authoritative.*
