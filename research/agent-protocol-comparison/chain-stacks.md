# Stack joins for the chain rubric (L10 continuity and "best member" exceptions)

Scope: only the joins between protocols. Member-level L1-L9 scores are done elsewhere. Primary sources read on 2026-11-25 (raw files fetched from the repositories named; no repository edited). Local copies were kept and are not committed.

Short names for citations:
- UCP = `Universal-Commerce-Protocol/ucp` docs (v2026-08-25 text): `docs/specification/payment/extensions/ap2-mandates.md`, `docs/specification/signatures.md`, `docs/specification/overview/index.md`.
- AP2 = `google-agentic-commerce/AP2` v0.2: `docs/ap2/specification.md`, `agent_authorization.md`, `checkout_mandate.md`, `payment_mandate.md`.
- VI = `agent-intent/verifiable-intent` v0.1-draft (2026-02-18): `spec/README.md`, `spec/credential-format.md`, `protocol-landscape/protocols.md`, `protocol-landscape/glossary.md`.
- WBA = draft-ietf-webbotauth-httpsig-protocol-01 (October 2026).
- TAP = `visa/trusted-agent-protocol` README plus the Visa developer page `developer.visa.com/docs/trusted-agent-protocol/trusted-agent-protocol-specifications`.
- PAP = personalagentprotocol.org `/docs/1.0/spec.md`, `/docs/1.0/extensions/ucp.md`, `/docs/1.0/guides.md`.
- x402 = `x402-foundation/x402` `specs/`. ERC-8004 = eips.ethereum.org/EIPS/eip-8004.
- KYA = `decentralized-identity/kya-os-mcp` `SPEC.md`, `SPEC-ENTITY-CARD.md`, `SPEC-MCP-EXTENSION.md`. MCP = modelcontextprotocol.io 2026-07-28.
- ACP = `agentic-commerce-protocol/agentic-commerce-protocol` (release 2026-04-17): `rfcs/rfc.delegate_payment.md`, `rfc.payment_handlers.md`, `rfc.agentic_checkout.md`, `rfc.delegate_authentication.md`, `docs/mcp-binding.md`. Stripe = docs.stripe.com/agentic-commerce/concepts/shared-payment-tokens (vendor documentation, not an ACP spec).

## Summary table

| # | Stack | Documented? | Normative join (MUST/SHOULD) | Stack L10 |
|---|---|---|---|---|
| 1 | AP2 + Verifiable Intent + UCP | AP2+UCP yes (normative, UCP side). VI+AP2/UCP: informal only, stale, one-sided | UCP `ap2-mandates.md`: MUST on mandate placement and nested signature | 2 (user-credential path); 1 under Trusted Platform Provider path. VI adds nothing verifiable |
| 2 | Visa TAP + Web Bot Auth | Only as a bracketed "aligned with web-bot-auth" in TAP. Not defined as a join; TAP tags are not WBA-conformant | None | 1 (TAP's own nonce link; WBA adds none) |
| 3 | PAP 1.0 + UCP + WBA | Yes: PAP UCP extension; PAP spec 5.3 (SHOULD WBA); UCP signatures "WBA Interop" | PAP: MUST Session header on UCP requests; SHOULD operator signature; UCP: WBA opt-in MAY, "RECOMMENDED" for interop | 1 |
| 4 | x402 + ERC-8004 | One-sided, example-level: ERC-8004 only. x402 repo has zero mentions | ERC-8004: OPTIONAL fields and an example `proofOfPayment` | 1 (weak). 0 if example text is not a defined mechanism |
| 5 | KYA-OS + MCP | Yes, KYA side: `SPEC-MCP-EXTENSION.md` (extension `org.kya-os/decentralized-authority`, SEP-2133). MCP core does not reference KYA-OS | MUST inside KYA spec; extension itself optional and draft | 2 for tool-call chain (not a commerce chain) |
| 6 | ACP (2026-04-17) + SPT | ACP internal (delegate_payment, payment_handlers): yes. Stripe SPT: Stripe docs. Other protocols: only MCP binding (ACP side), and a one-sentence mention by TAP and VI | `allowance.checkout_session_id` is a plain string; `Signature` only RECOMMENDED | 1 (weak) |

## Stack 1: AP2 + Verifiable Intent + UCP

### Documented?
- AP2 and UCP: yes, normatively. UCP `ap2-mandates.md` ("AP2 Mandates Extension"), capability `dev.ucp.common.payment.ap2_mandate`, extends `dev.ucp.shopping.checkout`. AP2 `specification.md` Overview: "AP2 is designed explicitly to be compatible with UCP"; `checkout_mandate.md`: "when used with UCP this MUST be the Checkout object".
- VI with AP2/UCP: informal. VI `protocol-landscape/protocols.md` ("Universal Commerce Protocol (UCP)"): "VI credentials can be carried in those fields without changes to UCP's core endpoints" and "Detailed adoption architecture can be developed through coordination". `glossary.md` maps terms. Neither AP2 nor UCP mentions VI (grepped every UCP doc file and the AP2 docs; no hits for "Verifiable Intent"). The VI text is also stale: it is pinned to UCP 23 Jan 2026 and AP2 16 Sep 2025, and names the capability `dev.ucp.shopping.ap2_mandate` (current: `dev.ucp.common.payment.ap2_mandate`). AP2 v0.2 now defines its own SD-JWT mandates with the same `vct` strings (`mandate.checkout.open.1`, `mandate.payment.1`), `checkout_hash`, `transaction_id`, `sd_hash` and `cnf`, so VI and AP2 v0.2 are now overlapping formats for the same layer, not stacked layers. Wire compatibility between them is not stated anywhere.
- Nearest documented alternative for the card stack: AP2 v0.2 + UCP, with VI's L1 role played by AP2's "User Credential" model (OpenID4VP presentation, `agent_authorization.md` "User Credential").

### Joins
| Join | Artefact referencing artefact | Mechanism | Strength | Where |
|---|---|---|---|---|
| UCP checkout -> AP2 checkout mandate | Business signs checkout; checkout mandate contains the full checkout including the business signature | Detached JWS (RFC 7515 App. F) over JCS of checkout minus `ap2`; the SD-JWT+kb checkout mandate embeds the whole checkout, so the platform/user signature covers the business signature | MUST | UCP "Business Authorization", "Mandate Structure" ("nested cryptographic binding"), `ap2.merchant_authorization`, `ap2.checkout_mandate` |
| Payment mandate -> checkout | Payment mandate | `transaction_id` = hash of `checkout_jwt` (AP2); carried in `payment.instruments[*].credential.token` (UCP) | MUST (placement MUST; hash per AP2) | AP2 `specification.md` "Payment Mandate"; AP2 `payment_mandate.md`; UCP "Mandate Structure" |
| Closed mandate -> open mandate (autonomous) | Closed mandate | SD-JWT `sd_hash` / delegate chain with agent `cnf` key; `payment.reference` constraint `conditional_transaction_id` | MUST in AP2 | AP2 `specification.md` "Autonomous"; `payment_mandate.md` "Reference" |
| Open mandate -> user identity | Mandate | User signs via a presented User Credential (OpenID4VP `transaction_data` type `delegate`, `delegate_payload` inside the key binding) | MUST for that path | AP2 `agent_authorization.md` "Delegation using OpenID4VP"; UCP Step 2 "Option 2" |
| Business verification on `complete` | n/a | Business MUST reject without `ap2.checkout_mandate` (`mandate_required`), verify mandate, then verify its own `merchant_authorization` and that terms match session | MUST | UCP "Business Verification", "Activation and Session Locking" |
| Receipt -> mandate | Signed receipt | `reference` = hash of received mandate | MUST in AP2 | AP2 `agent_authorization.md` "Mandate Receipt". UCP's extension defines no carrier for receipts and UCP Order has no mandate reference |
| VI L1/L2/L3 -> AP2/UCP | VI mandates | `sd_hash` chain, `checkout_hash` = SHA-256 of `checkout_jwt`, "carried in" UCP fields | Informal; "can be developed" | VI `protocols.md`, `glossary.md`; VI `credential-format.md` 6.3 says `checkout_jwt` schema and verification are implementation-defined |
| UCP key -> AP2 key | Business/platform signing key | Platform Provider flow: key in profile `keys`; User Credential flow: key bound to the credential | MUST (a key must be resolvable) | UCP "Signing Key Requirements" |
| One key for AP2 and WBA | Platform signing key | Allowed only under AP2's "entropy" reading of the signature-algorithm rule (AP2 issue #268 open); ES256 baseline otherwise | Note only | UCP "Note (algorithm requirement)" |

### L10 score: 2 (user-credential path), 1 (trusted-platform path)
- C1 (same principal across identity, grant, action): holds when the user signs through a User Credential. The credential issuer, the open mandate (key binding over `delegate_payload`) and the closed mandates are all rooted in the user's key. Under UCP Step 2 "Option 1: Trusted Platform Provider" the platform signs with its server key and "the business trusts the platform's signature implies user consent", so the principal is not in any artefact.
- C2 (each artefact references the previous cryptographically): holds across the UCP/AP2 boundary. Checkout -> business signature -> checkout mandate (nested), payment mandate -> checkout hash, closed -> open via `sd_hash`, receipt -> mandate hash.
- Gaps that stop it being cleaner: receipt carriage in UCP is undefined; UCP's checkout object plus detached JWS versus AP2's `checkout_jwt` string is a representation seam (UCP says AP2 binds via `hash(checkout_jwt)`; AP2 says "MUST be the Checkout object"); AP2 itself is internally inconsistent on the signature-algorithm rule (UCP note, AP2 #268).
- VI does not change the score. Its own internal chain is C1/C2 = 2 (`spec/README.md` 3.2, 8.2-8.3) but its join to AP2/UCP is non-normative.

### Links where "best member" does not hold
- L1/L4 (principal, grant): AP2's strongest option (user-signed via credential) is only one of two; UCP lets the platform provider sign instead, which downgrades D3 to "partial" by the rubric. Also, UCP's own buyer identity (identity linking, OAuth account at the business, `UCP-Agent` profile) is not referenced by any mandate, so the merchant account holder is not cryptographically tied to the mandate signer.
- L4/L6 (session lock): AP2 mandates exist in UCP only if `ap2_mandate` is negotiated into the capability intersection (UCP "Activation and Session Locking"). A plain UCP checkout carries no principal-signed grant. A stack score taking AP2's L4/L6 assumes that capability is negotiated.
- L2/L3 (operator, agent key): AP2 says closed mandates are validated "using a User Credential or a trust list of Agent Providers" but defines no trust list. UCP `keys[]` in the profile are self-published. VI `agent_attestation` (VI 9.2) is ignored if unrecognised and no scheme is defined.
- L7 (evidence): AP2 receipts are best-in-class (E1, E3 via "Dispute Evidence"), but UCP has no field for them, so the best member's evidence is not on the UCP wire.
- Overlap, not stacking: VI and AP2 v0.2 define the same layer. Choose one mandate format; do not count both.

## Stack 2: Visa TAP + Web Bot Auth

### Documented?
Partly, and not as a join. TAP's Visa developer page says: "The Agent recognition signature is based on the HTTP Message Signatures defined by RCF 9421 [and aligned with web-bot-auth]" (bracketed, informative; "Agent Recognition Signature" section). TAP's `README.md` says only "RFC 9421". WBA draft-01 does not mention TAP. The only third spec that names both is x402 `specs/extensions/http-message-signatures.md`, whose example `tags` is `["web-bot-auth", "agent-browser-auth"]`. That is evidence that they are sibling tag values, not that one implements the other.

Mismatches that make "aligned" weaker than "conformant":
- WBA 5.2: `tag` MUST be `web-bot-auth`, and 5.2.1: a signed request MUST carry `Signature-Agent` (dictionary form, direct JWK Set URL). TAP's required fields use `tag="agent-browser-auth"` or `"agent-payer-auth"`, and the required field list has no `Signature-Agent`. A WBA verifier following 5.2 will not treat a TAP signature as WBA.
- TAP covers `@authority` and `@path`; keys are looked up by `keyid` at a Visa-hosted well-known "Public Keys Retrieval Service" ("Additional Information"). WBA resolves a `Signature-Agent` URL as a JWK Set (4.1, 4.4).
- Lifetimes: TAP rejects if `created`/`expires` are more than 8 minutes apart and requires nonce de-duplication; WBA recommends `expires` within 24 hours and does not require a nonce.
- WBA 6.5 says a key SHOULD NOT be reused for different purposes. TAP signs the HTTP signature, the consumer object and the payment container with the same key.

Nearest documented alternatives: for WBA with a payment-scheme signature on one request, UCP `signatures.md` "WBA Interop" (a dual-audience signature) and PAP 5.3 are the documented WBA joins (stacks 3). For TAP, the only documented partners are the three TAP signatures themselves.

### Joins
| Join | Mechanism | Strength | Where |
|---|---|---|---|
| HTTP signature -> consumer recognition object | Same `nonce` signed in both; object signed with the same private key as the HTTP signature; `kid` equals `keyid` | MUST for the object's minimum fields; verifier "may" still use object if verification fails | TAP "Consumer Recognition" |
| HTTP signature -> payment container | Same shared `nonce` and key. "As there may be instances where a payment is required but a message signature is not required, this step may be skipped" | Conditional | TAP "Payment" |
| Consumer object -> principal | Embedded Visa-signed `idToken` (JWT, `typ` `JWT+ext.id_token`) carrying hashed phone/email identifiers | Visa implementation; "at least five fields" | TAP "Agentic Consumer Recognition Object" and "ID Token" |
| HTTP signature -> body | Not covered (components `@authority`, `@path`). WBA also covers no body unless `Content-Digest` is added (5.2) | Gap | TAP required fields; WBA 5.2 |

### L10 score: 1
- C1: a pseudonymous, scheme-verified consumer identifier (`idToken`) and the payment credential share a nonce and key, but there is no grant artefact (TAP's README asks "Does the agent carry valid instructions from the user" but defines no user-signed instruction), so principal -> grant -> action cannot be shown.
- C2: partial. The link between the three TAP artefacts is a shared signed nonce plus same key, not a hash of the predecessor, and the HTTP signature does not cover the body objects. WBA adds no artefact and no link.

### Links where "best member" does not hold
- L3 (key binding): TAP's key store ties a key to a Visa-onboarded agent ("Agent Providers are certified AI platforms that have been onboarded as an Agent to Payment Schemes"). WBA 4.1/4.4 say the URL "says nothing about who operates the Agent". A WBA-only edge verifier gets self-published keys; only a verifier that does TAP's key lookup gets the accountable binding. The stack takes the TAP score for L3 only where the verifier is TAP-aware.
- L5 (replay): TAP requires a nonce and an 8-minute window; WBA does not. A WBA verifier will not enforce TAP's replay rules.
- L9 (trust anchor): TAP names a scheme key store; WBA has no registry. Different verifiers, different trust anchors.

## Stack 3: PAP 1.0 + UCP + Web Bot Auth

### Documented?
Yes, in three places.
- PAP `/docs/1.0/extensions/ucp.md` ("UCP extension" v1) is a full integration page: sections 2 (advertising: `poppy.json` `extensions.ucp`), 3 (discovery; UCP profile at `https://{organization.domain}/.well-known/ucp`, no redirects), 4 (identity and authorisation layering), 6 (commerce and approval), 8 (sessions and UCP resources).
- PAP spec 5.3 "Operator signatures": "A Personal Agent SHOULD also sign requests carrying the Session header with an HTTP Message Signature (RFC 9421), using Web Bot Auth"; the signature "MUST cover `poppy-session`, and `authorization` when present".
- UCP `signatures.md` "WBA Interop" (opt-in dual-audience signature, "RECOMMENDED path for integrators wanting interop with WBA-conformant verifiers"). PAP UCP extension section 4 cites it, and says one signature can serve both protocols when it covers `poppy-session`, `authorization`, the request target, `content-digest`, `content-type`, `ucp-agent`, `idempotency-key`.
- Not documented: PAP with AP2 mandates. The PAP UCP page says UCP's checkout approval is "the one approval for a purchase" and that a Company SHOULD NOT also return a PAP operation. AP2 is not mentioned (grepped PAP spec, UCP page, guides). Nearest documented alternative for a principal-signed purchase grant: UCP's AP2 Mandates extension (stack 1), which PAP's page does not forbid but does not describe.

### Joins
| Join | Mechanism | Strength | Where |
|---|---|---|---|
| `poppy.json` -> UCP profile | Same host; domain is the shared identifier; redirect from `/.well-known/ucp` MUST NOT be followed; profile from another host MUST NOT be used | MUST | PAP UCP 3 |
| Session header on UCP requests | `Poppy-Session` JWT (`sub` User ID, `sid`, `htm`/`htu`, `ath` = SHA-256 of access token) on every UCP request via this extension | MUST (spec 5.2 and UCP 4); a UCP endpoint may ignore it | PAP spec 5.2; UCP page 4, 8 |
| UCP platform profile advertisement | `UCP-Agent` profile URL on every request; where a transport carries it twice the URL MUST be identical and the Company MUST reject a mismatch | MUST | PAP UCP 4 |
| Operator signature over both | One RFC 9421 signature covering `poppy-session`, `authorization`, `content-digest`, `ucp-agent`, `idempotency-key`; if key is in profile `keys`, the signature identifies the same profile the request negotiates | SHOULD (PAP), opt-in MAY (UCP) | PAP spec 5.3; PAP UCP 4; UCP WBA Interop |
| WBA signature -> `client_id` | Not bound. "A verified operator signature establishes control of its key source. It does not establish every client metadata URL on the same origin. Verify the Session JWT's exact `iss`" | Explicit non-link | PAP guides "Operator signatures and bot defenses"; spec 5.3 |
| Account access | UCP identity linking and PAP Direct Sign-In are made one at the same issuer; token is Bearer for UCP | MUST (if both offered) | PAP UCP 4 "Signing in" |
| Approval | UCP checkout is the approval; PAP Operations not used for UCP actions | SHOULD NOT (Company) | PAP UCP 6 |

### L10 score: 1
- C1: the pairwise `sub` User ID and the access token's account appear in the Session JWT on every request; the access token is bound into the JWT by `ath`; with the operator signature the UCP request body is bound too (`content-digest`). These are per-request links. The User ID does not appear in the UCP checkout or the payment token, and PAP says a Personal Agent "MUST NOT assume that a cart or checkout it created through UCP appears on the Company's website ... unless the Company says so" (UCP page 8), grouping being a Company-side MAY.
- C2: there is no signed purchase grant and no persistent record chain. Session JWTs are minted per request and PAP's guides note the JWT "covers method, URL without query, and access token, not the request body".
- Principal identifiability is deliberately blocked: User IDs "MUST NOT contain or be derived from personal information" and are different per Company (PAP 5.1). That is right for privacy but means P1 cannot be met by this stack unless the Company's own account (OAuth sign-in) is counted, and nothing carries that identity to the payment party.

### Links where "best member" does not hold
- L1: UCP/AP2-style identifiable principals and PAP's pairwise anonymous User ID are in tension. A stack that adds AP2 for L4 must carry a user credential that PAP deliberately keeps out of the Company-facing session.
- L2/L3 (operator, key): the WBA operator key source (Signature-Agent URL) and PAP's `client_id` (CIMD, `jwks_uri`) are separate; the Company must decide they are the same client. Both are self-published. UCP `keys[]` are a third source. WBA draft-01 5.2.1 says "Dictionary members MUST NOT carry parameters. A verifier MUST ignore a member that carries parameters" and its changelog "Remove the directory, jwks_uri, and cimd types"; UCP's WBA example uses `Signature-Agent: sig1="https://platform.example/.well-known/ucp";type=jwks_uri` and cites draft-meunier-00. So UCP's documented WBA shape, which PAP cites, does not interoperate with a verifier following draft-01 unless `Signature-Agent` is pointed at a bare JWK Set URL (which UCP allows: "`Signature-Agent` MAY point elsewhere"). PAP's guides warn "current products do not all implement the same revision".
- L4/L6: PAP adds no grant. The best member for L4 is UCP's AP2 extension, which is not in the PAP page.
- L5 (S3 human presence): PAP defers to "a trusted interface, as UCP requires"; neither gives an assurance level.

## Stack 4: x402 + ERC-8004

### Documented?
One side only, and at example level.
- ERC-8004 Abstract/Motivation: "Payments are orthogonal to this protocol and not covered here. However, examples are provided showing how x402 payments can enrich feedback signals."
- ERC-8004 registration file: `"x402Support": false` (a boolean advertisement).
- ERC-8004 off-chain feedback file: `"proofOfPayment": { // this can be used for x402 proof of payment  "fromAddress", "toAddress", "chainId", "txHash" }` (the "ALL OPTIONAL FIELDS" block; the MUST fields are `agentRegistry`, `agentId`, `clientAddress`, `createdAt`, `value`, `valueDecimals`).
- ERC-8004 `agentWallet` (reserved metadata, set only by owner with an EIP-712/ERC-1271 signature) is "the address where the agent receives payments"; "When the feedback is given by an agent ... the agent SHOULD use the address set in the on-chain optional agentWallet metadata as the clientAddress".
- x402: no mention. I fetched every `.md`/`.mdx` under `docs/`, `specs/` and the package READMEs (177 files) and grepped "8004": zero hits. x402's `extension-offer-and-receipt.md` section 4.5.1 lists "External key registry (e.g., on-chain attestations ...)" as a signer-authorisation option without naming ERC-8004.
- AP2 pairs with x402 in its own samples (`code/samples/python/scenarios/a2a/human-not-present/x402/README.md`) and FAQ ("We will be aligning this closely with AP2 over time"). That is the nearest documented alternative for a grant plus x402 payment, though sample-level.

### Joins
| Join | Mechanism | Strength | Where |
|---|---|---|---|
| ERC-8004 feedback -> x402 payment | `proofOfPayment.txHash` (plus from/to/chainId) in the off-chain feedback file; file integrity by `feedbackHash` = keccak256 of the file at `feedbackURI` | OPTIONAL field, labelled example; registry does not verify it | ERC-8004 "Off-Chain Feedback File Structure"; `giveFeedback` |
| ERC-8004 agent -> paying wallet | `agentWallet` (proved by signature at set time) versus x402 `payTo`/`payer`; SHOULD use agentWallet as feedback `clientAddress` | SHOULD, and about the agent as feedback giver | ERC-8004 Identity Registry; Reputation Registry |
| x402 receipt -> chain | `transaction` is optional and omitted by default "to reduce correlation risk" | OPTIONAL | x402 offer-receipt 5.2 |
| x402 -> ERC-8004 | none | n/a | n/a |

### L10 score: 1 (weak)
- C1: no principal on either side (no human or organisation; ERC-8004 identifies an NFT owner and wallet, x402 identifies a payer address). The only shared identifier is a wallet address, and ERC-8004's `agentWallet` is a receiving address, so the paying wallet need not be the registered one.
- C2: the one cross-boundary reference is feedback -> payment by transaction hash, which is verifiable against the ledger independently but is an unvalidated claim in an off-chain file. Neither protocol has a grant artefact, so grant -> action cannot be shown. Score 1 only because a cross-protocol reference exists in a spec; 0 if the example block is not counted as a defined mechanism.

### Links where "best member" does not hold
- L1/L2: ERC-8004's `supportedTrust` is OPTIONAL ("If absent or empty, this ERC is used only for discovery, not for trust"); registries are permissionless, so there is no verifier accountable for the identity. x402 adds none.
- L3: x402's signing wallet and ERC-8004's registered agent key are not required to be the same key.
- L4/L6: neither defines delegation or a grant; x402's payload binds amount, `payTo` and resource, which is action-side only.
- L7: x402's signed receipt (E1) names the service key; its authorisation is "external key registry", which could be ERC-8004 but is not said to be. ERC-8004 feedback is ledger-timed (E2) but its off-chain file has no required signer beyond the submitting transaction.
- L9: ERC-8004 `getSummary` requires a non-empty `clientAddresses` filter because unfiltered results "are subject to Sybil/spam attacks", so reputation is only as trustworthy as the reviewer list the verifier brings.

## Stack 5: KYA-OS + MCP

### Documented?
Yes, from the KYA side. `SPEC-MCP-EXTENSION.md`: "KYA-OS MCP Extension Binding", extension id `org.kya-os/decentralized-authority`, declared in `capabilities.extensions` per MCP 2026-07-28 SEP-2133 (MCP changelog: "Add extensions field to ClientCapabilities and ServerCapabilities"). Status: Draft 1.0.0-draft; it is "an optional, strictly additive extension". It is not yet an MCP-registered extension ("authoritative on any conflict until an MCP extension repository adopts the binding", section 1.3 graduation is conditional). MCP core does not reference KYA-OS. "KYA-OS being an MCP profile" is therefore accurate only as "a draft MCP extension that KYA-OS defines". The `_kyaos_handshake` session profile is explicitly outside the extension (2.1).

### Joins
| Join | Mechanism | Strength | Where |
|---|---|---|---|
| Request -> proof | `_meta["org.kya-os/request-proof"]`; `requestHash` over `{method, params}` with `params._meta` removed; detached JWS over JCS of covered claims; EdDSA or ES256 | MUST (inside extension) | KYA-MCP 6; ENTITY-CARD 8.3, 8.4 |
| Proof -> delegation chain | Chain in `_meta["org.kya-os/delegation-chain"]` (outside `requestHash`), so proof MUST state the chain's last-credential digest in JWS protected header `org.kya-os/delegation` (`sha256:` hex or `none`); leaf delegate = verified `proof.did` | MUST | ENTITY-CARD 8.4, 10.2, 10.5; KYA-MCP 7.1 |
| Response -> request / chain | `org.kya-os/response-proof`, `responseHash`, optional `delegationChainDigest` | Body profile is the wire default; envelope profile SHOULD where verifiers support it | KYA-MCP 6; SPEC 7.3, 7.8 |
| MCP OAuth token -> KYA proof | AS SHOULD mint token with `cnf.jkt` (RFC 9449); if present then `token.cnf.jkt` = `proof.cnf.jkt` = thumbprint of the `kid` key MUST fuse; token `cnf` with no proof `cnf` fails closed (`cnf_required_by_token`); no token `cnf` degrades to "L3-minus" | SHOULD (AS side), MUST (when present) | ENTITY-CARD 7.5, 8.6 |
| MCP client identity -> DID | `_meta["org.kya-os/did"]` in a Client ID Metadata Document; CIMD is "the shared on-ramp" | Discovery | KYA-MCP 2.2, 13.1 |
| Consent step-up | Signed `needs_authorization` challenge; `responseHash` binds `authorizationUrl` | MUST verify before redirect | KYA-MCP 7.2; SPEC 9 |

### L10 score: 2 (for a tool-call chain; not a commerce chain)
- C1: principal -> delegation chain root -> leaf delegate = `proof.did` -> response proof binding the chain digest: one identifier thread, checked by recomputation.
- C2: proof -> chain (digest in protected header), proof -> request (`requestHash`), response -> request/chain, token -> proof (`cnf.jkt`, when the AS emits it). Cross-boundary to MCP is real: the MCP-layer OAuth token and the JSON-RPC request are both referenced.
- Caveats: the extension is optional and draft, and by the rubric's "optional extension = partial" rule a strict reading would give 1 for the MCP binding specifically (the core KYA-OS spec's own chain is MUST). Token fusion is conditional on the AS emitting `cnf.jkt`. Neither KYA-OS nor MCP defines a payment or commerce action (KYA-OS `payments.transfer` appears only as an example scope), so the "action record" is a tool call, and nothing here references money movement.

### Links where "best member" does not hold
- L5/L7 (coverage gap): `params._meta` is excluded from `requestHash`, and `_meta` carries MCP's own `io.modelcontextprotocol/protocolVersion` and `clientCapabilities`. Under the default body response profile, `resultType`, `isError` and `structuredContent` are "unauthenticated". MCP's own envelope is therefore only partly under KYA's proof unless the envelope profile is used (SHOULD).
- L4 (grant model): MCP core authorisation is user-level OAuth 2.1 with scopes; KYA delegation is VC chains. They compose through `cnf.jkt` only; an OAuth-only MCP deployment gets no D5 (sub-delegation) and the KYA delegation constraints are enforced only by a KYA verifier.
- L8 (redress): none in either; KYA-OS has no liability allocation or rulebook mapping, MCP none.
- L9 (trust anchor): KYA verifiers use a "trust-root policy" they configure (KYA-MCP 13.2), and revocation status lists are per issuer (7.1). MCP supplies no registry. Trust anchor is entirely verifier policy.
- Nearest documented alternative for a commerce chain over MCP: none that names KYA-OS. UCP, ACP and x402 each define MCP bindings (UCP MCP binding docs, ACP `docs/mcp-binding.md`, x402 `specs/transports-v2/mcp.md`) but none references KYA-OS.

## Stack 6: ACP (release 2026-04-17) on its own, with Stripe Shared Payment Tokens

### Documented?
- ACP's own parts: yes. `rfc.delegate_payment.md` (agent calls `POST /agentic_commerce/delegate_payment` with a credential and an Allowance; response is a token `id`), `rfc.payment_handlers.md` section 7.1/7.2 ("SPT (Shared Payment Token): ACP's standardized delegation token"; flow: "PSP creates vault token (SPT) with allowance constraints"), `rfc.agentic_checkout.md` (`payment_data.instrument.credential {type: "spt", token}` on `POST .../complete`), `rfc.delegate_authentication.md` (3DS2, `authentication_result` returned in `complete`), `docs/mcp-binding.md` (MCP transport binding; `Signature`, `Timestamp` map to `meta`; `Authorization` "handled via MCP server auth, not per-request").
- Other protocols named by ACP: MCP only (binding). `rfc.payment_handlers.md` 7.1/7.2 names "Agentic Tokens: MC/Visa tokens specifically designed for agentic commerce" as an underlying credential type, but defines no Visa TAP or Mastercard protocol join. ACP does not mention UCP, AP2, Web Bot Auth, x402 or VI.
- From the other side: TAP's developer page lists "protocols (e.g., MCP, ACP)" as channels (one sentence). VI `protocol-landscape/protocols.md` ("Agentic Commerce Protocol") says ACP's extension mechanism "provides a natural carrier" for VI and that "Detailed adoption design can be developed". Neither is a join definition.
- Stripe: SPT docs describe the grant ("The agent grants SPTs to your Stripe profile, each with usage and expiration limits"; `usage_limits` `currency`, `max_amount`, `expires_at`, `recurring_interval`; `agent_details`; revocation by the agent; `resolve` API returning `dpan`, `fpan` or `agentic_token` credentials with cryptogram; test path via `link-cli ... spend-request create ... --request-approval`). Stripe's documented `usage_limits` do not show `checkout_session_id` or `merchant_id`, which ACP's Allowance (3.5) requires; Stripe scopes the SPT to a seller `network_business_profile`. Whether the Stripe field set implements ACP's Allowance exactly is not established from these sources.

### Joins
| Join | Mechanism | Strength | Where |
|---|---|---|---|
| Credential -> SPT | PSP issues token for credential plus Allowance | MUST (endpoint is "single, MUST-implement") | ACP delegate_payment 2.3-2.5 |
| SPT -> checkout session | `allowance.checkout_session_id`, `merchant_id`, `max_amount`, `currency`, `expires_at`; token "MUST ONLY be usable within the provided Allowance"; allowance set in the agent's request | Plain identifiers; PSP-enforced | ACP delegate_payment 2.5, 3.5 |
| Checkout complete -> SPT | `payment_data.handler_id` plus embedded `credential.token` | MUST in schema | ACP agentic_checkout 4.4 and complete example; payment_handlers 7.1 |
| Request integrity | `Signature` over canonical JSON plus `Timestamp` | RECOMMENDED (checkout, delegate_payment); REQUIRED for delegate_authentication | ACP delegate_payment 2.3; agentic_checkout 3.1; delegate_authentication 3.1 |
| Cardholder authentication -> checkout | 3DS `authentication_result` in `complete` body when status is `authentication_required` | MUST include | ACP agentic_checkout 4.4 |
| Order events | Webhook `Merchant-Signature` HMAC with shared secret | MUST emit | ACP agentic_checkout 2.3; changelog 2026-04-17 |

### L10 score: 1 (weak)
- C1: the `buyer` object on checkout is agent-supplied; the SPT is bound to the customer's payment method in Stripe's system; the 3DS result is issuer-side. They share no principal identifier. Common reference is the `checkout_session_id` and `merchant_id` strings.
- C2: the action embeds the grant (SPT in `payment_data`) and the grant names the session by plain ID, not hash. Request `Signature` is RECOMMENDED and algorithm policy is "out-of-band". Webhook HMAC is symmetric. No artefact is signed by the principal.
- Score 1 only because token embedding and PSP enforcement of the allowance are real mechanisms; it is not a hash or signature chain.

### Links where "best member" does not hold
- L1/L4 (principal, grant): the principal's authorisation is a Stripe-side or agent-platform-side act (Stripe's `spend-request --request-approval`), not an artefact the merchant or an auditor can verify. VI's glossary notes that SPT constraints "are set by the agent, not the buyer" (VI secondary text; ACP 3.5 agrees the allowance is in the agent's request). D3 is partial at best.
- L3 (agent key): ACP leaves key binding to out-of-band policy; Stripe SPT carries `agent_details` (name, `network_business_profile`) as PSP-asserted metadata.
- L5 (S3 human presence): 3DS (delegate_authentication) gives issuer-grade cardholder authentication, which is better than anything else in the ACP/Stripe set, but nothing ties the 3DS result to the SPT or to the `allowance.checkout_session_id` other than the session. It evidences the cardholder, not the instruction.
- L6: A2 (counterparty verifies the action is within the grant) is performed by the PSP on amount, currency and expiry. The seller cannot check line items against the principal's grant because the grant does not contain them.
- L7: webhook HMAC with a shared secret is not E1; the PSP's own records are the evidence.
- L8: delegation to card rules is implicit (Visa/Mastercard brand fields); ACP maps no evidence to a dispute rulebook.
- Agentic tokens: if the SPT wraps a network agentic token with cryptogram (Stripe `resolve`), the network-level artefact is strong, but ACP does not describe how it relates to Visa TAP or Mastercard agent programmes.

## Notes on method and limits
- The ACP-only combination with Stripe SPTs relies on Stripe's vendor documentation for the SPT field set; the ACP text does not mention Stripe by name except as an example PSP value (`"psp": "stripe"`).
- TAP's normative text sits on the Visa developer page; the GitHub repository is a sample implementation (agent, registry, CDN proxy) and carries no spec text. Statements about TAP's tags and fields come from that page and the sample README (`tap-agent/README.md` shows the same `agent-browser-auth`/`agent-payer-auth` tags).
- PAP and UCP pages were read as published on 2026-11-25. WBA is an Internet-Draft; its 5.2/5.2.1 rules and changelog are quoted from -01.
- No stack above was tested against running implementations.
