# Chain rubric scores, group 3 (read 25 Nov 2026)

Rubric: [chain-rubric.md](chain-rubric.md) (10 links, 2 / 1 / 0; chain score is the minimum). Scored afresh from primary text. The earlier file `scores-group-3.md` was used only to locate sources.

## Sources and how they were read

| Protocol | Source | Read how |
|---|---|---|
| Visa TAP | `https://developer.visa.com/docs/trusted-agent-protocol/trusted-agent-protocol-specifications` (HTTP 200, 710 KB, server-rendered HTML) | Raw fetch with curl, converted to text with a local script. Field names below are quoted from that raw text. This is no longer second-hand. |
| Visa TAP | `https://developer.visa.com/docs/trusted-agent-protocol` (getting started, raw) and `https://developer.visa.com/capabilities/visa-intelligent-commerce` (VIC overview, raw, HTTP 200) | Raw. The VIC page is an overview only. The purchase-instruction and passkey API reference pages were not fetched. |
| Visa TAP | `github.com/visa/trusted-agent-protocol` (commit of 28 Oct 2025) | Cloned. Only sample code and READMEs; no normative text. |
| x402 | `x402-foundation/x402` at 866e399 (25 Nov 2026): `specs/x402-specification-v2.md`, `specs/extensions/*`, `specs/schemes/{exact,upto,auth-capture,batch-settlement}` | Cloned, read raw. wg-identity not counted. |
| MPP | `tempoxyz/mpp-specs` at aeaeb83 (24 Nov 2026): `specs/core/draft-httpauth-payment-01.md`, `specs/methods/{tempo,stripe,card}/*`, `specs/extensions/draft-payment-discovery-01.md` | Cloned, read raw. Method-only features scored as partial. |
| ERC-8004 | `eips.ethereum.org/EIPS/eip-8004` (status Draft, created 2025-08-13); text read from `ethereum/ERCs` `ERCS/erc-8004.md` | Raw. |

Corrections to the earlier pass found by reading the Visa text raw:
- The `agenticConsumer` and `agenticPaymentContainer` objects are signed "with the same private key used to sign the message signature" (Consumer Recognition, Payment sections), so by the agent's key. Only `idToken` is signed by Visa ("The Visa implementation of the ID Token is digitally signed by Visa", ID Token section). The earlier note that the payment container is signed by an issuer or wallet provider was wrong.
- The page spells the field `idToken` in the field table and `"IdToken"` in the JSON example. It is inconsistent within the page.
- The `/keys` JWK table lists only `kty, kid, use, alg, n, e`. It has no field naming the key's owner.
- The page says the ID token is "an attestation that a Consumer has been identified by the respective Payment Scheme" and that "no identities are provided in the clear" (hashed or obfuscated phone and email, with a merchant-side mapping table).

---

## 1. Visa Trusted Agent Protocol (with VIC overview for context)

| Link | Score | Tests met / not met | Citation |
|---|---|---|---|
| L1 Principal identity | 1 | P1 partial: the merchant can recognise a consumer only by matching hashed or obfuscated `email` / `phone_number` to its own account mapping table; no party is named as able to resolve `sub` on request. P2 met: Visa-signed ID token attesting the consumer "has been identified by the respective Payment Scheme"; `email_verified` / `phone_number_verified` set by the OP. P3 partial: `iss` and `kid` name the signer and the key sits in the Visa Key Store, but no trust-framework listing is defined beyond Visa itself. | TAP spec, "Consumer Recognition" (`agenticConsumer`: `nonce`, `idToken`, `contextualData`, `kid`, `alg`, `signature`); "ID Token" (Token Claims: `iss`, `sub`, `aud`, `exp`, `iat`, `email`, `email_verified`, `phone_number`, `phone_number_mask`). |
| L2 Operator identity | 1 | O1 partial: the agent is identified only by `keyid` plus the statement that Agent Providers are "certified AI platforms that have been onboarded as an 'Agent' to Payment Schemes"; the JWK carries no operator name. O2 met by onboarding and certification by the scheme (stated, process not specified). O3 met in that the scheme is named and accountable. The artefact itself does not name the operator. | TAP spec, "Participants" (Agent Providers), "Agent Recognition Signature" ("proves the Agent's participation in the Payment Scheme specific program"); "Public Key Retrieval" JWK table. VIC overview, Prerequisites (VARS registration). |
| L3 Agent key binding | 1 | K1 met: the key is served from the scheme's Key Store ("retrieved from a trusted Key Store"), not self-published. K2 not met: the spec says only "if ... the public key has expired, the message should be blocked". No rotation, revocation or as-at-time lookup is defined. The sample agent-registry README mentions multiple keys per agent for rotation, but that is sample code. | TAP spec, "Verification Steps" ("Locate the public key"), "Public Keys Retrieval Service". |
| L4 Delegation | 1 (unsure) | TAP itself has no grant artefact: D1 to D4 not met. The only grant-like text is outside TAP: the VIC overview names "consumer-approved purchase instructions" and passkey "consumer consent to a purchase instruction" and an `encryptedInstruction` payload. Field names for amount, payee, window and expiry were not read. D5 none. | TAP spec: none. VIC overview: intro paragraph; "Passkeys enrollment and device binding"; Prerequisites (`encryptedInstruction`). |
| L5 Session authentication | 1 | S1 met: RFC 9421 `Signature` / `Signature-Input`, `keyid`, `alg`. S2 met: `created`, `expires` (not more than 8 minutes apart), `nonce` (recorded for 8 minutes). S3 only optional: `auth_time` (0..1) and `amr` (0..n) in the ID token; no assurance level is required. Passkey consent sits in VIC, not in TAP. | TAP spec, "Required Message Signature Fields", "Verification Steps" (Timestamps, Nonce); ID Token claims `auth_time`, `amr`. |
| L6 Action conformance | 0 (unsure) | A1 not met: there is no grant for the action to reference. The only linkage is the shared `nonce` / `kid`. A2 not met: the signature covers `@authority` and `@path` and the `tag` (`agent-browser-auth` / `agent-payer-auth`); no amount or scope check exists. The `browsingIOU` is checked against the merchant's own 402 data, not against a grant. The VIC endpoint name `credentials-for-instruction` hints at instruction linkage, but its fields were not read. | TAP spec, "Browsing IOU" (`invoiceId`, `amount`, `cardAcceptorId`, `acquirerId`, `uri`, `sequenceCounter`, `paymentService`, `kid`, `alg`, `signature`). VIC overview, example endpoint. |
| L7 Evidence | 1 | E1 partial: the agent-signed request, `agenticPaymentContainer` and `browsingIOU` are records signed by a scheme-onboarded party. No receipt is defined. E2 not met: `created` / `expires` are self-asserted by the agent. E3 not met: no retention or as-at-time key status; nonces are kept for 8 minutes only. | TAP spec, "Payment" (`agenticPaymentContainer`: `nonce`, `kid`, `alg`, `signature`, `paymentCredentialsHash`), "Browsing IOU", "Verification Steps". |
| L8 Redress | 0 | R1 not met: no liability allocation. R2 not met: no dispute path or evidence mapping. The repo README says only "minimize chargebacks from unauthorized transactions" (benefit statement, not a path). | TAP spec: no text. Repo `README.md`, "Reduce Fraud". |
| L9 Trust anchor | 1 | T1 met in part: the "Key Store", scheme onboarding and "Visa Intelligent Commerce program requirements"; VIC adds the Visa Agent Registry Service, used so "Visa can validate your agent signatures ... at the time of credential retrieval". No list format or lookup is defined for the merchant. T2 not met: expiry only; no revocation or status mechanism. | TAP spec, "Participants" (Key Store), "Agent Recognition Signature". VIC overview, Prerequisites. |
| L10 Continuity | 1 | C1 partial: the agent `keyid`, `kid` and `nonce` are shared across the header signature, `agenticConsumer` and `agenticPaymentContainer`; the principal appears only via `idToken` `sub`, with no grant. C2 partial: the objects are tied by the same `nonce` and key, not by hash of a predecessor; `idToken` carries no nonce of its own. | TAP spec, "Consumer Recognition" and "Payment" (each says the object is signed with the same key and one signed field is the same nonce as the message signature). |

D5 (sub-delegation): not addressed.
Chain score (minimum): **0** (L6 and L8 are 0). Total: **8 / 20**.

| Amended | Score | Reason | Citation |
|---|---|---|---|
| I1' Principal identifiable | 0.5 | Verified (by the scheme) but obfuscated identifiers; the merchant can match them only to accounts it already holds. No named party is stated as able to resolve `sub` on request. | ID Token, Token Claims; "Processing of Identity Data" (mapping table). |
| I2' Operator identifiable | 0.5 | Visa-approved agent attested by key membership of the scheme Key Store, but no operator name or legal entity in any artefact field. | "Participants"; `/keys` JWK table. |
| A2' Key accountable and checkable over time | 0.5 | Binding by a third party (scheme Key Store) met; validity as at time of use after the fact not defined. | "Verification Steps"; "Public Keys Retrieval Service". |

---

## 2. x402 v2 (core, with in-repo extensions and schemes; wg-identity not counted)

| Link | Score | Tests met / not met | Citation |
|---|---|---|---|
| L1 Principal identity | 1 (unsure) | P1 partial, extension only: the payer is a wallet address (pseudonymous; no named party is bound to resolve it). The `http-message-signatures` extension lets a network associate the signing agent "with a billing identity" via `registrationUrl`. P2 and P3 not met. | Core §5.2.2 (`authorization.from`), §5.3.2 (`payer`). `specs/extensions/http-message-signatures.md` ("Fields": `registrationUrl`). |
| L2 Operator identity | 1 | O1 partial: the agent hosts keys at `/.well-known/http-message-signatures-directory` and registers its signature-agent URL with the network (bare domain plus network registration). O2 and O3 not defined (the registration process is the network's own; the Cloudflare example only links to its docs). The offer-receipt signer authorisation (DID, DNS, registry) covers the server's identity only. | `http-message-signatures.md` ("Usage", "Example Networks"). |
| L3 Agent key binding | 1 | K1 partial, extension only: key published by the agent and registered with a network; core binds the key to the address by recovery only. K2 not met for the agent key (the offer-receipt text on as-at-`issuedAt` evaluation covers the server key and is SHOULD). | Core §10.1; `http-message-signatures.md` ("Usage"); `extension-offer-and-receipt.md` §4.5.1 and §5 (verification). |
| L4 Delegation | 1 (unsure) | D1 partial: the signed EIP-3009 `authorization` is a grant for one transfer, but it is the payer's authorisation to pay, not a principal-to-agent grant. D2 met: `value`, `to`, `validAfter` / `validBefore`; `upto` enforces a maximum ("Maximum Amount Enforcement"); `auth-capture` bounds the hold. D3 not distinguishable: the payer key signs, with no principal/agent separation. D4 met: `validBefore`, `captureDeadline`. D5 none. | Core §5.2.1 and §5.2.2 (`Authorization` fields); `schemes/upto/scheme_upto.md` §4; `schemes/auth-capture/scheme_auth_capture.md` ("Expiry enforcement"). Core §Document Scope: "Client-side budget management" is out of scope. |
| L5 Session authentication | 1 | S1 met: EIP-712 `signature` per payment; RFC 9421 per request in the extension. S2 met: 32-byte `nonce`, `validAfter` / `validBefore`, contract-level nonce reuse prevention. S3 not met: `extension-auth-hints` (OAuth with DPoP) and `sign-in-with-x` authenticate the client, not a human; core §10.2 treats authentication as separate from payer. | Core §10.1, §10.2; `extension-auth-hints.md`; `sign-in-with-x.md` (`nonce`, `issuedAt`, `expirationTime`). |
| L6 Action conformance | 1 (unsure) | A1 partial: `PaymentPayload.accepted` and `resource` echo the terms, and the settlement spends the signed authorisation. A2 met at payment level: facilitator `/verify` and the invariant that "at least one check ... MUST run before the resource executes". Conformance to an agent mandate or budget is not covered. | Core §5.2.1, §6.1 (Invariant), §7.1. |
| L7 Evidence | 1 | E1 partial: the on-chain settlement is signed by the payer key (an address, not an identified party); the optional offer-receipt is signed by a server key whose authorisation is verified by DID, DNS or registry. E2 met: ledger time; receipt `issuedAt` (server-signed). E3 partial: chain data persists; the extension says verifiers SHOULD preserve "temporally immutable authorization evidence". The receipt is optional (MAY), and `transaction` is optional. | `extension-offer-and-receipt.md` §5.1, §5.2 (`resourceUrl`, `payer`, `issuedAt`, `transaction`), §4.5.1; core §5.3.2. |
| L8 Redress | 1 | R1 not met in core. R2 met only in the optional `auth-capture` scheme: `void`, `refund`, `reclaim`, `refundDeadline`, with refund liquidity coming from the named operator ("Refund funding"). Core `exact` is non-reversible. No rulebook or evidence mapping. | `schemes/auth-capture/scheme_auth_capture.md` (operations table, "Relationship to `exact`"); `scheme_auth_capture_evm.md` (`refundDeadline`, `receiverAuthorizer`). |
| L9 Trust anchor | 1 (unsure) | T1 partial: offer-receipt names optional external key registries and DNS/DID for server keys; no list of trusted agents or issuers. Facilitators are "trusted third parties" with no listing. T2 partial: removal from a DID document or DNS is "prospective" status; no revocation list for the agent chain. | `extension-offer-and-receipt.md` §4.5.1; core §7. |
| L10 Continuity | 1 | C1 partial: the same `payer` appears in `authorization.from`, `SettlementResponse.payer` and the receipt; there is no identity credential. C2 partial: the receipt may carry `transaction` (optional), and the offer is signed by the server; the grant is bound to the action by the contract's nonce, not by a hash chain. | Core §5.2.2, §5.3.2; offer-receipt §5.2. |

D5 (sub-delegation): not addressed.
Chain score (minimum): **1**. Total: **10 / 20**.

| Amended | Score | Reason | Citation |
|---|---|---|---|
| I1' Principal identifiable | 0 | A wallet address; the "billing identity" in the extension concerns the signature agent, and no party is named as able to resolve on request. | Core §5.2.2; `http-message-signatures.md`. |
| I2' Operator identifiable | 0.5 | Domain-hosted key directory plus registration with a named network, but no attestation of who controls it. | `http-message-signatures.md` ("Usage"). |
| A2' Key accountable and checkable over time | 0.5 (unsure) | Registration with a network is a third-party binding (extension only, content unspecified). Validity at the time of use is not defined for the agent key; the on-chain authorisation window is checkable later but that is not key validity. | `http-message-signatures.md`; core §10.1. |

---

## 3. MPP (draft-httpauth-payment-01 plus method drafts; method-only features partial)

| Link | Score | Tests met / not met | Citation |
|---|---|---|---|
| L1 Principal identity | 1 (unsure) | Core not met: the scheme "does not identify the client, the payer's principal, or any other party". Method level partial: optional `source` (DID, self-asserted unless the method verifies it); Tempo recovers the root signer (a pseudonymous address); the card method uses issuer-provisioned network tokens and carries `cardholderFullName` in the encrypted payload (self-asserted by the client side). | Core, "Interaction with Other Authentication Schemes"; Credentials table (`source`); `methods/tempo/draft-tempo-subscription-00.md` "Source Verification"; `methods/card/draft-card-charge-00.md` (flow steps, payload). |
| L2 Operator identity | 1 | Core not met (same text). Partial through the card method's MAY: "The client may include Trusted Agent Protocol signature headers for additional identity assurance." Nothing is defined in MPP itself. | `methods/card/draft-card-charge-00.md`, Overview (VISA-TAP). |
| L3 Agent key binding | 1 | K1 partial, Tempo method only: the access key is bound to the account by a keyAuthorization signed by the root key; the root is a pseudonymous account, not an accountable party. K2 partial: the keyAuthorization carries an expiry and can be revoked on-chain through the AccountKeychain; on-chain state is checkable after the fact (not stated as a requirement). | `draft-tempo-subscription-00.md` "Key Authorization Payload", "Revocation", "Source Verification". |
| L4 Delegation | 1 | Core has no grant. Method level: Tempo `keyAuthorization` (D1; D2 amount per period, recipient, `allowed_calls`; D3 signed by the root key; D4 `subscriptionExpires` MUST, user revocation); the Stripe SPT (`usage_limits.max_amount`, `expires_at`, `seller_details.networkId`) is a platform-issued token (D3 partial). Method-only, so partial. D5: none. | `draft-tempo-subscription-00.md` "Request Fields", "Key Authorization Payload", "Revocation"; `methods/stripe/draft-stripe-charge-00.md` (SPT example). |
| L5 Session authentication | 1 | S1 partial: core `payload` is "Method-specific payment proof"; key possession is proven at method level. S2 met in core: challenge `id` with HMAC-SHA256 binding, `expires`, and "Payment methods ... MUST provide single-use proof semantics". S3 not met. | Core "Required Parameters", "Challenge Binding", "Replay Protection"; Credentials table. |
| L6 Action conformance | 1 | Core: the credential echoes the `challenge` object (HMAC-bound to the payment terms), a reference to the request but not to a grant. Method level: Tempo servers MUST verify the key scope (limit equals `amount`, recipient, `allowed_calls`, expiry) before settling. Method-only. | Core Credentials table (`challenge`); `draft-tempo-subscription-00.md` "Authorization Scope Verification". |
| L7 Evidence | 1 | E1 not met: `Payment-Receipt` (`status`, `method`, `timestamp`, `reference`) is unsigned JSON and only a SHOULD. E2 partial: the receipt `timestamp` is server-asserted; chain methods give ledger time. E3 partial: an on-chain `reference` persists; no retention text. | Core "Payment-Receipt Header"; `draft-tempo-subscription-00.md` "Receipt Generation". |
| L8 Redress | 1 | R1 not met. R2 partial: the card method says reversibility "is subject to card network chargeback rules"; no evidence mapping. | `methods/card/draft-card-charge-00.md` (fulfilment mechanism text). |
| L9 Trust anchor | 1 (unsure) | T1 not met for agents or issuers; the discovery draft refers to registries for services (MCP Registry, ERC-8004 "operates entirely off-chain"). Stripe uses Business Network Profiles for sellers. T2 partial: Tempo on-chain key revocation (method). | `extensions/draft-payment-discovery-01.md` "Registry and Aggregator Guidance", "ERC-8004"; `draft-tempo-subscription-00.md` "Revocation". |
| L10 Continuity | 1 | C1 partial: `source` in the credential (optional); the receipt does not carry it. C2 partial: the credential echoes the HMAC-bound challenge, and the receipt `reference` points to the settlement transaction; no hash chain from identity to grant to action. The core says "This specification does not define such a binding" for other authentication. | Core "Binding Other Authentication to a Challenge"; receipt table. |

D5 (sub-delegation): not addressed.
Chain score (minimum): **1**. Total: **10 / 20**.

| Amended | Score | Reason | Citation |
|---|---|---|---|
| I1' Principal identifiable | 0.5 | Core disclaims identification. Optional `source` DID is self-asserted; card-network tokens are resolvable by the issuer, but the spec does not say so. | Core "Interaction with Other Authentication Schemes"; Credentials table. |
| I2' Operator identifiable | 0.5 | Core disclaims it; only the card method's MAY pointer to TAP gives any route. | `draft-card-charge-00.md` Overview. |
| A2' Key accountable and checkable over time | 0.5 (unsure) | Tempo: expiry and on-chain revocation are checkable, and the root signs the key authorisation, but the root is a pseudonymous account and the feature is method-only. | `draft-tempo-subscription-00.md`. |

---

## 4. ERC-8004 Trustless Agents (Draft)

| Link | Score | Tests met / not met | Citation |
|---|---|---|---|
| L1 Principal identity | 0 | No principal artefact: the identity is the agent (`agentId`). The owner is an ERC-721 owner address. | Identity Registry (`agentRegistry`, `agentId`, `Registered(..., owner)`). |
| L2 Operator identity | 1 (unsure) | O1 partial: the ERC-721 owner address and optional `services` entries (`ENS`, `DID`, `email`) are self-declared; the optional "Endpoint Domain Verification" proves control of a domain, not who controls it. O2 and O3 not met. | Identity Registry, registration file `services`; "Endpoint Domain Verification (Optional)". |
| L3 Agent key binding | 1 | K1 partial: `setAgentWallet(agentId, newWallet, deadline, signature)` needs an EIP-712 or ERC-1271 signature from the new wallet, recorded by the registry (self-asserted by the owner; no accountable third party). K2 met: `MetadataSet`, `URIUpdated` events, `unsetAgentWallet`, and the clearing of `agentWallet` on transfer are ledger history. | Identity Registry, "On-chain metadata", "Update agentURI". |
| L4 Delegation | 0 | No grant artefact. Owner-to-operator delegation is ERC-721 approval for managing the registration only. D5 none. | Identity Registry (opening paragraph, "delegate management ... to operators"). |
| L5 Session authentication | 0 (unsure) | No per-request or per-session proof for agent interactions (left to A2A and MCP). `deadline` in `setAgentWallet` is registry-operation freshness only. | Abstract and Motivation (A2A "handles agent authentication"); `setAgentWallet`. |
| L6 Action conformance | 0 | No grant and no conformance check. | n/a |
| L7 Evidence | 1 (unsure) | E1 partial: `NewFeedback`, `ValidationRequest` and `ValidationResponse` events are signed by addresses (pseudonymous; validators are named by `validatorAddress`). E2 met: ledger time, `lastUpdate`. E3 met: "On-chain pointers and hashes cannot be deleted, ensuring audit trail integrity"; `feedbackHash`, `requestHash`, `responseHash` commit to off-chain files. The records are about feedback and validation, not the transaction itself, except where `proofOfPayment.txHash` is included (optional). | Reputation Registry (`giveFeedback`, off-chain file `proofOfPayment`); Validation Registry; Security Considerations. |
| L8 Redress | 0 | No dispute, refund or liability path. `appendResponse` may show "a refund"; slashing is "outside the scope of this registry". | "Appending Responses"; end of Validation Registry. |
| L9 Trust anchor | 1 | T1 partial: the registries are the trust substrate (`supportedTrust`: reputation, crypto-economic, tee-attestation) but nothing says which issuers or operators are trusted; "Sybil attacks are possible". T2 partial: `revokeFeedback`, `unsetAgentWallet` and the self-declared `active` flag; no status for identity credentials. | Registration file; "Revoking Feedback"; Security Considerations. |
| L10 Continuity | 1 (unsure) | C1: `agentId` (via `agentRegistry`) is the common identifier across registration, feedback and validation; there is no principal. C2 partial: `requestHash`, `responseHash` and `feedbackHash` hash-link off-chain evidence; `validationResponse` references the `requestHash`; `proofOfPayment` references a payment optionally. No grant. | Reputation and Validation Registry sections. |

D5 (sub-delegation): not addressed.
Chain score (minimum): **0** (L1, L4, L5, L6 and L8 are 0). Total: **5 / 20**.

| Amended | Score | Reason | Citation |
|---|---|---|---|
| I1' Principal identifiable | 0 | No principal in the spec. | n/a |
| I2' Operator identifiable | 0.5 (unsure) | Owner address plus optional domain control proof; no attestation of who. | "Endpoint Domain Verification (Optional)". |
| A2' Key accountable and checkable over time | 0.5 | Validity over time is checkable from registry events; the binding is by the owner's own signature, not an accountable party. | "On-chain metadata" (`setAgentWallet`). |

---

## Summary row

| Protocol | L1 to L10 | Chain | Total | I1' / I2' / A2' |
|---|---|---|---|---|
| Visa TAP | 1 1 1 1 1 0 1 0 1 1 | 0 | 8 | 0.5 / 0.5 / 0.5 |
| x402 v2 | 1 1 1 1 1 1 1 1 1 1 | 1 | 10 | 0 / 0.5 / 0.5 |
| MPP | 1 1 1 1 1 1 1 1 1 1 | 1 | 10 | 0.5 / 0.5 / 0.5 |
| ERC-8004 | 0 1 1 0 0 0 1 0 1 1 | 0 | 5 | 0 / 0.5 / 0.5 |

No protocol scores 2 on any link. Every 1 for x402 and MPP rests on an optional extension, scheme or method, so a different reading of "partial" would move these toward 0.

## Unsure cells

- Visa L4 (1 vs 0): the VIC overview names "consumer-approved purchase instructions" and passkey consent, but the purchase-instruction and passkey reference pages (amount, payee, window, expiry fields) were not fetched. TAP itself scores 0.
- Visa L6 (0 vs 1): the VIC endpoint `POST /vacp/v2/credentials-for-instruction` suggests the action references an instruction, but its fields were not read.
- Visa L5 (1 vs 2): passkey consent in VIC would meet S3 if counted as part of the same protocol; TAP alone has only optional `auth_time` and `amr`.
- Visa L2 (1 vs 2): onboarding and certification by the scheme is stated, but no field in any artefact names the operator.
- Visa I1', I2': 0.5 chosen; 1 is arguable if Visa's resolution of `sub` and `keyid` on request counts, although the spec does not say so.
- x402 L1, L4, L6, L9, A2': whether the payer wallet signature counts as a principal grant (L4), whether payment-level `/verify` counts as conformance (L6), and how much the `registrationUrl` extension and optional external registries carry (L1, L9, A2').
- MPP L1, L9, A2': how much weight the card and Tempo method drafts carry; the card method's MAY reference to TAP drives L2 and I2'.
- ERC-8004 L2, L5, L7, L10: the owner-address and optional domain proof for L2; whether registry-level `deadline` and caller signatures count as session authentication (L5); whether feedback and validation records count as evidence of the action (L7, L10).
