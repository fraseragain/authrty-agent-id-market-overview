# Chain-rubric review: consistency pass and adjudication of unsure cells

Reviewer: independent of the four scorers. Read 25 Nov 2026. Group files were not edited. Sources were re-read from the local copies (`cmp2/src/`, `src/`, `g3/`, `g4/`). Revisions: x402 `866e399`, mpp-specs `aeaeb83`, AP2 `e1ea56d` (v0.2.0 tree), VI `356c296`, UCP `v2026-08-25` (`87dd4b1`), WBA draft-01, PAP 1.0, A2A 1.0.1, MCP 2026-07-28 with EAA, x401 0.2.0, KYA-OS 1.0.0.

## Rules applied, and the readings I had to fix for consistency

- **A** (in-spec only): official extensions, schemes and methods published in the protocol's own spec set count, but only as partial. A MAY or SHOULD pointer to another protocol earns nothing. This is decisive for MPP (card method pointing at TAP) and x401 (agent binding via WBA, mTLS, DPoP, SPIFFE).
- **B** (L10): an identifier match counts towards C1 only. C2 needs a hash of, or signature over, the predecessor artefact. To score 2, C2 must cover the record step as well ("the record references the action").
- **C** (L8): R2 is partial if the spec defines dispute-evidence steps or typed refund or dispute records. Pointing at card rules, or declaring disputes out of scope, scores 0.
- **D** (TAP): VIC fields that were not read get no credit.
- **E** (L3): a self-published key fails K1. K2 needs validity as at the time of use to be checkable later. Expiry carried inside a signed artefact counts as partial K2.
- **A2 in L6 (my reading):** A2 is met only when core checks the action against action-level terms (amount, payee, the specific operation). A check of OAuth scope alone is partial. This is applied to PAP, MCP, A2A and x401 alike.
- **T1 in L9 (my reading):** a verifier-local allowlist or trusted key store that the spec defines or mentions counts as partial. It does not count where the spec says trust is out of scope (Web Bot Auth 4.6).
- **T2 in L9:** expiry alone is not a status mechanism.
- **Multi-mode specs:** I score the strongest mode that core makes normative, unless the rubric marks a mode down. The rubric does this for D3, where a platform-issued grant is partial. On this reading AP2 L10 stays at 2, and AP2 L4 stays at 1 because of D4.
- **A2' (1 / 0.5 / 0):** 0.5 needs one half fully met. The halves are (a) the key is bound by an accountable party, and (b) the key's validity at the time of use can be checked later. A partly met half on its own scores 0.
- **I1':** 0.5 where a third party verified the principal but the spec never says that party resolves the identifier on request. That wording appears nowhere in the 14 specs, so no protocol scores 1.

## 1. Cells changed (16)

| Protocol | Cell | From → to | Rule or reason | Citation |
|---|---|---|---|---|
| PAP | L6 | 2 → 1 | A2 reading. A1 is met: the signed Session JWT carries `ath`, `htm` and `htu`. In core, A2 only checks scope and token. Checking the action's terms ("asks for exactly what it describes") exists only in the optional Operations extension. | PAP spec 5.3 steps 2 and 3 ("Access token validation, scope enforcement… still apply"); Operations §6 "What the Company checks" item 3 |
| PAP | L7 | 1 → 0 | Not met. E1: approvals are "the Personal Agent's statements", and the Session JWT does not cover `Poppy-Approval`. E2: no time anyone else can rely on. E3: the Company "MUST remember that it performed an operation at least until… `expires_at`", which is retention for idempotency, as with ACP's 24 h key (ACP was scored 0 for this). Signed approvals are "on the roadmap". | Operations §6 (fields, "they are the Personal Agent's statements"), §7, §8.1; spec 5.2 claim list |
| PAP | A2' | 0.5 → 0 | Half (a) fails: rule E applies, because the delegation is vouched for by a key in its own `jwks_uri`. Half (b) is only partly met: the delegation `exp` (24 h at most) travels in each request, but revocation is "Removing a key from `jwks_uri`", and that cannot be checked afterwards. L3 stays at 1 (K2 partial). | spec 5.2 "Delegated keys"; 10.7 |
| Web Bot Auth | L9 | 1 → 0 | T1: the draft "does not define how trust is accrued, held, or exchanged" (4.6). `[REGISTRY]` is a separate individual draft, mentioned only as an example (rule A). T2: key rotation "is not a revocation mechanism, and this document does not define any". 6.3 says "This document defines no revocation". JWK `exp` is expiry only. | WBA 4.6, 5.5.2, 5.5.3, 6.3 |
| AP2 | L8 | 0 → 1 | Rule C. The spec defines normative dispute-evidence steps: "When performing verification at the time of dispute, the following steps MUST be followed". These cover recomputing `checkout_jwt`, checking that the receipt `reference` matches the mandate hash, and so on. R1 is not met. | `specification.md` "Dispute Evidence" and "Verification: Dispute" |
| VI | L8 | 0 → 1 | Rule C. It defines a dispute-evidence package and a "Verification procedure" for a dispute investigator. It says it does not assign liability (R1 not met). | `security-model.md` §2.5 |
| VI | L10 | 2 → 1 | Rule B. C1 is met. C2 is met from identity to grant and from grant to action (L2 `sd_hash` over L1, L3 `sd_hash` over L2). There is no record of the action that references the L3 (no receipt object). The scorer flagged this. AP2 keeps 2 because its receipt `reference` is a hash of the closed mandate. | `credential-format.md` §5.4, §6; `security-model.md` §2.5 (the chain is the "evidence package") |
| VI | I1' | 1 → 0.5 | Brought into line with TAP, which has the same structure: a named issuer verified the user and holds the binding (VI: "maintains user identity binding"; TAP: a Visa-signed ID token, "identified by the respective Payment Scheme"). Neither says the identifier is resolved on request. | VI `README.md` §5.1, `credential-format.md` §3.3; TAP "ID Token" |
| Visa TAP | L4 | 1 → 0 | Rule D. The TAP text has no grant artefact. The 1 rested on VIC "purchase instructions", whose fields were not read. | TAP spec (no grant object); group-3 note |
| x402 | L1 | 1 → 0 | The payer is a wallet address with no party named to resolve it. In `http-message-signatures`, `registrationUrl` associates the *signature agent* with a "billing identity", which is the operator, not the principal. SIWX and `auth-hints` authenticate a wallet or client. | core §5.2.2; `extensions/http-message-signatures.md` "Fields"; `extension-auth-hints.md` ("authentication identifies the client") |
| x402 | L3 | 1 → 0 | Rule E. Agent keys are self-hosted at `/.well-known/http-message-signatures-directory`. Registering with the network produces no binding statement or artefact. K2 is not defined for the agent key. The "as of `issuedAt`" text covers server receipt keys only. | `http-message-signatures.md` "Usage"; `extension-offer-and-receipt.md` lines 246–248, 387 |
| x402 | A2' | 0.5 → 0 | Follows L3: neither half is met for the agent key. | as above |
| MPP | L2 | 1 → 0 | Rule A. Core: "it does not identify the client, the payer's principal, or any other party". The only route is the card method's "The client may include Trusted Agent Protocol signature headers", which is a MAY pointer to another protocol. | `core/draft-httpauth-payment-01.md` lines 235–237; `methods/card/draft-card-charge-00.md` lines 98–99 |
| MPP | I2' | 0.5 → 0 | Follows L2. | as above |
| x401 | L3 | 1 → 0 | Rule A. Every agent-binding option (WBA key directory, mTLS, DPoP, SPIFFE or WIMSE) is another protocol, offered as a MAY. "Agent binding is OPTIONAL… This specification does not select a single mechanism." K2 is not defined for an agent key. | x401 "Agent Binding Options", "OAuth Proof-of-Possession…", "Workload Identity" |
| x401 | A2' | 0.5 → 0 | Follows L3. | as above |

## 2. Cells checked and kept

| Protocol | Cell | Score | Basis for keeping |
|---|---|---|---|
| PAP | L3 | 1 | K1 fails under rule E. K2 is partial: delegation `iat`/`exp` (24 h at most) is signed into every Session JWT, so expiry at the time of use can be checked later. This is treated the same as AP2's mandate `exp`. |
| PAP | I1' | 0.5 | The pairwise User ID mapping is held by the operator named by `client_id`. Operations `reference` lets the operator "look into the approval later". |
| PAP | L10 | 1 | `ath` is a hash of the grant (the token) in the action, which is a C2 element. The `sub` match is C1 partial. There is no identity credential and no record. |
| MCP | L1 / I1' | 1 / 0.5 | EAA is an official MCP extension ("Protocol Revision 2026-07-28") and so in-spec under rule A. It carries an IdP-signed `sub` and `email` under a named `iss`. It is optional, so partial. |
| MCP | L6 | 1 | A1 partial (bearer token, audience-bound, not bound to the action). A2 partial (scope only). This is the same reading as PAP and A2A. |
| MCP | L10 | 0 | `sub` is in the ID-JAG only. The access token need not carry it and does not reference the ID-JAG. There is no record. |
| MCP | L9 | 1 | T1 is partial (CIMD trust policies are a MAY, plus the EAA admin allowlist). T2 should read "not met" (expiry only). The score is unchanged. |
| A2A | L4 | 1 | The `OAuth2SecurityScheme` with scopes is declared on the card and per skill (4.5.4), so D1/D2 are partial. The credential comes out of band (7.3). D4 revocation is a SHOULD. 0 is a defensible alternative. |
| A2A | L6 | 1 | A1 partial: credentials go with every request and the server MUST authenticate each one (7.3, 7.4). A2 only "MAY consider" scopes (7.5). |
| A2A | L9 | 1 | T1 partial ("MAY maintain a trusted key store"). Unlike WBA, trust is not declared out of scope. |
| Web Bot Auth | L2 | 1 | The rubric itself says "A bare domain or URL with no attestation… is partial". The draft's "says nothing about who operates the Agent" (4.1) confirms O2 and O3 are not met, but does not remove the O1 partial. Same treatment as PAP, A2A and UCP. |
| AP2 | L4 | 1 | D1 and D2 met. D3 met on the User Credential path and partial on the Trusted Agent Provider path. D4 partial: `exp` is not in `required` (`open_checkout_mandate.json`, `open_payment_mandate.json` require only `vct`, `constraints`, `cnf`) and there is no revocation. D4 keeps it at 1 whichever way D3 is read. |
| AP2 | L10 | 2 | The `delegate_payload` "MUST be included as part of the Key Binding" over the User Credential presentation, the closed mandate `sd_hash` references the open mandate, and the receipt "`reference` MUST match the hash of the closed Checkout Mandate". This scores the strongest normative mode. The Trusted Agent Provider path would give 1. |
| AP2 | L1, L3, L9 | 1, 1, 1 | Kept as scored. L9 T1 is partial under the local-trust-list reading ("trust list of Agent Providers", not defined). |
| VI | L2, L5, L7, L9 | 1 each | Kept. L9 T2 is partial because the spec itself calls JWKS removal "the VI-layer revocation mechanism". |
| UCP | L3 | 0 | Platform keys are self-published in profile `keys[]` (rule E). Revocation is only removal ("a key still listed continues to verify"). The user-credential flow binds the user's key, not an agent key. Agent `cnf` binding is defined in AP2, not in UCP (rule A). `ap2-mandates.md` "Signing Key Requirements". |
| UCP | L1, L4, L6, L10 | 1 each | Each rests on UCP's own extension text (Identity Linking scopes, the `(iss, sub)` pair and its revocation endpoint; the `ap2.checkout_mandate` nesting of `merchant_authorization` and the "terms match" check). It does not rest on AP2's text. |
| UCP | L8 | 1 | Typed `adjustments` (`refund`, `return`, `dispute`) under rule C. Merchant of Record "financial liability" is in the glossary only. |
| ACP | L8 | 1 | Typed `Adjustment` records (`refund`, `dispute`, `chargeback`) under rule C. |
| ACP | L10 | 1 | `checkout_session_id` is a plain string linking allowance, completion and order. Rule B allows C1 at most. There is no C2. |
| Visa TAP | L2 | 1 | Kept on TAP text alone ("Participants": "certified AI platforms that have been onboarded… approved and trusted by the respective Payment Schemes"). O1 is partial because no field names the operator. The VIC VARS citation is dropped. |
| Visa TAP | L5 | 1 | S1 and S2 are met in TAP. S3 has only optional `auth_time`/`amr`. VIC passkeys get no credit. |
| Visa TAP | L6 | 0 | No grant. The `credentials-for-instruction` endpoint was not read (rule D). |
| Visa TAP | L3, L9, L10 | 1, 1, 1 | L3: K1 is met because the key is "retrieved from a trusted Key Store" run by the scheme. L9 is kept on the Key Store alone (the VIC Agent Registry citation is dropped). L10: shared `nonce` and `kid` are identifier links, so C1 partial and no C2 (rule B). |
| x402 | L2 | 1 | A domain-hosted directory plus registration through the in-spec `http-message-signatures` extension. A bare domain is O1 partial. |
| x402 | L4, L5, L6 | 1, 1, 1 | In-spec core and schemes: EIP-3009 `authorization` (`value`, `to`, `validBefore`), `upto` maximum, `auth-capture` deadlines. Per-payment EIP-712 signature and nonce. Facilitator `/verify` before the resource runs. L4 is contestable: this is the payer's authorisation of a transfer, not a principal-to-agent grant. |
| x402 | L7 | 1 | The in-spec offer-receipt extension gives a server-signed receipt with `issuedAt`. Ledger time. SHOULD preserve "temporally immutable authorization evidence". |
| x402 | L8 | 1 | The in-spec `auth-capture` scheme defines `void`, `refund`, `reclaim` and `refundDeadline` (rule C). |
| x402 | L9 | 1 | T1 partial: `registrationUrl` (required in the extension) points to the network's registry of signature agents. T2 partial: verifiers SHOULD evaluate signer authorisation "as of the receipt's `issuedAt`" and treat removal "as prospective". Contestable, and could be 0. |
| x402 | L10 | 1 | The same `payer` across authorisation, settlement and receipt is C1 partial. The optional receipt `transaction` hash is a record-to-action element. |
| MPP | L1 / I1' | 1 / 0.5 | The card method (in-spec) uses issuer-provisioned network tokens, and `cardholderFullName` "SHOULD include when available from the TSP". This is a third-party-backed instrument, treated the same as ACP's 3DS. The `source` DID is self-asserted. |
| MPP | L3 / A2' | 1 / 0.5 | Tempo charge: access keys are authorised through the AccountKeychain. Servers MUST check `isRevoked` and `expiry` on-chain. Half (b) is met through ledger state. K1 is partial because the root is pseudonymous. `draft-tempo-charge-00.md` "Access Keys". |
| MPP | L4, L5, L6, L7, L9, L10 | 1 each | All rest on MPP's own method drafts (Tempo `keyAuthorization` and "Authorization Scope Verification" MUSTs, the Stripe SPT) or on core (HMAC challenge binding, single-use proof). L9 rests on Tempo `isRevoked` (T2). The discovery draft's mentions of the MCP Registry and ERC-8004 earn nothing under rule A. |
| MPP | L8 | 1 | Kept, on a new basis. The card method's "subject to card network chargeback rules" earns 0 under rule C. Two things carry the 1 instead. Tempo session: "Servers MUST implement challenge-to-voucher mapping for: Dispute resolution". Lightning session: receipts carry `refundSats` and `refundStatus` (refund records). Contestable, because these are refunds of unspent deposits, not purchase refunds. |
| ERC-8004 | L3 / A2' | 1 / 0.5 | The basis is corrected, but the score is unchanged. K1 is *not* met: the owner sets `agentWallet` on its own registration, which is self-published. K2 is met: registry events give the history of the wallet binding. |
| ERC-8004 | L7 | 1 | E2 (ledger time) and E3 (hash commitments that "cannot be deleted") are met for feedback and validation records. E1 is partial (pseudonymous addresses). The records concern the agent's work, not the payment. Contestable. |
| ERC-8004 | L10 | 1 | No principal, so C1 is not met. C2 partial: `validationResponse` references `requestHash`, and `feedbackHash` commits to the off-chain file (hash of the predecessor). |
| ERC-8004 | L8 | 0 | "showing a refund" is an example use of `appendResponse`, not a defined refund record. |
| x401 | L4 | 1 | The Verification Token is scoped (MUST) and expires (MUST). It is an access token, as in MCP's D1. D3 is not met because the Verifier issues it. |
| x401 | L7 | 0 | The token records an access decision ("not a credential, payment artifact…"). Its claims are deployment-specific and the time is SHOULD-level. There is no retention text. |
| x401 | L5, L9 | 1, 1 | L5: S1 comes only through other protocols (rule A), and S2 is met for the credential result (OpenID4VP nonce, Proof Validation 4). L9: T1 partial, because `trusted_authorities` naming `etsi_tl` or `openid_federation` *is* a reference to a trust list (the test itself, so rule A does not apply). T2 is met (MUST check status). |
| KYA-OS | L1 | 1 | The Responsible Party DID is the root issuer (MUST). KYC/KYB `IdentityVerificationCredential` is an in-spec optional profile, so P2 partial. P3 is an allowlist only. |
| KYA-OS | L10 | 1 | Rule B. C1 is met by DID match. Action to grant is by signed digest (MUST) and record to action by `requestHash`/`responseHash`. Grant to identity is by DID match only: the root delegation is signed *by* the Responsible Party key, not *over* an identity credential. |
| KYA-OS | L8 | 0 | "the entity ultimately accountable for actions" (SPEC §2, line 807 MUST) names an accountability root. It does not allocate liability between roles. UCP's partial R1 rests on explicit "financial liability" wording, which KYA lacks. Contestable (1 if accountability is read as liability). |
| KYA-OS | L3, L4, L6 | 1, 2, 2 | L3: K1 is met (the delegator signs a credential naming the agent key). K2 is partial. L4: D3 is met on the model (root `issuerDid` = signer). L6: the digest MUST and the caveat MUST. |

## 3. Final rows

| Protocol | L1 | L2 | L3 | L4 | L5 | L6 | L7 | L8 | L9 | L10 | Chain | Total | I1' | I2' | A2' |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| PAP | 0 | 1 | 1 | 1 | 1 | 1 | 0 | 0 | 1 | 1 | 0 | 7 | 0.5 | 0.5 | 0 |
| MCP | 1 | 1 | 0 | 1 | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 6 | 0.5 | 0.5 | 0 |
| A2A | 0 | 1 | 0 | 1 | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 5 | 0 | 0.5 | 0 |
| Web Bot Auth | 0 | 1 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 0.5 | 0 |
| AP2 | 1 | 1 | 1 | 1 | 1 | 2 | 1 | 1 | 1 | 2 | 1 | 12 | 0.5 | 0.5 | 0.5 |
| VI | 1 | 1 | 1 | 2 | 1 | 2 | 1 | 1 | 1 | 1 | 1 | 12 | 0.5 | 0.5 | 0.5 |
| UCP | 1 | 1 | 0 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 0 | 9 | 0.5 | 0.5 | 0 |
| ACP | 1 | 0 | 0 | 1 | 1 | 1 | 0 | 1 | 0 | 1 | 0 | 6 | 0.5 | 0 | 0 |
| Visa TAP | 1 | 1 | 1 | 0 | 1 | 0 | 1 | 0 | 1 | 1 | 0 | 7 | 0.5 | 0.5 | 0.5 |
| x402 | 0 | 1 | 0 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 0 | 8 | 0 | 0.5 | 0 |
| MPP | 1 | 0 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 0 | 9 | 0.5 | 0 | 0.5 |
| ERC-8004 | 0 | 1 | 1 | 0 | 0 | 0 | 1 | 0 | 1 | 1 | 0 | 5 | 0 | 0.5 | 0.5 |
| x401 | 1 | 1 | 0 | 1 | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 6 | 0.5 | 0.5 | 0 |
| KYA-OS | 1 | 1 | 1 | 2 | 1 | 2 | 1 | 0 | 1 | 1 | 0 | 11 | 0.5 | 0.5 | 0.5 |

The headline change is that x402 and MPP no longer have a chain with no missing link at 1. Both fall to 0: x402 on L1 and L3, MPP on L2. AP2 and VI move up to a chain with no missing link at 1 once their dispute-evidence procedures are credited under rule C. No protocol scores 2 on L1, L2, L3, L5, L7, L8 or L9.

## 4. Disagreements with stacks.md

| Stack | stacks.md L10 | Mine | Reason |
|---|---|---|---|
| 1 AP2 + VI + UCP | 2 (user-credential path), 1 (trusted platform) | 2 / 1, kept | The UCP to AP2 join is MUST (nested checkout in `checkout_mandate`, `transaction_id` = checkout hash). The record step is AP2's receipt `reference` hash. Caveat: UCP defines no carrier for receipts, so the record exists in AP2 but not on the UCP wire. If "across the boundary" is read strictly, 1. VI adds nothing, as stacks.md says. |
| 2 TAP + WBA | 1 | 1, kept | A shared nonce and key is an identifier link (rule B: C1 at most). The join is undefined, so the stack cannot take best-member scores for L1–L9. |
| 3 PAP + UCP + WBA | 1 | 1, kept | `ath` and `content-digest` give per-request links. There is no purchase grant and no record chain. |
| 4 x402 + ERC-8004 | 1 (weak) | 1, kept | `proofOfPayment.txHash` is an optional field defined in ERC-8004's own text, so it is in-spec under rule A. It is a hash reference to the x402 settlement. There is no principal and no grant. |
| 5 KYA-OS + MCP | 2 (tool-call chain) | **1** | Two reasons. (i) Rule B: inside KYA the grant does not hash or sign over an identity credential (DID match only), so C2 is incomplete before any boundary is crossed. KYA-OS scores 1 on its own. (ii) The MCP binding is an optional draft extension, which stacks.md itself says gives 1 under a strict reading. |
| 6 ACP + SPT | 1 (weak) | 1, kept | Plain `checkout_session_id` and an embedded opaque token: C1 at most. |

There are also knock-on effects for the stacks' L1–L9 best-member scores, which are outside stacks.md's scope. With AP2 L8 now 1, stack 1 reaches L8 = 1 through AP2 (AP2+UCP is a documented join). UCP gives L8 = 1 through its adjustments in any case. Stack 1's L3 should come from AP2 (1), not from UCP's self-published keys. That holds only where the `ap2_mandate` capability is negotiated, as stacks.md notes.

## 5. Still contestable

- x402 L4 (is a payer's EIP-3009 transfer authorisation a "grant" at all?) and x402 L9 (does network registration count as a registry?). Either could go to 0.
- MPP L8: whether refunds of unspent deposits and a MUST to keep a mapping "for dispute resolution" amount to a refund or dispute record. 0 is defensible, which would leave every L8 above 0 resting on rule C partials (AP2, VI, UCP, ACP, x402).
- AP2 L10 = 2 rests on scoring the strongest normative mode. If the Trusted Agent Provider path pulls it down, as it does D3 in L4, then AP2 L10 = 1.
- KYA-OS L8: "ultimately accountable" read as a partial R1 would give 1, and a chain score of 1.
- I1' at 0.5 for both VI and TAP. Both have a named, accountable issuer that verified the user and holds the binding. Read generously, both would be 1. They should move together.
- A2A L4 (1 vs 0) and ERC-8004 L7 and L10 (records concern work or feedback, not the payment).
- The A2' "one half fully met" rule moved PAP to 0. A rule allowing half credit for a partly met half would restore 0.5.
