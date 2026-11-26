# Review: general-actions chain scores and stack rows

Reviewer: independent of the two general-actions scorers and of the stack assessor. Read 25 Nov 2026. Group files, `new-stacks.md`, `chain-stacks.md`, `scores.json` and the research README were not edited. No repository was touched. One page was fetched: MCP 2026-07-28 `basic/utilities/cancellation` (saved at `cmp3/rev/mcp-cancel.md`). Everything else was re-read from the local copies (`cmp2/src/`, `cmp3/src/`, `src/`, `g3/`, `g4/`).

Final data: `cmp3/final-general.json`.

## Rules applied

- **F (L8).** R2 is partial when the spec defines any of these: cancelling an in-flight action, revoking a consent or grant (including prospective-only revocation), or rollback. R2 is met only when the spec defines reversal or remedy of an action already taken. R1 is partial when the spec names a single accountable party for actions. It is met only when responsibility is allocated between named roles. L8 = 2 needs R1 and R2 both met. L8 = 1 needs either one to be at least partial.
- **G (classes).** "Yes" means the spec defines class-specific semantics in the grant or the record: a named scope, operation, mandate, constraint or consent type. "Partial" means the action can be named only through a generic, implementer-defined hook, such as a free-form scope, tool name, skill, route, resource URL or custom constraint type. "No" means neither the grant nor the record can express the action. I applied one corollary uniformly: a generic hook reaches every class it can name. If a tool name or skill string gives partial for C, it also gives partial for B and D.
- **H (payment-only).** A mechanism earns nothing in this variant when it exists only to make, authorise, evidence or remedy a payment or purchase. Examples are a payment instrument or network token, 3-D Secure, a payment proof, a payment receipt, a checkout or order remedy, or a key that may only sign transfers. The test is on the mechanism itself. Request signing and replay protection on a checkout endpoint are not payment mechanisms, so ACP L5 is kept. MPP's credential is a payment proof, so MPP L5 stays 0. The general rubric says payment-only mechanisms score nothing "in this variant", so I applied H to the carried links (L1, L2, L3, L9, L10) as well. Neither group did this. Section 1b lists those cells separately, so they can be reverted as a block.
- **A to E** from `chain-review.md` still apply. So do the A2 reading (a scope-only check is partial), T1 (a verifier-local allowlist is partial) and T2 (expiry is not a status mechanism).

## 1a. Cells changed under F and G (protocols)

| Protocol | Cell | From → to | Rule | Citation |
|---|---|---|---|---|
| PAP | L8 | 0 → 1 | F. R2 is partial: refresh-token revocation at a `revocation_endpoint` (RFC 7009), which is "Required" in issuer metadata, and sign-out by revoking every refresh token. Both are prospective revocation of the grant. R1 is not met. | spec 3.2 ("`revocation_endpoint` revokes refresh tokens (4.6). Required."), 4.6, 5.5 "Sign-out" |
| MCP | L8 | 0 → 1 | F. R2 is partial: `notifications/cancelled` cancels an in-progress request ("A client SHOULD send a cancellation notification"). On Streamable HTTP, the server "MUST treat a client disconnect as cancellation". R1 is not met. | MCP 2026-07-28 Basic › Utilities › Cancellation, "Cancellation Flow", "Transport-Specific Cancellation" |
| A2A | L8 | 0 → 1 | F. R2 is partial: `CancelTask` "Requests the cancellation of an ongoing task… success is not guaranteed". R1 is not met. | A2A 1.0.1 §3.1.5, §9.4.5 |
| x401 | L8 | 0 → 1 | F. R2 is partial: the Verification Token "SHOULD… support replay detection and revocation", and a Verifier reusing a token MUST check that it "has not expired or been revoked". This is token revocation (prospective). R1 is not met. | x401 0.2.0 "Verification Token Contents" item 4; "Reuse Across Routes" item 2; "Verification Token Scope" ("short-lived, revocable") |
| ERC-8004 | Class B | no → partial | G corollary. The feedback file's `mcp.tool` and `a2a.skills` fields and the validation `requestURI` (inputs and outputs) name any tool or skill. That is the same generic hook that gave C partial, so it reaches B in the same way. | Reputation Registry "Off-Chain Feedback File Structure"; Validation Registry "Validation Request" |
| ERC-8004 | Class D | no → partial | G corollary, as for B. | as above |
| ACP | Class A | partial → no | G and H. No grant or record outside the payment `Allowance` names a read. `GET /checkout_sessions/{id}` and the Feed API are operations, but neither the grant nor any record covers them, and the bearer token is unspecified. | `schema.delegate_payment.json` `Allowance`; `openapi.agentic_checkout.yaml`; `rfc.discovery.md` §2.2 |
| ACP | Class C | partial → no | G and H. Create, update and cancel apply only to a checkout session, which is part of a purchase (class E), and the Allowance does not cover them. | `openapi.agentic_checkout.yaml` |
| ACP | Class D | partial → yes | G. `MarketingConsent` is a typed consent record ("Buyer's marketing consent decision for a specific channel", `channel`, `opted_in`) submitted at completion against seller-declared `MarketingConsentOption`. It is unsigned, which is the same evidential weakness as UCP Buyer Consent (rated yes). The two now match. | `json-schema/schema.agentic_checkout.json` `MarketingConsent`, `MarketingConsentOption`; `openapi.agentic_checkout.yaml` `marketing_consent_options` |
| x402 | Class A | partial → no | H. The resource is named only inside payment requirements, payloads and receipts. SIWX exists "to identify returning users and skip payment for addresses that have previously paid", so it is also payment-bound. | core §5.1; `extensions/sign-in-with-x.md` "Summary" |
| x402 | Class C | partial → no | H. The MCP transport names the tool in the payment `resource`. | `transports-v2/mcp.md` |
| MPP | Class A | partial → no | H. The only hook is a paid resource under a payment challenge. | core "Request Body Digest Binding"; `draft-payment-transport-mcp-00.md` |

UCP L8 is unchanged at 1, but its basis is replaced. Under H, order `adjustments` (cancellation, return, dispute, refund) are purchase remedies and earn nothing. R2 partial now rests on two things. The first is the Identity Linking revocation endpoint (MUST), which revokes the grant prospectively. The second is the Buyer Consent extension's withdrawal of consent ("unsubscribe affordance"). Source: `common/identity-linking/index.md`; `shopping/extensions/buyer-consent.md`.

## 1b. Cells changed under H on carried links (L1, L2, L3, L9, L10)

| Protocol | Cell | From → to | Basis now payment-only | Citation |
|---|---|---|---|---|
| ACP | L1 | 1 → 0 | P2 rested only on the 3-D Secure `authentication_result`. The general rubric itself names 3-D Secure as payment-only. `Buyer` is self-asserted. | `schema.agentic_checkout.json` `Buyer`, `AuthenticationResult`; `rfc.delegate_authentication.md` |
| ACP | L10 | 1 → 0 | C1 rested on `checkout_session_id` across the Allowance, completion and Order. All three are purchase artefacts. | `rfc.delegate_payment.md` §3.5; `schema.agentic_checkout.json` `Order` |
| MPP | L1 | 1 → 0 | The card method's issuer-provisioned network token and `cardholderFullName` are a payment instrument. Core "does not identify the client, the payer's principal, or any other party". | `methods/card/draft-card-charge-00.md`; core "Interaction with Other Authentication Schemes" |
| MPP | L3 | 1 → 0 | Tempo access keys may sign transfers only ("MUST NOT authorize `approve` or any other non-transfer selector"). | `methods/tempo/draft-tempo-subscription-00.md` "Key Authorization" |
| MPP | L9 | 1 → 0 | T2 rested on Tempo `isRevoked` for those payment-only keys. T1 is not met. | `draft-tempo-subscription-00.md` "Revocation" |
| MPP | L10 | 1 → 0 | The challenge, the credential echoing it, and the receipt `reference` to the settlement are all payment artefacts. | core "Binding Other Authentication to a Challenge"; receipt table |
| x402 | L10 | 1 → 0 | `payer` across `authorization`, `SettlementResponse` and the receipt, and the receipt's optional `transaction` hash, are payment fields. There is no non-payment grant (L4 = 0). | core §5.2.2, §5.3.2; offer-receipt §5.2 |

If H is confined to L4 to L8, as both groups had it, these seven cells revert. Totals would then be ACP 3, MPP 4 and x402 5. Chain scores do not change either way.

## 2. Cells checked and kept

| Protocol | Cell | Score | Basis |
|---|---|---|---|
| KYA-OS | L8 | 1 | This is F exactly. R1 is partial: one accountable role, "Every chain MUST terminate at a Responsible Party", "the entity ultimately accountable for actions" (SPEC §2, §6.4). R2 is partial: cascading delegation revocation with status lists (§6.5). The purchase score stays 0, because F belongs to this variant only. |
| UCP | L8 | 1 | New basis (see 1a). |
| AP2 | L8 | 0 | No revocation and no cancel. The roles in `specification.md` have "responsibilities from a processing perspective" (verification duties), which is not an accountable party for actions. The dispute steps are payment-only (H). |
| VI | L8 | 0 | "VI v0.1 does not define a credential-layer revocation protocol" (`security-model.md` §6.1). Removing a JWKS key is key-compromise containment, not revocation of a grant. "It does not assign liability" (§2.5). |
| WBA, TAP, MPP | L8 | 0 | Nothing under F. WBA "defines no revocation" (6.3). |
| ACP | L8 | 0 | `cancelCheckoutSession` cancels an in-flight purchase. Under H it is a purchase remedy. Contestable (see section 5). |
| x402 | L8 | 0 | `void`, `refund` and `reclaim` are payment remedies (H). |
| ERC-8004 | L8 | 0 | `revokeFeedback` and `appendResponse` act on a reputation signal, not on the agent's action, and there is no grant to revoke. Contestable. |
| x402 | L7 | 1 | Not payment-only under H. The receipt confirms "that payment was received **and service was delivered**", so it evidences the non-payment outcome (offer-receipt §263, §862). Contestable. |
| ACP, x402, TAP, UCP | L5 | 1 | S1 and S2 are request authentication, not payment mechanisms. ACP's `Signature`/`Idempotency-Key` apply to every checkout operation. S3 via 3-D Secure is partial by the rubric's own text. |
| MPP | L5 | 0 | Every authenticating element is the payment credential (H). |
| VI | L5 | 1 | S1 and S2 come only through signing L3 checkout and payment mandates, which is payment-only content. S3 is partial (user confirmation in Immediate mode), so the link stays at 1. |
| AP2 | L4, L6, L7, L10 | 1, 1, 1, 2 | Credited on the generic Agent Authorization model (open/closed mandate, `cnf`, `sd_hash`, generic Mandate Receipt). G gives A to D partial, because new mandate and constraint types "MAY be defined". |
| VI | L4, L6 | 1, 1 | Same treatment as AP2. Custom URN constraint types are the generic hook. |
| AP2, VI | L1 | 1, 1 | The issuer credential binds the user's key. That identity function is not payment-only, even though the issuer is a payment-credential issuer (EMVCo DPC; Mastercard card VCT). Contestable. |
| TAP | L1, L3, L9, L10 | 1 each | The ID token, the Key Store and the shared nonce apply to `agent-browser-auth` (browsing) as well as payment, so H does not remove them. |
| x402 | L2, L9 | 1, 1 | `http-message-signatures` registration identifies the signature agent and is not a payment artefact. L9 keeps T1 partial (`registrationUrl`). |
| UCP | L1, L7, L10 | 1 each | L1 rests on Identity Linking `(iss, sub)`. L7 rests on signed order webhooks that report class C changes (cancellation, modification). L10 rests on the identity-linked token presented on gated requests (C1 partial). All are contestable under H. |
| x401 | L4, L6 | 1, 1 | The token is scoped to "route, policy, action, resource", is not payment-specific, and the check is scope-level. |
| KYA-OS | L4, L6 | 2, 2 | CRISP scopes and caveats, and the `delegationRef`/digest MUST, are action-agnostic. |
| All | Classes, other cells | as JSON | PAP C yes (Operations). UCP A, C, D yes (`order:read`, `order:manage`, Buyer Consent). KYA-OS E yes (`MaxAmount` caveat type), F yes (attenuating chains). A2A F partial (task chain native, no onward grant). MCP F no (token passthrough forbidden). x401 E no ("MUST NOT be treated as payment"). PAP A partial: `scope_hints.changes: none` are the Company's claims, not grant semantics. TAP A partial: the browse tag names a recognition context, not a data scope. |

## 3. Final general-actions rows

| Protocol | L1 | L2 | L3 | L4 | L5 | L6 | L7 | L8 | L9 | L10 | Chain | Total | A | B | C | D | E | F |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| PAP | 0 | 1 | 1 | 1 | 1 | 1 | 0 | 1 | 1 | 1 | 0 | 8 | partial | partial | yes | partial | partial | no |
| MCP | 1 | 1 | 0 | 1 | 1 | 1 | 0 | 1 | 1 | 0 | 0 | 7 | partial | partial | partial | partial | partial | no |
| A2A | 0 | 1 | 0 | 1 | 1 | 1 | 0 | 1 | 1 | 0 | 0 | 6 | partial | partial | partial | partial | partial | partial |
| Web Bot Auth | 0 | 1 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | no | no | no | no | no | no |
| AP2 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 0 | 1 | 2 | 0 | 10 | partial | partial | partial | partial | yes | no |
| VI | 1 | 1 | 1 | 1 | 1 | 1 | 0 | 0 | 1 | 1 | 0 | 8 | partial | partial | partial | partial | yes | no |
| UCP | 1 | 1 | 0 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 0 | 9 | yes | partial | yes | yes | yes | no |
| ACP | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | no | no | no | yes | yes | no |
| Visa TAP | 1 | 1 | 1 | 0 | 1 | 0 | 0 | 0 | 1 | 1 | 0 | 6 | partial | no | no | no | yes | no |
| x402 | 0 | 1 | 0 | 0 | 1 | 0 | 1 | 0 | 1 | 0 | 0 | 4 | no | no | no | no | yes | no |
| MPP | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | no | no | no | no | yes | no |
| ERC-8004 | 0 | 1 | 1 | 0 | 0 | 0 | 1 | 0 | 1 | 1 | 0 | 5 | partial | partial | partial | partial | partial | no |
| x401 | 1 | 1 | 0 | 1 | 1 | 1 | 0 | 1 | 1 | 0 | 0 | 7 | partial | partial | partial | partial | no | no |
| KYA-OS | 1 | 1 | 1 | 2 | 1 | 2 | 1 | 1 | 1 | 1 | **1** | 12 | partial | partial | partial | partial | yes | yes |

KYA-OS is still the only protocol with a chain with no missing link. The F changes lift four L8 cells (PAP, MCP, A2A, x401), but each of those protocols has a 0 elsewhere, so no chain score moves.

## 4. Stacks

### Basis ("documented today")

- For each link, a stack takes the best score among the members whose artefact for that link reaches the counterparty through a documented join.
- A member with no documented join earns nothing.
- A member whose join is documented, but does not carry the relevant artefact, earns nothing on that link.
- Otherwise the stack takes the score of the anchor, meaning the member on whose artefacts the counterparty acts. This is how `new-stacks.md` builds its documented rows ("PAP leads, WBA adds nothing, KYA-OS is credited nowhere").
- L10 is scored across the documented joins only.
- Under the general rubric, a join that is itself a payment mechanism carries nothing (H).

"If joined as proposed" takes the best member on each link, with L10 as `new-stacks.md` derives it. It is an upper bound.

### Checks on `new-stacks.md`

- PAP's published spec has no reference to KYA-OS or AP2. I grepped `cmp3/src/pap/` (spec 1.0, guides, all extension pages including `ucp`, the 1.1 draft, changelog and introduction) for `AP2|Agent Payments|kya|know your agent|did:|Verifiable Intent|mandate`. The only hit is the introduction's roadmap on signed approvals, which describes mandates as a future concept and does not name AP2. Confirmed.
- PAP issue #61 is state OPEN and is an issue, not a pull request ("Proposal: payments extension…", `pap-issues.json`). Revision 3 (`pap-61-v3.md`) calls itself a proposal: "Until adopted, it can be published under a domain name". It scores 0. Confirmed.
- There is no reference to Poppy or PAP in the KYA-OS spec files or the AP2 docs. The `kya` hits in AP2's `checkout_mandate.md` are base64 inside example tokens. Confirmed.
- The `new-stacks.md` documented rows (equal to the PAP row) and its if-joined rows (11, 12, 13) are consistent with the basis above. No change to its purchase numbers.

### Changes to the six existing stack rows in the research README (purchase)

On the same basis, two README rows change.

| Stack | Cell | README → today | Reason |
|---|---|---|---|
| AP2 + UCP (+ VI) | L10 | 2 → 1 | Rule B needs the record step for a 2. AP2's receipt `reference` (hash of the closed mandate) is the record step, but UCP's AP2 Mandates extension has no carrier for receipts (zero occurrences of "receipt" in `ap2-mandates.md`), and UCP Order references the checkout only by plain `checkout_id`. The record step is not carried by the documented join. `chain-review.md` §4 flagged this as the strict reading. Total 12 → 11. Chain stays at 1. L7 stays at 1 (UCP's own signed webhooks), and L3 = 1 is carried because the mandate `cnf` travels in `ap2.checkout_mandate`. |
| x402 + ERC-8004 | L3 | 1 → 0 | The 1 came from ERC-8004's `agentWallet` history. No documented join binds that wallet to the x402 payer or signer. `agentWallet` is a receiving address, and "x402's signing wallet and ERC-8004's registered agent key are not required to be the same key" (`chain-stacks.md` stack 4). x402's own L3 is 0. Total 9 → 8. |

The other four rows are unchanged on this basis: PAP + UCP + WBA 10, KYA-OS + MCP 11, TAP + WBA 7, ACP + SPT 6.

### Stack rows

| Stack | Rubric | Basis | L1 | L2 | L3 | L4 | L5 | L6 | L7 | L8 | L9 | L10 | Chain | Total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| AP2 + UCP (+ VI) | purchase | today | 1 | 1 | 1 | 1 | 1 | 2 | 1 | 1 | 1 | 1 | 1 | 11 |
| AP2 + UCP (+ VI) | general | today | 1 | 1 | 0 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 0 | 9 |
| PAP + UCP + WBA | purchase | today | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 10 |
| PAP + UCP + WBA | general | today | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 10 |
| KYA-OS + MCP | purchase | today | 1 | 1 | 1 | 2 | 1 | 2 | 1 | 0 | 1 | 1 | 0 | 11 |
| KYA-OS + MCP | general | today | 1 | 1 | 1 | 2 | 1 | 2 | 1 | 1 | 1 | 1 | 1 | 12 |
| x402 + ERC-8004 | purchase | today | 0 | 1 | 0 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 0 | 8 |
| x402 + ERC-8004 | general | today | 0 | 1 | 0 | 0 | 1 | 0 | 1 | 0 | 1 | 0 | 0 | 4 |
| Visa TAP + WBA | purchase | today | 1 | 1 | 1 | 0 | 1 | 0 | 1 | 0 | 1 | 1 | 0 | 7 |
| Visa TAP + WBA | general | today | 1 | 1 | 1 | 0 | 1 | 0 | 0 | 0 | 1 | 1 | 0 | 6 |
| ACP + Stripe SPT | purchase | today | 1 | 0 | 0 | 1 | 1 | 1 | 0 | 1 | 0 | 1 | 0 | 6 |
| ACP + Stripe SPT | general | today | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 1 |
| WBA + PAP + KYA-OS | purchase | today | 0 | 1 | 1 | 1 | 1 | 1 | 0 | 0 | 1 | 1 | 0 | 7 |
| WBA + PAP + KYA-OS | purchase | if joined | 1 | 1 | 1 | 2 | 1 | 2 | 1 | 0 | 1 | 1 | 0 | 11 |
| WBA + PAP + KYA-OS | general | today | 0 | 1 | 1 | 1 | 1 | 1 | 0 | 1 | 1 | 1 | 0 | 8 |
| WBA + PAP + KYA-OS | general | if joined | 1 | 1 | 1 | 2 | 1 | 2 | 1 | 1 | 1 | 1 | **1** | 12 |
| WBA + PAP + AP2 | purchase | today | 0 | 1 | 1 | 1 | 1 | 1 | 0 | 0 | 1 | 1 | 0 | 7 |
| WBA + PAP + AP2 | purchase | if joined | 1 | 1 | 1 | 1 | 1 | 2 | 1 | 1 | 1 | 2 | 1 | 12 |
| WBA + PAP + AP2 | general | today | 0 | 1 | 1 | 1 | 1 | 1 | 0 | 1 | 1 | 1 | 0 | 8 |
| WBA + PAP + AP2 | general | if joined | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 2 | 1 | 11 |
| WBA + PAP + KYA-OS + AP2 | purchase | today | 0 | 1 | 1 | 1 | 1 | 1 | 0 | 0 | 1 | 1 | 0 | 7 |
| WBA + PAP + KYA-OS + AP2 | purchase | if joined | 1 | 1 | 1 | 2 | 1 | 2 | 1 | 1 | 1 | 2 | 1 | 13 |
| WBA + PAP + KYA-OS + AP2 | general | today | 0 | 1 | 1 | 1 | 1 | 1 | 0 | 1 | 1 | 1 | 0 | 8 |
| WBA + PAP + KYA-OS + AP2 | general | if joined | 1 | 1 | 1 | 2 | 1 | 2 | 1 | 1 | 1 | 2 | 1 | 13 |

Notes on the general rows:

- **AP2 + UCP, general.** The AP2 to UCP join is UCP's AP2 *Mandates* extension. It carries checkout and payment mandates only, which is payment-only under H. So AP2 contributes nothing, and the row equals UCP's general row. L3 falls to 0, because the AP2 `cnf` arrives only inside a payment mandate.
- **PAP + UCP + WBA, general.** This row keeps a chain of 1. PAP supplies L3 (the delegated key on every UCP request, which is MUST) and L8 (token revocation). UCP supplies L1 (Identity Linking), L7 (signed order webhooks) and L8. L10 comes from `ath` and operator-signature coverage. This rests on UCP L7. If order webhooks are read as purchase records under H, L7 goes to 0 and the chain to 0.
- **KYA-OS + MCP, general.** This row moves to chain 1 because KYA-OS L8 is 1 in this variant. MCP's L8 of 1 (cancellation) would also carry it.
- **x402 + ERC-8004, general.** The only documented join is `proofOfPayment.txHash`, which is a payment reference under H. ERC-8004 therefore contributes nothing, and the row equals x402's general row.
- **WBA + PAP + AP2, general, if joined.** The only proposed carrier is PAP #61, a *payments* extension. AP2 is credited here on its generic model, consistent with AP2's own general row (structure credited, A to D partial). For a non-payment action, this needs a mandate type that neither AP2 nor #61 defines. On a strict reading the general upper bound equals the documented row (8).
- **WBA + PAP + KYA-OS, general, if joined.** This reaches chain 1, where the purchase upper bound stays at 0. The difference is L8: PAP's token revocation and KYA-OS's delegation revocation plus Responsible Party give 1 under F.

## 5. Still contestable

- **H on the carried links (section 1b).** This was my extension of H. Without it, ACP is 3, MPP 4 and x402 5, and no chain score changes. If H applied to identity credentials from payment issuers as well, AP2 L1 and VI L1 would also go to 0, and VI's total to 7.
- **UCP L7 and L10 under H.** Order webhooks and identity-linked tokens are commerce-bound. If they were treated as purchase artefacts, UCP would fall to 7, and PAP + UCP + WBA (general) would fall to chain 0 (L7 = 0).
- **x402 L7.** Is a receipt that exists only for paid access "payment-only"? It is 0 on a strict reading, which would put x402 at 3.
- **x401 L8.** Token revocation is a SHOULD with no mechanism defined, and it is the Verifier's own access decision. It is 0 if F's "revoking a grant" is read as needing a defined mechanism. The chain is unaffected.
- **ACP L8 and x402 L8.** `cancelCheckoutSession` is literally an in-flight cancel (F), and x402 `void` likewise. I treated both as purchase remedies (H). If F prevails over H for cancels, ACP L8 goes to 1, and x402 L8 arguably too.
- **ERC-8004 L8.** `revokeFeedback` is a reversal of a recorded act, but the act is the reviewer's, not the agent's.
- **AP2 + UCP L10 (purchase), 1 versus 2.** It is 2 if the AP2 receipt is read as AP2-internal and needing no UCP carrier. That is the README's current value.
- **KYA-OS + MCP L4 and L6 = 2.** These ride on MCP only through a draft, optional extension. A strict "optional extension = partial" reading would make both 1, and the purchase total 9.
- **Classes.** PAP A could be yes on `scope_hints.changes: none` with `personal_data`. TAP A could be yes on the browse tag. ERC-8004 E could be yes on the defined `proofOfPayment` structure. A2A F could be no. ACP D (yes) and UCP D (yes) rest on unsigned consent records.
- **The general upper bounds** for the two AP2 stacks credit AP2's generic structure. No non-payment mandate type exists anywhere.
- MCP, A2A and WBA text comes from earlier fetched copies, apart from the MCP cancellation page fetched in this pass.
