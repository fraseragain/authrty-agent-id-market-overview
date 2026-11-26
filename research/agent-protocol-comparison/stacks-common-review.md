# Review: common stack scores (cmp4)

Reviewer: independent of the stack scorer. Read 25 Nov 2026. `common-stacks.md` and `common-stacks.json` were not edited. No repository was touched. Final data: `cmp4/final-common.json`.

Member rows used by the scorer were checked cell by cell against `scores.json` `chain_scores` (purchase) and `final-general-adjusted.json` `general_protocols` (general, with H confined to L4 to L8). All eight rows match.

Fetched in this pass (GET only, saved under `cmp4/rev/`): x402 `specs/transports-v2/mcp.md` at `28ddebb`, `866e399` and `main` (byte-identical to the local copy); live UCP profiles for allbirds, gymshark, puffy and checkout.puffy; `www.meta.com` signature directory; Sierra's `releasing-poppy` post; the PPC Land article; Meta's crawler page; Cloudflare's signed-agents pages.

## 1. Changes

| Stack | Cell | From → to | Reason | Citation |
|---|---|---|---|---|
| 3 x402 + MPP + MCP | general, if joined | 1 1 1 1 1 1 1 1 1 1 (chain 1, 10) → 1 1 0 1 1 1 1 1 1 1 (chain 0, 9) | The old row took L7 from x402 (signed receipt) and L3 from MPP (Tempo access key). One request pays by one of the two, so no request has both. Best single path: the x402 path, which equals stack 1's general if-joined row. The MPP path reaches at most 9, with L7 = 0 (MPP and MCP both have general L7 0). L3 would also be 0 there on the strict reading, because Tempo keys "MUST NOT authorize… any other non-transfer selector". | `common-stacks.md` stack 3; `review-general.md` 1b (Tempo key); `final-general-adjusted.json` MPP L7 0 |
| 3 x402 + MPP + MCP | purchase, if joined | 1×10 (chain 1), kept, but the basis changes | The row is now derived as a single path and is no longer a per-link maximum. Path: MPP's Tempo method over MPP's MCP draft transport, plus the proposed join of MCP identity into the MPP credential. MCP supplies L1 (EAA) and L2 (CIMD). Tempo supplies L3 to L10 (keyAuthorization, Authorization Scope Verification, `isRevoked`, session dispute mapping). This holds even on a one-method reading of MPP, so the chain-1 upper bound is robust to question 1. | `draft-payment-transport-mcp-00.md` ("server MUST respond… `-32042`", credential in `_meta`); `chain-review.md` MPP rows |
| 5 PAP + WBA (+ UCP, MCP) | purchase, as deployed | 1 1 0 1 1 1 1 1 1 1 (9) → 1 1 0 1 1 1 0 1 1 1 (8) | L7 1 → 0. UCP's L7 rests on signed webhooks (E1), plus `merchant_authorization` (AP2 extension). Business signatures are verified against keys in the business's profile ("Business → Platform webhooks: Profile URL from `UCP-Agent` header"). The live Shopify profiles have no `keys` member anywhere and offer no AP2 capability. A platform following UCP therefore cannot verify a Shopify signature, and E1 fails as deployed. | `ucp-sig.md` "When Signatures Apply" ("Webhook notifications MUST be signed"), identity resolution "Applicability"; live `/.well-known/ucp` (top-level keys: `version`, `supported_versions`, `services`, `capabilities`, `payment_handlers`) |
| 5 PAP + WBA (+ UCP, MCP) | general, as deployed | 1 1 0 1 1 1 1 1 1 1 (9) → 1 1 0 1 1 1 0 1 1 1 (8) | Same L7 reason. | as above |
| 5 | JSON | as-deployed rows added | They were in the md but missing from the JSON. Added under `purchase.as_deployed` and `general.as_deployed`. | — |

Text corrections (no score change):
- **Stack 1, if-joined note.** The md says the x402 MCP transport "defines only the unsigned `SettlementResponse`", so the receipt "would have to be carried". That is wrong. The transport carries the core `SettlementResponse` type in `_meta["x402/payment-response"]`, and offer-receipt says "the `SettlementResponse` MAY include a receipt in the `extensions` field". The signed receipt can ride MCP today. The general "today" L7 is 0 only because the join is a payment transport (the join-carriage reading, section 3). It is not 0 for want of a field. So the general if-joined row needs a change of reading, not a new join. (`specs_transports-v2_mcp.md` "Settlement Response Delivery"; `x402-extension-offer-and-receipt.md` line 267.)
- **Stack 4, UCP to A2A AP2 text.** The DataPart text uses lowercase "must" ("must create…", "must be specified in the `DataPart` as `ap2.checkout_mandate`"). UCP adopts RFC 8174, so lowercase is not BCP 14 language. The AP2 join stays normative through the AP2 Mandates extension itself, which has uppercase MUSTs. The A2A binding text is descriptive.
- **Stack 5, "all Shopify-hosted".** The UCP profiles return `powered-by: Shopify`, and the MCP endpoints are `*.myshopify.com/api/ucp/mcp`. However, puffy's `poppy.json` is served by Vercel and points to `checkout.puffy.com/.well-known/ucp`, which is Shopify. herocosmetics.com redirects to `.us`. These are 45 Shopify-backed stores, with one `poppy.json` not served by Shopify.
- **Stack 5, meta.ai.** Today `meta.ai` and `www.meta.ai` return 404 `application/json`, not an HTML app. They are still not a directory.

## 2. Checks kept

- **Stack 1.** All four rows are kept. x402 transport claims verified: MUST `isError: true` with both `structuredContent` and `content[0].text`; `_meta["x402/payment"]`; `_meta["x402/payment-response"]`; resource `mcp://tool/<name>`. No mention of OAuth, MCP authorization or caller identity (grep). The file is the same at `28ddebb` and `866e399`. Purchase anchor x402 is kept: unlike the PAP UCP extension, the x402 transport says nothing about the MCP auth artefacts on the same request. The sensitivity in the md (9 if MCP host artefacts are credited) is fair.
- **Stack 2.** All rows are kept (5 / 6 / 6 / 7, chain 0). See question 2.
- **Stack 3, purchase today** (best single path, 9) and the floor (7) are kept. Both are conditional on the MPP member row (section 5).
- **Stack 3, general today** (MCP row, 7) is kept on the join-carriage reading.
- **Stack 4.** All rows are kept. Today equals the reviewed AP2 + UCP rows. The UCP MCP binding names `dev.ucp.common.payment.ap2_mandate` only as a capability (3 hits, all capability lists). The if-joined general row follows the WBA + PAP + AP2 precedent, which credits AP2's generic mandate model.
- **Stack 5, spec rows** (1×10 under both rubrics) are kept. They equal the reviewed PAP + UCP + WBA row. MCP adds nothing: purchase MCP L8 is 0, and general MCP L8 1 duplicates UCP. Against PAP + WBA (purchase 0 1 1 1 1 1 0 0 1 1; general 0 1 1 1 1 1 0 1 1 1), the stack lifts only L1, L7 and L8, all from UCP through the documented `ucp` extension. That is consistent.
- **Stack 5, deployment data.** Verified from `survey.json`: 81 domains probed, 45 JSON. All 45 are `protocol_version: "0.4"`, with the same keys (`protocol_version`, `organization`, `auth`, `agent`, `web`, `extensions`). The files differ only in organisation and endpoint host (3 shapes after normalising the domain: default, the `.us` redirect, and `checkout.` subdomain). Each has one `agent.protocols` entry of type `ucp`, `extensions.ucp` v1, one scope `dev.ucp.shopping.checkout:manage` marked `changes: irreversible`, `web: {}`, and no `apis`, `tasks` or `supported_versions`. MCP 0, OpenAPI 0. The PAP 3.4 claim is verified: "before 1.0, the same minor version". With no `supported_versions`, a 1.0 Personal Agent "MUST NOT use any of them". Live profiles are UCP `2026-08-25`, with transports `mcp` and `embedded` only, no `keys`, and no AP2. Capabilities include order, buyer_consent, ask, identity_linking (provider `app.shop.accounts`) and catalog. The `oauth-protected-resource` detail was not re-checked.

## 3. Answers

### Q1. Stack 3: best single path, and whether if-joined may combine alternatives

"Today = best single path" is correct. A counterparty that receives one request receives one payment credential. Taking the best member per link across x402 and MPP would credit a request that cannot exist. The floor row is a useful companion for a merchant that accepts both.

The if-joined row must not combine per-link maxima across alternatives either. An upper bound is still a bound on some achievable request. "If joined" relaxes missing joins. It does not merge two payment credentials into one request. Recomputed as the best single path with its documented MCP transport plus the proposed MCP-identity join:
- **Purchase.** MPP (Tempo) over the MPP MCP draft, plus MCP L1 and L2: 1×10, chain 1. The same as the scorer's number, now on a valid basis.
- **General.** The x402 path: 1 1 0 1 1 1 1 1 1 1, chain 0, 9. The MPP path reaches at most 9 (L7 0, and L3 0 on the strict reading). The scorer's 1×10 general row combined x402 L7 with MPP L3, so it falls.

### Q2. No normative join: weaker hop or the member that owns the layer

One rule, stated so that it covers all 15 stacks:

> A link scores what the counterparty of the consequential action can rely on. Members on the **same hop** (they sign or carry artefacts on the same request to the same counterparty, or one is a profile or carrier of the other) are scored as before: the best member whose artefact a documented join carries, otherwise the anchor. Where the chain crosses **separate hops** and no join carries the principal's artefacts from one hop into the next, each link takes the **lowest** hop, because the downstream hop's artefacts describe its own caller, not the principal.

"Owner of the layer" only works where there is one layer. In MCP + A2A there are two counterparties: the A2A server acts on A2A artefacts and the MCP server acts on MCP artefacts. So no member owns the end-to-end chain. MCP's EAA identity names whoever the A2A server agent's MCP client signs in as. Nothing makes that person the upstream principal. A pure "weaker hop" rule applied blindly would wreck same-hop stacks. For example, TAP + WBA would fall to WBA's row, but TAP signatures *are* WBA-shaped signatures on the same request, so there is no second hop.

Applied to the 15 stacks: only MCP + A2A is multi-hop. Stacks 1, 3, 4 and 5 here, and all 10 in `final-general-adjusted.json`, are single-hop. x402 + ERC-8004 is a registry lookup, not a second hop. ACP + SPT: the SPT is presented on the ACP request. KYA-OS + MCP: KYA rides the tool call. Stack 2 keeps the min row. **No earlier stack row changes under this rule** (`earlier_stack_changes` carries only the rule).

A separate finding, not caused by the Q2 rule, is given in `earlier_stack_flags`. **x402 + ERC-8004, general today, L10 0 → 1** (total 4 → 5, chain 0 unchanged). The row is x402's general row (ERC-8004 adds nothing because its join is a payment hash). x402's general L10 reverted to 1 when H was confined to L4 to L8. The ACP + SPT row was updated in that same revert (L1 and L10 0 → 1), and this one was missed.

### Q3. Stack 5: consistency, UCP L7 under H, deployment

- **Consistency.** The spec rows equal PAP + UCP + WBA (1×10 under both rubrics). Compared with PAP + WBA, the extra credit (L1, L7, L8) all comes from UCP through PAP's normative `ucp` extension. One nuance the earlier row also has: the PAP L3 credit rests on the Personal Agent sending the Session header on UCP requests (MUST), but "A Company MAY verify the Session header on UCP requests… a UCP service that uses no Session claims can ignore it" (`pap/extensions/ucp.md` §4, §8). Verifier-side MAY is still partial, so L3 = 1 stands.
- **UCP general L7 under H.** On the letter of H ("exists only to… evidence… a purchase"), order webhooks fail. They exist only for orders: fulfilment events and adjustments, and they are the only UCP webhooks (grep across `ucpall`). The same review stripped order adjustments from UCP L8 as "order remedies". Response signing is no rescue: UCP recommends it only for "Payment authorization responses" and "Checkout completion responses", and makes it OPTIONAL for cart and catalog. The earlier review kept x402 general L7 on a "service was delivered" reading, and fulfilment events are the same kind of delivery record. I keep UCP general L7 = 1 for consistency with that reviewed member cell, which I am not re-scoring. But **the general chain of 1 for stack 5 (spec) and for PAP + UCP + WBA rests entirely on this reading**. Strict H gives L7 0 and chain 0 for both. This is the most contestable cell in the set.
- **As deployed.** The scorer's description is confirmed: 45 files, all 0.4, UCP only, no MCP or OpenAPI surface in `poppy.json`. MCP is reachable only as UCP's own transport. Because the files are 0.4, a 1.0 Personal Agent must not use them, so PAP adds no artefact on the wire. WBA adds nothing, because it never scores above UCP. The row is UCP as Shopify deploys it:

| Rubric | L1 | L2 | L3 | L4 | L5 | L6 | L7 | L8 | L9 | L10 | Chain | Total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Purchase, spec | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 10 |
| Purchase, as deployed | 1 | 1 | 0 | 1 | 1 | 1 | 0 | 1 | 1 | 1 | 0 | 8 |
| General, spec | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 10 |
| General, as deployed | 1 | 1 | 0 | 1 | 1 | 1 | 0 | 1 | 1 | 1 | 0 | 8 |

Cell bases for the deployed row:
- **L1:** Identity Linking with provider `app.shop.accounts`.
- **L2:** the platform profile, platform-side.
- **L3:** 0. PAP is unusable, and UCP L3 is 0 anyway.
- **L4:** identity-linking scope `checkout:manage`, with revocation.
- **L5:** idempotency and buyer review are on the business side. S1 depends on whether the platform signs, which is unobserved.
- **L6:** UCP's own L6 basis is the AP2 extension, which is not deployed. 1 survives only on the MCP-equivalent reading (identity-linked bearer token with a scope check). Guest checkout has no grant at all.
- **L7:** 0, because the profiles publish no keys.
- **L8:** purchase, order adjustments (order capability present). General, identity-linking revocation and Buyer Consent (present).
- **L9:** IdP allowlist and token revocation.
- **L10:** C1 partial through the identity-linked token.

**Verdict:** the spec stack has chain 1. What runs on Shopify today is UCP over MCP with chain 0. PAP is a 0.4 pointer file that 1.0 agents must ignore. Neither PAP nor WBA is shown to act on these requests.

### Q4. Spot-checks on the cited joins

- **x402 `specs/transports-v2/mcp.md`.** Confirmed in every detail cited, at both revisions. One correction: the signed receipt can already ride MCP (section 1).
- **UCP A2A binding naming AP2 DataParts.** Confirmed: `ap2.merchant_authorization` in a `DataPart`, payment in `a2a.ucp.checkout.payment`, `ap2.checkout_mandate` (`docs/specification/shopping/checkout/a2a.md`, "AP2 based Checkout Completion"). The wording is lowercase "must", which is not BCP 14 under UCP's RFC 8174 adoption. The MCP binding has no AP2-specific text beyond capability lists. Also confirmed: the MPP MCP draft `-32042` MUST, `_meta` credential and receipt, and `InitializeResult` SHOULD. It is `category: info`.

### Q5. Muse and Web Bot Auth evidence

| Claim | Class | Basis |
|---|---|---|
| Meta signs some Muse and Meta-WebIndexer requests with WBA since about 12 Oct, low volume, possibly first as `Meta-ExternalTest` | **Secondary** | PPC Land, 31 Oct 2026, reporting a LinkedIn post by DataDome's VP of Threat Research (30 Oct). The LinkedIn post was not fetched. "Testing" and the `Meta-ExternalTest` labelling are his inferences. No Meta statement. Not upgraded. |
| DataDome added validation | Secondary for Meta traffic | DataDome's changelog says WBA verification is live for all customers (primary for DataDome's general feature). That it validates *Meta's* signatures comes only from the same post. |
| Signature-Agent value | **Not found** | Not reported anywhere. |
| `www.meta.com/.well-known/http-message-signatures-directory` is live with 5 Ed25519 keys and self-signed (5 signatures, `tag="http-message-signatures-directory"`) | **Primary** | Re-fetched: 200, `application/http-message-signatures-directory+json`, 5 OKP/Ed25519 JWKs (`kid`, `kty`, `crv`, `x`), sig1 to sig5. Nothing in it names Muse, so it is primary for "Meta publishes a WBA directory" only. |
| facebook.com has no directory; meta.ai is not a directory | Primary | Re-fetched: www.facebook.com 404 HTML, meta.ai and www.meta.ai 404 JSON. |
| Meta crawler docs list five agents, not Muse, with IP-based verification only | **Primary** (now) | Fetched today: FacebookExternalHit, Meta-WebIndexer, Meta-ExternalAds, Meta-ExternalAgent, Meta-ExternalFetcher. Verification is by allowlisting user agent strings or IPs. No WBA. |
| Cloudflare: signed agents distinguished from 1 Jul 2026 | Primary | Cloudflare signed-agents and policy pages ("As of July 1, 2026…"). |
| Cloudflare: automated review validates signatures from 28 Aug 2026 | **Not found** | Not on either Cloudflare page fetched. Remove it or cite its source. |
| Meta or Muse in Cloudflare's signed-agent list | Not found | Neither page names them. The directory is not readable. |
| Sierra: Muse "automatically looks for Poppy first on every site it visits"; "every Shopify store now automatically publishes a Poppy file"; v1.0 available (13 Nov 2026) | **Primary** for what Sierra says, secondary for Meta's and Shopify's behaviour | `sierra.ai/blog/releasing-poppy`. The post does not mention WBA or signing. The Shopify half is contradicted in part by the live files, which are 0.4. |
| Muse sends `Poppy-Session` or operator signatures on Poppy or UCP requests | **Not found** | No public trace. The 5.3 operator signature is SHOULD. |
| Meta keys Ed25519 vs PAP Session keys ES256, so the keys are separate | Primary (directory plus PAP spec), but the inference is the scorer's | There is no evidence of which key Muse would use. |

## 4. Still contestable

- **UCP general L7 (order webhooks under H).** This carries the general chain of 1 for stack 5 (spec) and PAP + UCP + WBA. Strict H gives 0 for both.
- **The join-carriage reading.** The general rows for stacks 1, 3 and 4, and for the earlier AP2 + UCP and x402 + ERC-8004 rows, treat a payment-only join as carrying nothing on *any* link. This is a stack-level rule kept from the earlier reviewed data, distinct from H. If only H applies (L4 to L8), the payment join would carry L1, L2, L3, L9 and L10, plus x402's non-payment-only receipt (L7):
  - Stacks 1 and 3, general today, would become 1 1 0 1 1 1 1 1 1 1 (9, chain 0).
  - AP2 + UCP general L3 would become 1 (AP2 `cnf`), giving 1×10 and **chain 1**.
  - That last change would be the single biggest move in the set.
- **The MPP member row combines methods.** L1 comes from the card method and L3 from the Tempo method. That is the cross-alternative combination question 1 rejects, but applied inside one protocol. On a one-method reading, stack 3 purchase today falls from 9 to 8 (Tempo path 0 0 1 1 1 1 1 1 1 1). The purchase if-joined chain 1 survives (section 1). The earlier review's "strongest mode" rule should state whether it scores per mode.
- **Stack 1 purchase anchor.** If MCP host artefacts on the same request are credited without a join, today becomes 9. The chain does not change.
- **Stack 5 as deployed.** L5 (platform signing unobserved) and L6 (MCP-equivalent reading, guest checkout has no grant) could each be 0. The chain is 0 regardless.
- **x402 + ERC-8004 general L10** (flagged in section 3, Q2). It is a stale cell, unless the earlier reviewer meant L10 to be scored across the join only. In that case the TAP + WBA and ACP + SPT rows would need the same treatment.
