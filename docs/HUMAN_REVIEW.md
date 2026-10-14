# Human Evidence Review

## 1. Review Information

**Course:** CYBERSEC 590 – Assignment 2  
**Case ID:** SMB-SIGNING-FILE04  
**Project Type:** Individual Project  
**Reviewer:** Project Author (Self-Review)  
**Review Date:** October 14, 2026  
**Review Status:** Completed

## 2. Evidence Review

I checked the environment data and compared it with the agent's final assessment. My main goal was to see whether the agent used the correct evidence and whether its risk decision made sense.

| Evidence | What I Checked | Result |
|---|---|---|
| S02 | Network restrictions and SMB access | Pass |
| S03 | FILE04 SMB signing settings | Pass |
| S05 | Possible business impact | Pass |
| EXT01 | Microsoft SMB signing documentation | Pass |

### S02 – Network Security

The environment data shows that public SMB access is not allowed and the network uses a default-deny policy for unlisted traffic between zones.

The agent also mentions that internal SMB access is still unknown. I think this is correct because the network rules do not tell us whether FILE04 can be reached from another internal machine.

**Result:** Pass

### S03 – SMB Configuration

FILE04 is running Windows Server 2022, and SMB signing is not required. SMB1 is also disabled on the W05 file servers.

The agent correctly identifies the SMB signing setting as a possible security risk. However, it does not assume that an SMB relay attack will definitely work.

**Result:** Pass

### S05 – Business Impact

The environment data mentions that file service problems could interrupt work or expose confidential information. It also gives an RTO of 24 hours and an RPO of 8 hours.

However, we do not know what files are stored on FILE04 or how important they are. Because of this, I agree that the business impact is still unknown.

**Result:** Pass

### EXT01 – Microsoft Reference

**Source:** Microsoft Learn  
**Link:** https://learn.microsoft.com/en-us/windows-server/storage/file-server/smb-signing-overview

I checked the Microsoft documentation about SMB signing. It explains how SMB signing helps prevent relay attacks.

One important point is that SMB signing can be required by either the client or the server. This means FILE04 not requiring signing does not automatically mean its SMB connections are unsigned.

The agent uses this information correctly and does not treat the documentation as proof that FILE04 can be attacked.

**Result:** Pass

## 3. Risk Assessment Review

I also checked the main fields in the agent's output.

| Field | Agent Output |
|---|---|
| Applicability | Potential |
| Impact | Unknown |
| Decision | Insufficient Evidence |
| Policy Rule | P1: Decisive evidence missing |

I agree with the final decision.

The environment shows that FILE04 does not require SMB signing, so there is a possible risk. However, there is not enough information to confirm whether an SMB relay attack is possible.

For example, we still do not know:

1. Whether an attacker could reach FILE04 through the internal network.
2. Whether the NTLM relay requirements are met.
3. Whether SMB signing is actually used during connections.
4. What types of files are stored on FILE04 and how serious the impact could be.

Because the applicability is only potential and the impact is unknown, **Insufficient Evidence** matches the risk policy used in this project.

**Review Result:** Pass

## 4. Recommendations

Based on the current results, I would recommend the following steps:

1. Check the actual SMB signing settings on FILE04 and its clients.
2. Check internal network access and the requirements for NTLM relay attacks.
3. Review FILE04's shared folders and access permissions.
4. Enable required SMB signing if it is compatible with the environment.
5. Run the risk assessment again after collecting more evidence.

## 5. Limitations

This project uses a simulated company environment, so the results do not represent a real security assessment.

The Microsoft documentation provides technical information about SMB signing, but it cannot confirm whether FILE04 is vulnerable.

I did not perform any penetration testing or try to exploit the SMB configuration.

Since this is an individual project, I reviewed the evidence myself. There was no separate team member to review the results.

## 6. Final Review

| Review Item | Result |
|---|---|
| Evidence matches environment data | Pass |
| Sources are correctly identified | Pass |
| Risk decision follows the policy | Pass |
| Unknown information is explained | Pass |

**Reviewer:** Project Author  
**Review Date:** October 14, 2026  
**Self-Review Status:** Completed  
**Final Result:** Approved

### Final Comments

After comparing the environment data with the agent's output, I did not find any major inconsistencies.

The agent correctly identified the SMB signing issue on FILE04, but it also explained what information was missing.

I agree with the **Insufficient Evidence** decision because the available evidence is not enough to confirm the attack conditions or the possible impact.

Overall, I think the agent handled this case correctly based on the information provided.