# Scores, group 1: PAP, MCP, A2A, Web Bot Auth

Rubric: [rubric.md](rubric.md) (1 / 0.5 / 0). Basis is `spec` for all four. Fetched sources were kept locally and are not committed.

Note on the PAP clone: `pap-src` is the website code only. It has no spec text (`content/versions/1.0/` holds only an empty `extensions/` folder). I read the published 1.0 Markdown from https://personalagentprotocol.org/docs/1.0/spec.md and `/extensions/operations.md`, `/extensions/ucp.md`.

Consistency rules applied across all four:
- Domain-validated TLS, or a URL fetched over HTTPS, is not third-party attestation of an operator's identity (I3 = 0). A CA-issued client certificate offered as a core auth scheme (A2A mTLS) earns 0.5.
- A bearer or OAuth token issued by the counterparty's own authorisation server, with scopes, counts for Z1 and Z2 when OAuth is mandated or declared in the core spec. It earns 0.5 at Z3, per the rubric.
- A per-request signature that binds identity to something action-specific (method, URL, token hash) is a partial C1/C2 (0.5).

---

## 1. PAP / Poppy 1.0
Spec: Personal Agent Protocol specification v1.0, https://personalagentprotocol.org/docs/1.0/spec. Extensions read: Operations v3 and UCP v1 (both optional). Basis: `spec`.

| ID | Score | Justification |
|---|---|---|
| I1 | 1 | Spec 5.1 and 5.2: `sub` in the Session JWT is the per-Company pairwise User ID. It is mandatory on every request to Company APIs. |
| I2 | 1 | Spec 4.1: `client_id` is an HTTPS URL to a metadata document (`client_name`, `logo_uri`, `jwks_uri`). It is carried as `iss` in the Session JWT (5.2). Which agents a Company accepts is "outside this specification". |
| I3 | 0 | Spec 4.1 and 10.3: the Company decides which agents it accepts. Nothing confirms that a domain belongs to the named organisation. No issuer, KYC or CA attestation of User or operator. |
| I4 | 0 | Nothing links the User ID to a legal person: 5.1 forbids deriving it from personal information. Signed approvals are on the roadmap (Operations 8.1), which scores 0. |
| A1 | 1 | Spec 4.1: `private_key_jwt` client assertion (ES256/PS384). Spec 5.2: the Session JWT is signed with a delegated key (`poppy_dlg`, `cnf.jwk`). DPoP is a SHOULD (4.5). |
| A2 | 1 | Spec 4.1: `jwks_uri` on the `client_id` domain (CIMD). Spec 5.3 step 1: the Company fetches it. |
| A3 | 1 | Spec 5.2 and 5.3: `iat` window, `jti`, `htm`/`htu` and `ath` are required per request. Client assertion `exp` is at most 5 minutes (4.1). Rejecting a reused `jti` is only a MAY. |
| A4 | 1 | Spec 4.2 and 4.3: Direct and Device Sign-In (OAuth) by the User. Spec 5.2 and 5.3 step 3: `ath` binds the access token to the signed Session JWT. The token must be issued to the same `client_id`. |
| Z1 | 1 | Spec 4.5 and 4.7: scoped access and refresh tokens, with `poppy:browser-sign-in` defined. The Operations extension adds an approval object (optional). |
| Z2 | 1 | Spec 4.7: scopes, `auth.scope_hints`, per-service `resource` (RFC 8707). No amount, payee or time-window constraint in core. Operations `terms` and `expires_at` express these, but only as an optional extension. |
| Z3 | 0.5 | Spec 4.2: the token is issued by the Company's own authorisation server after the User approves. It is not signed by the User's key. Operations 8.1: "signed user approvals are on the roadmap". |
| Z4 | 1 | Spec 4.4 (refresh with narrower `scope`), 4.5 (`expires_in`), 4.6 (RFC 7009 revocation), 5.5 (sign-out), Delegation `exp` of at most 24 hours (5.2). |
| C1 | 0.5 | Core: the signed Session JWT binds User ID, `htm`/`htu` and `ath`, but the spec defines no stored record. Operations 6: the optional `Poppy-Approval` header (`approver`, `approved_at`, `reference`) is something a Company "MAY record". |
| C2 | 0.5 | The Session JWT is signed, but body-less. The approval header is not itself signed, and Operations 8.1 says the Company "relies on the Personal Agent". The operator signature (RFC 9421) is a SHOULD and does not cover the body. |
| C3 | 0 | No dispute, refund or liability path. Payment and disputes are delegated to UCP (UCP ext. 6). Spec 8.9 handoff to a person is not a redress artefact. |
| C4 | 0 | No transparency log, registry or status list. 9.3 feedback is Company-side reporting only. |

Totals:
- Identity 2 / 4
- Authentication 4 / 4
- Authorisation 3.5 / 4
- Accountability 1 / 4

Unsure:
- Z3 (0.5 versus 0).
- C1/C2: partial credit rests on the Session JWT and the optional approval header.
- Z2 gets full marks for scopes alone.

---

## 2. MCP 2026-07-28 (+ Enterprise-Managed Authorization)
Specs read:
- Authorization (index, authorization-server-discovery, client-registration, security-considerations): https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization
- Extension overview: https://modelcontextprotocol.io/extensions/auth/enterprise-managed-authorization
- Full extension spec (ext-auth repo, 2026-07-28): https://github.com/modelcontextprotocol/ext-auth/blob/main/specification/stable/enterprise-managed-authorization/2026-07-28/enterprise-managed-authorization.mdx
- OAuth client-credentials extension, skimmed.

Basis: `spec`. Authorization itself is OPTIONAL for MCP (Authorization, "Protocol Requirements").

| ID | Score | Justification |
|---|---|---|
| I1 | 0.5 | Core defines no subject claim. The authorisation server's implementation is "beyond the scope" (Roles). EAA 4.3: ID-JAG carries `sub` and optional `email`. That is optional-extension only. |
| I2 | 1 | Client Registration: Client ID Metadata Documents (`client_id` URL, `client_name`, `redirect_uris`). Authorisation servers and clients SHOULD support it. |
| I3 | 0.5 | EAA: the enterprise IdP issues and signs the ID-JAG (`iss`, `typ: oauth-id-jag+jwt`). Core leaves user authentication to the authorisation server and does not attest the client. Security Considerations: attestation is only a MAY ("MAY require additional attestation mechanisms"). |
| I4 | 0 | The ID-JAG identifies an employee under an IdP issuer, verifiable via the IdP JWKS. It is not tied to a verified natural person or registered legal entity. |
| A1 | 0.5 | Core tokens are Bearer. Client Registration: `private_key_jwt` is only a MAY. Client secrets are used in the client-credentials extension. |
| A2 | 0.5 | CIMD `jwks_uri` is used only with the optional `private_key_jwt`. EAA: the authorisation server validates the ID-JAG against the IdP JWKS. Discovery of the authorisation server and its metadata is mandatory (RFC 9728/8414), but that is not agent key discovery. |
| A3 | 0.5 | Core: PKCE, `state`, `iss` check and token expiry (index, "Authorization Response Validation"). No per-request nonce or proof (Bearer). EAA: `jti`, `exp` of 300 seconds on the ID-JAG (extension only). |
| A4 | 1 | Authorization Flow Steps: OAuth 2.1 authorisation code with PKCE. The user authenticates, the token is issued to the `client_id`, and `resource` binds the audience (RFC 8707, MUST). EAA binds SSO login to the token. |
| Z1 | 1 | Access tokens with scopes (Scope Selection Strategy, `WWW-Authenticate scope`). |
| Z2 | 1 | Scopes and audience (`resource`), step-up scope challenges. No amount or payee limits. |
| Z3 | 0.5 | The authorisation server issues the token. In EAA the IdP signs the ID-JAG on the organisation's policy, not the principal's own key. |
| Z4 | 1 | Token expiry and refresh (Refresh Tokens). EAA: centralised revocation at the IdP, ID-JAG `exp`. |
| C1 | 0 | No action record. Tools spec: "Log tool usage for audit purposes" is an implementer SHOULD, not an artefact. EAA overview mentions an "auditable trail" but defines none. |
| C2 | 0 | Nothing signed per action. |
| C3 | 0 | No dispute or liability path. |
| C4 | 0 | None. IdP logging is described in prose only. |

Totals:
- Identity 2 / 4
- Authentication 2.5 / 4
- Authorisation 3.5 / 4
- Accountability 0 / 4

Unsure:
- I1 and I3: depend on how the extension is read.
- A2: CIMD `jwks_uri` is tied to an optional feature.
- C1 and C4: EAA prose about "auditable" access with no artefact. Scored 0.

---

## 3. A2A v1.0.1
Spec: https://github.com/a2aproject/A2A, tag v1.0.1 (`docs/specification.md`, `specification/a2a.proto`, `docs/topics/enterprise-ready.md`). Sections read: 4.4 and 4.5 (objects), 7 (Authentication and Authorization), 8.4 (Agent Card Signing). Basis: `spec`.

| ID | Score | Justification |
|---|---|---|
| I1 | 0 | Spec 7: "Identity information is handled at the protocol layer, not within A2A semantics". Enterprise-ready: "No Identity in Payload". There is no principal field or claim. |
| I2 | 1 | `AgentCard.provider` (`AgentProvider.organization`, `url`) carries the operator. It is signed if the card is signed (8.4). |
| I3 | 0.5 | Spec 7.2: clients SHOULD validate the server TLS certificate against CAs. `MutualTlsSecurityScheme` is a core scheme. Card signatures (8.4) are self-asserted, with `jku`/`kid` or a "trusted key store" (MAY). No attestation of the provider. |
| I4 | 0 | Nothing ties `provider.organization` to a registered legal entity. |
| A1 | 1 | `securitySchemes`: mTLS, OAuth2, OIDC, HTTP and API key. Agent Card JWS signature (8.4.2, `alg`, `kid`) proves provider key possession. Server MUST authenticate every request (7.4). |
| A2 | 1 | `AgentCardSignature` header `jku` (JWKS URL) plus `kid` (8.4.2, 8.4.3). `oauth2_metadata_url` (RFC 8414), OIDC discovery URL. |
| A3 | 0 | No nonce, timestamp or `jti` is defined at the protocol layer. Card signatures carry no validity time. Replay is left to the chosen scheme. |
| A4 | 0.5 | `OAuth2SecurityScheme` (authorisation code + PKCE, device code) is declared in the card. Credential acquisition is "Out-of-Band" (7.3), and `TASK_STATE_AUTH_REQUIRED` (7.6) hands it to the client. The binding to the agent is not specified. |
| Z1 | 1 | OAuth scopes in `securitySchemes`/`security_requirements` (card and skill level). Spec 7.5: authorisation logic is "implementation-specific". Scored on the declared scoped-token artefact. |
| Z2 | 1 | Scopes and per-skill security requirements (7.5, `AgentSkill.security_requirements`). No amount or payee limits. |
| Z3 | 0 | Not principal-signed. Credentials are obtained out of band. Spec 7.6.3: in-band credentials only "SHOULD be bound to the agent". |
| Z4 | 0.5 | `refresh_url` in the OAuth flows. A2A defines no expiry, revocation or sub-delegation. In-task credentials may be rejected or negotiated (7.6.2). |
| C1 | 0.5 | `Task`/`Message`/`Artifact` objects (`id`, `contextId`, status `timestamp`) record the work. They are not linked to the authenticated identity or grant by protocol. Enterprise-ready recommends logging and auditing. |
| C2 | 0 | Tasks and artefacts are unsigned. Only the Agent Card can be signed. |
| C3 | 0 | None. |
| C4 | 0 | None. Tracing and logging are recommended in the enterprise-ready guide only. |

Totals:
- Identity 1.5 / 4
- Authentication 2.5 / 4
- Authorisation 2.5 / 4
- Accountability 0.5 / 4

Unsure:
- I1 (0 versus 0.5 for the OAuth identity at the transport layer).
- I3 (0.5 rests on TLS CA validation and mTLS).
- Z1/Z2 (1 versus 0.5, since the spec delegates authorisation logic).
- Z4.

---

## 4. Web Bot Auth: draft-ietf-webbotauth-httpsig-protocol-01 (+ key directory)
Spec: https://datatracker.ietf.org/doc/draft-ietf-webbotauth-httpsig-protocol/01/, 2026-10 ("HTTP Message Signatures for Bots"). The key directory is not a separate draft here. It was merged in as section 5.5 (Key Distribution and Discovery), section 5.5.1 (Directory Format), section 8.1 (well-known URI `http-message-signatures-directory`), and Appendix B (directory response signature). The standalone `draft-ietf-webbotauth-http-message-signatures-directory` text was not retrievable under `-03` to `-06` at ietf.org, so I scored from the merged text. Basis: `spec`.

| ID | Score | Justification |
|---|---|---|
| I1 | 0 | Section 4.6: "does not authenticate human users... does not define authorization or delegation". Section 7.1 says it is unsuitable for agents tied to an individual. |
| I2 | 1 | Section 4.1 and 5.2.1: `Signature-Agent` URL is the agent identifier (MUST be carried). Section 4.5: the well-known URI names a domain. Section 4.1 stresses it says "nothing about who operates the Agent", so this is an agent or key-holder identifier. |
| I3 | 0 | Section 4.2: "No name and no third party are involved". Section 4.4 and 5.5: TLS authenticates only the host. |
| I4 | 0 | None. Section 4.4: the URL does not say the operator is honest or the party everyone knows. |
| A1 | 1 | Section 5.2: RFC 9421 signature, `tag="web-bot-auth"`, `keyid` is the JWK thumbprint. |
| A2 | 1 | Section 5.5 and 5.5.1: `Signature-Agent` URL resolves to a JWKS. `/.well-known/http-message-signatures-directory`, with `nbf`/`exp` per key. Appendix B: directory response signatures prove key possession. |
| A3 | 1 | Section 5.2: `created` and `expires` are MUST (24 hours recommended). Nonce per RFC 9421 and no additional nonce requirements (5.2.3). Section 5.2 admits replay inside the window. |
| A4 | 0 | Section 4.6: human authentication is out of scope. |
| Z1 | 0 | Section 4.6: "does not define authorization or delegation". |
| Z2 | 0 | Same. Covered components narrow the signature scope (5.2), but that is not a grant. |
| Z3 | 0 | Same. |
| Z4 | 0 | Directory key `nbf`/`exp` and rotation (5.5.2) apply to keys, not grants. Section 5.5.2: "not a revocation mechanism". |
| C1 | 0.5 | The signed request binds the Signature-Agent identity to `@authority`/`@target-uri`, and optionally method, path or `Content-Digest` (5.2). It is a retainable proof. No record or grant link is defined. |
| C2 | 0.5 | A signature is tamper-evident, but the body is not covered unless `Content-Digest` is added. "This document does not require it." |
| C3 | 0 | None. |
| C4 | 0 | None. Section 5.5.3 redistributed key material and `[REGISTRY]` references are informative or out of scope. |

Totals:
- Identity 1 / 4
- Authentication 3 / 4
- Authorisation 0 / 4
- Accountability 1 / 4

Unsure:
- I2: the draft itself denies the URL identifies the operator.
- A3: the timestamp window counts, but replay inside it is admitted.
- C1 and C2: partial credit on the signed request only.

### Not counted: draft-vilgalys-webbotauth-signed-agent-metadata-00 (2 Nov 2026)
Adds an optional `Signed-Agent-Metadata` header (RFC 9651 dictionary). It must be listed among the covered components of the Web Bot Auth signature, and a verifier ignores it otherwise (4.1, 4.2). Members: `product`, `project`, `session` (3.2).
- Gives the platform sub-identities (product, tenant workspace, task) under one shared `Signature-Agent` key. This is hierarchical scoping (3.3), meant for reputation isolation and rate limiting.
- Would strengthen I2 for multi-tenant platforms, because the tenant or operator becomes distinguishable. It is platform-asserted and opaque (3.4: platform SHOULD populate from authenticated platform state).
- Would partly help C1: a signed per-request session ID could be logged for later abuse reporting (5.2).
- It does not add principal identity (7.1 forbids PII), third-party attestation, authorisation, or redress. Total scores would not change beyond I2 (already 1).
- It refers to a "Signature Agent Card" (client_name, contacts, `web_bot_auth` object) in `draft-meunier-webbotauth-registry`. That is a separate document, and I did not read or score it.
