# Scores group 2: AP2, Verifiable Intent, UCP, ACP

Rubric: [rubric.md](rubric.md) (16 criteria, 1 / 0.5 / 0). All four scored on basis `spec` (primary spec text cloned from GitHub). Sources were cloned read-only into (local working copy, not committed) no repository was edited. Flagged items are marked (?).

## Summary

| Protocol | Identity | Authentication | Authorisation | Accountability | Total /16 |
|---|---|---|---|---|---|
| AP2 v0.2.0 | 2.5 | 3.5 | 4 | 3 | 13 |
| Verifiable Intent v0.1-draft | 3 | 3.5 | 4 | 2.5 | 13 |
| UCP v2026-08-25 (with its official extensions) | 3 | 3.5 | 2 | 1.5 | 10 |
| ACP 2026-04-17 (with delegate payment) | 1.5 | 2.5 | 3.5 | 1.5 | 9 |

## 1. AP2 (Agent Payments Protocol) v0.2.0

Read: github.com/google-agentic-commerce/AP2 at HEAD (CHANGELOG 0.2.0, 2026-04-28), `docs/ap2/specification.md`, `agent_authorization.md`, `checkout_mandate.md`, `payment_mandate.md`, `security_and_privacy_considerations.md`, `implementation_considerations.md`. Basis: spec.

| ID | Score | Justification |
|---|---|---|
| I1 | 0.5 | No user-ID claim. The user is represented only by the issuer-signed User Credential and its `cnf` key (agent_authorization.md, "User Credential"); mandates carry `payee`, `payment_instrument`, no subject (?). |
| I2 | 0.5 | Trusted Agent Provider model: mandate `iss` is the agent provider (agent_authorization.md). In the User Credential model the agent is only a `cnf` key. implementation_considerations.md "Agent Identification" leaves agent identity to the commerce protocol. |
| I3 | 1 | User Credential issued by a third party (example `com.emvco.dpc`, issuer `iss`) that the verifier trusts (agent_authorization.md, "User Credential"). |
| I4 | 0.5 | Issuer-signed SD-JWT VC is verifiable by the counterparty. The spec defines no legal-identity claims and puts issuance out of scope (?). |
| A1 | 1 | Open mandates MUST carry `cnf`; closed mandates are Key Binding JWTs signed with that key (agent_authorization.md, "Mandate Structure"; specification.md, "Autonomous"). |
| A2 | 0.5 | Agent key is inline in signed `cnf.jwk`. Issuer or agent-provider key resolution is not defined; only "trust list of Agent Providers" is mentioned (specification.md, "Modes"). The OpenID4VP example uses `x509_san_dns` (?). |
| A3 | 1 | Closed mandate KB-JWT carries `aud`, `nonce`, `iat` (checkout_mandate.md and payment_mandate.md examples). Double-spend rules and `sd_hash` binding (security_and_privacy_considerations.md). |
| A4 | 1 | Trusted Surface obtains user consent and signs via the User Credential (OpenID4VP `transaction_data` type `delegate`). Open mandate `cnf` binds the agent key (agent_authorization.md, "Mandate Delegation"). |
| Z1 | 1 | Checkout and Payment Mandates, open and closed (specification.md, "Mandates"). |
| Z2 | 1 | `constraints[]`: allowed merchants, line items, amount range, budget, payees, instruments, execution date, recurrence (checkout_mandate.md, payment_mandate.md). |
| Z3 | 1 | User signs open mandates via a User Credential key (agent_authorization.md). Platform-signed in the Trusted Agent Provider model, which is only the alternative path (?). |
| Z4 | 1 | `exp` on mandates, recommended minimal. Budget decrement and single-use on receipt (specification.md, "Autonomous"). Sub-delegation is out of scope ("Agent-to-Agent Delegation"). |
| C1 | 1 | Signed Checkout and Payment Receipts whose `reference` is the hash of the mandate (agent_authorization.md "Mandate Receipt"; checkout_mandate.md, payment_mandate.md). |
| C2 | 1 | Receipts are verifier-signed JWTs. Mandates are SD-JWT signed (specification.md, "Dispute Evidence": "non-repudiable"). |
| C3 | 0.5 | Normative "Dispute" verification steps (specification.md, "Verification: Dispute"). Retention, retrieval and resolution details are out of scope, no liability allocation or refund path (?). |
| C4 | 0.5 | Independent verifiers can replay the hash checks from stored artefacts (specification.md, "Dispute"). No log, registry or status list (?). |

Totals: Identity 2.5, Authentication 3.5, Authorisation 4, Accountability 3.

## 2. Verifiable Intent (Mastercard) v0.1-draft

Read: github.com/agent-intent/verifiable-intent at HEAD (spec dated 2026-02-18), `spec/README.md`, `credential-format.md`, `security-model.md`, `constraints.md`, `design-rationale.md`. verifiableintent.dev not separately fetched; the repo holds the spec. Basis: spec.

| ID | Score | Justification |
|---|---|---|
| I1 | 1 | L1 `sub` is the opaque user ID in the issuer's system, plus optional `email` (credential-format.md §3.3, §3.4). |
| I2 | 0.5 | L2 `aud` identifies the agent platform URL and L3 carries the agent `kid` (credential-format.md §4.3). `agent_attestation` is an optional claim with no scheme defined (README §9.2). |
| I3 | 1 | L1 is signed by an Issuer (bank or network) acting as trusted third party (README §5.1; credential-format.md §3.1). |
| I4 | 0.5 | Issuer-signed L1 checked against the issuer JWKS (§3.5). `sub` is opaque, with no legal-person or KYC claims defined (?). |
| A1 | 1 | L2 signed by the user key in L1 `cnf.jwk`. L3 signed by the agent key bound in L2 `cnf` (credential-format.md §4, §5; README §5.3). |
| A2 | 1 | Issuer keys via JWKS endpoint, `kid` resolution (credential-format.md §3.5). Agent key from L2 `cnf.jwk`. |
| A3 | 1 | `nonce`, `aud`, `iat`, `exp` on L2 and L3; nonce de-duplication (security-model.md §4.1; credential-format.md §7). |
| A4 | 0.5 | Chain binds the user key to the agent key. "VI binds a key, not a person"; biometric or PIN gating is an implementation concern, with a SHOULD for user confirmation (security-model.md §2.4, §3.5) (?). |
| Z1 | 1 | L2 mandates (checkout and payment) in Immediate and Autonomous mode (README §3.4). |
| Z2 | 1 | Registered constraint types: line items, allowed merchants, amount range, allowed payees, budget, recurrence, reference (constraints.md; README §9.1). |
| Z3 | 1 | L2 signed with the user's own key from L1 `cnf.jwk`, verifiable without trusting the agent (README §5.3). Server-custodial deployments hold the key server-side (security-model.md §3.5). |
| Z4 | 1 | Mandatory `exp`, lifetimes per layer (credential-format.md §7). L3 is terminal, with no sub-delegation (§5.1). Credential-layer revocation is not defined, but expiry suffices. |
| C1 | 1 | L3a and L3b are bound to L2 by `sd_hash` and cross-referenced by `transaction_id` and `checkout_hash` (credential-format.md §5.4, §6.2). No separate receipt (settlement "assurance data" is not defined). |
| C2 | 1 | Signed SD-JWT chain, described as a tamper-evident evidence package (security-model.md §2.5). |
| C3 | 0 | Explicit: "does not define how disputes are initiated, routed… does not assign liability, specify chargeback codes" (security-model.md §2.5, "What VI does NOT provide"). Evidence only. |
| C4 | 0.5 | Independent investigator can re-verify the full chain (security-model.md §2.5). Token Status List and CRL/OCSP are suggestions only (§6.1). No log or registry (?). |

Totals: Identity 3, Authentication 3.5, Authorisation 4, Accountability 2.5.

## 3. UCP (Universal Commerce Protocol) v2026-08-25

Read: github.com/Universal-Commerce-Protocol/ucp at tag `v2026-08-25`. Files: `docs/specification/overview/index.md` (Identity & Authentication, Payment Architecture, Security), `signatures.md`, `common/identity-linking/index.md`, `payment/extensions/ap2-mandates.md`, `shopping/order/index.md`, `shopping/checkout/index.md`, `glossary.md`. Basis: spec. Core = base profile, checkout, order, message signatures. 0.5 items come from optional official capabilities: Identity Linking (`dev.ucp.common.identity_linking`) and AP2 Mandates (`dev.ucp.common.payment.ap2_mandate`).

| ID | Score | Justification |
|---|---|---|
| I1 | 1 | `buyer` object (first_name, last_name, email, phone_number) in checkout (schema `shopping/types/buyer.json`). Identity Linking supplies a user token. |
| I2 | 1 | `UCP-Agent` header carries the platform profile URL. Signed requests resolve it (overview "Identity Resolution Algorithm"). |
| I3 | 0.5 | Core identity rests on TLS and domain control of the profile ("Integrity derives from TLS"). Third-party attestation only via Identity Linking trusted IdPs (`config.providers`) and the AP2 extension user-credential flow ("business trusts the Credential Issuer (Bank)"). |
| I4 | 0.5 | Only through the AP2 extension Option 2 (VDC from bank or network), with structure deferred to the AP2 spec ("Specification Boundary"). No legal-person claims in UCP itself (?). |
| A1 | 1 | RFC 9421 request signing, ES256 baseline (signatures.md). Platforms SHOULD sign; webhooks MUST. Alternatives allowed (API keys, OAuth, mTLS) (?). |
| A2 | 1 | `keys[]` JWK Set in `/.well-known/ucp`, `keyid` to `kid` (overview "Key Discovery"; signatures.md "Key Discovery"). |
| A3 | 1 | Idempotency-Key signed and mandatory on state-changing calls, 128-bit entropy, 24h storage (signatures.md "Replay Protection"). `created` is optional by default, so reads are not time-bound (?). |
| A4 | 0.5 | OAuth 2.0 identity linking (optional capability) yields a user token presented by the platform. Revocation is defined. AP2 extension binds the user wallet signature. Core has no mandatory principal authentication. |
| Z1 | 0.5 | Core has no grant object. Extensions only: Identity Linking scoped tokens, AP2 `checkout_mandate` and `payment_mandate`. |
| Z2 | 0.5 | Identity Linking `config.scopes`. Mandate constraints come from AP2 and are not restated in UCP. |
| Z3 | 0.5 | AP2 extension: Option 1 trusted platform signs ("business trusts the platform's signature implies user consent"), Option 2 user wallet signs. Optional, and the mandate structure is defined outside UCP. |
| Z4 | 0.5 | Identity Linking: token revocation endpoint MUST be supported. Mandate `exp` via AP2. Both optional. |
| C1 | 0.5 | Core `order` carries `checkout_id` and adjustments. The record linking transaction to the user's grant is only the AP2 `checkout_mandate` (embeds checkout and `merchant_authorization`) (?). |
| C2 | 0.5 | Signed webhooks are MUST (signatures.md "When Signatures Apply"). Non-repudiable binding only in the AP2 extension ("Transaction Integrity and Non-Repudiation"). |
| C3 | 0.5 | Order `adjustments` with types `refund`, `return`, `credit`, `dispute` (shopping/order/index.md "Adjustment"). Business is Merchant of Record retaining financial liability (glossary.md). No initiation or arbitration path (?). |
| C4 | 0 | No log, registry or status list. Key removal from `keys[]` is the only revocation mechanism. |

Totals: Identity 3, Authentication 3.5, Authorisation 2, Accountability 1.5.

## 4. ACP (Agentic Commerce Protocol) 2026-04-17

Read: github.com/agentic-commerce-protocol/agentic-commerce-protocol at HEAD (Jul 2026). Latest released spec version is `spec/2026-04-17` (JSON schema and OpenAPI). The RFCs hold the normative prose: `rfcs/rfc.agentic_checkout.md`, `rfc.delegate_payment.md`, `rfc.delegate_authentication.md`, `rfc.discovery.md`, `rfc.payment_handlers.md`, `rfc.orders.md`, `rfc.seller_backed_payment_handler.md`. Some RFC text is ahead of the released version (unreleased changes). Basis: spec. SPT appears only in `rfc.payment_handlers.md` as the token type returned by `delegate_payment`.

| ID | Score | Justification |
|---|---|---|
| I1 | 1 | `Buyer` object: `customer_id`, `email`, `account_type`, `authentication_status` (schema `Buyer`). |
| I2 | 0 | Agent identity and registration are "separate concerns" (rfc.discovery.md §2.2). The bearer API key is bilateral. Capabilities object carries no operator identity. |
| I3 | 0.5 | `authentication_result` carries a 3DS cryptogram from the issuer ACS (schema `AuthenticationResult`; rfc.delegate_authentication.md). Attests cardholder authentication, not identity. `Buyer` fields are asserted (?). |
| I4 | 0 | No legal-identity attestation. 3DS result is verified by the PSP or network, with no counterparty-checkable credential in the spec. |
| A1 | 0.5 | `Signature` over canonical JSON with the client's private key, but the header is RECOMMENDED for checkout (rfc.agentic_checkout.md §2). delegate_payment §2.2 says MUST compute, header table says RECOMMENDED. Canonicalisation and key format are unspecified. Bearer token is the REQUIRED mechanism (?). |
| A2 | 0 | Algorithms are advertised "out-of-band". Signing-key publication (JWK) is "deferred" (rfc.discovery.md "Signing keys"). |
| A3 | 1 | `Idempotency-Key` MUST on all POSTs, with replay semantics (rfc.agentic_checkout.md §6). `Timestamp` SHOULD with a bounded clock-skew window (§9). Webhook HMAC includes a timestamp. |
| A4 | 1 | `authentication_result` (3DS) is submitted on the complete request (schema `CheckoutSessionCompleteRequest`). It is conditional and card-specific (?). |
| Z1 | 1 | `delegate_payment` issues a delegated vault token (SPT) usable only within an `allowance` (rfc.delegate_payment.md §2.4, §3.5). Endpoint is MUST-implement. |
| Z2 | 1 | `Allowance`: `max_amount`, `currency`, `checkout_session_id`, `merchant_id`, `expires_at`. |
| Z3 | 0.5 | Token is created by the PSP or wallet provider on the buyer's behalf. No principal-signed artefact. |
| Z4 | 1 | `expires_at`, `reason: one_time`. Token invalid after expiry (rfc.delegate_payment.md §2.4). |
| C1 | 0.5 | `Order.checkout_session_id` and `client_reference_id` link the order to the session whose id also appears in the allowance. No record of the grant. |
| C2 | 0.5 | Webhooks carry `Merchant-Signature` HMAC with a shared secret (openapi.agentic_checkout_webhook.yaml). Tamper-evident between the pair, not non-repudiable. API responses unsigned. |
| C3 | 0.5 | `adjustments[]` with `refund`, `return`, `dispute` ("covers chargebacks") (rfc.orders.md §4; schema `Adjustment`). delegate_payment lists refund semantics as out of scope. No liability allocation. |
| C4 | 0 | None. |

Totals: Identity 1.5, Authentication 2.5, Authorisation 3.5, Accountability 1.5.

## Judgement calls to review

- AP2 and VI C4 (0.5): independent re-verification of signed evidence counted as "met in part". Strict reading gives 0 to both and drops each total by 0.5.
- AP2 C3 (0.5) vs VI C3 (0): AP2 has a normative "Dispute" verification section while stating resolution details are out of scope. VI's equivalent section is informative and explicitly disclaims dispute choreography. The two are close; both could score 0.
- AP2 I1, I4, A2: no user-ID claim, no legal-identity claim and no defined key resolution, so all half scores.
- UCP A1/A3: "SHOULD sign" and idempotency-based replay protection scored as met by core.
- ACP A1 (0.5) vs UCP A1 (1): ACP's signing is RECOMMENDED and underspecified (no canonicalisation, key format or discovery). UCP's is fully specified though also SHOULD.
- UCP identity linking and AP2 mandates both count as optional official extensions (0.5 each), per the brief.
- ACP A4 (1) rests on the 3DS `authentication_result`, which is card-only and conditional. A strict reading gives 0.5.
