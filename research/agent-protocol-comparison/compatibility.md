# Protocol compatibility

Which of the 14 protocols appear to fit together, pair by pair, as at 26 Nov 2026. Chart: [charts/compatibility-matrix.png](charts/compatibility-matrix.png). Data: [compatibility.json](compatibility.json). Per-protocol evidence, with a spec section or line for every claim: [compatibility-profiles.json](compatibility-profiles.json).

## What the matrix shows

The matrix is one triangle, so each pair appears once.

**Fill: is the pair seen together in the wild?** One scale, light to dark:
- **Live:** we found a generally available product that appears to run both in one flow. Each live cell was checked at the vendor's own page on 26 Nov 2026.
- **Announced:** announced, documented, preview or pilot; we could not confirm general availability.
- **Code only:** both appear in the same package manifest on GitHub (`evidence-code-cooccurrence.md`, 25 Nov 2026). This is unfiltered and noisy: one file is enough.
- **Not seen:** blank; none found in our search.

**Mark: what do the specs define?**
- **Overlapping circles with the overlap filled (joined):** at least one spec describes how the two combine. This includes core text, an extension, a transport binding, or a SHOULD or MAY.
- **One circle (mentioned):** one spec mentions, proposes or gives the other as an example, but defines no join.
- **No mark:** neither spec mentions the other.

A dark cell with overlapping circles is specified and seen in use. A pale cell with overlapping circles is specified, but we found no use yet.

**Also:**
- **≈** marks pairs that do the same job, so a product would usually choose one:
  - AP2 and Verifiable Intent (mandate formats);
  - ACP and UCP (checkout protocols);
  - x402 and MPP (HTTP 402 payment protocols);
  - Web Bot Auth and Visa TAP (RFC 9421 agent-signature profiles).
- **A numbered badge** points to a note in "Possible gaps and friction".

### Live pairs

These are the four pairs we found running together in a generally available product. There may be others we did not find:

| Pair | Where | Joined in a spec? | Source |
|---|---|---|---|
| UCP + MCP | Shopify Checkout MCP implements UCP checkout. Google's MCP transport is in beta; its live checkout uses REST | Yes (transport binding) | [shopify.dev](https://shopify.dev/docs/agents/carts-and-checkout), [Google UCP FAQ](https://developers.google.com/merchant/ucp/faq) |
| PAP + UCP | Poppy enabled for every Shopify merchant; every Shopify store supports UCP | Yes (PAP `ucp` extension) | [Sierra, 13 Nov 2026](https://sierra.ai/blog/releasing-poppy) |
| x402 + MCP | AWS Bedrock AgentCore payments (GA): Coinbase Bazaar MCP server of x402 endpoints | Yes (x402 MCP transport) | [AWS, 18 Aug 2026](https://aws.amazon.com/about-aws/whats-new/2026/08/bedrock-agentcore-payments-ga/) |
| x402 + MPP | AWS Bedrock AgentCore payments supports both | No (MPP mentions x402 only) | [AWS docs](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/payments.html) |

x402 + MPP is live yet marked as the same job: AWS offers the two side by side as alternatives, not as layers in one chain.

### Leads we could not confirm

The earlier vendor survey (`evidence-vendor-stacks.md`) suggested more live pairs. We could not confirm them on the vendors' own pages as at 26 Nov 2026:
- **UCP + AP2 (Google).** Google's live UCP checkout pays with Google Pay, not AP2. Google's UCP FAQ calls AP2 "useful for future scenarios".
- **AP2 anywhere.** I found no live AP2 product. AP2's FAQ says its samples mock payment providers, and its core spec work is moving to FIDO.
- **PAP + Web Bot Auth.** Sierra's Poppy launch post does not mention Web Bot Auth. A reported Cloudflare Radar entry for Muse could not be loaded.
- **ACP + MCP (OpenAI).** Embedded checkout is limited to select marketplaces. OpenAI moved Instant Checkout's focus to discovery in March 2026.
- **x402 + ERC-8004.** The only link is an open x402 proposal (issue #931). The Base contracts page has no ERC-8004 content.
- **KYA-OS + MCP.** The repository and a demo deployment exist. Vouched says it is not commercialising the technology, and no production use is confirmed.
- **Visa Intelligent Commerce Connect (TAP, MPP, ACP, UCP).** Visa says it is "currently in pilot with select partners".

The key-sharing test that an earlier version of the matrix showed is now in the next section.

## Signing keys by protocol

Can one key pair satisfy both specs? Almost always, if a spec with no algorithm restriction is read as allowing all of them. The friction is with KYA-OS:
- Its core uses Ed25519.
- The ES256-only specs are PAP's Session JWT, Verifiable Intent and UCP's required verifier support.
- So KYA-OS meets these specs only through optional profiles.

Payment wallet keys (secp256k1) meet those same ES256-only specs only through x402's optional HTTP-signatures extension or an ERC-1271 contract wallet. Sharing a key is not always wise: Web Bot Auth advises against reusing a key for different purposes.

| Protocol | Agent or payer key algorithms | How a verifier finds the key | Agent identifier |
|---|---|---|---|
| Web Bot Auth | Any IANA-registered RFC 9421 algorithm; none mandatory; HMAC forbidden | `Signature-Agent` URL to a JWK Set; RFC 7638 thumbprint `keyid` | `Signature-Agent` URL |
| Visa TAP | Not mandated; examples Ed25519, sample code also rsa-pss-sha256 | Visa-hosted key service by `keyid` | Visa-approved `keyid` |
| KYA-OS | Ed25519 in core; Entity Card per-request proof allows EdDSA or ES256 | `did:key`, `did:web`; CIMD `jwks_uri` projects only Ed25519 keys | DID |
| PAP 1.0 | Session JWT ES256 (MUST); client assertions and delegations ES256 or PS384 | CIMD `jwks_uri`; delegated key in `cnf.jwk` | `client_id` URL; pairwise user ID |
| x401 | None set; delegated to OpenID4VP and the DC API | Verifier `x5c` or resolvable `client_id` | Optional, no scheme |
| MCP | No agent signing key in core; `private_key_jwt` is a MAY | OAuth metadata; CIMD JWKS (optional) | OAuth `client_id` |
| A2A | Agent Card JWS, `alg` unrestricted | `jku` (MAY) or trusted key store | Agent Card URL |
| AP2 | Agent key is a `cnf` JWK, unrestricted (examples P-256); checkout JWT ECDSA, but contradicted elsewhere | `cnf` in the open mandate; issuer keys not specified | Not specified |
| Verifiable Intent | ES256 at every layer (MUST) | Issuer JWKS by `kid`; `cnf.jwk` | L2 `aud` |
| UCP | Verifiers MUST support ES256; ES384, EdDSA optional | `keys[]` in the `/.well-known/ucp` profile | Profile URL in `UCP-Agent` |
| ACP | Request signature algorithm agreed out-of-band; webhooks HMAC-SHA256 | Bilateral | Bearer credential |
| x402 | EIP-712 on EVM; Ed25519 on Solana and TON; optional RFC 9421 extension unrestricted | Payer address in payload | Payer wallet address |
| MPP | Per method: secp256k1 (EVM), secp256k1/P-256/WebAuthn (Tempo), Ed25519 (Solana, NEAR) | Payer `source` DID (RECOMMENDED); addresses | Not specified |
| ERC-8004 | EIP-712 from an Ethereum account, or ERC-1271 contract wallet | On-chain registry | Registry plus token ID |

## Possible gaps and friction

These are our reading of the spec text as at 26 Nov 2026. Specs are moving quickly, and implementations may already handle some of these.

1. **PAP and KYA-OS look unlikely to share the agent's delegated key as written.** PAP's Session JWT must be ES256 (PAP spec 5.2), while KYA-OS uses Ed25519 "for all cryptographic operations" in core (`SPEC.md` 4.2) and its `did:key` delegate is Ed25519. ES256 is allowed only for the Entity Card per-request proof (`SPEC-ENTITY-CARD.md` 8.4). An agent would probably need two keys, linked in a way neither spec currently describes.
2. **Visa TAP and Web Bot Auth are described as "aligned", but may not interoperate directly.** Both build on RFC 9421. A verifier following Web Bot Auth draft-01 5.2 is unlikely to accept a TAP signature as is:
   - TAP's tags are `agent-browser-auth` and `agent-payer-auth`, not `web-bot-auth`.
   - TAP sends no `Signature-Agent`.
   - TAP's keys come from Visa's key service, not a JWK Set URL.
   - TAP adds a nonce and an 8-minute window.
3. **UCP and AP2 appear to have seams.** They are linked by UCP's optional AP2 Mandates extension, but:
   - UCP signs a checkout object with a detached JWS, where AP2 expects a checkout JWT.
   - UCP has no obvious field for AP2's receipts.
   - AP2's `specification.md` excludes Ed25519 for the checkout, while its security section allows Ed25519 with a salt.
4. **A Web Bot Auth signature does not on its own show that the signer is PAP's `client_id`.** PAP spec 5.3 says operators SHOULD sign with Web Bot Auth, but the two key sources are separate and both self-published.
5. **UCP's Web Bot Auth example differs from draft-01.** UCP puts a `type` parameter on `Signature-Agent`, and draft-01 5.2.1 says a verifier MUST ignore a member that carries parameters. They should still interoperate where `Signature-Agent` points at a bare JWK Set URL, which UCP allows.
6. **KYA-OS and Web Bot Auth look technically compatible.** Both identify keys by the RFC 7638 thumbprint, and Web Bot Auth allows Ed25519. KYA-OS claims compatibility informatively (`SPEC-ENTITY-CARD.md` 8.5), but neither spec describes the join yet.
7. **x402 over MCP has no evident payer binding.** x402 describes an MCP transport, but we found nothing that ties the paying wallet to the MCP caller.
8. **Verifiable Intent and AP2 0.2 overlap.** Both cover much the same mandate layer, so in most designs they would be alternatives rather than layers.
9. **ERC-8004's link to x402 appears weak.** The only link we found is an optional `proofOfPayment` transaction hash in the off-chain feedback file, given as an example. The registry does not check it, and we found no mention of ERC-8004 in the x402 repository.
10. **PAP and AP2: proposed, not yet specified.** The join is proposed in open PAP issue #61. The keys look compatible: PAP's delegated key and AP2's `cnf` key are both P-256.
11. **Some UCP verifiers may not accept KYA-OS signatures.** UCP verifiers are only required to support ES256; EdDSA is optional (`signatures.md`). So a KYA-OS core Ed25519 signature may not be accepted by every conformant UCP verifier.

## Counts

Of the 91 pairs:
- 16 have a defined join.
  - Only one is a core MUST: KYA-OS is itself an MCP extension.
  - The rest are optional extensions, transport bindings, or SHOULD or MAY text.
- 18 more are mentioned without a join.
- 57 are not mentioned by either spec.

## Corrections to earlier notes

Checking the spec text for this matrix found four overstatements in the notes. These are now corrected:
- **PAP keys.** PAP does not require ES256 for every key. Only the Session JWT must be ES256 (README, stacks section).
- **KYA-OS keys.** KYA-OS is Ed25519 only in core. Its Entity Card proof also allows ES256.
- **Web Bot Auth algorithm.** Web Bot Auth sets no mandatory algorithm. Ed25519 is a deployment convention (`stacks-new-combinations.md`).
- **Visa TAP algorithms.** TAP mandates no algorithm. The earlier "Ed25519 or PS256" came from examples, and the sample code's RSA option is rsa-pss-sha256, not PS256 (`scores-group-3.md`).

## Not confirmed

These points are open:
- the algorithms Cloudflare's production Web Bot Auth verifier accepts;
- the curves for MPP's Stellar and XRPL methods;
- whether TAP requires a `Signature-Agent` component.

TAP has no versioned spec, so its row rests on Visa's developer page and sample code. The AP2 clone is v0.2 (29 Apr 2026).
