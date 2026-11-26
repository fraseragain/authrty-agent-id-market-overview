# Chain-rubric scores, group 4: x401 and KYA-OS

Rubric: `ov/research/agent-protocol-comparison/chain-rubric.md` (10 links, 2 / 1 / 0; chain score = lowest link). Scored afresh from the primary text, read 25 Nov 2026.

Sources read:
- x401 Standard Draft 0.2.0: `spec.md` from github.com/proof/x401 (same text as x401.proof.com/spec/latest). Local copy: a local copy (not committed).
- KYA-OS v1.0.0: `SPEC.md`, `SPEC-ENTITY-CARD.md` (v1.1 profile), `SPEC-MCP-EXTENSION.md`, `SPEC-AUDIT-READ.md` (Draft) from github.com/decentralized-identity/kya-os-mcp (local copies in a local copy (not committed)), and `AUDITABILITY.md` (fetched to a local copy (not committed)). Optional profiles (Entity Card KYC/KYB, Audit Assurance Profile) are treated as partial, as instructed.

Scoring conventions used: a test counts as "met" for a 2 only if the core text makes it MUST. SHOULD, MAY, optional layers and optional profiles give 1 at most. Roadmap/open-question text gives 0.

---

# x401 (Standard Draft 0.2.0)

x401 is a route-scoped proof-requirement protocol. The Verifier challenges (`PROOF-REQUEST`), the Agent returns an OpenID4VP/DCQL Digital Credentials result (`PROOF-RESPONSE`), and an optional OAuth token exchange yields a Verification Token. Agent identification, agent authentication and delegation are explicitly optional or open questions.

| Link | Score | Tests met / not met | Citation |
|---|---|---|---|
| L1 Principal identity | 1 | P1 partial: the Verifier receives only the claims its DCQL query asks for, so identification is possible but not required, and the spec leans to minimal disclosure. P2 met: claims come from issuer-signed credentials; the Verifier MUST validate issuer trust, status, revocation (Verifier Processing Rules 9-10; Proof Validation 5-6). P3 partial: issuers are constrained by DCQL `trusted_authorities` (`openid_federation`, `etsi_tl`), but the Verifier SHOULD (not MUST) express them so, and the Verifier's own policy decides. | Terminology "Holder"; Credential Requirements (`dcql_query`, `assurance_level` example); Verifier Processing Rules 7, 10; Proof Validation 5-6; Security Considerations "Issuer Trust"; Privacy "Data Minimization" |
| L2 Operator identity | 1 | O1 partial only: `agent_id` (Agent Identifier) is OPTIONAL and may be a DID, HTTPS origin, domain-bound `client_id`, certificate-bound id or SPIFFE ID; the spec registers no scheme and the Verifier chooses. That identifies the calling agent, not an operator, and a domain with no attestation is partial. O2 not met (no operator verification). O3 not met. Score rests on an optional layer. | Result Artifact (`agent_id`, OPTIONAL); Agent Binding Options; Agent Identifier Schemes and HTTP-Layer Binding; Web Bot Auth (`Signature-Agent` key directory) |
| L3 Agent key binding | 1 | K1 partial: the base protocol binds the result to the Verifier, not to an agent key ("the result is not, by itself, bound to the Agent"). Optional layers can bind a key through an accountable third party (mTLS certificate-bound identifiers, SPIFFE SVIDs), or only by self-publication (Web Bot Auth key directory); none is required or profiled. K2 not met: no key validity-at-time-of-use or after-the-fact check for the agent key (only credential status for the Holder's credential). | Security Considerations "Agent Binding"; Agent Binding Options; OAuth Proof-of-Possession and Client Authentication; Workload Identity; Open Questions "Adding Agent Authentication" |
| L4 Delegation | 1 | D1 partial: the optional Verification Token records what the Verifier accepted (`scope`/`resource`, `x401_satisfied_requirements`, `x401_request_id`); it is not a grant by the principal of what the agent may do. D2 partial: scoped to audience, route, method, resource; no amount or payee. D3 not met: issued by the Verifier, not signed by the principal; principal delegation is an open question. D4 met for the token: MUST expire, SHOULD support revocation. | Verification Token Contents (items 2-4); Delegation and Actor Evidence; Open Questions "Fully Autonomous Delegation" |
| L5 Session authentication | 1 | S1 partial: optional only (Web Bot Auth HTTP Message Signatures, mTLS, DPoP, SPIFFE). S2 met for the credential result (OpenID4VP `nonce`, request `exp`; Proof Validation 4) and SHOULD-level for WBA freshness; DPoP on the Verification Token is not defined in 0.2.0 (Bearer only). S3 not met: the Holder authorises the Credential Manager to present, but no human-presence or assurance level is captured by the protocol. | Proof Validation 4; Security Considerations "Replay Prevention"; Web Bot Auth and HTTP Message Signatures; OAuth Proof-of-Possession (Bearer note); Terminology "Credential Manager" |
| L6 Action conformance | 1 | A1 partial: the retry carries the Result Artifact or Verification Token for the same route; the token names `request_id`, resource, method. It does not reference a grant for an action or transaction. A2 partial: the Verifier MUST check token scope, audience, expiry and any agent binding before serving (Verifier Processing Rule 13), but only against proof satisfaction, not against amount, payee or other grant constraints. | Verifier Processing Rules 13-14; Verification Token Contents; Reuse Across Routes; Payment Separation |
| L7 Evidence | 0 | E1 not met: no record of the action is defined. The Verification Token is a short-lived access token recording a proof-satisfaction decision ("not a credential, payment artifact, or new issuer attestation"); its claim set is deployment-specific. E2 not met in any defined form (`iat` and "proof time" are SHOULD-level claims in a deployment-defined JWT). E3 not met: no retention, audit or after-the-fact re-verification text. | Verification Token Contents (intro and JWT claim list); no audit or retention section |
| L8 Redress | 0 | R1 not met; R2 not met. Payment and disputes are out of scope. | Security Considerations "Payment Separation"; Open Questions "Machine Payments and 402"; Payment Object (informational only) |
| L9 Trust anchor | 1 | T1 partial: DCQL `trusted_authorities` can point to `openid_federation` and `etsi_tl` trust lists, but the Verifier SHOULD (not MUST) use them, applies "its own issuer policy", and only issuers are covered, not operators or agents. T2 met: Verifier MUST check credential status, revocation and expiry (Proof Validation 6); the Verification Token SHOULD support revocation. | Verifier Processing Rules 7, 10; Proof Validation 6; Security Considerations "Issuer Trust"; Credential Acquisition Guidance |
| L10 Continuity | 0 | C1 not met: the Verification Token `sub` is the Agent Identifier and the spec says the credential subject MUST NOT be the token holder unless it is the Agent, so the principal does not carry through. C2 not met: the result is tied to the request only by the OpenID4VP `nonce`, and the token carries `request_id` and optionally `x401_query_hash`; there is no hash or signature chain from identity credential to grant to action to record. | Verification Token Contents (item 1; `x401_query_hash`); Proof Validation 3-4; Result Artifact |

D5 note (x401): not met. No multi-hop sub-delegation with narrowing scope. Delegation evidence is a "MAY layer on" suggestion (Delegation and Actor Evidence) and a stated open question (Open Questions "Fully Autonomous Delegation").

Chain score (minimum): **0** (L7, L8, L10).
Total: **7 / 20** (1+1+1+1+1+1+0+0+1+0).

## x401: amended criteria

| Criterion | Score | Reason | Citation |
|---|---|---|---|
| I1' Principal identifiable | 0.5 | The Verifier can obtain issuer-attested identity claims through DCQL, which is stronger than a self-asserted name, but nothing requires any claim that identifies the Holder, the design favours minimal or predicate disclosure, and no party is named to resolve a pseudonym. Would be 1 if "the protocol lets the counterparty demand a third-party-attested identity claim" suffices. | Credential Requirements; Privacy "Data Minimization", "Selective Disclosure"; Terminology "Holder" |
| I2' Operator identifiable | 0.5 | Only the optional `agent_id` (domain, DID, certificate or SPIFFE identifier, Verifier-defined) and Web Bot Auth key-directory authority: a bare domain with no attestation of who controls it. No operator concept. | Result Artifact (`agent_id`); Agent Binding Options; Web Bot Auth and HTTP Message Signatures |
| A2' Key accountable and checkable over time | 0.5 | Accountable-party binding exists only as optional layers (mTLS certificates, SPIFFE) that the spec names but does not profile; no check of agent-key validity after the fact. Counted as one of the two, weakly. Could be 0 if optional unprofiled layers are discounted. | Agent Binding Options; OAuth Proof-of-Possession; Workload Identity |

---

# KYA-OS (v1.0.0, Stable; with Entity Card 1.1, Audit profile, AUDITABILITY.md)

KYA-OS defines agent DIDs, a W3C VC delegation chain rooted at a Responsible Party with CRISP constraints and status-list revocation, per-request holder-of-key proofs naming the delegation, and detached JWS server proofs. The Entity Card (typed entity, KYC/KYB attestation, per-request proof) and the Audit Assurance Profile are profiles.

| Link | Score | Tests met / not met | Citation |
|---|---|---|---|
| L1 Principal identity | 1 | P1 partial: the root issuer is the Responsible Party DID (MUST be a DID that signed the chain). A `did:web` DID resolves to a domain; a `did:key` DID is a pseudonym, and the spec defines no named party to resolve it on request; the Card `name` is self-asserted. P2 partial (optional): KYC/KYB as an `IdentityVerificationCredential` on the `responsibleParty` carries only fact and level (`basic`, `enhanced`, `loa3`), "never raw PII", surfaced in Card `attestations[]`. P3 partial: trusted-issuer allowlist, default `did:web:example.com`, caller-overridable; no accreditation or trust framework named. | SPEC §2 Terminology (Responsible Party, Principal); §6.4 (root `issuerDid` = signer); §6.10 "KYC/KYB"; ENTITY-CARD §4.1 (`responsibleParty`, `attestations`), §9.5, §10.4, §13 |
| L2 Operator identity | 1 | O1 partial: no operator role (Entity Card §2.3 forbids `operator` as an accountability synonym). The nearest is the Responsible Party (employing organisation in organisational use) and a `did:web` agent DID hosted by an organisation, which is domain-level identification. O2 optional (same KYB credential, on the Responsible Party). O3 as P3. | SPEC §2 (Responsible Party); §4.1 (`did:web` organisation-hosted); ENTITY-CARD §2.3, §5.2, §10.4 |
| L3 Agent key binding | 1 | K1 met: the Delegation Credential is signed by the delegator and names the agent key as subject (`credentialSubject.id`, or `invoker`); the verifier MUST check `leafInvoker === proof.did`. K2 partial: `did:web` rotation SHOULD keep old keys in `assertionMethod`; delegations expire and are revoked through a status list (current state, fail-closed); `did:key` has no rotation. After-the-fact checking of key validity "as observed" is specified only in the optional audit verifier (`keyRevocationMode`, key `validFrom`/`validUntil`, "Artifacts whose key has ended"). | SPEC §6.2; §6.4; §6.6; §11.5; ENTITY-CARD §10.2, §1.4; AUDITABILITY "Replay bundles and offline verification" |
| L4 Delegation | 2 | D1 met: `DelegationCredential` VC (SPEC §6.2; §6.10). D2 met: CRISP `scopes`, `notBefore`/`notAfter`, `audience`, `budget` (unit, cap, window); ZCAP `MaxAmount`, `ValidUntil` caveats, `allowedAction`, `invocationTarget`; a verifier MUST hold each call to every caveat. D3 met on the model: the root `issuerDid` MUST equal the Responsible Party DID whose key signed it (§6.4). Caveat: in the consent flow an authorization service issues the credential and the user's authentication method is unspecified (§9.3), which would be partial; flagged unsure. D4 met: `expirationDate`/`notAfter`/`validUntil` plus status-list and cascading revocation. | SPEC §6.2, §6.3, §6.4, §6.5, §6.6, §6.10, §9.3; ENTITY-CARD §10 |
| L5 Session authentication | 1 | S1 met: per-request holder-of-key proof (SPEC §7.4, §7.8 "a holder MUST state it in every request proof"; ENTITY-CARD §8 normative). S2 met: nonce, `ts` window, `jti`, MUST-level nonce retention. S3 not met: consent is obtained through `authorizationUrl` ("user authenticates and grants") with no human-presence or assurance level captured in an artefact; `step_up_required` is an outcome, not a presence proof. | SPEC §5.2, §5.5, §7.2, §7.8, §9.2, §9.3; ENTITY-CARD §8, §11.2 |
| L6 Action conformance | 2 | A1 met: a holder's request proof MUST state the digest of the credential the call presents (`delegationRef`, `delegationChainDigest`); a verifier MUST refuse a mismatch. A2 met: the verifier checks scope designation (§6.4.1 MUST), audience, validity window, `MaxAmount`/budget caveats ("MUST hold each call to every caveat ... or refuse") before the handler runs. | SPEC §7.8, §6.4.1, §6.10 (Caveats), §11.6; ENTITY-CARD §11.4 |
| L7 Evidence | 1 | E1 met: detached JWS proof binding `requestHash`, `responseHash`, `delegationRef`, `delegationChainDigest`, `outcome`, signed by the server's DID key (a did:web resolves to an organisation, not necessarily accredited). E2 partial: the proof `ts` is the signer's own claim; independent recorder time, signed append receipt, RFC 9162 checkpoints and RFC 3161/SCITT anchors exist only in the optional Audit Assurance Profile. E3 partial: SHOULD keep old keys listed (§11.5); retention is a SHOULD-level consideration (§12.4); the audit profile addresses retention, replay bundles and offline re-verification, with `valid`/`invalid`/`indeterminate`. | SPEC §7.1, §7.2, §7.4, §11.5, §12.4, §15.3; AUDITABILITY "The result", "Evidence, retention, and access", "Replay bundles", "Artifacts whose key has ended" |
| L8 Redress | 0 | R1 not met as liability: the Responsible Party is named as "ultimately accountable", but that is a technical accountability root, not an allocation of liability between roles. R2 not met: no dispute, refund or rulebook path; §11.12 covers reputation scope only. The audit text disclaims compliance conclusions. | SPEC §2 (Responsible Party); §11.12; AUDITABILITY "Production checklist" (closing note) |
| L9 Trust anchor | 1 | T1 partial: a Trust Registry type is defined but is advisory and verifier-local ("friction signal"); trusted issuers are an allowlist (default `did:web:example.com`); accountability roots are authorised under the Verifier's own policy; no external registry or governance framework named. T2 met: Bitstring Status List / StatusList2021 revocation, cascading, fail-closed, with freshness reporting. | SPEC §6.6, §6.8, §11.0; ENTITY-CARD §9.5, §10.3, §12.0 |
| L10 Continuity | 1 | C1 met: Responsible Party DID appears in the Card (`responsibleParty`), as root issuer of the grant (recomputed `responsibleParty === issuer(rootVC)`), and is bound to action records through the chain digest. C2 partial: grant to action by signed digest (MUST), action to record by `requestHash`/`responseHash`/chain digest, audit entries hash-chained (profile), re-delegations may commit to the parent by `parentCredentialDigest` (MAY now, required in 2.0). But identity credential to grant is by DID equality, not a hash or signature over the predecessor. | SPEC §7.8, §6.2 (parent commitment), §6.10; ENTITY-CARD §10.2; AUDITABILITY (previous-entry digest) |

D5 note (KYA-OS): met. Multi-hop sub-delegation as a DAG with `parentId`, subset discipline and narrowing of scope, budget and validity (SPEC §6.4; §6.10 attenuation invariants), cascading revocation (§6.5). Not required for the 2.

Chain score (minimum): **0** (L8).
Total: **11 / 20** (1+1+1+2+1+2+1+0+1+1).

## KYA-OS: amended criteria

| Criterion | Score | Reason | Citation |
|---|---|---|---|
| I1' Principal identifiable | 0.5 | Root issuer is a Responsible Party DID. `did:web` points at a domain; `did:key` is a pseudonym with no named party defined to resolve it. Third-party KYC/KYB exists but is optional and conveys "verified at level X", not who. Card `name` is self-asserted. | SPEC §2, §6.4, §6.10 "KYC/KYB", §12.1; ENTITY-CARD §4.1, §10.4 |
| I2' Operator identifiable | 0.5 | No operator role; the agent `did:web` host or the Responsible Party organisation DID is a domain-level identifier, with optional KYB. | ENTITY-CARD §2.3, §5.2, §10.4; SPEC §4.1 |
| A2' Key accountable and checkable over time | 0.5 | Binding half is met: the Responsible Party signs a credential naming the agent key, and the verifier joins it to the proof key. The after-the-fact half is only partly met: status lists give current state, `did:web` old keys are SHOULD-retained, and key-validity-at-signing-time checking sits in the optional audit verifier and concerns recorder, observer and server keys more than the agent key. | SPEC §6.2, §6.6, §11.5; ENTITY-CARD §10.2; AUDITABILITY "Replay bundles", "Artifacts whose key has ended" |

---

# Unsure cells

x401
- L1 (1): P1 turns on whether a spec-allowed but not required identity claim counts; P3 on whether DCQL `trusted_authorities` (SHOULD) counts as trust-list referencing.
- L2 (1): O1 rests entirely on an optional, unregistered `agent_id`; 0 is defensible because the spec never names an operator.
- L3 (1): rests on optional mTLS/SPIFFE layers named but not profiled; 0 is defensible. A2' follows the same call.
- L4 (1): whether the Verification Token is a "grant artefact" at all; 0 is defensible because it records the Verifier's decision, not the principal's authority.
- L7 (0): the Verification Token is a Verifier-signed record of an access decision (method, resource, proof time). If that counts as a record of the action, E1 and E2 would be partial and L7 would be 1.
- L9 (1): T1 depends on SHOULD-level use of `etsi_tl`/`openid_federation`.
- L10 (0): `x401_query_hash` and `request_id` give a thin link between request and token; scored as no continuity because the principal and the credential do not carry through.
- I1' (0.5) and A2' (0.5) as noted above.

KYA-OS
- L1 (1): whether P1 is met by a `did:web` Responsible Party; whether optional KYC/KYB lifts P2 to met.
- L3 (1): K2 depends on how much weight the optional audit verifier's key-interval checks carry for the agent key; K1 depends on treating the Responsible Party's signature on a delegation as an "accountable party" statement.
- L4 (2): D3 is met by the model (root issuer is the Responsible Party DID that signs) but in the §9.3 consent flow an authorization service issues the credential with an unspecified user authentication, which the rubric calls partial.
- L5 (1): S1 depends partly on the Entity Card profile being normative; core §7.8 applies to every request proof a holder makes but does not itself mandate that holders make one.
- L7 (1): E1 "accountable party" is the server DID, not an accredited party; E2 and E3 are met only by the optional audit profile or SHOULD text.
- L8 (0): the "ultimately accountable" Responsible Party could be read as a partial R1.
- L9 (1): the Trust Registry is defined in the core but advisory; unclear whether that satisfies T1.
- L10 (1): could be 2 if a DID-equality join to the identity (a `did:key` is itself a cryptographic identifier) is accepted as a cryptographic reference.
- I1', I2' and A2' as noted above.
