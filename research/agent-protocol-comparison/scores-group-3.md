# Rubric scores, group 3 (read 25 Nov 2026)

Rubric: [rubric.md](rubric.md)

| Protocol | Identity | Authentication | Authorisation | Accountability |
|---|---|---|---|---|
| Visa TAP | 3.5 | 4 | 2 | 1 |
| x402 | 1 | 3 | 3.5 | 2.5 |
| MPP | 0.5 | 2 | 2 | 1.5 |
| ERC-8004 | 0.5 | 2.5 | 0 | 2.5 |

Scoring convention: extensions or method profiles that live in the same spec repository and are optional score 0.5. Unsure criteria are marked "(unsure)".

## 1. Visa Trusted Agent Protocol (TAP)

- Basis: **docs**. The GitHub repo (github.com/visa/trusted-agent-protocol, commit of 28 Oct 2025) holds only sample code and READMEs, with no normative spec. The normative content is the Visa Developer page "Trusted Agent Protocol: Merchant specifications" (https://developer.visa.com/docs/trusted-agent-protocol/trusted-agent-protocol-specifications). I read that page through a summarising fetch tool, not as raw text, so field names are second-hand. The repo README and sample READMEs were read directly.
- Version: no version number is published. The sample code uses RFC 9421.

| ID | Score | Justification |
|---|---|---|
| I1 | 1 | Consumer Recognition Object (`agenticConsumer`) carries `idToken`, an OIDC-style JWT with `iss`, `sub`, `aud`, and hashed or masked email and phone claims. |
| I2 | 1 | Agent Recognition Signature carries `keyid` and `tag`. The merchant maps the key to an issuer or agent onboarded to a payment scheme (Key Discovery section, "find the issuer via iss or keyid"). |
| I3 | 1 | Agents are described as "certified" and "Visa-approved" and are onboarded to payment schemes. The ID token is signed by an issuer (`iss`), not by the agent. |
| I4 | 0.5 (unsure) | The attestation is verifiable against the issuer's JWKS, but identities are obfuscated, so the merchant keeps its own mapping table. No legal-entity or KYC claim is in the artefact. |
| A1 | 1 | RFC 9421 `Signature` and `Signature-Input` headers. No algorithm is mandated: examples use Ed25519 and the sample code also supports rsa-pss-sha256. |
| A2 | 1 | Public Keys Retrieval Service, `GET /keys` by `keyID`, returning JWK fields (`kty`, `kid`, `alg`, `n`, `e`). The sample repo also has an agent-registry `/keys/{key_id}`. |
| A3 | 1 | `nonce` and `created`/`expires`, with a maximum 8-minute window. Merchants keep nonces for 8 minutes and block reuse. |
| A4 | 1 (unsure) | `idToken` has `auth_time` and `amr` claims. A shared `nonce` binds it to the header signature and the payment container. The docs do not say how the user authenticates. |
| Z1 | 0.5 | `tag="agent-payer-auth"` or `agent-browser-auth`, and the `agenticPaymentContainer`, show per-action authority. There is no mandate or delegation object. |
| Z2 | 0.5 | The signature is bound to `@authority` and `@path` and to the tag (browse or pay). No amount, payee or scope limits. |
| Z3 | 0.5 (unsure) | The ID token and payment container are signed by an issuer or wallet provider on the user's behalf, not by a user-held key. |
| Z4 | 0.5 (unsure) | Signature `expires` (at most 8 minutes) and ID token `exp`. These are per-message lifetimes, with no grant revocation or sub-delegation. |
| C1 | 0.5 | The signed objects (agent signature, `idToken`, payment container with `paymentCredentialsHash`) are tied together by one `nonce`. The merchant can keep them, but no receipt is defined. |
| C2 | 0.5 | The inputs are signed (JWS and RFC 9421) and tamper-evident. No signed output record exists. |
| C3 | 0 | The docs do not cover disputes. The README only says the protocol "reduces chargebacks". Redress is left to the card network. |
| C4 | 0 | No transparency log or status list. A key service exists, but the docs say no central registry of approved agents is specified. |

Totals: Identity 3.5, Authentication 4, Authorisation 2, Accountability 1.

## 2. x402

- Basis: **spec**. https://github.com/x402-foundation/x402, `specs/x402-specification-v2.md` (Protocol Version 2, repo HEAD of 25 Nov 2026).
- Extensions also read: `specs/extensions/http-message-signatures.md`, `sign-in-with-x.md`, `extension-auth-hints.md`, `extension-offer-and-receipt.md`.
- The identity working-group repo (x402-foundation/wg-identity) is not merged into the spec. The v2 spec and README contain no "identity" content. Not counted.

| ID | Score | Justification |
|---|---|---|
| I1 | 0.5 (unsure) | Core §5.2.2 `authorization.from` is the payer wallet address. It is a pseudonymous account, not a named principal. `sign-in-with-x` (CAIP-122) adds a wallet identity as an extension. |
| I2 | 0.5 | Extension `http-message-signatures` establishes "the cryptographic identity of the paying agent" and a `registrationUrl` to bind it to a billing identity. |
| I3 | 0 | No third-party attestation. `registrationUrl` is a network's own onboarding. The offer-receipt DID, DNS and registry options are for server signers only. |
| I4 | 0 | No legal-identity binding. |
| A1 | 1 | §5.2.2 and §10.1: EIP-712 `signature` over the EIP-3009 authorisation by the payer key. |
| A2 | 0.5 | In core, the key is recovered from the address, so no directory is needed. The `http-message-signatures` extension requires `/.well-known/http-message-signatures-directory`. |
| A3 | 1 | §10.1: 32-byte `nonce`, `validAfter`/`validBefore`, and contract-level nonce reuse prevention. |
| A4 | 0.5 (unsure) | `auth-hints` (OAuth 2.0 with DPoP, SIWX) and `sign-in-with-x` let the principal authenticate. The spec says authentication identity and payer identity are independent and not required to match. |
| Z1 | 1 | The signed EIP-3009 `authorization` (`from`, `to`, `value`, window) is an explicit grant for a specific transfer. |
| Z2 | 1 | Amount (`value`), payee (`to`), time window (`validAfter`/`validBefore`) and `maxTimeoutSeconds`. The `upto` scheme sets a maximum. |
| Z3 | 0.5 (unsure) | The payer's own key signs, verifiable without the facilitator. The spec does not distinguish a human principal's key from an agent-held wallet. |
| Z4 | 1 | `validBefore` expiry. The spec also defines `settlement_pending` and offer `validUntil`. |
| C1 | 1 (unsure) | Core `SettlementResponse` gives a `transaction` hash and `payer`. The signed payload names `resource` and `accepted`. The offer-receipt extension adds a receipt with `payer`, `resourceUrl`, `issuedAt`. |
| C2 | 1 | The payer-signed `PaymentPayload` is on-chain and tamper-evident. The extension adds signed offers and receipts (`format` eip712 or jws). |
| C3 | 0 | No dispute, refund or liability path. The offer-receipt text lists "dispute evidence" as a downstream use only. |
| C4 | 0.5 (unsure) | The public chain ledger and the receipt extension's optional attestation and transparency-log references. No protocol-defined registry or status list. |

Totals: Identity 1, Authentication 3, Authorisation 3.5, Accountability 2.5.

## 3. MPP (Machine Payments Protocol)

- Basis: **spec**. https://github.com/tempoxyz/mpp-specs at HEAD of 24 Nov 2026:
  - Core: `specs/core/draft-httpauth-payment-01.md` (`draft-ryan-httpauth-payment-01`).
  - Intents: `specs/intents/draft-payment-intent-subscription-00.md`.
  - Methods: `specs/methods/stripe/draft-stripe-charge-00.md`, `methods/card/draft-card-charge-00.md`, `methods/tempo/draft-tempo-subscription-00.md` and `draft-tempo-session-00.md`.
  - Extension: `specs/extensions/draft-payment-discovery-01.md`.
- The IETF datatracker page showed `-01` with the same content as the repo. The repo was used as the primary text.
- Method specs are separate drafts in the same repo, so method-defined features score 0.5.

| ID | Score | Justification |
|---|---|---|
| I1 | 0.5 | Credential field `source` ("Payer identifier", DID recommended) is optional. The core spec says the scheme "does not identify the client, the payer's principal, or any other party" (§Interaction with Other Authentication Schemes). |
| I2 | 0 | Same section: no operator identification. Other authentication is left unspecified. |
| I3 | 0 | No attested identity. The Stripe SPT and card network token are payment instruments, not identity attestations. |
| I4 | 0 | None. The discovery draft treats ERC-8004 as "operates entirely off-chain", with future anchoring only. |
| A1 | 0.5 | Core: `payload` is "method-specific payment proof". Proof of key possession is defined in methods (Tempo `keyAuthorization`, session EIP-712 vouchers). |
| A2 | 0.5 | `source` as a DID (`did:key`, `did:pkh`). Tempo subscription §Source Verification recovers the root signer. Method-level only. |
| A3 | 1 | Core: challenge `id`, HMAC-SHA256 binding, `expires`, `digest`, and §Replay Protection ("MUST provide single-use proof semantics"). |
| A4 | 0 | Core delegates principal authentication to "other authentication", which it "does not define". |
| Z1 | 0.5 | Method-defined grants: Tempo subscription `keyAuthorization` (TIP-1011 access key), the Stripe SPT, and the session channel with vouchers. |
| Z2 | 0.5 | The Stripe SPT has `usage_limits` (`max_amount`, `expires_at`). Tempo has per-period spend limits and recipient-scoped keys. |
| Z3 | 0.5 | The Tempo `keyAuthorization` is signed by the account's root key and verified by the server (§Source Verification, §Authorization Scope Verification). The Stripe SPT is platform-issued. |
| Z4 | 0.5 | Core has only a challenge `expires`. Tempo has `subscriptionExpires` and user revocation (§Revocation). |
| C1 | 0.5 (unsure) | Core `Payment-Receipt` (`status`, `method`, `timestamp`, `reference`) is returned only by "SHOULD". It does not carry the grant or identity. |
| C2 | 0.5 (unsure) | The receipt is unsigned base64url JSON. Method artefacts (on-chain `reference`, signed credentials) are tamper-evident. |
| C3 | 0 | The card method says reversibility "is subject to card network chargeback rules". That is delegated. |
| C4 | 0.5 (unsure) | The on-chain `reference` in chain methods is publicly checkable. Core defines no registry or log. |

Totals: Identity 0.5, Authentication 2, Authorisation 2, Accountability 1.5.

## 4. ERC-8004 Trustless Agents

- Basis: **spec**. https://eips.ethereum.org/EIPS/eip-8004, status Draft, created 2025-08-13. Sections used: Identity Registry, Reputation Registry, Validation Registry, Security Considerations.
- The EIP states "Payments are orthogonal to this protocol and not covered here".

| ID | Score | Justification |
|---|---|---|
| I1 | 0 | The identity is the agent (`agentId`). No principal or user artefact. |
| I2 | 0.5 (unsure) | The ERC-721 owner of the agent is on-chain. The registration file lists `services` (A2A, ENS, DID, email). Endpoint-domain verification via `/.well-known/agent-registration.json` is optional. The owner is only an address. |
| I3 | 0 | Self-asserted registration. Validation attests work output, not identity. §Security Considerations says it "cannot cryptographically guarantee" capabilities. |
| I4 | 0 | No legal-entity binding. |
| A1 | 1 | `setAgentWallet` needs an EIP-712 or ERC-1271 signature from the new wallet. Registry calls come from the owner or operator. |
| A2 | 1 | The on-chain Identity Registry resolves `agentURI`, `agentWallet` and `getMetadata`. The `/.well-known/agent-registration.json` check is optional. |
| A3 | 0.5 | The `deadline` in `setAgentWallet` only. No per-request freshness for interactions. |
| A4 | 0 | No principal authentication. |
| Z1 | 0 | No grant or delegation object. Owner and operator delegation is ERC-721 approval only. |
| Z2 | 0 | None. |
| Z3 | 0 | None. |
| Z4 | 0 | None. |
| C1 | 0.5 | `giveFeedback` ties feedback to `agentId` and `clientAddress`. Linking to an action needs the optional `endpoint`, `proofOfPayment` (`txHash`) and a2a `taskId`. |
| C2 | 1 | On-chain `NewFeedback` and `ValidationResponse` events, plus `feedbackHash`. §Security Considerations: "pointers and hashes cannot be deleted". |
| C3 | 0 | `appendResponse` can show "a refund", but no dispute or liability path is defined. Slashing is "outside the scope of this registry". |
| C4 | 1 | Public Reputation and Validation Registries with read functions. This is the protocol's purpose. |

Totals: Identity 0.5, Authentication 2.5, Authorisation 0, Accountability 2.5.

## Cross-cutting uncertainties

- TAP: the main risk is that Visa's docs were read through a summariser, so field names such as `agenticConsumer` and `IdToken` casing may differ in the original. Also uncertain: A4, Z3, Z4.
- x402: whether core payer wallet signing counts as principal-grade (I1, Z3), and whether on-chain settlement counts as C1 and C4 or only the optional receipt extension does. Counting only the extension would drop C1 and C4 by 0.5 each.
- MPP: how much weight method-level specs carry. Treating them as part of core would raise Authorisation to about 3.5 and Authentication to about 3.
