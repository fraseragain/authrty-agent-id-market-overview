# Chain rubric scores, group 2: AP2, Verifiable Intent, UCP, ACP

Rubric: `.../ov/research/agent-protocol-comparison/chain-rubric.md` (10 links, 2 / 1 / 0; chain score = lowest link). Scored afresh from specification text. The earlier file `scores-group-2.md` was used only to locate sections.

Sources (shallow or full clones, not committed; no repository edited):

| Protocol | Source and revision read |
|---|---|
| AP2 v0.2.0 | github.com/google-agentic-commerce/AP2, tag `v0.2.0` (2026-04-28). `docs/ap2/{specification,agent_authorization,checkout_mandate,payment_mandate,security_and_privacy_considerations,implementation_considerations,flows}.md`, `docs/{overview,faq}.md`, `code/sdk/schemas/ap2/*.json` (receipt and mandate schemas). |
| Verifiable Intent draft v0.1 | github.com/agent-intent/verifiable-intent, HEAD (2026-04-20). `spec/{README,credential-format,security-model,constraints,design-rationale}.md`. |
| UCP v2026-08-25 | github.com/Universal-Commerce-Protocol/ucp, tag `v2026-08-25`. `docs/specification/{overview/index,signatures,glossary}.md`, `common/identity-linking/index.md`, `payment/extensions/ap2-mandates.md`, `shopping/{checkout,order}/index.md`, `source/schemas/shopping/types/{buyer,adjustment}.json`. |
| ACP 2026-04-17 | github.com/agentic-commerce-protocol/agentic-commerce-protocol, release commit `9abf303` (2026-04-17). `spec/2026-04-17/{json-schema,openapi}`; `rfcs/rfc.{agentic_checkout,delegate_payment,delegate_authentication,discovery,orders,payment_handlers,seller_backed_payment_handler}.md` at that commit. |

Scoring conventions applied:
- UCP: its own official extensions (Identity Linking `dev.ucp.common.identity_linking`, AP2 Mandates `dev.ucp.common.payment.ap2_mandate`) count as optional, so they can give 1 but not 2.
- AP2: both delegation models (User Credential and Trusted Agent Provider) are normative in `agent_authorization.md`, so the User-Credential path counts as core. The Trusted Agent Provider path is treated as the D3 "platform-signed" partial case.
- A normative MUST dependency on an external standard (SD-JWT RFC 9901, OpenID4VP, RFC 9421) counts as core.
- "Statement is only a bare domain" is O1 partial, as the rubric says.

---

## 1. AP2 v0.2.0

| Link | Score | Tests met / not met | Citation |
|---|---|---|---|
| L1 Principal identity | 1 | P1 partial: the user is represented by an issuer-signed User Credential (e.g. `com.emvco.dpc`, `credential_id`, `card_last_four`); no user-ID claim is defined, but the named `iss` can resolve its own credential. P2 partial: credential issued by a third party, but issuance and identity proofing are "outside the scope" and the Trusted Agent Provider model has no issuer at all. P3 not met: no accreditation or listing of issuers. | `agent_authorization.md` "User Credential" ("mechanism for issuance is outside the scope"), "Delegation using OpenID4VP" decoded SD-JWT (`iss`, `vct`, `cnf`, disclosures); `specification.md` "Modes". |
| L2 Operator identity | 1 | O1 partial: in the Trusted Agent Provider model mandate `iss` is the agent provider URL (bare URL); in the User Credential model the agent is only a `cnf` key with no operator named. O2, O3 not met. "Agent Identification" is left to the commerce protocol. | `agent_authorization.md` "Trusted Agent Provider" (`iss: https://agent-provider.example.com`); `implementation_considerations.md` "Agent Identification". |
| L3 Agent key binding | 1 | K1 met: the open mandate carries the agent key in `cnf` (MUST) and is signed by the user via the User Credential key (or by the agent provider), so the binding is a statement by the principal or provider, not self-published by the agent. K2 partial: `exp` on mandates (schema optional, RECOMMENDED short) and receipt `iat` allow an expiry check afterwards; no revocation, rotation or key-status mechanism. | `specification.md` "Autonomous (Human Not Present)"; `agent_authorization.md` "Mandate Structure" (`cnf` REQUIRED if open); `code/sdk/schemas/ap2/open_checkout_mandate.json` (`required`: vct, constraints, cnf; `exp` optional). |
| L4 Delegation | 1 | D1 met (open Checkout and Payment Mandates). D2 met (`constraints[]`: allowed merchants, line items, amount range, budget, payee, instrument, execution date, recurrence). D3 partial: user-signed through the User Credential path, platform/provider-signed in the Trusted Agent Provider path. D4 partial: `exp` is RECOMMENDED not required; budget and single-use decrement on receipt; no revocation (mandate management "outside the scope"). | `specification.md` "Autonomous"; `checkout_mandate.md`, `payment_mandate.md` constraints; `agent_authorization.md` "Action Authorization"; `implementation_considerations.md` "Mandate Management". |
| L5 Session authentication | 1 | S1 met: closed mandate is a Key Binding JWT with the agent key. S2 met: `aud`, `nonce`, `sd_hash` in KB-JWT (SD-JWT RFC 9901 normative), double-spend rule. S3 partial: Trusted Surface MUST obtain "informed user consent" (OpenID4VP `transaction_data`, Digital Credentials API RECOMMENDED) but no assurance level is captured or defined. | `agent_authorization.md` "Mandate Structure", "Delegation using OpenID4VP"; `specification.md` "Roles" (Trusted Surface); `security_and_privacy_considerations.md` "Double Spend". |
| L6 Action conformance | 2 | A1 met: closed mandates MUST contain `sd_hash` binding to the open mandate; Payment Mandate `transaction_id` = `checkout_hash`. A2 met: Merchant, Credential Provider and Network MUST evaluate each constraint against the closed mandate before proceeding; unknown constraints fail (`unresolved_constraint`). | `specification.md` "Verification" (Merchant, Credential Provider and Network); `agent_authorization.md` "Verification and Processing Rules"; `security_and_privacy_considerations.md` "Manipulated Checkout". |
| L7 Evidence | 1 | E1 met: Checkout and Payment Receipts are verifier-signed JWTs with `iss`; mandates signed. E2 met in the "signed time from an accountable party" sense: receipt `iat` is required and signed by `iss`. E3 not met: retention and retrieval "outside the scope"; only a note to store SD-JWTs with disclosures; no statement that issuer/agent keys or credential status stay available. | `agent_authorization.md` "Mandate Receipt"; `code/sdk/schemas/ap2/{checkout,payment}_receipt.json` (required `iss`, `iat`, `reference`); `specification.md` "Dispute Evidence"; `implementation_considerations.md` "Hashes". |
| L8 Redress | 0 | R1 not met: no liability allocation. R2 not met: dispute resolution, retention and retrieval are explicitly out of scope; the only content is a normative evidence-verification procedure and a non-normative FAQ/overview aim to "help payment networks establish accountability and liability principles", with no named rulebook or evidence mapping. | `specification.md` "Dispute Evidence" and "Verification: Dispute"; `docs/faq.md` ("transaction accountability"); `docs/overview.md` s2.4. |
| L9 Trust anchor | 1 | T1 partial: verifiers use "a trust list of Agent Providers" and "trust" the credential issuer, but no list, registry or framework is defined or referenced. T2 not met: no status or revocation mechanism for credentials or keys (Credential Provider/MPP "MAY" invalidate tokens on overlapping mandates). | `specification.md` "Modes" (Direct and Autonomous paragraphs); `agent_authorization.md` "User Credential"; `security_and_privacy_considerations.md` "Double Spend". |
| L10 Continuity | 2 | C1 met by cryptographic link: credential key signs the delegation, open mandate `cnf` -> agent KB-JWT, payment and checkout joined by `checkout_hash`/`transaction_id`. C2 met: delegate payload is inside the credential's Key Binding (grant to identity), closed mandate `sd_hash` (action to grant), receipt `reference` = hash of closed mandate (record to action). | `agent_authorization.md` "Delegation using OpenID4VP" ("`delegate_payload` MUST be included as part of the Key Binding"), "Mandate Receipt" (`reference`); `specification.md` "Verification: Dispute". |

D5 (multi-hop sub-delegation with narrowing scope): not supported. "Agent-to-Agent Delegation ... outside the scope of the current specification" (`specification.md`).

Chain score (minimum): 0 (L8). Total: 11 / 20.

| Criterion | Score | Justification and citation |
|---|---|---|
| I1' Principal identifiable | 0.5 | No subject or user-ID claim is defined. The user appears only as an issuer-signed credential holder (card-level claims, `credential_id`) so a named issuer could resolve it, but the spec says nothing about resolution on request. `agent_authorization.md` "User Credential"; mandate schemas have `payee` and `payment_instrument`, no subject. |
| I2' Operator identifiable | 0.5 | Only the agent provider `iss` URL in the Trusted Agent Provider model (bare URL, no attestation of control); absent in the User Credential model. `agent_authorization.md` "Trusted Agent Provider"; `implementation_considerations.md` "Agent Identification". |
| A2' Key accountable and checkable over time | 0.5 | Binding by a statement from the user (via issuer-backed credential) or agent provider: yes. Validity at time of use checkable afterwards: only `exp`/`iat`, no revocation, rotation or key status. `specification.md` "Autonomous"; receipt `iat`. |

Unsure cells (AP2): L1 (1 vs 0 or 2: no user identity claim defined, but issuer-backed credential); L3 (K1 counted as met for a user-signed `cnf`); L4 (D3 counted as partial because of the provider-signed path, which could be read as 2 if the User Credential path alone is taken as core); L8 (0, could be 1 given the normative Dispute verification steps); L9 (1 rests on a passing mention of trust lists).

---

## 2. Verifiable Intent draft v0.1

| Link | Score | Tests met / not met | Citation |
|---|---|---|---|
| L1 Principal identity | 1 | P1 met: L1 `sub` is an opaque stable user identifier within the Issuer's system and the Issuer "maintains user identity binding", so a named party can resolve it; optional selectively disclosable `email` is self-reported-level only. P2 met: Issuer (bank or network) is "responsible for user identity verification and L1 signing". P3 not met: Issuer is named by `iss` and JWKS but no accreditation, registry or trust framework is referenced. | `README.md` s2 Terminology (Issuer), s5.1 Roles; `credential-format.md` s3.3 (`iss`, `sub`), s3.4 (`email`). |
| L2 Operator identity | 1 | O1 partial: L2 `aud` is "typically the agent platform URL"; L2 `iss` (wallet) optional. `agent_attestation` is optional and "future companion documents will define" schemes, so O2 and O3 not met. | `credential-format.md` s4.3; `README.md` s9.2 Agent Attestation; `security-model.md` s2.4. |
| L3 Agent key binding | 1 | K1 met: L2 mandates carry the agent key in `cnf.jwk` (with `kid`), signed by the user key bound by the Issuer in L1; agent key is not self-published. K2 partial: L2 and L3 `exp` required, retired Issuer keys MUST stay in JWKS for the maximum L1 lifetime, but "does not define a credential-layer revocation protocol" and agent-key provisioning/rotation is left to implementers. | `README.md` s5.3, s10.2; `credential-format.md` s4.5, s7; `security-model.md` s3.2, s3.3, s6.1. |
| L4 Delegation | 2 | D1 met (L2 checkout and payment mandates, Autonomous mode). D2 met (registered constraints: allowed merchants, line items, payees, amount range, budget, recurrence, reference). D3 met: L2 signed with the user key bound in L1 (server-custodial holding is a deployment variant, spec states verifiers cannot and need not distinguish). D4 met: `exp` REQUIRED on L2 and L3, L2 MUST NOT exceed L1 `exp`. | `README.md` s3.4, s10.2; `constraints.md` s4; `credential-format.md` s4.3, s7; `security-model.md` s3.5. |
| L5 Session authentication | 1 | S1 met: L3 signed by the L2-bound agent key, `kid` resolved against L2 `cnf.jwk`. S2 met: `nonce` REQUIRED, `aud`, `iat`, `exp`, nonce de-duplication in a sliding window. S3 partial: Immediate mode "user reviews and confirms"; "VI binds a key, not a person"; biometric/PIN is SHOULD for on-device keys, authenticated session MUST for server-custodial, no assurance level. | `credential-format.md` s5.2-5.3; `security-model.md` s2.4, s3.4, s3.5, s4.1, s5.2; `README.md` s3.3 table (Human presence). |
| L6 Action conformance | 2 | A1 met: L3 `sd_hash` binds to the L2 presentation (selective). A2 met: verifiers MUST check L3 values against disclosed L2 constraints, machine-enforceable ones MUST be verified; network enforces budget and one-L3-per-pair. | `credential-format.md` s5.4, s5.7(7-9); `README.md` s10.4(10). |
| L7 Evidence | 1 | E1 partial: L3 records are signed by the agent key (not an identifiable accountable party); merchant `checkout_jwt` signature verification is only SHOULD (checkout schema "implementation-defined"); no receipt object. E2 not met: `iat`/`exp` are issuer-, user- or agent-asserted, no trusted time. E3 partial: independent re-verification of the full chain is described and retired JWKS keys MUST be kept, but record retention is not addressed. | `security-model.md` s2.5 (evidence table), s3.2, s6.6; `README.md` s5.1 (network "maintains audit trail"); `credential-format.md` s6.3. |
| L8 Redress | 0 | R1 not met and R2 not met: "does not define how disputes are initiated, routed ... It does not assign liability, specify chargeback codes, or prescribe arbitration"; evidence only. | `security-model.md` s2.4, s2.5 "What VI does NOT provide for disputes". |
| L9 Trust anchor | 1 | T1 not met: "known issuer" and JWKS endpoints only; no registry or trust list of issuers (constraint-type and VCT registries are about formats). T2 partial: removing a key from the Issuer JWKS is "the VI-layer revocation mechanism"; Token Status List and OCSP are suggestions only, "a future version will define credential status". | `security-model.md` s3.2, s6.1; `README.md` s9.1; `credential-format.md` s10. |
| L10 Continuity | 2 | C1 met by cryptographic link: L1 `cnf` -> L2 signature -> L2 `cnf` -> L3, plus `checkout_hash`/`transaction_id` cross-reference. C2 met: L2 `sd_hash` over L1, L3 `sd_hash` over the L2 presentation, `conditional_transaction_id`. There is no separate record layer beyond L3 (the signed chain is the "evidence package"). | `credential-format.md` s4.3, s5.4, s6; `README.md` s8; `security-model.md` s2.5. |

D5: not supported by design. L3 is terminal: MUST NOT contain `cnf` ("prevents agents from sub-delegating") (`security-model.md` s3.3; `credential-format.md` s5.5-5.6).

Chain score (minimum): 0 (L8). Total: 12 / 20.

| Criterion | Score | Justification and citation |
|---|---|---|
| I1' Principal identifiable | 1 | L1 `sub` is a pseudonymous identifier issued by a named Issuer (`iss`) that "maintains user identity binding" and is "responsible for user identity verification", so a named party can resolve it. `README.md` s2 Terminology, s5.1; `credential-format.md` s3.3; linkability noted in `security-model.md` s6.2. Resolution on request is implied, not specified. |
| I2' Operator identifiable | 0.5 | Agent platform is a URL in `aud` only; `agent_attestation` undefined. `credential-format.md` s4.3; `README.md` s9.2. |
| A2' Key accountable and checkable over time | 0.5 | Binding by the user's key (itself bound by the Issuer): yes. Validity at time of use checkable afterwards: only `exp`/`iat` and retention of retired Issuer keys; no agent-key status or revocation. `security-model.md` s3.2, s6.1; `credential-format.md` s7. |

Unsure cells (VI): L2 (1 rests on a bare URL; could be 0 if `aud` is read as audience not operator); L7 (1, E1 and E3 each only partial); L9 (1, rests on JWKS-removal as a revocation mechanism); L10 (2 treats the L3 pair as the record; strictly there is no record layer beyond the action, so 1 is arguable); L5 (S3 partial); I1' (1 vs 0.5).

---

## 3. UCP v2026-08-25 (core plus Identity Linking and AP2 Mandates as optional extensions)

| Link | Score | Tests met / not met | Citation |
|---|---|---|---|
| L1 Principal identity | 1 | P1: core `buyer` (name, email, phone) is self-asserted so not met; extensions give a path: Identity Linking user token with `(iss, sub)` at a business-listed IdP, and AP2 Option 2 credential from a bank (partial, optional). P2 partial via the same extensions only. P3 not met: IdPs are per-business allowlisted, no accreditation. | `source/schemas/shopping/types/buyer.json`; `common/identity-linking/index.md` "Identity Providers", "IdP Requirements"; `payment/extensions/ap2-mandates.md` "Option 2: Digital Payment Credential". |
| L2 Operator identity | 1 | O1 partial: platform identified by the `UCP-Agent` profile URL, key resolved from `keys[]`, integrity "derives from TLS to the resolved origin"; namespace "binding guarantees provenance, not trust". O2, O3 not met (no third-party attestation of who controls the domain). | `overview/index.md` "Identity & Authentication", "Identity Resolution Algorithm", "Authority Binding". |
| L3 Agent key binding | 0 | K1 not met: platform signing keys are self-published in the profile `keys[]`; the AP2 platform-provider flow uses the same key; the user-credential flow binds the user's key, not an agent key. K2 not met as at-time-of-use: rotation steps and 7-day grace are defined, but "remove old key ... a key still listed continues to verify" and removal is the only revocation, so historic validity cannot be checked afterwards. | `signatures.md` "Key Discovery", "Key Rotation", "Replay Protection" (closing note); `overview/index.md` "Key Discovery"; `ap2-mandates.md` "Signing Key Requirements". |
| L4 Delegation | 1 | D1 only by extension: Identity Linking scopes; AP2 `checkout_mandate`/`payment_mandate` (structure and constraints defined in AP2, "Specification Boundary"). D2 partial (scopes; AP2 constraints not restated). D3 partial: Option 1 platform signs server-side, Option 2 user wallet signs. D4 partial: Identity Linking revocation endpoint MUST; mandate `exp` via AP2 (`mandate_expired`). All optional. | `identity-linking/index.md` "Scopes", "For Businesses" (revocation MUST); `ap2-mandates.md` "Mandate Structure", "Step 2", "Error Codes". |
| L5 Session authentication | 1 | S1 partial: RFC 9421 signatures, platforms SHOULD sign, API keys/OAuth/mTLS allowed instead. S2 partial: signed `Idempotency-Key` (128-bit, 24 h) is the replay control; `created` OPTIONAL for default signatures; `nonce` only SHOULD in WBA shape. S3 partial: `requires_buyer_review` handoff, OAuth user consent, AP2 mandate; no assurance level. | `signatures.md` "Replay Protection", "When Signatures Apply", WBA Interop items 5-6; `shopping/checkout/index.md` error severities; `identity-linking/index.md`. |
| L6 Action conformance | 1 | A1 partial (extension): `checkout_mandate` embeds the full checkout including `merchant_authorization`; `mandate_scope_mismatch`. A2 partial: business verifies mandate and "terms match" per UCP, constraints evaluation per the AP2 spec (not restated); no core grant to check against. | `ap2-mandates.md` "Business Verification", "Error Codes"; `overview/index.md` "Transaction Integrity and Non-Repudiation". |
| L7 Evidence | 1 | E1 partial: webhooks MUST be signed by the business and `merchant_authorization` is a business JWS (extension), but the core checkout/order record is not signed by default (completion responses only RECOMMENDED). E2 not met: `occurred_at` and `Webhook-Timestamp` are unsigned or business-asserted, no trusted time. E3 partial: AP2 extension's JCS rationale says mandates "may be retrieved and verified days or months later", but key removal and no retention rule undercut it. | `signatures.md` "When Signatures Apply"; `ap2-mandates.md` "Canonicalization"; `shopping/order/index.md` (`occurred_at`, `Webhook-Timestamp`). |
| L8 Redress | 1 | R1 partial: Business is Merchant of Record "retaining financial liability and ownership of the order" (glossary, non-normative); no other roles allocated. R2 partial: order `adjustments` of type `refund`, `return`, `dispute`, `cancellation`, `refund_policy` links; no initiation or arbitration path and no rulebook mapping. | `glossary.md` (Business, Merchant of Record); `shopping/order/index.md` "Adjustment"; `source/schemas/shopping/types/adjustment.json`; `shopping/checkout/index.md` policies. |
| L9 Trust anchor | 1 | T1 partial: per-business `config.providers` is a closed allowlist of trusted IdPs, and "business trusts the Credential Issuer"; namespace governance is explicitly "provenance, not trust" and there is no registry. T2 partial: token revocation endpoint MUST (Identity Linking), key removal from `keys[]`. | `identity-linking/index.md` "Identity Providers"; `overview/index.md` "Governance Model", "Authority Binding"; `signatures.md` "Key Rotation". |
| L10 Continuity | 1 | C1 partial: user token and mandates tie to a checkout session, but the principal is not carried as one identifier across identity, grant and action. C2 partial: `checkout_mandate` embeds the signed checkout (extension), payment mandate placed in `payment.instruments[*].credential.token`; core `order.checkout_id` is a plain identifier, not a hash or signature. | `ap2-mandates.md` "Mandate Structure"; `shopping/order/index.md`; `source/schemas/shopping/order.json` (`checkout_id`). |

D5: not supported (no sub-delegation in UCP; AP2 Agent-to-Agent delegation is out of scope).

Chain score (minimum): 0 (L3). Total: 9 / 20.

| Criterion | Score | Justification and citation |
|---|---|---|
| I1' Principal identifiable | 0.5 | Core `buyer` is self-asserted (name, email). Identity Linking `(iss, sub)` and the AP2 bank credential could let a named party resolve the user, but both are optional. `buyer.json`; `identity-linking/index.md` "IdP Requirements" ("stable per-IdP identification remains `(iss, sub)`"). |
| I2' Operator identifiable | 0.5 | Platform profile URL (`UCP-Agent`) with TLS-derived integrity; no attestation of who controls the domain. `overview/index.md` "Identity Resolution Algorithm" step 3 and "Authenticated identity". |
| A2' Key accountable and checkable over time | 0 | Keys self-published in the profile; no third-party or accountable-party statement about the platform key. Removal from `keys[]` is the only revocation, so validity at a past time is not checkable. `signatures.md` "Key Rotation". |

Unsure cells (UCP): L1 (1 rests on optional extensions only); L3 (0 versus 1: rotation and revocation procedure exists but fails the as-at-time test); L4 (1, optional extensions); L5 (1, each of S1 to S3 is partial); L8 (1, glossary-level liability only); L9 (1); L10 (1); A2' (0 versus 0.5).

---

## 4. ACP release 2026-04-17 (with delegate payment)

| Link | Score | Tests met / not met | Citation |
|---|---|---|---|
| L1 Principal identity | 1 | P1 not met: `Buyer` (name, email, `customer_id` merchant-internal, `account_type`, `authentication_status`) is self-asserted. P2 partial: delegate authentication returns a 3DS result (cryptogram, ECI) from the card issuer's ACS, which verifies the cardholder, but it is conditional, card-only and "not_supported" lets checkout proceed without it. P3 not met. | `json-schema/schema.agentic_checkout.json` `Buyer`, `AuthenticationResult`; `rfc.delegate_authentication.md` s1, s4.2-4.3. |
| L2 Operator identity | 0 | O1 not met: agent registration and whitelisting are "separate concerns"; the bearer token is bilateral and unspecified; signing-key publication is "deferred". O2, O3 not met. 3DS client "verified infrastructure" allowlisting is not an attested identity. | `rfc.discovery.md` s2.2 ("Agent registration or whitelisting"), s11 ("Signing keys"); `rfc.delegate_authentication.md` s8. |
| L3 Agent key binding | 0 | K1 not met: signing key format, canonicalisation and publication are unspecified ("algorithm policy advertised out-of-band"). K2 not met: no key status, rotation or revocation. | `rfc.agentic_checkout.md` s2.1; `rfc.delegate_payment.md` s2.1; `rfc.discovery.md` s11. |
| L4 Delegation | 1 | D1 met: `delegate_payment` issues a delegated vault token usable "only within" the `Allowance`. D2 met: `max_amount`, `currency`, `checkout_session_id`, `merchant_id`, `expires_at`. D3 partial: token created by the PSP/vault on the buyer's behalf, no principal-signed artefact. D4 met: `expires_at` (token MUST become invalid), `reason: one_time`. | `rfc.delegate_payment.md` s2.5, s3.5; `json-schema/schema.delegate_payment.json` `Allowance`. |
| L5 Session authentication | 1 | S1 partial: `Signature` over canonical JSON is RECOMMENDED/SHOULD for checkout and delegate_payment (MUST for delegate_authentication). S2 met in core: `Idempotency-Key` MUST on all POSTs, `Timestamp` with clock-skew window (SHOULD), webhook timestamp window. S3 partial: 3DS `authentication_result` with ECI conveys an authentication level, but it is conditional and card-specific. | `rfc.agentic_checkout.md` s3.1, s6, s7; `rfc.delegate_payment.md` s2.3, s6; `rfc.delegate_authentication.md` s3.1, s8; `AuthenticationResult` schema. |
| L6 Action conformance | 1 | A1 met: complete request carries the token (`payment_data`), allowance binds `checkout_session_id` and `merchant_id`. A2 partial: allowance enforcement is by the token issuer/PSP (token opaque to the merchant), not independently verifiable from a signed artefact. | `rfc.delegate_payment.md` s2.5, s3.5; `CheckoutSessionCompleteRequest`, `PaymentData` schemas. |
| L7 Evidence | 0 | E1 not met: webhooks use a shared-secret HMAC `Merchant-Signature` (tamper-evident between the pair, not verifiable by a third party); API responses unsigned. E2 not met: `created`, `occurred_at` and HMAC `t=` are unsigned or sender-asserted. E3 not met: only idempotency-key retention of 24 h; no evidence retention. | `spec/2026-04-17/openapi/openapi.agentic_checkout_webhook.yaml` header description; `rfc.delegate_payment.md` s2.4, s5.6. |
| L8 Redress | 1 | R1 not met: no liability allocation (merchant "system of record" is not liability). R2 partial: Order `adjustments[]` of type `refund`, `partial_refund`, `return`, `dispute`, `chargeback` record post-order events; refund semantics are explicitly out of scope of delegate_payment, no initiation path, no rulebook mapping. | `schema.agentic_checkout.json` `Adjustment`; `rfc.orders.md` s4.5, s6.2; `rfc.delegate_payment.md` s1 (out of scope). |
| L9 Trust anchor | 0 | T1 not met: agent trust is out of scope; payment-handler declarations are not a registry of trusted issuers/operators. T2 not met: no status or revocation mechanism for keys or credentials (token expiry only). | `rfc.discovery.md` s2.2, s11; `rfc.payment_handlers.md`. |
| L10 Continuity | 1 | C1 partial: `checkout_session_id` links allowance, completion and order (`Order.checkout_session_id`, `client_reference_id`) by identifier; the principal is not carried across identity (3DS), grant (delegate_payment has no buyer) and action. C2 not met: no artefact references a predecessor by hash or signature. | `rfc.delegate_payment.md` s3.5; `schema.agentic_checkout.json` `Order`. |

D5: not supported.

Chain score (minimum): 0 (L2, L3, L7, L9). Total: 6 / 20.

| Criterion | Score | Justification and citation |
|---|---|---|
| I1' Principal identifiable | 0.5 | `Buyer` is self-asserted (name, email, merchant-internal `customer_id`); 3DS authenticates the cardholder to the issuer but nothing in the spec lets the counterparty or a named party resolve the principal. `schema.agentic_checkout.json` `Buyer`; `rfc.delegate_authentication.md`. |
| I2' Operator identifiable | 0 | Not even a bare URL is defined in the artefact: agent identity is a "separate concern", bearer token is bilateral. `rfc.discovery.md` s2.2. |
| A2' Key accountable and checkable over time | 0 | Key publication deferred, no binding statement, no status. `rfc.discovery.md` s11; `rfc.delegate_payment.md` s2.1. |

Unsure cells (ACP): L1 (1 rests on 3DS as a P2 partial; could be 0); L2 (0, though a bearer token issued bilaterally to a known platform lets a merchant identify it in practice, which the spec does not state; I2' could be 0.5 on that reading); L4 (1 due to D3, otherwise D1/D2/D4 met); L6 (1, A2 partial); L7 (0, HMAC webhooks could earn 1 for E1); L8 (1, adjustment records only); L10 (1).

---

## Cross-protocol summary

| Protocol | L1 | L2 | L3 | L4 | L5 | L6 | L7 | L8 | L9 | L10 | Chain | Total | I1' | I2' | A2' |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| AP2 v0.2.0 | 1 | 1 | 1 | 1 | 1 | 2 | 1 | 0 | 1 | 2 | 0 | 11 | 0.5 | 0.5 | 0.5 |
| Verifiable Intent v0.1 | 1 | 1 | 1 | 2 | 1 | 2 | 1 | 0 | 1 | 2 | 0 | 12 | 1 | 0.5 | 0.5 |
| UCP v2026-08-25 | 1 | 1 | 0 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 0 | 9 | 0.5 | 0.5 | 0 |
| ACP 2026-04-17 | 1 | 0 | 0 | 1 | 1 | 1 | 0 | 1 | 0 | 1 | 0 | 6 | 0.5 | 0 | 0 |

No protocol scores 2 on L1 to L3, L5, L7, L8 or L9. L8 is 0 for AP2 and VI because both disclaim liability and dispute resolution; UCP and ACP get 1 only for adjustment-record models.

## Unsure cells (consolidated)

- AP2 L1, L3, L4, L8, L9.
- VI L2, L5 (S3), L7, L9, L10, I1'.
- UCP L1, L3, L4, L5, L8, L9, L10, A2'.
- ACP L1, L2 (and I2'), L4, L6, L7, L8, L10.
- Cross-protocol consistency calls: R2 credited as partial (1) where an order-adjustment model exists (UCP, ACP) but not for AP2's evidence-only Dispute steps or VI's evidence table (both 0); the L10 "record" element is counted as present for AP2 (receipts) and treated as satisfied by the L3 chain for VI.
