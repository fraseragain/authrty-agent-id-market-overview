# General-actions chain scores, group B (ACP, Visa TAP, x402, MPP, ERC-8004, x401, KYA-OS)

Rubric: `ov/research/agent-protocol-comparison/chain-rubric-general-actions.md` (variant of `chain-rubric.md`). Read 25 Nov 2026. L1, L2, L3, L9, L10 are carried over from `scores.json` `chain_scores` (reviewed purchase scores); the variant does not change their tests. L4 to L8 were re-scored from the primary text already held locally: `src/agentic-commerce-protocol` (spec/2026-04-17 plus rfcs and docs), `cmp2/raw/visa-spec.txt` (TAP, raw page), `g3/x402/specs`, `g3/mpp-specs/specs`, `cmp2/src/erc8004.txt`, `g4/x401/spec.md`, `g4/kya/*` (SPEC, SPEC-MCP-EXTENSION, SPEC-ENTITY-CARD) and `cmp2/src/AUDITABILITY.md`.

Rules applied: in-spec text only; a pointer to another protocol earns nothing; a shared identifier is not a cryptographic link; a self-published key is not an accountable binding; unread features are not credited. Payment-only mechanisms (amount-limited allowances, payment receipts, refunds, chargebacks, payment challenges) earn nothing in L4 to L8 unless the same mechanism also covers a non-payment action. A scope-only check is partial in L6 (A2). Chain score = lowest link; total = sum of L1 to L10.

## Summary rows

| Protocol | L1 | L2 | L3 | L4 | L5 | L6 | L7 | L8 | L9 | L10 | Chain | Total | A | B | C | D | E | F |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ACP 2026-04-17 | 1 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 1 | 0 | 3 | partial | no | partial | partial | yes | no |
| Visa TAP | 1 | 1 | 1 | 0 | 1 | 0 | 0 | 0 | 1 | 1 | 0 | 6 | partial | no | no | no | yes | no |
| x402 v2 | 0 | 1 | 0 | 0 | 1 | 0 | 1 | 0 | 1 | 1 | 0 | 5 | partial | no | partial | no | yes | no |
| MPP | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 1 | 1 | 0 | 4 | partial | no | no | no | yes | no |
| ERC-8004 | 0 | 1 | 1 | 0 | 0 | 0 | 1 | 0 | 1 | 1 | 0 | 5 | partial | no | partial | no | partial | no |
| x401 0.2.0 | 1 | 1 | 0 | 1 | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 6 | partial | partial | partial | partial | no | no |
| KYA-OS 1.0.0 | 1 | 1 | 1 | 2 | 1 | 2 | 1 | 1 | 1 | 1 | 1 | 12 | partial | partial | partial | partial | yes | yes |

Change from the reviewed purchase scores (`scores.json`): ACP L4 1 to 0, L6 1 to 0; TAP L7 1 to 0; x402 L4 1 to 0, L6 1 to 0, L8 1 to 0; MPP L4, L5, L6, L7, L8 each 1 to 0; ERC-8004 none; x401 none; KYA-OS L8 0 to 1 (KYA-OS chain score 0 to 1). L1, L2, L3, L9, L10 unchanged for all seven.

---

## 1. ACP release 2026-04-17

Source: local clone `src/agentic-commerce-protocol` (HEAD `7fdd78d`, later than the release commit; the release commit `9abf303` is not in the clone). Normative text taken from `spec/2026-04-17/{json-schema,openapi,openrpc}`. Rfcs and docs were used only for context, and `rfc.orders.md` carries later revisions (dated 2026-04-23), so nothing in L4 to L8 rests on it alone.

| Link | Score | Tests met / not met | Citation |
|---|---|---|---|
| L4 Delegation | 0 | The only grant is the `delegate_payment` `Allowance` (`max_amount`, `currency`, `checkout_session_id`, `merchant_id`, `expires_at`, `reason: one_time`). It is a payment-only mechanism and carries no operation, tool, resource or data scope, so under the variant D1 and D2 earn nothing outside E. D3 not met (vault token issued by the PSP on the buyer's behalf). D4 met for the token only. Nothing in the spec grants the agent anything for read, message, state-change or consent actions; the bearer token on the other endpoints is bilateral and unspecified. | `json-schema/schema.delegate_payment.json` `Allowance`; `openapi/openapi.delegate_payment.yaml`; `rfc.discovery.md` s2.2 (agent registration "separate concerns") |
| L5 Session authentication | 1 | S1 partial: `Signature` over canonical JSON is a parameter on every checkout and cancel operation, but SHOULD-level. S2 met: `Idempotency-Key` MUST on POSTs, `Timestamp`, webhook timestamp window. Both apply to non-payment operations (update, cancel). S3 partial at best: the 3DS `authentication_result` is card-only step-up, so it is payment-only and earns partial. No step-up for non-payment actions. | `openapi/openapi.agentic_checkout.yaml` parameters `Signature`, `Timestamp`, `IdempotencyKey`; `schema.agentic_checkout.json` `AuthenticationResult`; `openapi.delegate_authentication.yaml` |
| L6 Action conformance | 0 | A1 not met for non-payment actions: update, cancel and read requests carry no reference to any grant. For payment, the token and allowance reference `checkout_session_id` and `merchant_id`, which is payment-only. A2 not met: no check of an operation on a resource against a grant outside the PSP's token check. | `openapi.agentic_checkout.yaml` (`updateCheckoutSession`, `cancelCheckoutSession`); `schema.delegate_payment.json` `Allowance` |
| L7 Evidence | 0 | E1 not met: the order webhook is an HMAC `Merchant-Signature` under a shared secret, which a third party cannot verify; API responses are unsigned. E2 not met: sender-asserted times. E3 not met: only 24 h idempotency retention. E4 not met: nothing signs the counterparty's response. | `openapi/openapi.agentic_checkout_webhook.yaml` header; `rfc.delegate_payment.md` s2.4 |
| L8 Redress | 0 | R1 not met: no allocation of responsibility, monetary or not. R2 not met under the variant: every remedy is purchase-specific (`cancel` of an uncompleted session; `Adjustment` records of `refund`, `return`, `dispute`; order management is out of scope in `rfc.orders.md`). Chargebacks and refunds alone score 0, and a pre-completion cancel does not remedy an executed action. | `openapi.agentic_checkout.yaml` `cancelCheckoutSession`; `schema.agentic_checkout.json` `Adjustment`; `rfc.orders.md` header ("Out of scope: Order management APIs") |

L1 1, L2 0, L3 0, L9 0, L10 1: carried over, unchanged.
Row: 1 0 0 0 1 0 0 0 0 1. Chain 0. Total 3.

| Class | Rating | Citation |
|---|---|---|
| A Read or retrieve | partial | `GET /checkout_sessions/{id}`, cart read and the merchant-to-agent Feed API exist, but no grant or record covers a data scope. `openapi.agentic_checkout.yaml`, `openapi.feed.yaml` |
| B Communicate | no | Nothing expresses sending a message for the buyer. |
| C Change state | partial | Create, update and cancel of a checkout session are defined operations; the grant (`Allowance`) does not cover them. `openapi.agentic_checkout.yaml` |
| D Legally significant | partial | `MarketingConsent` decisions per channel are captured on complete; `Disclosure` and `Link terms_of_use` are display only, with no acceptance record or signature. `schema.agentic_checkout.json` `MarketingConsent`, `Disclosure`, `Link` |
| E Pay | yes | `delegate_payment` allowance plus `complete`. `schema.delegate_payment.json` |
| F Delegate onward | no | No sub-delegation or agent-to-agent instruction. |

Unsure cells (ACP): L8 (1 if a cancel path and typed adjustments are credited as remedies regardless of purchase scope); L5 (S1 is SHOULD, so 0 is defensible); D marketing consent (could be yes as a defined consent record, but it is unsigned and narrow).

---

## 2. Visa Trusted Agent Protocol

Source: Visa developer specification page, raw (`cmp2/raw/visa-spec.txt`, same text as `src/tap-spec.txt`). VIC pages not credited.

| Link | Score | Tests met / not met | Citation |
|---|---|---|---|
| L4 Delegation | 0 | No grant artefact (D1 to D4 not met), as in the purchase scoring. The spec covers only two interactions: browsing and payment. | "Overview" (two interactions), whole page: no grant object |
| L5 Session authentication | 1 | S1 met and S2 met: RFC 9421 signature over `@authority` and `@path` with `created`, `expires`, `nonce`, `keyid`, `tag`, on both browsing and payment requests (action-agnostic). S3 not met for any class: only optional `auth_time` and `amr` in the ID token, with no step-up. | "Required Message Signature Fields"; "Verification Steps" (timestamps, nonce); "ID Token" claims |
| L6 Action conformance | 0 | A1 not met: no grant to reference. A2 not met: the signature covers only authority and path plus `tag` (`agent-browser-auth` or `agent-payer-auth`); there is no check of operation or resource against a grant. | "Required Message Signature Fields" (components `@authority`, `@path`, `tag`) |
| L7 Evidence | 0 | E1 not met: the agent-signed request records which authority and path were hit, but not the operation (`@method` is not covered) or inputs (no body digest); `agenticPaymentContainer` and `browsingIOU` are payment-only. E2 not met: `created` is agent-asserted. E3 not met: nonces are kept 8 minutes; no retention. E4 not met: nothing signs the merchant's response. | "Required Message Signature Fields"; "Payment"; "Browsing IOU"; "Verification Steps" |
| L8 Redress | 0 | R1 and R2 not met: no allocation, dispute path or remedy defined. | whole page: no text |

L1 1, L2 1, L3 1, L9 1, L10 1: carried over, unchanged.
Row: 1 1 1 0 1 0 0 0 1 1. Chain 0. Total 6.

| Class | Rating | Citation |
|---|---|---|
| A Read or retrieve | partial | Signed `agent-browser-auth` interaction for retrieving product information or "paid access to a Merchant resource"; no grant and no data scope. "Overview"; "Agent Recognition Signature" |
| B Communicate | no | Not defined. |
| C Change state | no | Not defined. |
| D Legally significant | no | Not defined. |
| E Pay | yes | `agent-payer-auth` signature, `agenticPaymentContainer`, `browsingIOU`. "Payment"; "Browsing IOU" |
| F Delegate onward | no | Not defined. |

Unsure cells (TAP): L7 (1 if the signed request on a named authority and path counts as a partial E1; the purchase pass scored 1); A (a defined browse tag is a record class, yes is arguable).

---

## 3. x402 v2 (core, in-repo extensions and schemes)

Source: `g3/x402/specs` at `866e399`: `x402-specification-v2.md`, `extensions/*`, `schemes/*`, `transports-v2/mcp.md`.

| Link | Score | Tests met / not met | Citation |
|---|---|---|---|
| L4 Delegation | 0 | The only grant-like artefact is the payer's EIP-3009 `authorization` or the `upto` / `auth-capture` limits: payment-only. No grant for any non-payment operation. "Client-side budget management" is out of scope. `sign-in-with-x` signs a login message (`uri`, `resources`, `expirationTime`) by the wallet itself; it authenticates the payer and is not a grant to an agent (D1 not met, D3 not distinguishable). | core "Document Scope" (out of scope list), s5.2.1 to 5.2.2; `extensions/sign-in-with-x.md` "Message Metadata" |
| L5 Session authentication | 1 | S1 partial: RFC 9421 per-request signature in `http-message-signatures` and the SIWX wallet signature, both usable on non-payment requests to a gated resource. S2 met: SIWX `nonce`, `issuedAt`, `expirationTime`; payment nonce. S3 not met: no step-up for any class; `auth-hints` is client authentication. | `extensions/http-message-signatures.md` "Usage"; `sign-in-with-x.md`; `extension-auth-hints.md` ("Authentication Without Hints") |
| L6 Action conformance | 0 | A1 not met for non-payment: nothing references a grant for a non-payment operation (the payload `accepted` and `resource` echo payment terms). A2 not met: facilitator `/verify` checks the payment only. | core s5.2.1, s6.1, s7.1 |
| L7 Evidence | 1 | E1 partial: the optional receipt is signed by the server (DID, DNS or registry authorised) and names `resourceUrl`, `payer`; it records neither the operation nor the inputs. E2 met: `issuedAt` server-signed. E3 partial: SHOULD preserve evidence; the receipt is optional and says it omits the transaction reference by default. E4 partial: the receipt is issued "after successful payment and service delivery", so it is a server-signed statement of outcome, but only for a paid resource and without response content. The record is payment-gated, so this is the weakest credit available. | `extensions/extension-offer-and-receipt.md` s1, s5.2, s5.5 |
| L8 Redress | 0 | R1 not met. R2: `void`, `refund`, `reclaim` in `auth-capture` are payment remedies only; `exact` is irreversible. | `schemes/auth-capture/scheme_auth_capture.md` (operations); core s6 |

L1 0, L2 1, L3 0, L9 1, L10 1: carried over, unchanged.
Row: 0 1 0 0 1 0 1 0 1 1. Chain 0. Total 5.

| Class | Rating | Citation |
|---|---|---|
| A Read or retrieve | partial | Payment and receipt bind `resource.url`; SIWX binds `uri` and `resources`. Gated retrieval only, no data scope. core s5.1; `sign-in-with-x.md` |
| B Communicate | no | Not expressed. |
| C Change state | partial | MCP binding gates a named tool (`mcp://tool/...` in `resource`); the payment, not an operation grant, is signed. `transports-v2/mcp.md` |
| D Legally significant | no | Not expressed. |
| E Pay | yes | `exact`, `upto`, `auth-capture`, `batch-settlement`. `schemes/` |
| F Delegate onward | no | Not expressed; A2A transport pays for tasks but defines no onward grant. |

Unsure cells (x402): L7 (0 if a payment-gated receipt earns nothing); L5 (SIWX and message-signature extensions authenticate the client, not the human or an agent grant; 0 on a strict reading); L10 (the shared `payer` across authorisation, settlement and receipt is a payment-only continuity, kept at 1 as the variant leaves L10 unchanged); class cells A and C (partial only because the payment names a resource or tool).

---

## 4. MPP (tempoxyz/mpp-specs)

Source: `g3/mpp-specs/specs` at `aeaeb83`: core `draft-httpauth-payment-01`, intents, `methods/{tempo,stripe,card,lightning,...}`, `extensions/transports/draft-payment-transport-mcp-00`, `extensions/draft-payment-discovery-01`.

| Link | Score | Tests met / not met | Citation |
|---|---|---|---|
| L4 Delegation | 0 | Core has no grant. The Tempo `keyAuthorization` is payment-only: per-period token limit, recipient allowlist, `allowed_calls` restricted to `transfer` selectors, and the spec forbids any other selector ("MUST NOT authorize `approve` or any other non-transfer selector"). The Stripe SPT is a payment token. No grant for non-payment actions. | `methods/tempo/draft-tempo-subscription-00.md` "Key Authorization"; `methods/stripe/draft-stripe-charge-00.md` |
| L5 Session authentication | 0 | S1 not in core (`payload` is "method-specific payment proof"). S2 met in core, but only for payment challenges (HMAC-bound `id`, `expires`, single-use proof). S3 not met. Everything that authenticates is a payment proof, so the variant gives nothing. | core "Challenge Binding", "Replay Protection", Credentials table |
| L6 Action conformance | 0 | A1: the credential echoes the payment `challenge`; the optional `digest` binds the challenge to the request body (SHOULD), but there is no grant for a non-payment action. A2 not met: Tempo scope verification covers payment terms only. | core "Request Body Digest Binding"; `draft-tempo-subscription-00.md` "Authorization Scope Verification" |
| L7 Evidence | 0 | E1 not met: `Payment-Receipt` is unsigned, SHOULD-level JSON naming `status`, `method`, `timestamp`, `reference`, with no operation or inputs. E2 not met (server-asserted time). E3 not met. E4 not met. | core "Payment-Receipt Header" |
| L8 Redress | 0 | R1 not met. R2: the card method's chargeback reference is 0 under the earlier rule; refunds of unspent session deposits and the dispute-mapping MUST (Tempo session) concern payments only. | `methods/card/draft-card-charge-00.md`; `methods/tempo/draft-tempo-session-00.md`; `methods/lightning/draft-lightning-session-00.md` |

L1 1, L2 0, L3 1, L9 1, L10 1: carried over, unchanged.
Row: 1 0 1 0 0 0 0 0 1 1. Chain 0. Total 4.

| Class | Rating | Citation |
|---|---|---|
| A Read or retrieve | partial | A paid HTTP resource under a `realm`, with an optional request-body `digest`; the MCP transport allows `tools/call` and resource access to be gated. core "Request Body Digest Binding"; `draft-payment-transport-mcp-00.md` |
| B Communicate | no | Not expressed. |
| C Change state | no | The signed artefact names `realm`, `method`, `intent`, `request` and no operation or tool; a gated `tools/call` is possible but nothing binds the tool. |
| D Legally significant | no | Not expressed. |
| E Pay | yes | Intents `charge`, `subscription`, sessions. `specs/intents/` |
| F Delegate onward | no | Not expressed. |

Unsure cells (MPP): L5 (1 if the core challenge binding and single-use proof are credited as action-agnostic HTTP authentication); L8 (0 here on payment-only grounds, consistent with x402); class A and C (the credential does not name a resource or tool, unlike x402's `resource`).

---

## 5. ERC-8004 Trustless Agents (Draft)

Source: `cmp2/src/erc8004.txt` (ERC page text); `g3/eip8004.txt` cross-checked in the earlier pass.

| Link | Score | Tests met / not met | Citation |
|---|---|---|---|
| L4 Delegation | 0 | No grant artefact. ERC-721 owner and operator approval governs the registration file only. | Identity Registry opening paragraph ("delegate management ... to operators") |
| L5 Session authentication | 0 | No per-request or per-session proof, no step-up; authentication is left to A2A and MCP (a reference to another protocol earns nothing). | Motivation |
| L6 Action conformance | 0 | No grant, so no reference and no check. | n/a |
| L7 Evidence | 1 | E1 partial: `validationRequest` MUST be called by the owner or operator, with `requestURI` holding "all information needed ... including inputs and outputs" and `requestHash` as the commitment; `validationResponse` is called by the named validator. This is action-agnostic evidence of what was done and with what inputs, signed by an address (pseudonymous). E2 met: ledger time, `lastUpdate`. E3 met: "On-chain pointers and hashes cannot be deleted". E4 partial: the validator's `response` (0 to 100) and `responseHash` evidence an assessment of the outcome, not the counterparty's own response. Optional, and only when the agent chooses to request validation. | Validation Registry "Validation Request", "Validation Response"; Security Considerations |
| L8 Redress | 0 | R1 not met. R2: `revokeFeedback` and `appendResponse` annotate a reputation signal, not the action; slashing is out of scope. | Reputation Registry "Revoking Feedback", "Appending Responses"; Validation Registry closing line |

L1 0, L2 1, L3 1, L9 1, L10 1: carried over, unchanged.
Row: 0 1 1 0 0 0 1 0 1 1. Chain 0. Total 5.

| Class | Rating | Citation |
|---|---|---|
| A Read or retrieve | partial | The feedback file can name `mcp.resource`; validation inputs and outputs are generic. Reputation Registry "Off-Chain Feedback File Structure" |
| B Communicate | no | Not expressed. |
| C Change state | partial | `mcp.tool` and `a2a.skills`/`taskId` can be named in feedback; no operation semantics. same |
| D Legally significant | no | Not expressed. |
| E Pay | partial | Optional `proofOfPayment` in the feedback file; "Payments are orthogonal to this protocol". Motivation; feedback file |
| F Delegate onward | no | Owner-to-operator approval is registry management, not onward action. |

Unsure cells (ERC-8004): L7 (0 if feedback and validation records about an agent's work are not "a record of the action"; they are optional and name the agent, not a principal); classes A and C (partial only through free-form fields).

---

## 6. x401 Standard Draft 0.2.0

Source: `g4/x401/spec.md` (proof/x401).

| Link | Score | Tests met / not met | Citation |
|---|---|---|---|
| L4 Delegation | 1 | D1 partial: the optional Verification Token records what the Verifier accepted; it is not a grant by the principal to the agent. D2 met under the variant: the token MUST be scoped to the audience and to "the route, policy, action, resource, or resource class", MUST expire; method and action claims are SHOULD. D3 not met: the Verifier issues it; principal delegation is an open question ("Fully Autonomous Delegation"). D4 met: MUST expire, SHOULD support revocation. | "Verification Token Contents" items 2, 3, 4, 6; "Open Questions" |
| L5 Session authentication | 1 | S1 partial: optional layers only (and those are other protocols). S2 met for the credential result: OpenID4VP `nonce`, request expiry. S3 not met: no step-up or assurance for any class (`assurance_level` in a credential request is an issuer-attested claim, not human re-confirmation). | "Proof Validation" 4; "Replay Prevention"; "Agent Binding" |
| L6 Action conformance | 1 | A1 partial: the retry presents the token (or Result Artifact) for the same route; the token names `request_id`, resource and method, so the reference is to the proof decision, not to a principal grant. A2 partial: Verifier MUST validate "token scope, audience, expiration, any Agent binding, and satisfied requirement metadata" before serving. This is a scope-level check; method and action claims are SHOULD. Not payment-specific: the spec's example is `POST /accounts/applications`. | "Verifier Processing Rules" 13 and 14; "Verification Token Contents"; "x401 Gated Resource Configuration" (example) |
| L7 Evidence | 0 | E1 not met: the token records "a Verifier's decision that a credential result satisfied" a requirement and is "not a credential, payment artifact, or new issuer attestation"; no record of the action. E2 not met in a defined form. E3 not met. E4 not met. | "Verification Token Contents" |
| L8 Redress | 0 | R1 and R2 not met. Payment and disputes are out of scope; the token SHOULD be revocable, which does not remedy an action. | "Payment Separation"; "Verification Token Scope" |

L1 1, L2 1, L3 0, L9 1, L10 0: carried over, unchanged.
Row: 1 1 0 1 1 1 0 0 1 0. Chain 0. Total 6.

| Class | Rating | Citation |
|---|---|---|
| A Read or retrieve | partial | Route-scoped proof gate with token scoped to "resource, or resource class"; no data-scope semantics. "Verification Token Contents" |
| B Communicate | partial | Any route can be gated, but nothing names a message or recipient. same |
| C Change state | partial | Token scoped to "action" and "method"; example gates `POST /accounts/applications`. "x401 Gated Resource Configuration" |
| D Legally significant | partial | The gated example is an application submission, but the spec defines no consent or signature record; the proof is of a credential, not of an act. same |
| E Pay | no | "A proof artifact MUST NOT be treated as payment"; 402 is separate. "Payment Separation" |
| F Delegate onward | no | "Delegation and Actor Evidence" only names other protocols as possible carriers (a reference earns nothing); onward delegation is an open question. |

Unsure cells (x401): L4 (D2 is met under the variant, but D1 and D3 keep it at 1; 0 if the token is treated as an access decision and not a grant); L6 (1; A2 would be met if the SHOULD method and action claims were MUST); classes A to D are all partial because the same generic route and action scope covers each.

---

## 7. KYA-OS v1.0.0

Source: `g4/kya/SPEC.md`, `SPEC-MCP-EXTENSION.md`, `SPEC-ENTITY-CARD.md`; `cmp2/src/AUDITABILITY.md`.

| Link | Score | Tests met / not met | Citation |
|---|---|---|---|
| L4 Delegation | 2 | D1 met: `DelegationCredential` VC. D2 met for non-payment actions: CRISP `scopes` (tool names and resource patterns with `exact`, `prefix`, `path-prefix`, `regex` matchers), `audience`, `notBefore`/`notAfter`, and `budget` with unit `ops` (a count) as well as `USD` and `points`; ZCAP `allowedAction` and `invocationTarget`. D3 met on the model: the root `issuerDid` is the Responsible Party's DID and the signer. D4 met: validity window, status list, cascading revocation. D5 met (not required). | SPEC s6.2, s6.3 (CRISP envelope, matchers), s6.4, s6.5, s6.6, s6.10 |
| L5 Session authentication | 1 | S1 met: per-request holder-of-key proof. S2 met: nonce, `ts` window, `jti`, MUST-level nonce retention. S3 partial: a `needs_authorization` challenge returns a signed consent step-up with `authorizationUrl` ("User authenticates and grants authorization") when delegation is missing or insufficient, for any tool. It is triggered by missing scope, not by risk, and captures no assurance level. | SPEC s5.2, s5.5, s7.8, s9.1 to 9.3; SPEC-MCP-EXTENSION s7.2 |
| L6 Action conformance | 2 | A1 met: the request proof MUST state `delegationRef` and `delegationChainDigest`; a verifier MUST refuse a mismatch. A2 met: the verifier checks the scope designation, audience, window and caveats for the tool and resource called ("MUST hold each call to every caveat ... or refuse") before the handler runs. Action-agnostic. | SPEC s6.4.1, s7.8, s6.10 (caveats), s11.6 |
| L7 Evidence | 1 | E1 met: the detached JWS proof binds `requestHash` (operation and inputs), `responseHash`, `delegationRef`, `delegationChainDigest` and `outcome`, signed by the server's DID key (did:web resolves to an organisation, not necessarily an accredited one). E4 met: the response and the outcome (`allowed`, `denied`, `step_up_required`, `needs_authorization`) are signed by the acting server, and the request proof by the agent. E2 partial: `ts` is the signer's own claim; independent time only in the optional Audit Assurance Profile. E3 partial: SHOULD keep old keys (s11.5), retention SHOULD-level (s12.4); replay bundles and offline re-verification only in the audit profile. Score stays 1 because E2 and E3 are not met by core. | SPEC s7.2 (ProofMeta), s7.4, s11.5, s12.4, s15.3; AUDITABILITY "Replay bundles", "Evidence, retention, and access" |
| L8 Redress | 1 | R1 partial: "Every chain MUST terminate at a Responsible Party" who is "the entity ultimately accountable for actions taken under any descendant delegation". That names one accountable role for any action (not only payments), but it does not allocate responsibility between roles or address unauthorised or mistaken action. R2 partial: the Responsible Party, the direct issuer or an ancestor can revoke a delegation, with cascading revocation, status-list update and MUST-level propagation, which is a way to revoke a consent. It is prospective only, with a stated revocation race; there is no rollback, cancel or incident-report path. AUDITABILITY says only that the evidence "supports audit, incident-response". | SPEC s2 (Responsible Party), s6.4 line "Every chain MUST terminate", s6.5, s6.5.1, s6.5.2; AUDITABILITY opening |

L1 1, L2 1, L3 1, L9 1, L10 1: carried over, unchanged.
Row: 1 1 1 2 1 2 1 1 1 1. Chain 1. Total 12.

| Class | Rating | Citation |
|---|---|---|
| A Read or retrieve | partial | `tool:read_file`, `files:read` scopes with `path-prefix` matching for files and URL paths; scope strings are opaque to the protocol. SPEC s6.2 example, s6.3 |
| B Communicate | partial | Any named tool, with `constraints` an opaque record; no recipient semantics. SPEC s6.3 |
| C Change state | partial | `allowedAction`, tool and resource matchers, `files:write`; no state-change semantics. SPEC s6.10, s7.8 example |
| D Legally significant | partial | Generic tool scope; consent is only for granting the delegation itself (`needs_authorization`), not for an act. SPEC s9 |
| E Pay | yes | CRISP `budget` (`USD`), ZCAP `MaxAmount`, `allowedAction: payments.transfer`. SPEC s6.3, s6.10 |
| F Delegate onward | yes | Multi-hop delegation graph with scope, budget and validity narrowing, `parentCredentialDigest`, cascading revocation, and outbound propagation headers. SPEC s6.4, s6.10 (attenuation invariants), s8 |

Unsure cells (KYA-OS): L8 (the only change from the purchase score; 0 if "ultimately accountable" is not an allocation between roles and revocation is not a remedy, which would leave the chain score at 0 as before); L5 S3 (partial credit for the consent step-up; 1 either way); L7 (2 would need E2 and E3 in core); classes A to D (partial because the scope strings carry no class semantics, yes is arguable for A).

---

## Cross-cutting notes

- The purchase scores for ACP, TAP, x402 and MPP fall because their grants, receipts and remedies are payment mechanisms. Only x402's receipt (names a resource, server-signed) and ERC-8004's validation records (carry inputs and outputs) keep any L7 credit.
- x401 and KYA-OS are the two protocols whose grant or token is not payment-specific. x401 holds at chain 0 because it has no action record and no redress; KYA-OS is the only one with a nonzero chain (1, via L8).
- Class F is yes only for KYA-OS. For x401, "Delegation and Actor Evidence" names other protocols and earns nothing.
