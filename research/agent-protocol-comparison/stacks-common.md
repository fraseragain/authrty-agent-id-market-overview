# Common agent protocol stacks scored against the chain rubric

Read 25 Nov 2026. Rubric: `chain-rubric.md` (purchase) and `chain-rubric-general-actions.md` (general). Member scores are the reviewed ones (`scores.json` `chain_scores`; `final-general-adjusted.json` `general_protocols`) and are not re-scored. Rules A to H as in `chain-review.md` and `review-general.md` (H applied to L4 to L8 only). No repository was edited. The only network writes were GET requests, plus one unauthenticated `tools/list` POST to a public Shopify MCP endpoint.

## Basis

"Documented today": a member counts on a link only where a documented join carries its artefact. Otherwise the stack takes the score of the anchor, the member on whose artefacts the counterparty acts. Under the general rubric a join that carries only payment artefacts carries nothing (H). "If joined as proposed" takes the best member per link, an upper bound, and names the extension point.

Two stacks need a reading the earlier stacks did not:
- **Alternatives, not layers (stack 3).** x402 and MPP are two ways to pay one request. Taking the best member per link would give a row no single request can achieve. "Today" is therefore the best single payment path, and the floor (elementwise minimum of the two paths, what a counterparty accepting both can rely on) is shown beside it.
- **No join at all (stack 2).** The two protocols sit on different hops (client to agent, agent to tool). A chain through both is limited by the weaker hop on each link, so "today" takes the lower member on each link, not the better.

Member rows used (L1 to L10):

| | Purchase | General |
|---|---|---|
| x402 | 0 1 0 1 1 1 1 1 1 1 | 0 1 0 0 1 0 1 0 1 1 |
| MPP | 1 0 1 1 1 1 1 1 1 1 | 1 0 1 0 0 0 0 0 1 1 |
| MCP | 1 1 0 1 1 1 0 0 1 0 | 1 1 0 1 1 1 0 1 1 0 |
| A2A | 0 1 0 1 1 1 0 0 1 0 | 0 1 0 1 1 1 0 1 1 0 |
| UCP | 1 1 0 1 1 1 1 1 1 1 | 1 1 0 1 1 1 1 1 1 1 |
| AP2 | 1 1 1 1 1 2 1 1 1 2 | 1 1 1 1 1 1 1 0 1 2 |
| PAP | 0 1 1 1 1 1 0 0 1 1 | 0 1 1 1 1 1 0 1 1 1 |
| WBA | 0 1 0 0 1 0 0 0 0 0 | 0 1 0 0 1 0 0 0 0 0 |

Stack-level reference rows already reviewed: AP2 + UCP (+VI) purchase 1 1 1 1 1 2 1 1 1 1 and general 1 1 0 1 1 1 1 1 1 1; PAP + UCP + WBA 1 1 1 1 1 1 1 1 1 1 for both.

## Summary

| # | Stack | Purchase today (chain / total) | Purchase if joined | General today | General if joined | Most important missing join |
|---|---|---|---|---|---|---|
| 1 | x402 + MCP | 0 / 8 | 0 / 9 | 0 / 7 | 0 / 9 | Neither spec binds the MCP caller (OAuth client or user) to the x402 payer wallet |
| 2 | MCP + A2A | 0 / 5 | 0 / 6 | 0 / 6 | 0 / 7 | Nothing carries the principal or the grant from an A2A hop into the MCP hop |
| 3 | x402 + MPP + MCP | 0 / 9 (floor 0 / 7) | 1 / 10 | 0 / 7 | 1 / 10 | Same as stack 1: no join from the MCP caller's identity to either payment credential |
| 4 | UCP + AP2 over MCP/A2A | 1 / 11 | 1 / 12 | 0 / 9 | 1 / 11 | UCP has no carrier for the AP2 receipt; AP2 has no non-payment mandate |
| 5 | PAP + Web Bot Auth (+ UCP, MCP) | 1 / 10 (as deployed 0 / 9) | n/a | 1 / 10 (as deployed 0 / 9) | n/a | A signed User approval or mandate; PAP's approval is the agent's word |

---

## 1. x402 + MCP

### Documented joins
| Pair | Strength | Citation |
|---|---|---|
| x402 in MCP | Normative, in x402's own spec set | `x402-foundation/x402` @ `28ddebb`, `specs/transports-v2/mcp.md`: servers MUST return `PaymentRequired` as an `isError: true` tool result in both `structuredContent` and `content[0].text`; the client sends the `PaymentPayload` in `_meta["x402/payment"]`; settlement returns in `_meta["x402/payment-response"]`. Guide: `docs/guides/mcp-server-with-x402.mdx`. |
| MCP to x402 | None | MCP 2026-07-28 `basic` and `basic/authorization`: no mention of x402 or payment. The x402 MCP transport does not mention MCP authorization, OAuth, EAA or CIMD. |

Implementations (vendor docs, not specs, so no join credit): Cloudflare Agents `withX402`/`paidTool` (charge) and `withX402Client` with an `onPaymentRequired` human-confirmation callback (pay); npm `x402-mcp` 0.1.1 (the Vercel blog post it links to; published by an individual maintainer, x402 0.5.3, a v1 dependency); AWS AgentCore Payments (GA) manages the 402 flow with a Coinbase or Stripe/Privy wallet, per-`PaymentSession` budget (`maxSpendAmount`, expiry), and a Coinbase Bazaar MCP server behind AgentCore Gateway. The budget and the confirmation callback are vendor controls outside the x402 and MCP specs.

What the join carries: only x402 artefacts. MCP's own artefacts (OAuth token, EAA identity, CIMD client metadata) ride the same HTTP request but no join ties them to the payment. The signed EIP-3009 authorisation does not cover the tool arguments, only `resource.url` (`mcp://tool/<name>`).

### Rows
| Rubric | Basis | L1 | L2 | L3 | L4 | L5 | L6 | L7 | L8 | L9 | L10 | Chain | Total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Purchase | today (anchor x402) | 0 | 1 | 0 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 0 | 8 |
| Purchase | if joined | 1 | 1 | 0 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 0 | 9 |
| General | today (MCP; payment carries nothing, H) | 1 | 1 | 0 | 1 | 1 | 1 | 0 | 1 | 1 | 0 | 0 | 7 |
| General | if joined | 1 | 1 | 0 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 0 | 9 |

- If joined, purchase: MCP's L1 (EAA identity) reaches the payment. Extension point: the x402 `extensions` object in `PaymentPayload`, or an `x402/…` key in MCP `_meta`, carrying a hash of the MCP access token's `sub`/`client_id`. L3 stays 0: x402's agent key directory is self-published and MCP's CIMD is not an accountable-party statement.
- If joined, general: x402's signed receipt (offer-and-receipt extension, L7 1) and its L10 would have to be carried in `_meta["x402/payment-response"]`; the current transport defines only the unsigned `SettlementResponse`.
- Sensitivity: if MCP's native artefacts are credited because MCP is the host, the purchase "today" row becomes the if-joined row (total 9, chain 0). The chain does not change.

### Gaps
- Most important missing join: principal and agent continuity. The payer is a wallet address; the caller is an OAuth client. Nothing says they are the same actor.
- No member covers L3 (agent key binding by an accountable party) in either rubric.

---

## 2. MCP + A2A

### Documented joins
| Pair | Strength | Citation |
|---|---|---|
| A2A to MCP | Informative only | A2A spec Appendix B "Relationship to MCP": the A2A server agent "might use MCP" for tools; guide `topics/a2a-and-mcp`. No MUST or SHOULD, no field, no header, no extension. |
| MCP to A2A | None | MCP 2026-07-28 `basic` and `basic/authorization`: no mention of A2A. |

No payments are involved, so purchase is scored for completeness; every payment-specific cell is as the members score it.

### Rows
| Rubric | Basis | L1 | L2 | L3 | L4 | L5 | L6 | L7 | L8 | L9 | L10 | Chain | Total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Purchase | today (weaker hop per link) | 0 | 1 | 0 | 1 | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 5 |
| Purchase | if joined | 1 | 1 | 0 | 1 | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 6 |
| General | today | 0 | 1 | 0 | 1 | 1 | 1 | 0 | 1 | 1 | 0 | 0 | 6 |
| General | if joined | 1 | 1 | 0 | 1 | 1 | 1 | 0 | 1 | 1 | 0 | 0 | 7 |

- The members differ only at L1 (MCP 1 through the optional EAA extension, A2A 0). With no join, EAA identity stays on the tool hop and the A2A hop has none, so the end-to-end chain takes the A2A value.
- If joined: extension point is an A2A extension (AgentCard `capabilities.extensions`, message `metadata`) carrying the MCP access token's identity claims, or MCP `_meta` carrying the A2A `taskId`/`contextId`. That lifts L1 only. L7, L3 and L10 stay 0 because neither member has them.
- General classes: A2A covers F (delegate onward) as partial through generic skills; MCP does not. Both are partial on A to E.

### Gaps
- Most important missing join: delegation across the hop. A2A has no grant artefact and MCP's token is issued to the A2A server agent, not derived from the caller. Scope cannot narrow, and nothing says whose authority the tool call uses.
- No member covers L3 or L7 (no signed action record) in either rubric.

---

## 3. x402 + MPP + MCP

### Documented joins
| Pair | Strength | Citation |
|---|---|---|
| x402 in MCP | Normative | `specs/transports-v2/mcp.md` (stack 1). |
| MPP in MCP | Normative, but an individual draft | `tempoxyz/mpp-specs` @ `aeaeb83`, `specs/extensions/transports/draft-payment-transport-mcp-00.md`: challenge as JSON-RPC error `-32042` (MUST); credential and receipt in `_meta`; servers SHOULD advertise payment methods at `initialize`. |
| MPP and x402 | Informative and implementation only | MPP core `draft-httpauth-payment-01` does not mention x402. `draft-payment-discovery-01` lists x402 and x402scan as related discovery mechanisms (informative). `wevm/mppx` has `--protocol auto|mpp|x402` and an `examples/x402-mpp` example. Cloudflare MPP docs (updated 5 Aug 2026): "MPP is backwards-compatible with x402", with guides to charge for a Worker route or MCP tool and to pay from the Agents SDK. Vendor claim, not a spec join. |
| MCP to either | None | As in stack 1. The MPP MCP draft carries no MCP identity either. |

### Rows
| Rubric | Basis | L1 | L2 | L3 | L4 | L5 | L6 | L7 | L8 | L9 | L10 | Chain | Total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Purchase | today, best single path (MPP over MCP) | 1 | 0 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 0 | 9 |
| Purchase | today, x402 path | 0 | 1 | 0 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 0 | 8 |
| Purchase | today, floor of both paths | 0 | 0 | 0 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 0 | 7 |
| Purchase | if joined | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 10 |
| General | today (MCP; payment carries nothing, H) | 1 | 1 | 0 | 1 | 1 | 1 | 0 | 1 | 1 | 0 | 0 | 7 |
| General | if joined | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 10 |

- The JSON "today" for purchase is the best single path. Chain is 0 on every variant.
- If joined: extension point is the MPP MCP transport `_meta` credential (the MPP `source` field) or an x402 `extensions` entry, carrying the MCP caller's identity (CIMD `client_id` hash). That fills L2 on the MPP path and L1 on the x402 path. Caveat: this takes the best member per link across two protocols a single payment cannot use together, and the L1 and L3 credit for MPP rests on a payment key (Tempo access key or card/Stripe token), not the MCP agent's key. A strict reading gives chain 0 with L3 at 0 for MCP actions. The upper bound is therefore the most generous reading.
- MPP method-dependent cells: L8 rests on Tempo session dispute mapping and Lightning refund records, so it varies by payment method.

### Gaps
- Most important missing join: as in stack 1, the MCP caller to the payer. A second gap is that nothing says which of x402 or MPP governs a request that offers both.
- No member covers L2 on the MPP path or L1 on the x402 path without MCP, and none covers L3 for an MCP agent key.

---

## 4. UCP + AP2 over MCP/A2A (Google and Shopify)

### Documented joins
| Pair | Strength | Citation |
|---|---|---|
| UCP to AP2 | Normative (UCP extension) | UCP `v2026-08-25` AP2 Mandates extension (`dev.ucp.common.payment.ap2_mandate`): when active, the business MUST include `ap2.merchant_authorization` in all checkout responses and MUST NOT accept `complete_checkout` without `ap2.checkout_mandate`; the platform MUST verify the business signature before presenting. Platform provider flow MUST publish a key in profile `keys`. Also `docs/documentation/ucp-and-ap2.md`. |
| UCP to A2A | Normative, and the only binding that spells out AP2 | UCP checkout A2A binding "AP2 based Checkout Completion": merchant authorisation returned in a `DataPart` as `ap2.merchant_authorization`; payment mandate in `a2a.ucp.checkout.payment`; checkout mandate as `ap2.checkout_mandate`. Agent card endpoint listed in the UCP profile `services`. |
| UCP to MCP | Normative for UCP, by capability only for AP2 | UCP checkout MCP binding: profile in `meta` on every request (MUST), tools via `tools/call`. The AP2 extension is one of the capabilities the tools accept; no MCP-specific AP2 text. Authentication of agents (OAuth, mTLS or HTTP signatures) is SHOULD. |
| AP2 to A2A, MCP | Informative | AP2 v0.2.0 overview: "designed as an extension for emerging" A2A and MCP. AP2 defines no transport and leaves agent trust to "the Commerce Protocol layer" (`implementation_considerations.md`). |
| MCP, A2A to UCP identity | None | UCP does not require MCP's EAA or A2A's signed agent cards. |

MCP and A2A add no artefact to a UCP + AP2 request that UCP does not already score for, so the rows equal the reviewed AP2 + UCP rows.

### Rows
| Rubric | Basis | L1 | L2 | L3 | L4 | L5 | L6 | L7 | L8 | L9 | L10 | Chain | Total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Purchase | today | 1 | 1 | 1 | 1 | 1 | 2 | 1 | 1 | 1 | 1 | 1 | 11 |
| Purchase | if joined | 1 | 1 | 1 | 1 | 1 | 2 | 1 | 1 | 1 | 2 | 1 | 12 |
| General | today (AP2 payment-only, H; equals UCP) | 1 | 1 | 0 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 0 | 9 |
| General | if joined | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 2 | 1 | 11 |

- L3 today (purchase) is 1 because the AP2 mandate `cnf` travels in `ap2.checkout_mandate`. In general it is 0 because the AP2 mandate carrying it is payment-only.
- If joined, purchase L10 2: UCP needs a receipt carrier. Extension point: a field in UCP's AP2 Mandates extension or in UCP Order that returns the AP2 receipt, whose `reference` is the closed mandate hash. Today UCP Order refers to the checkout only by plain `checkout_id` and the AP2 extension text has no "receipt".
- If joined, general: AP2 needs a non-payment mandate type through its constraint-`type` extension point (unknown constraints fail verification, so both sides must implement it), carried by a new UCP capability. On a strict reading the general upper bound equals today (chain 0).

### Gaps
- Most important missing join: the AP2 receipt has no carrier in UCP (purchase L10), and for non-payment actions AP2 has no mandate type (general L3 and L10).
- No member covers L3 for the agent key outside the mandate `cnf`, or a signed liability allocation (R1) at L8 in the general rubric beyond UCP's typed adjustments.

---

## 5. PAP (Poppy) + Web Bot Auth, with UCP and MCP (Meta Muse, Shopify)

### Documented joins
| Pair | Strength | Citation |
|---|---|---|
| PAP to WBA | SHOULD | PAP 1.0 spec 5.3: a Personal Agent SHOULD sign requests carrying the Session header with Web Bot Auth; the signature MUST cover `poppy-session` and `authorization` when present. 1.1 draft extends it to the authorisation server endpoints. WBA draft-01 does not mention PAP. |
| PAP to UCP | Normative extension | PAP `ucp` extension v1: a `ucp` entry in `agent.protocols` plus `extensions.ucp`; Personal Agent sends the UCP platform profile (`UCP-Agent`) and, where a transport carries it in several places, the same URL in each (MUST); an operator signature SHOULD cover `poppy-session`, `authorization` and the UCP components; a company that lists a `ucp` entry MUST list the extension and its profile MUST offer `dev.ucp.common.ask`; a company MUST NOT require PAP for access UCP otherwise permits. |
| PAP to MCP | Normative | PAP 1.0 spec 7: `apis` type `mcp`, Streamable HTTP, MCP 2025-06-18 or later; every listed API MUST accept the Session header; the token `resource` MUST equal the MCP server `url`. |
| UCP to WBA | Opt-in profile | UCP Message Signatures spec, WBA opt-in list: once a signer opts in, it MUST send `Signature-Agent` beside `UCP-Agent`, set `keyid` to the JWK thumbprint and `tag="web-bot-auth"`. Opting in is optional. |
| UCP to MCP | Normative | UCP MCP binding (stack 4). |
| Not documented | | PAP carries no purchase grant. Approval is the Personal Agent's word (Operations 8.1, roadmap "Signed approvals"). No PAP text names AP2 or Verifiable Intent; AP2 issue-level proposal only (PAP #61, open). |

### Rows (documented today)
| Rubric | Basis | L1 | L2 | L3 | L4 | L5 | L6 | L7 | L8 | L9 | L10 | Chain | Total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Purchase | today (spec) | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 10 |
| Purchase | as deployed | 1 | 1 | 0 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 0 | 9 |
| General | today (spec) | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 10 |
| General | as deployed | 1 | 1 | 0 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 0 | 9 |

- Spec row equals the reviewed PAP + UCP + WBA row; MCP adds nothing above UCP at any link. L1 comes from UCP Identity Linking, L3 from the PAP delegated key on UCP requests, L7 and L8 from UCP (signed order webhooks, typed adjustments). General chain 1 rests on UCP L7; read order webhooks as purchase records under H and it is 0. MCP's L8 (cancellation) would still carry L8.
- "As deployed" is UCP alone (UCP over MCP) plus whatever WBA signing exists. PAP contributes no artefact on the wire because the live files do not meet 1.0 (below). No member scores 2 on any link.
- No "if joined" row: every join between these members is documented. The one missing join is to a signed approval format (AP2 or Verifiable Intent), which is not a member.

### Deployment evidence

**Shopify poppy.json (fetched 25 Nov 2026).** Probed `/.well-known/poppy.json` on 81 domains. 45 returned JSON, all Shopify-hosted storefronts (allbirds.com, kyliecosmetics.com, brooklinen.com, gymshark.com, fashionnova.com, rarebeauty.com, colourpop.com, glossier.com, everlane.com, harrys.com and 35 others); 36 returned 404, HTML or an error (some of those domains are mistyped or not Shopify). Raw data: `cmp4/poppy/survey.json`.
- All 45 are `protocol_version: "0.4"`. None are 1.0. PAP 3.4: before 1.0 two versions are compatible only on the same minor, so a 1.0 Personal Agent must not use a 0.4 document unless it also implements 0.4. The files were still 0.4 eleven days after Sierra's 13 Nov release post said every Shopify store "now automatically publishes a Poppy file" (spec 1.0 published 14 Nov).
- All 45 are identical apart from `organization` and the endpoint host: `agent.protocols` has one entry, `{type: "ucp", endpoint: "https://{domain}/.well-known/ucp"}` with no `description`; `extensions: {ucp: [{version: "1"}]}`; `auth.scopes` has one scope, `dev.ucp.shopping.checkout:manage`, with `scope_hints` `changes: irreversible`; `web: {}`.
- Surfaces listed: UCP only, 45 of 45. MCP 0, OpenAPI 0 (no `apis`), no `poppy` conversation entry, no `tasks`, no `web.browser_session_endpoint`, no `auth.issuer`, and `auth.issuer` is not needed because each domain has one authorisation server. MCP is reachable but only through the UCP profile: `/.well-known/ucp` (version `2026-08-25`) lists transports `mcp` (`/api/ucp/mcp`) and `embedded`, no `a2a`, no REST. `tools/list` on allbirds returned the UCP tools without credentials.
- The domain `oauth-protected-resource` lists the shop domain only (not the MCP endpoint) with the Shopify issuer; the issuer advertises `dev.ucp.shopping.checkout:manage`.
- Live UCP profiles (allbirds, kyliecosmetics, gymshark) have no top-level `keys` and no AP2 mandate capability. Payment handlers are `com.google.pay`, `dev.shopify.card`, `dev.shopify.shop_pay`. So in the Shopify deployment AP2 (stack 4) and signed UCP responses are not advertised.

**Muse and Web Bot Auth.**
- Only a secondary source says Muse signs: DataDome's VP of Threat Research, reported by PPC Land on 31 Oct 2026 (LinkedIn post of 30 Oct): Meta started signing some requests from Muse and Meta-WebIndexer around 12 Oct, unannounced, "a relatively small number" of requests, possibly first labelled `Meta-ExternalTest`. DataDome says it added validation. The Signature-Agent value was not reported.
- Primary: `https://www.meta.com/.well-known/http-message-signatures-directory` is live. It returns five Ed25519 JWKs (`kty: OKP`, no extra members) with content type `application/http-message-signatures-directory+json`, and the response itself carries five signatures (`tag="http-message-signatures-directory"`, one per key). It is on `www.meta.com`, not a Muse hostname, and nothing in it names Muse. `facebook.com` returned 404; `meta.ai` returned an HTML app, not a directory.
- Meta's crawler documentation as quoted on 31 Oct lists five agents (no Muse) and describes only IP-based verification. I could not fetch the Meta developer page now (client-rendered). No Meta or Sierra document I could fetch says Muse signs with Web Bot Auth.
- Cloudflare: the signed-agents docs say signed agents are Verified from 1 Jul 2026 and automated review validates signatures from 28 Aug 2026; the list is a dynamic directory I could not read, so Meta's presence is not confirmed or denied.
- Sierra's 13 Nov post says Muse "automatically looks for Poppy first on every site it visits". Nothing public shows Muse sending `Poppy-Session` or operator signatures on Poppy requests. The 5.3 operator signature is SHOULD.
- Key algorithms: Meta's directory keys are Ed25519, which WBA permits; PAP delegated Session keys must be ES256, so the operator key and Session key are separate keys, as PAP's guides require.

**Deployed versus PAP 1.0.** Deployed: discovery file that points to UCP; possibly signed Muse traffic of unknown scope. Specified in 1.0 and absent in the live files: 1.0 version, Company Agent conversations, `apis` (OpenAPI, MCP), Operations approvals (the `Poppy-Approval` field), Links and Disclosures extensions, tasks and feedback, browser join, and Session verification at the endpoints. The live Shopify MCP endpoint is UCP's, not a Poppy `mcp` API. The spec stack therefore describes where PAP + WBA + UCP + MCP can go, not what runs today. The evidence for UCP over MCP on Shopify is strong; the evidence for PAP and WBA doing anything on those requests is not.

### Gaps
- Most important missing join: a User-signed approval or mandate carried by PAP and checked by UCP at checkout. PAP's approval is "the Personal Agent's word", so the grant (L4), conformance (L6) and evidence (L7) links rest on the agent and the Company alone.
- No member covers L3 (an accountable party binding the agent key; PAP keys are self-published in `jwks_uri`, UCP profile keys likewise), and none scores 2 on any link. Under the general rubric nothing covers L7 outside UCP's order webhooks.

---

## Rule application notes

- A: pointers to other protocols earn nothing (x402 MCP transport to MCP auth; MPP discovery to x402; AP2 prose on A2A and MCP). Official extensions in a protocol's own set count (x402 MCP transport, MPP MCP draft, UCP AP2 extension, PAP UCP extension).
- B (L10): identifier matches count for C1 only. The L10 for the stacks takes the members' own cell; the only cross-boundary lift is stack 4's AP2 receipt, which has no carrier, so it is an upper bound.
- C, D: unchanged. E: self-published keys fail K1 for every key in these stacks.
- F, G: unchanged; classes for the stacks are the union of members' classes where a join carries them, otherwise the anchor's.
- H: payment mechanisms (x402, MPP, AP2 mandates, the x402 and MPP MCP transports) earn nothing at L4 to L8 in the general rows, so the general "today" rows for stacks 1 and 3 equal MCP, and stack 4 equals UCP.
- MPP's MCP transport is an individual -00 draft; it scores as in-spec (rule A) only for the MPP set it belongs to.
