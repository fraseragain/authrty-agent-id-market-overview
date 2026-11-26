# General-actions chain scores, group A: PAP, MCP, A2A, Web Bot Auth, AP2, Verifiable Intent, UCP

Rubric: `ov/research/agent-protocol-comparison/chain-rubric.md` as rewritten by `chain-rubric-general-actions.md` (L4 to L8 re-scored; L1, L2, L3, L9, L10 carried over from `scores.json` "chain_scores"). Chain score = lowest link. Rules from `chain-review.md` applied: own spec set only, a pointer to another protocol earns nothing, a shared identifier is not a cryptographic link, a self-published key is not an accountable binding, unread features get no credit.

## Sources and how they were read

- PAP 1.0: `spec.md` and the `operations` extension re-fetched from personalagentprotocol.org/docs/1.0 on 25 Nov 2026 (spec is 165,333 bytes, identical to the earlier local copy). `disclosures`, `links`, `mediated-sign-in`, `browser-control` and `ucp` extension pages fetched. `mediated-sign-in` and `browser-control` were not read in full, so they earn nothing.
- MCP 2026-07-28 with Enterprise-Managed Authorization (EAA): Authorization (index, security considerations), Tools, Elicitation, and the EAA page. These are the earlier fetched copies of the primary pages (`cmp2/src/mcp-*.txt`, `eaa.mdx`), not re-fetched in this run.
- A2A v1.0.1: `a2a.md` (primary spec, `cmp2/src`), sections 3.1, 7, 8.4 and security considerations.
- Web Bot Auth draft-ietf-webbotauth-httpsig-protocol-01: `wba.txt` (the IETF text), sections 4.6, 5.2, 5.2.2, Appendices C and D.1.
- AP2: git tree `e1ea56d`, which is tag `v0.2.0` (the newest tag; checked with `gh api`). Read `specification.md`, `agent_authorization.md` and the receipt and mandate schemas.
- Verifiable Intent: HEAD `356c296` (2026-04-20), `spec/{README,constraints,credential-format,security-model}.md`. The upstream HEAD is still this commit.
- UCP v2026-08-25: tag `v2026-08-25` (`87dd4b1`, newest tag). Read `common/identity-linking`, `shopping/order`, `shopping/extensions/buyer-consent.md`, glossary and overview.

No repository was edited.

---

## 1. PAP (Poppy) 1.0

| Link | Score | Tests met / not met | Citation |
|---|---|---|---|
| L4 Delegation | 1 | D1 met: the scoped access and refresh tokens are the grant. D2 partial: core limits are OAuth scopes and the RFC 8707 `resource`, with Company-defined scope names. Operations terms (the operation, order, item, `expires_at`, at most once) constrain exactly what may be done, but they are an approval of one revision, not the grant, and the extension is optional. Recipient, count and rate are not in the grant. D3 partial: the Company's own authorisation server issues the token after the User signs in. Operations approvals are the Personal Agent's unsigned statements, and signed approvals are "on the roadmap". D4 met: token expiry, RFC 7009 revocation, sign-out, and operation `expires_at`. | Spec 4.5, 4.6, 4.7, 5.5; Operations 3, 5, 6, 8.1 |
| L5 Session authentication | 1 | S1 met: the `Poppy-Session` JWT is signed per request with a delegated key (MUST). S2 met: `iat` window, `htm`/`htu`/`ath` checks (a `jti` reject is only a MAY). S3 partial: Operations is a step-up the Company can require for any action it chooses, for any class, but `approver` and `input_type` are the Personal Agent's own statements and there is no assurance level. | Spec 5.2, 5.3; Operations 1, 5, 6, 8.1 |
| L6 Action conformance | 1 | A1 met for every class: the signed Session JWT carries `ath` (hash of the access token), `htm` and `htu`; an Operations approval names `operation_id` and `revision`. A2 partial: core checks token and scope only (`insufficient_scope`). The check that "the request asks for exactly what it describes" exists only in the optional Operations extension, and it checks the operation against the approved terms, not against the grant. | Spec 5.2, 5.3, 7; Operations 6 "What the Company checks" 3 |
| L7 Evidence | 0 | E1 not met: the Session JWT covers method, URL and token hash but not the body or terms, and it is signed by a delegated key vouched for in the agent's own `jwks_uri`, so it is not an accountable party. `approver`, `approved_at`, `input_type` and `reference` are "the Personal Agent's statements". E2 not met. E3 not met: the Company must remember a performed operation until `expires_at`, which is retention for at-most-once, not for evidence. E4 not met: the Company response and `status` (`performed`) are not signed. | Operations 6, 7, 8.1; Spec 5.2, 10.7 |
| L8 Redress | 0 | R1 not met: no allocation between named roles for non-monetary harm. A Company "MAY revoke the `client_id`" of an agent that sends an approval the User did not give, which is a sanction and not an allocation. R2 not met: nothing defines a way to contest, reverse or remedy a performed action. Revocation (4.6) and sign-out (5.5) stop future access and do not remedy past acts. `scope_hints.changes` (`reversible` or `irreversible`) is advisory. Handoff to a person (8.9) and feedback (9.3) are not redress. | Spec 4.6, 4.7, 5.5, 8.9, 9.3; Operations 8.1 |

Row (L1 to L10): 0, 1, 1, 1, 1, 1, 0, 0, 1, 1. Chain score 0. Total 7 / 20.
Compared with `scores.json`: L4 to L8 unchanged. L1, L2, L3, L9, L10 kept (the variant does not change them).

Action classes:

| Class | Rating | Basis |
|---|---|---|
| A. Read | partial | Company-defined scopes such as `orders:read`. `scope_hints` give `changes: none` and `personal_data`, but they are the Company's claims, not the grant (spec 4.7). |
| B. Communicate | partial | Conversations with the Company Agent are core (spec 8). Spec 4.7 names "sending a message" as an irreversible change. No grant or record semantics for messages. |
| C. Change state | yes | Operations defines the terms-approval flow for "exchanging an item, changing a booking, or cancelling a subscription", and `scope_hints.changes` marks reversible or irreversible (Operations 1, 3). |
| D. Legally significant act | partial | Operations terms are free-form (the decline example is an account closure). Spec 10.1 says Company text is "never the User's approval or consent", but no consent or acceptance semantics are defined. |
| E. Pay | partial | Operations terms can carry a price (`price_difference`). Payment itself is delegated to UCP in the `ucp` extension (Section 6), which earns nothing here. |
| F. Delegate onward | no | The Agent ID only labels the agent's own sub-agents (5.1). There is no onward grant or narrowing. |

Unsure cells (PAP):
- L8 = 0. It would be 1 if revoking tokens and sign-out count as "revoke a consent" under R2. They act only on future access, so I did not credit them.
- L6 = 1 rests on Operations being optional. If the Operations check counted as core, A2 would still be "terms, not grant", so 1 holds.
- L7 = 0 follows the earlier review (Personal Agent statements, no signature by an accountable party).
- Class A and B ratings: `scope_hints` could lift A to yes. I kept partial because they are advisory.

---

## 2. MCP 2026-07-28 with Enterprise-Managed Authorization

| Link | Score | Tests met / not met | Citation |
|---|---|---|---|
| L4 Delegation | 1 | D1 met: scoped, audience-bound access token. D2 partial: scopes plus the `resource` audience; the server may derive required scopes "dynamically based on the specific request arguments", which is a SHOULD and server policy. No resource, recipient, count or window constraint is defined. EAA lets the IdP policy decide "which scopes a given user can request". D3 partial: the authorisation server issues the token, and the ID-JAG is signed by the enterprise IdP, not the principal. D4 met: token expiry, ID-JAG `exp` of 300 s. | Authorization index (scope challenge handling); EAA 4.1, 4.3, 5.2, 7.2 |
| L5 Session authentication | 1 | S1 not met (Bearer). S2 partial: the ID-JAG has `jti` and `exp`, nothing per request. S3 partial: the scope-challenge step-up (403 `insufficient_scope`, SHOULD) is a re-authorisation flow, not a human re-confirmation with an assurance level. Tool confirmation prompts and "human in the loop" are SHOULD, with no assurance level. | Authorization index (Step-Up Authorization Flow); Tools (User Interaction Model); EAA 3, 4.3 |
| L6 Action conformance | 1 | A1 partial: the token goes on every request (MUST) and is audience-bound, but it is not bound to the operation. A2 partial: the server validates token, audience and scope. Scope-only checks are partial in this variant. | Authorization index (token handling, error handling); Security considerations |
| L7 Evidence | 0 | E1 not met: "Log tool usage for audit purposes" is an implementer SHOULD, and no record is defined. E2 not met. E3 not met. E4 not met: `CallToolResult` is unsigned. EAA 7.2 says the IdP sees issuance only. | Tools (implementation guidelines); EAA 7.2 |
| L8 Redress | 0 | R1 not met. R2 not met: no revocation endpoint, rollback or incident path is defined in the pages read. The request-cancellation utility only stops an in-flight request and was not credited. | none |

Row: 1, 1, 0, 1, 1, 1, 0, 0, 1, 0. Chain score 0. Total 6 / 20.
Compared with `scores.json`: L4 to L8 unchanged. L1, L2, L3, L9, L10 kept.

Action classes:

| Class | Rating | Basis |
|---|---|---|
| A. Read | partial | Resources and tools exist, and scopes are server-defined strings. Tool `annotations` are "untrusted unless they come from trusted servers" (Tools). |
| B. Communicate | partial | Any tool can send a message. No defined semantics. |
| C. Change state | partial | Same: tool name and scope only. |
| D. Legally significant act | partial | Elicitation records an `accept` action by the user (Elicitation, URL mode) but defines no legal-act semantics. |
| E. Pay | partial | Elicitation URL mode is named for "payment flows" and "must not pass through the MCP client", which is a hand-off and not a grant. |
| F. Delegate onward | no | Token passthrough is forbidden and the server must use a separate upstream token (Security considerations, confused deputy). Sampling is the reverse direction. |

Unsure cells (MCP):
- L8 = 0. The MCP cancellation utility and A2A `CancelTask` are both in-flight cancels. If counted, each would give R2 partial and L8 = 1. I applied 0 to both for consistency.
- L5 = 1 rests on EAA `jti` and SHOULD-level consent, the same as in the purchase scoring.
- A to E all partial because everything goes through server-defined tools and scopes. A could be yes on a generous reading of tool and resource semantics.

---

## 3. A2A v1.0.1

| Link | Score | Tests met / not met | Citation |
|---|---|---|---|
| L4 Delegation | 1 | D1 and D2 partial: the Agent Card declares OAuth2 and OIDC schemes with scopes at card and skill level, so the operation (skill) and scope can be named. The credential comes from an out-of-band process, and authorisation logic is "implementation-specific". D3 not met. D4 partial: `refresh_url`, and credential revocation is a SHOULD. | Spec 4.5, 7.3, 7.5; security considerations (Credential Management) |
| L5 Session authentication | 1 | S1 partial: optional `MutualTlsSecurityScheme` (key possession per connection). S2 not met. S3 partial: In-Task Authorization (`TASK_STATE_AUTH_REQUIRED`) is a defined step-up for any task action, with "human approval before a destructive action" as a named example, but the credential or approval is passed out of band and no assurance level exists. | Spec 4.5.6, 7.4, 7.6, 7.6.1 |
| L6 Action conformance | 1 | A1 partial: credentials accompany every request (7.3) and the server MUST authenticate each (7.4). A2 partial: the server "MAY consider" skills, actions within tasks and scopes (7.5). This is policy, and no grant is referenced. | Spec 7.3 to 7.5 |
| L7 Evidence | 0 | E1 not met: Tasks, Messages and Artifacts are unsigned (only the Agent Card can be signed). E2 not met: status `timestamp` is server-asserted. E3 not met: audit trails and retention are SHOULD and about privacy. E4 not met: responses are unsigned. | Spec 4.1, 4.4.7, 8.4; security considerations (Audit and Monitoring, Data Privacy) |
| L8 Redress | 0 | R1 not met. R2 not met: `CancelTask` asks to cancel an ongoing task and "success is not guaranteed". It is not a remedy for a performed action. | Spec 3.1.5 |

Row: 0, 1, 0, 1, 1, 1, 0, 0, 1, 0. Chain score 0. Total 5 / 20.
Compared with `scores.json`: L4 to L8 unchanged. L1, L2, L3, L9, L10 kept.

Action classes:

| Class | Rating | Basis |
|---|---|---|
| A. Read | partial | Skills and Artifacts, with OAuth scopes per skill (4.5). Generic. |
| B. Communicate | partial | `SendMessage` is the core operation (3.1.1), but the grant side is a generic scope or skill. |
| C. Change state | partial | A task can do anything. 7.6 names "destructive action" only as an approval example. |
| D. Legally significant act | partial | Only through `AUTH_REQUIRED` human approval (7.6), with no semantics. |
| E. Pay | partial | Generic only. |
| F. Delegate onward | partial | The task chain is native (a client may itself be an agent processing a Task, 7.6.2). Credentials "SHOULD be bound to the agent which originated the request" (7.6.3). There is no scoped onward grant, no narrowing, and signed hand-offs do not exist. |

Unsure cells (A2A):
- L8 = 0 (see MCP: `CancelTask` as an in-flight cancel).
- L4 = 1 versus 0, as in the purchase scoring (credential out of band).
- F: partial rather than yes. The act is native, but the grant side is not defined.

---

## 4. Web Bot Auth, draft-ietf-webbotauth-httpsig-protocol-01

| Link | Score | Tests met / not met | Citation |
|---|---|---|---|
| L4 Delegation | 0 | No grant: the draft "does not define authorization or delegation". Appendix D.1: "Delegation and chaining are out of scope". | 4.6; D.1 |
| L5 Session authentication | 1 | S1 met: RFC 9421 signature with `tag="web-bot-auth"` on requests. S2 met: `created` and `expires` MUST, nonce per RFC 9421. S3 not met: human authentication is out of scope, and no step-up is defined. Nothing in S3 is partial, and the score of 1 rests on S1 and S2. | 4.6, 5.2, 5.2.3 |
| L6 Action conformance | 0 | No grant to reference or check. The signed components can narrow to `@method`, `@path` or `@query-param`, but that is optional and says what the signature reaches, not what a grant allows. | 5.2 |
| L7 Evidence | 0 | E1 not met: only `@authority` or `@target-uri` is mandatory; `@method` and `Content-Digest` are optional ("No component covers the body"). The signer's key is self-published, and no record, keeper or retention is defined. 5.2.2: an outer signature "does not express authorization, delegation, or consent". E2, E3, E4 not met. | 5.2, 5.2.2 |
| L8 Redress | 0 | None. The draft "defines no revocation". | 6.3 |

Row: 0, 1, 0, 0, 1, 0, 0, 0, 0, 0. Chain score 0. Total 2 / 20.
Compared with `scores.json`: nothing changes.

Action classes:

| Class | Rating | Basis |
|---|---|---|
| A. Read | no | No grant or record semantics (4.6). |
| B. Communicate | no | Same. |
| C. Change state | no | Same. |
| D. Legally significant act | no | 5.2.2: the signature does not express consent. |
| E. Pay | no | Not addressed. |
| F. Delegate onward | no | D.1: out of scope. |

Unsure cells (WBA):
- A to C could be read as partial because a signature can optionally cover method, path and a body digest (5.2). I rated them no because there is no grant and the signature is not a record.
- L2 and L9 are carried from `scores.json` (L9 = 0 after the review).

---

## 5. AP2 v0.2.0

AP2's Agent Authorization model is written generically ("A User authorizes an Agent to perform some action (or actions)"). It states "AP2 makes use of this model for the payments use case, but the model could be applied more generally in the future" and "The AP2 specification provides mandate types and constraint types for use with payments. New mandate types and new constraint types MAY be defined." The only mandate types, constraints, receipts and dispute steps defined are for checkout and payment. I credited the generic machinery (open and closed mandates, `cnf`, `sd_hash`, constraint evaluation, signed receipts) and nothing in the payment-only content.

| Link | Score | Tests met / not met | Citation |
|---|---|---|---|
| L4 Delegation | 1 | D1 met in structure: an open Mandate is an explicit grant with `vct`, `constraints` and `cnf`. D2 partial: the extensible `constraints` array can express the operation, but every defined constraint is a purchase or payment one (merchants, line items, amount range, budget, payee, instrument, execution date, recurrence). The extension point (a new constraint needs a type, a schema and an evaluation algorithm) defines none for non-payment actions. D3 partial: user-signed via the User Credential path, provider-signed via the Trusted Agent Provider path. D4 partial: `exp` is optional in the schema and there is no revocation. | `agent_authorization.md` "Mandate Structure", "Mandates using SD-JWT VCs"; `specification.md` "Extension Points"; `open_checkout_mandate.json` (`required`: `vct`, `constraints`, `cnf`) |
| L5 Session authentication | 1 | S1 met: a Key Binding JWT with the key in `cnf`. S2 met: `aud`, `nonce` and `sd_hash` in the KB-JWT (SD-JWT normative). S3 partial: a Trusted Surface obtains "informed user consent" for any Mandate Content, and Human Present mode has the user sign the closed mandate, but no assurance level and no step-up for high-risk non-payment actions is defined. | `agent_authorization.md` "Mandate Delegation", "Mandate Structure"; `specification.md` "Roles" |
| L6 Action conformance | 1 | A1 met by the generic mechanism: a closed mandate references the open one (`sd_hash`), and the mandate is presented in "Action Authorization" for any action. A2 partial: the Verifier MUST check that "the Mandate Content allows the Agent to perform the action", and unknown constraints fail (`unresolved_constraint`), which is fail-closed. But no operation or resource vocabulary exists outside checkout and payment, so a non-payment check cannot run without a new type. | `agent_authorization.md` "Verification and Processing Rules", "Action Authorization", "Errors" |
| L7 Evidence | 1 | E1 partial: the Mandate Receipt is a Verifier-signed JWT (`iss`, `result`, `reference` = hash of the closed mandate) and "MAY contain additional use-case specific properties". It evidences that the Verifier accepted a mandate, not what was then done. E2 partial: `iat` is required only in the checkout and payment receipt schemas, not in the generic receipt text. E3 not met: retention and retrieval are out of scope. E4 partial: the receipt is the counterparty's signed response to the agent, and the payment and checkout receipts carry `order_id` and `payment_id`, but these are payment-specific. | `agent_authorization.md` "Action Authorization" (Mandate Receipt); `checkout_receipt.json`, `payment_receipt.json`; `specification.md` "Dispute Evidence" |
| L8 Redress | 0 | R1 not met. R2: the dispute-evidence verification steps cover only Checkout and Payment Mandates and Receipts. The spec says "Specific details of how this is used for dispute resolution, retention, and retrieval requirements are outside the scope." Payment-only, so nothing in this variant. | `specification.md` "Dispute Evidence", "Verification: Dispute" |

Row: 1, 1, 1, 1, 1, 1, 1, 0, 1, 2. Chain score 0. Total 10 / 20.
Compared with `scores.json`: L6 2 to 1 (A2 is payment-only in content), L8 1 to 0 (the dispute steps are payment-only). L4, L5, L7 unchanged. L1, L2, L3, L9 kept. L10 kept at 2 because the variant leaves it unchanged and the hash links (`delegate_payload` in the Key Binding, `sd_hash`, receipt `reference`) are generic.

Action classes:

| Class | Rating | Basis |
|---|---|---|
| A. Read | partial | A new mandate type may be defined (`agent_authorization.md`), but none is. |
| B. Communicate | partial | Same. |
| C. Change state | partial | Same. |
| D. Legally significant act | partial | Same. The Checkout Mandate commits the user to a purchase, which is class E. |
| E. Pay | yes | Checkout Mandate, Payment Mandate and receipts. |
| F. Delegate onward | no | "Agent-to-Agent Delegation ... is outside the scope of the current specification" (`specification.md`). |

Unsure cells (AP2):
- L6 = 1 versus 2. If the generic verification rules count as meeting A2 for any action, it stays at 2.
- L8 = 0 versus 1. The dispute steps check a generic hash chain, but the section is written for the checkout and payment mandates only.
- L4 D1: structure is generic and content is payment-only, so 1 either way.
- L7 = 1 depends on crediting the generic receipt. Without it, 0.
- L10 = 2 is the strongest-mode reading, as in the review.

---

## 6. Verifiable Intent v0.1 (draft)

VI says it binds "an AI agent's commercial actions to an end-user's explicitly stated purchase intent". The L1 credential is a payment card credential (`https://credentials.mastercard.com/card`), and the VCT registry has only checkout and payment mandates. Custom constraint types are allowed (URN or reverse-DNS names, "for organization-specific constraints that don't fit the checkout/payment model"), but none is defined, and a verifier that does not recognise a URN type "SHOULD skip it in permissive mode".

| Link | Score | Tests met / not met | Citation |
|---|---|---|---|
| L4 Delegation | 1 | D1 partial: L2 mandates are explicit grants, but only `mandate.checkout.*` and `mandate.payment.*` exist. D2 partial: the eight registered constraints are purchase and payment ones. Non-payment constraints are possible only as custom types. D3 met: L2 is signed with the user key bound in L1. D4 met: `exp` is required on L2 and L3, and L2 cannot outlive L1. | `constraints.md` 4, 6.1; `credential-format.md` 4.3, 7, 10; `README.md` 9.1 |
| L5 Session authentication | 1 | S1 met: L3 is signed by the L2-bound agent key. S2 met: `nonce` required, `aud`, `iat`, `exp`, nonce de-duplication. S3 partial: Immediate mode has the user review and confirm, but "VI binds a key, not a person", and no assurance level or non-payment step-up is defined. | `credential-format.md` 5.2 to 5.3; `security-model.md` 2.4, 3.5 |
| L6 Action conformance | 1 | A1 met by the generic chain: L3 `sd_hash` over the L2 presentation. A2 partial: verifiers MUST check L3 against disclosed L2 constraints, but only for the registered checkout and payment types, and custom types may be skipped in permissive mode. | `credential-format.md` 5.4, 5.7; `README.md` 9.1; `constraints.md` 6.1 |
| L7 Evidence | 0 | E1 not met: L3 records are signed by the agent key, there is no verifier receipt, and they are checkout and payment only. E2 not met. E3 only for issuer keys: retired L1 issuer keys MUST stay in the JWKS for the maximum L1 lifetime. That keeps the card-credential chain verifiable but does not address keeping the record. E4 not met. | `security-model.md` 2.5, 3.2 (line 127), 6.6; `credential-format.md` 6.3 |
| L8 Redress | 0 | R1 not met. R2: the dispute-evidence package is a payment-dispute mechanism, and VI "does not define how disputes are initiated, routed ... It does not assign liability". Payment-only. | `security-model.md` 2.4, 2.5 |

Row: 1, 1, 1, 1, 1, 1, 0, 0, 1, 1. Chain score 0. Total 8 / 20.
Compared with `scores.json`: L4 2 to 1 (D1 and D2 are payment-only in content), L6 2 to 1, L7 1 to 0, L8 1 to 0. L1, L2, L3, L9, L10 kept. L1 rests on a payment-card credential, but the variant does not change L1, so it is kept.

Action classes:

| Class | Rating | Basis |
|---|---|---|
| A. Read | partial | Only through a custom URN constraint type (`constraints.md` 6.1). None defined. |
| B. Communicate | partial | Same. |
| C. Change state | partial | Same. |
| D. Legally significant act | partial | Same. |
| E. Pay | yes | `mandate.payment.*` and `mandate.checkout.*`. |
| F. Delegate onward | no | L3 MUST NOT contain `cnf`, which "prevents agents from sub-delegating" (`security-model.md` 3.3; `credential-format.md` 5.5). |

Unsure cells (VI):
- L7 = 0 versus 1. The retired-key retention rule is a generic E3 element, but it covers the issuer key of a card credential, not the action record.
- L4 = 1 versus 2. If the chain mechanism (which is generic SD-JWT) is credited without the content, D1 and D2 would be met and L4 = 2.
- L6 = 1 versus 2, for the same reason.
- L8 = 0 versus 1, as for AP2.

---

## 7. UCP v2026-08-25 (core plus Identity Linking, Buyer Consent and AP2 Mandates as optional extensions)

| Link | Score | Tests met / not met | Citation |
|---|---|---|---|
| L4 Delegation | 1 | D1 partial (extension): Identity Linking scopes `{capability}:{scope}` such as `dev.ucp.shopping.order:read`, `order:manage` and `checkout:manage`. Third-party capabilities may define their own scopes. D2 partial: scopes name an operation group on a resource, and a business may add custom scopes "at finer granularity" (for example to gate `complete`). Per-scope policy can add `min_acr`, `max_token_age`, `require_mfa`. No recipient, count or rate. D3 partial: the user consents at the business's own authorisation server, which issues the token. D4 met: a revocation endpoint (MUST) and token expiry. All of this sits in an optional extension. | `common/identity-linking/index.md` "Scopes", "Scope Token Format", "Per-Scope Policy and Metadata" |
| L5 Session authentication | 1 | S1 partial: RFC 9421 signatures SHOULD, with API keys, OAuth or mTLS allowed instead. S2 partial: signed `Idempotency-Key` is the replay control. S3 partial: per-scope `min_acr`, `max_token_age` and `require_mfa` give an assurance-level step-up for any scoped operation, returned as 403 `insufficient_scope` with `requires_buyer_review`. It is a re-authentication gate in an optional extension, not a re-confirmation of the specific action. | `signatures.md` "Replay Protection"; `identity-linking/index.md` "Per-Scope Policy", "`insufficient_scope`" |
| L6 Action conformance | 1 | A1 partial: the user token is presented on every gated request and checked for audience and `azp`. For purchases, `checkout_mandate` embeds the signed checkout (extension, payment-specific). A2 partial: the business enforces scope per operation (MUST, 401 `identity_required` or 403 `insufficient_scope`), which is a scope check. | `identity-linking/index.md` "Error Handling"; `payment/extensions/ap2-mandates.md` |
| L7 Evidence | 1 | E1 partial: webhooks MUST be signed by the business and report order events, including `cancellation`, `return` and fulfilment events, which are not only payments. The business is named only by its profile domain. E2 not met: `occurred_at` and `Webhook-Timestamp` are business-asserted. E3 partial: the AP2 extension notes mandates may be verified "days or months later", but key removal undercuts it and no retention rule exists. E4 partial: webhooks carry the business's outcome, but signed responses to the platform's request are only RECOMMENDED. | `signatures.md` "When Signatures Apply"; `shopping/order/index.md` (Adjustments, `occurred_at`) |
| L8 Redress | 1 | R1 not met for non-monetary harm: the Merchant of Record "financial liability" appears only in the glossary and is monetary. R2 partial: typed order `adjustments` (`cancellation`, `return`, `dispute`, `refund`) give a defined way to cancel or return, and the Buyer Consent extension lets a buyer's consent state be overridden ("unsubscribe affordance"). Both are commerce-bound, and adjustments are "typically money movements". No initiation or arbitration path. | `shopping/order/index.md` "Adjustments"; `shopping/extensions/buyer-consent.md` "Scope"; `glossary.md` |

Row: 1, 1, 0, 1, 1, 1, 1, 1, 1, 1. Chain score 0. Total 9 / 20.
Compared with `scores.json`: L4 to L8 unchanged in value, but each now rests on non-payment text (scopes, signed order events, cancellation and consent records) where possible. L1, L2, L3, L9, L10 kept.

Action classes:

| Class | Rating | Basis |
|---|---|---|
| A. Read | yes | `dev.ucp.shopping.order:read`, plus identity `claims` in per-scope policy (Identity Linking "Scopes"). |
| B. Communicate | partial | Third-party capabilities may define scopes (`com.example.loyalty:points`). No message semantics. |
| C. Change state | yes | `dev.ucp.shopping.order:manage` ("cancel, return, or modify post-purchase") and `checkout:manage`; order `adjustments` record the changes. |
| D. Legally significant act | yes | Buyer Consent extension: purposes and segments with `granted`, `source` and `description`, carried in `buyer.consent` (`shopping/extensions/buyer-consent.md`). The consent state is unsigned and asserted by the platform or business, so the evidence side is weak. |
| E. Pay | yes | Checkout completion, payment handlers, and the AP2 Mandates extension. |
| F. Delegate onward | no | No sub-delegation. AP2's Agent-to-Agent delegation is out of scope, and a pointer to AP2 earns nothing. |

Unsure cells (UCP):
- L8 = 1 versus 0. Both R2 elements are bound to commerce orders or data-use consent. If those count as payment-only, 0.
- D = yes versus partial. The consent record is defined, but unsigned.
- L5 S3 and L4 are optional-extension-only, so they cap at 1.
- L3 = 0 carried over (platform keys self-published).

---

## Summary table

| Protocol | L1 | L2 | L3 | L4 | L5 | L6 | L7 | L8 | L9 | L10 | Chain | Total | A | B | C | D | E | F |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| PAP 1.0 | 0 | 1 | 1 | 1 | 1 | 1 | 0 | 0 | 1 | 1 | 0 | 7 | partial | partial | yes | partial | partial | no |
| MCP 2026-07-28 + EAA | 1 | 1 | 0 | 1 | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 6 | partial | partial | partial | partial | partial | no |
| A2A 1.0.1 | 0 | 1 | 0 | 1 | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 5 | partial | partial | partial | partial | partial | partial |
| Web Bot Auth -01 | 0 | 1 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | no | no | no | no | no | no |
| AP2 v0.2.0 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 0 | 1 | 2 | 0 | 10 | partial | partial | partial | partial | yes | no |
| Verifiable Intent v0.1 | 1 | 1 | 1 | 1 | 1 | 1 | 0 | 0 | 1 | 1 | 0 | 8 | partial | partial | partial | partial | yes | no |
| UCP v2026-08-25 | 1 | 1 | 0 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 0 | 9 | yes | partial | yes | yes | yes | no |

No protocol has a chain with no missing link at 1 under this variant. Only UCP defines non-payment semantics for A, C and D, and its evidence for them (signed order webhooks, unsigned consent state) is thin.

## Cross-cutting unsure cells

- "Partial" for classes with only a generic extension point (a scope string, a tool name, a skill, a custom mandate or constraint type) is applied the same way for every protocol. A stricter reading would mark the generic cases "no" and leave only UCP, PAP (class C) and the payment protocols (class E) above no.
- In-flight cancellation (MCP cancellation utility, A2A `CancelTask`) was not credited as R2 for either protocol. Crediting it would lift each L8 to 1 and change nothing in the chain score.
- MCP, A2A and WBA text was read from earlier fetched copies of the primary pages, not re-fetched in this run. PAP was re-fetched, and the AP2, VI and UCP revisions were checked against the upstream tags and HEAD.
