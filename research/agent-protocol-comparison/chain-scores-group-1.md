# Chain rubric scores, group 1: PAP, MCP, A2A, Web Bot Auth

Rubric: `ov/research/agent-protocol-comparison/chain-rubric.md` (10 links, 2 / 1 / 0; chain score = minimum link). Basis: spec text, read afresh. Local copies of sources are in `cmp2/src/`.

Sources read:
- PAP 1.0: `/docs/1.0/spec.md` (sections 3, 4, 5, 10), extensions `operations` (v3), `ucp`, `disclosures`, `links` (the last two have nothing relevant). The `mediated-sign-in` and `browser-control` extensions were fetched but not read in full.
- MCP 2026-07-28: Authorization (index, authorization-server-discovery, client-registration, security-considerations), Tools and Elicitation pages, and the Enterprise-Managed Authorization (EAA) text in ext-auth.
- A2A v1.0.1: `docs/specification.md` sections 4.4 to 4.6, 7, 8.4 and the security considerations.
- Web Bot Auth: draft-ietf-webbotauth-httpsig-protocol-01 sections 4, 5, 6, 7 and Appendix B.

Scoring rules applied throughout:
- A test met only by an optional extension, a SHOULD, or a MAY gives that link at most 1.
- A signed request is not a "record of the action signed by an accountable party" (L7 E1) unless the spec says someone keeps it as a record.
- Domain control (URL, TLS) is not third-party attestation.
- Authorization in MCP is OPTIONAL for the protocol as a whole. It counts as "core" only for the parts that are MUST once authorization is used.
- L8 (redress) is 0 for all four, so every chain score is 0.

---

## 1. PAP (Poppy) 1.0

| Link | Score | Tests met / not met | Citation |
|---|---|---|---|
| L1 Principal identity | 0 | P1 not met: the User ID is opaque and pairwise, and MUST NOT be derived from personal information. The Personal Agent holds the mapping, MUST keep it confidential, and no resolution on request is specified. P2 and P3 not met: no third-party verification of the User. | Spec 5.1; Ops 6 (`reference`, "look into the approval later"); Ops 8.1 |
| L2 Operator identity | 1 | O1 partial: `client_id` is an HTTPS URL, and the metadata carries `client_name` and `logo_uri`. These are self-published, with no attestation of who controls the domain. Which agents a Company accepts is "outside this specification". O2 and O3 not met. | Spec 4.1; 10.3 (the same limit stated for Company domains) |
| L3 Agent key binding | 1 | K1 not met: delegated keys are vouched for by a key in the operator's own `jwks_uri`, which is self-published. K2 partly met: each delegation (`poppy_dlg`) carries `iat`, `exp` (at most 24h) and `jti`, and travels in every Session JWT, so the delegated key's validity at the time of use is checkable from the retained request. This is expiry only, with no revocation. The state of the `jwks_uri` key afterwards is not covered. | Spec 5.2 "Delegated keys"; 5.3 |
| L4 Delegation | 1 | D1 met: scoped access and refresh tokens (core OAuth). In the optional Operations extension, an approval names the `operation_id` and `revision`. D2 partial: core gives scopes and `resource` only. Amount, payee and date constraints live in Operations `terms` and `expires_at`, which is an optional extension. D3 partial: the Company's own authorisation server issues the token after the User signs in. User approvals are unsigned statements by the Personal Agent, and signed approvals are "on the roadmap" (scores 0). D4 met: `expires_in`, RFC 7009 revocation, sign-out, and the operation `expires_at`. D5: not defined. The Agent ID is a label, not sub-delegation. Another company's agent connects under its own `client_id`. | Spec 4.2, 4.4 to 4.7, 5.1, 5.5; Ops 3, 5, 6, 8.1 |
| L5 Session auth | 1 | S1 met: a `Poppy-Session` JWT is signed per request with a delegated key (MUST). S2 met: the Company MUST check `iat` against a window it chooses, `htm`/`htu` and `ath`. Rejecting a reused `jti` is only a MAY. S3 not met as written: Direct and Device Sign-In require that the User signs in themselves, and Operations carries `approver` and `input_type`. There is no assurance level, and the Company "relies on the Personal Agent" for how the approval was given. | Spec 5.2, 5.3, 5.4; Ops 6, 8.1 |
| L6 Action conformance | 2 | A1 met: the signed Session JWT carries `ath` (a hash of the access token) with `htm`/`htu` on every request. The Operations approval names `operation_id` and `revision`. A2 met: the Company MUST verify the token and scope before acting. Under Operations it MUST perform only what the approved revision describes (that part is an extension). | Spec 5.2, 5.3 step 3, 7; Ops 3, 6 |
| L7 Evidence | 1 | E1 partial: a signed Session JWT binds method, URL, token hash and User ID, and the Company MAY record `approver`, `approved_at` and `reference`. These are the Personal Agent's own statements, not a signed record by an accountable party. E2 not met: `iat` and `approved_at` are self-asserted. E3 partial: the Company MUST remember a performed operation until `expires_at`, but this is for idempotency, not for evidence. Nothing keeps keys or status available for later verification. | Ops 6, 7, 8.1; Spec 5.2 |
| L8 Redress | 0 | R1 not met. R2 not met: payment goes to UCP (UCP ext. 6) with no dispute path or evidence mapping. Handoff to a person (8.9) and feedback (9.3) are not redress. | Spec 8.9, 9.3; UCP ext. 6 |
| L9 Trust anchor | 1 | T1 not met: acceptance of agents is a Company decision outside the spec, and 10.3 says nothing confirms who owns a domain. T2 met for tokens: RFC 7009 revocation, refresh and access expiry, and a Company may revoke a `client_id`. Delegated keys expire. The `jwks_uri` has no status list. | Spec 4.1, 4.6, 10.3; Ops 8.1 |
| L10 Continuity | 1 | C1 partial: the same `sub` is MUST-carried in every Session JWT for a Session, and the token is tied to the same `client_id`. There is no identity credential to match it against. C2 partial: the action (Session JWT) references the grant by hash (`ath`). The grant does not reference an identity credential, and no record references the action. | Spec 5.1, 5.2, 5.3 steps 3 and 4 |

D5 note: not defined. The Agent ID (5.1) tells a Personal Agent's own agents apart. It is not narrowing delegation.

Chain score (minimum): 0 (L1 and L8). Total: 9 / 20.

| Criterion | Score | Basis |
|---|---|---|
| I1' Principal identifiable | 0.5 | The pairwise User ID can be resolved by the Personal Agent operator, who is named by `client_id` and holds the mapping (5.1). The spec does not say it resolves to a real party on request. Ops 6 describes the operator "looking into the approval later" using the `reference`. |
| I2' Operator identifiable | 0.5 | A `client_id` URL with `client_name` and `logo_uri` (4.1). The domain is not attested (compare 10.3). |
| A2' Key accountable and checkable | 0.5 | The binding is self-published (not met). Delegation `iat`/`exp` is signed into each request, so the delegated key's validity at the time of use can be checked afterwards (5.2). The `jwks_uri` key's state afterwards is not covered. |

---

## 2. MCP 2026-07-28 (with Enterprise-Managed Authorization)

| Link | Score | Tests met / not met | Citation |
|---|---|---|---|
| L1 Principal identity | 1 | Core: the authorisation server authenticates the user, with no subject claim defined. EAA only: the IdP-signed ID-JAG carries `sub` and an optional `email`, with a named `iss`. P1 and P2 are met by the extension only (P2 because the enterprise IdP verifies the user). P3 not met: no accreditation or trust framework. | EAA 3, 4.3; Authorization index (roles) |
| L2 Operator identity | 1 | O1 partial: a Client ID Metadata Document (`client_id` URL, `client_name`, `client_uri`) is self-asserted. EAA assumes clients are pre-registered at the IdP, which gives a policy attestation but no named verifier artefact. O2 and O3 not met. | Client Registration (CIMD); EAA 7.1; Security Considerations (attestation is a MAY) |
| L3 Agent key binding | 0 | K1 not met: tokens are Bearer. `private_key_jwt` is a MAY with a self-published `jwks_uri`, and the EAA ID-JAG binds `client_id`, not a key. K2 not met: no key validity or revocation checking. | Client Registration; EAA 4.3 |
| L4 Delegation | 1 | D1 met: scoped access token. D2 partial: scopes and the `resource` audience (RFC 8707 MUST), but no amounts or payees. EAA IdP policy constrains scope. D3 partial: the token is issued by the authorisation server, and the ID-JAG is signed by the enterprise IdP on organisation policy. It is not signed by the principal. D4 met: token expiry, refresh, and ID-JAG `exp` of 300 seconds. No revocation endpoint is specified in the pages read. D5: none. | Authorization index; EAA 4.1, 4.2, 5.2 |
| L5 Session auth | 1 | S1 not met: Bearer on every request, with no proof of possession. S2 not met per request: PKCE, `state` and `iss` checks cover the authorisation flow only. Only EAA adds `jti` and `exp` on the ID-JAG. S3 not met as written: the user authenticates at the authorisation server, and the enterprise IdP "may" enforce MFA. Tool confirmation prompts and elicitation consent are SHOULD, with no assurance level. The score of 1 rests on the EAA `jti` and the SHOULD-level consent. | Authorization index; EAA 3, 4.3; Tools ("human in the loop", SHOULD); Elicitation |
| L6 Action conformance | 1 | A1 partial: the token is sent on every request (MUST) and is audience-bound, but it is not bound to the action. A2 partial: the server MUST validate the token, audience and scope (403 `insufficient_scope`), but no action-level constraints exist, and authorization is OPTIONAL for MCP. | Authorization index (token handling, error handling); Security Considerations |
| L7 Evidence | 0 | E1 not met: no record is defined. "Log tool usage for audit purposes" is an implementer SHOULD in the Tools page. E2 not met. E3 not met. | Tools (best practices); EAA 7.2 (IdP sees issuance only) |
| L8 Redress | 0 | R1 and R2 not met. | none |
| L9 Trust anchor | 1 | T1 partial: domain-based trust policies for CIMD are a MAY, and EAA lets the enterprise IdP admin decide which clients and servers may be used (extension). T2 partial: token expiry only, and no revocation mechanism is stated in the pages read. | Security Considerations (Trust Policies); EAA 1.1, 4.1 |
| L10 Continuity | 0 | C1 not met: `sub` appears in the ID-JAG, and in the access token only if the authorisation server issues a JWT, which is not required. No identity credential is linked to an action record. C2 not met: the access token does not cryptographically reference the ID-JAG. | EAA 4.3, 5, 5.2 |

D5 note: not defined.

Chain score (minimum): 0. Total: 6 / 20.

| Criterion | Score | Basis |
|---|---|---|
| I1' Principal identifiable | 0.5 | Only in the optional EAA extension: an IdP-signed `sub` and optional `email` under a named `iss`, which the IdP can resolve (EAA 4.3). Core defines no principal identity. |
| I2' Operator identifiable | 0.5 | A CIMD `client_id` URL with `client_name` is self-asserted (Client Registration). Pre-registration at the IdP (EAA 7.1) is not an attestation artefact. |
| A2' Key accountable and checkable | 0 | There is no agent key in core. `private_key_jwt` is a MAY with a self-published JWKS. Neither half is met. |

---

## 3. A2A v1.0.1

| Link | Score | Tests met / not met | Citation |
|---|---|---|---|
| L1 Principal identity | 0 | "Identity information is handled at the protocol layer, not within A2A semantics". There is no principal field. | Spec 7 |
| L2 Operator identity | 1 | O1 partial: `AgentCard.provider` (`organization`, `url`), optionally JWS-signed by a key the provider publishes (self-asserted). O2 and O3 not met. TLS CA validation (a SHOULD) and the mTLS scheme do not attest the operator. | Spec 4.4.2, 4.4.7, 8.4, 7.2 |
| L3 Agent key binding | 0 | K1 not met: the card signature uses a `jku` or trusted store the provider controls. Credentials are acquired out of band. K2 not met: "Expired or revoked keys MUST NOT be used" is stated with no mechanism for checking validity as at the time of use. | Spec 8.4.2, 8.4.3, 7.3 |
| L4 Delegation | 1 | D1 and D2 partial: OAuth2 and OIDC `securitySchemes` declare scopes at card and skill level (4.5). Authorisation logic is "implementation-specific" (7.5), and the credential is obtained out of band (7.3). D3 not met. D4 partial: `refresh_url`, and "SHOULD implement credential revocation" with periodic rotation (SHOULD). D5 note below. | Spec 4.5, 7.3, 7.5, security considerations (Credential Management) |
| L5 Session auth | 1 | S1 partial: the optional `MutualTlsSecurityScheme` gives a proof of key possession per connection. Other schemes are bearer, API key or HTTP. S2 not met: nothing is defined at the protocol layer. S3 not met: `TASK_STATE_AUTH_REQUIRED` allows "human approval" as an example, with no assurance level. | Spec 4.5.6, 7.4, 7.6 |
| L6 Action conformance | 1 | A1 partial: credentials MUST accompany every request (7.3) and the server MUST authenticate each one (7.4). A2 not defined: authorisation is the server's own policy and "MAY consider" scopes or actions (7.5). | Spec 7.3 to 7.5 |
| L7 Evidence | 0 | E1 not met: Tasks, Messages and Artifacts are unsigned (only the Agent Card can be signed). E2 not met: status `timestamp` is server-asserted. E3 not met: audit trails and "data retention policies" are SHOULD at most, and the retention language is about data privacy rather than verifying evidence. | Spec 5.6.1; security considerations (Audit, Data Privacy) |
| L8 Redress | 0 | None. | none |
| L9 Trust anchor | 1 | T1 partial: "Clients MAY maintain a trusted key store for known agent providers". T2 partial: "Expired or revoked keys MUST NOT be used for verification", with no mechanism defined. | Spec 8.4.3 |
| L10 Continuity | 0 | `contextId` and `taskId` link messages, but no principal or grant appears in the artefacts. | Spec 4.1 |

D5 note: not defined. 7.6.2 lets a client forward an `AUTH_REQUIRED` request up a chain of Tasks. There is no narrowing of scope. 7.6.3 only recommends binding credentials to the originating agent.

Chain score (minimum): 0. Total: 5 / 20.

| Criterion | Score | Basis |
|---|---|---|
| I1' Principal identifiable | 0 | Spec 7: no identity in A2A semantics. |
| I2' Operator identifiable | 0.5 | `AgentProvider` (organisation name and URL) is self-asserted, even when the card is signed (4.4.2, 8.4). |
| A2' Key accountable and checkable | 0 | The card key is self-published (`jku`). Revoked-key rejection has no mechanism, and nothing makes validity at the time of use checkable afterwards. |

---

## 4. Web Bot Auth, draft-ietf-webbotauth-httpsig-protocol-01

| Link | Score | Tests met / not met | Citation |
|---|---|---|---|
| L1 Principal identity | 0 | The draft "does not authenticate human users... does not define authorization or delegation". An agent tied to an individual is the case the draft says it does not suit. | 4.6, 7.1 |
| L2 Operator identity | 1 | O1 partial: the `Signature-Agent` URL is the identifier, and 4.5 says the domain operator "stands behind the key set". 4.1 says it "says nothing about who operates the Agent". O2 and O3 not met: "No name and no third party are involved". | 4.1, 4.2, 4.4, 4.5 |
| L3 Agent key binding | 0 | K1 not met: self-published directory, with TLS authority only (Appendix B adds possession proof, not accountability). K2 not met: key `nbf`/`exp` and rotation apply to the current directory. The draft "defines no revocation" and gives no after-the-fact check. | 5.5.1, 5.5.2, 6.3, Appendix B |
| L4 Delegation | 0 | "does not define authorization or delegation". | 4.6 |
| L5 Session auth | 1 | S1 met: RFC 9421 signature, `tag="web-bot-auth"`, per request. S2 met: `created` and `expires` are MUST, nonce is per RFC 9421, and replay within the window is admitted. S3 not met: human authentication is out of scope. | 4.6, 5.2, 5.2.3 |
| L6 Action conformance | 0 | No grant exists to reference or check. | 4.6 |
| L7 Evidence | 0 | E1 not met: the signed request covers `@authority` and `@target-uri`, and `Content-Digest` is optional. No record or retention is defined, and no one is named as accountable. 5.2.2 lets a signer cover another signature "to preserve evidence", which is not a record. E2 not met. E3 not met. | 5.2, 5.2.2 |
| L8 Redress | 0 | None. | none |
| L9 Trust anchor | 1 | T1 informative only: `[REGISTRY]` lists directory URLs (5.5.3), and trust accrual is out of scope (4.6). T2 partial: key `nbf`/`exp` and removal from the directory act as a status signal (4.4, 6.10), but the draft says it is "not a revocation mechanism" and "defines no revocation". | 4.4, 4.6, 5.5.2, 5.5.3, 6.3, 6.10 |
| L10 Continuity | 0 | No principal, grant or record. | 4.6 |

D5 note: not defined.

Chain score (minimum): 0. Total: 3 / 20.

| Criterion | Score | Basis |
|---|---|---|
| I1' Principal identifiable | 0 | 4.6 and 7.1. |
| I2' Operator identifiable | 0.5 | A bare URL or domain, with no attestation. 4.1 itself says it says nothing about who operates the agent. |
| A2' Key accountable and checkable | 0 | The directory is self-published, with no revocation, and nothing for checking afterwards. |

---

## Summary row (L1 to L10)

| Protocol | L1 | L2 | L3 | L4 | L5 | L6 | L7 | L8 | L9 | L10 | Chain | Total | I1' | I2' | A2' |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| PAP 1.0 | 0 | 1 | 1 | 1 | 1 | 2 | 1 | 0 | 1 | 1 | 0 | 9 | 0.5 | 0.5 | 0.5 |
| MCP 2026-07-28 | 1 | 1 | 0 | 1 | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 6 | 0.5 | 0.5 | 0 |
| A2A 1.0.1 | 0 | 1 | 0 | 1 | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 5 | 0 | 0.5 | 0 |
| Web Bot Auth -01 | 0 | 1 | 0 | 0 | 1 | 0 | 0 | 0 | 1 | 0 | 0 | 3 | 0 | 0.5 | 0 |

## Unsure cells

- PAP L3 = 1 and A2' = 0.5. These rest on the signed delegation carrying `iat`/`exp` into the request. A stricter reading gives 0 and 0, because K1 fails and the `jwks_uri` key's state is not checkable afterwards. This is the main swing cell.
- PAP L6 = 2. A stricter reading gives 1, because action-level terms (amount, payee) are checked only under the optional Operations extension, and core checks only scope.
- PAP L7 = 1. A stricter reading gives 0, because the Session JWT and `Poppy-Approval` are the Personal Agent's own unsigned or self-keyed statements, and retention is for idempotency only.
- PAP I1' = 0.5. The operator holds the User ID mapping, but the spec does not say it resolves to a real party on request. It could be 0.
- PAP L5 S3: counted as not met (no assurance level). The score stays 1 either way.
- MCP L1 = 1 and I1' = 0.5. Both depend on counting the optional EAA extension. I1' could be 1 if the IdP-signed `sub`/`email` is accepted as fully meeting it.
- MCP L6 = 1 (it could be 2 if OAuth scope checks count as core, since authorization is MUST once used). MCP L5 = 1 rests on EAA `jti`/`exp` and SHOULD-level consent. MCP L10 = 0 (it could be 1 if a JWT `sub` is assumed in the access token). MCP L9 = 1 (T1 is a MAY or extension; T2 has no revocation text in the pages read).
- A2A L4 = 1 and L6 = 1. A stricter reading gives 0 for both, because grants are acquired out of band and authorisation is left to the implementation. A2A L5 = 1 rests on the optional mTLS scheme. A2A L7 = 0, though "SHOULD provide audit trails" and the retention SHOULD could support 1.
- WBA L2 = 1: the draft itself says the URL says nothing about who operates the agent, so this could be 0. WBA L9 = 1 rests on key `nbf`/`exp` and removal acting as a status signal, against the draft's statement that it defines no revocation. It could be 0.
- The Web Bot Auth key-directory draft was read only as merged into section 5.5 and Appendix B. The `[REGISTRY]` draft was not read.
