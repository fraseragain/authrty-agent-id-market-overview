# Scores G4: x401 and KYA-OS, plus eight untracked protocols

Rubric: [rubric.md](rubric.md). Read on 25 Nov 2026. Fetched sources were kept locally and are not committed.

# Task A

## x401 (HTTP Proof Requirement Protocol)

- Version: Standard Draft 0.2.0 (the spec header says `Status: Draft`, `Version: 0.2.0`). Editors are Daniel Buchner (Proof) and Bhushit Agarwal (Circle).
- Read: https://x401.proof.com/spec/latest/ and `spec.md` in https://github.com/proof/x401 (the source of the same text).
- Basis: `spec`.
- Orientation. x401 is a route-scoped proof-requirement protocol. A Verifier challenges with `PROOF-REQUEST`. The Agent returns a Digital Credentials result (OpenID4VP over the DC API, DCQL) in `PROOF-RESPONSE`. A Verification Token can optionally be issued by OAuth Token Exchange. Agent identification and delegation are explicitly optional or left as open questions (sections "Composable Agent and Entity Identification" and "Open Questions & Future Additions").

| ID | Score | Justification |
|---|---|---|
| I1 Principal conveyed | 0.5 | The Holder's credential result (Result Artifact `credential_result`) reaches the Verifier. Only the claims the DCQL query asks for are disclosed, so a subject identifier is conveyed only if the Verifier requests one (Terminology "Holder"; Request Members). UNSURE. |
| I2 Operator conveyed | 0.5 | `agent_id` (Agent Identifier) is optional in the Result Artifact. The spec registers no scheme and says the Verifier defines accepted schemes (Agent Binding Options). It identifies the calling agent, not an operator specifically. UNSURE. |
| I3 Third-party verified | 1 | Claims come from credentials issued by third parties. The Verifier enforces issuer trust through DCQL `trusted_authorities` (`openid_federation`, `etsi_tl`) (Issuer Trust; Verifier Processing Rules 7 and 10). |
| I4 Legal-person grade, checkable | 0.5 | The Verifier verifies the presentation cryptographically (Proof Validation 2 to 6). Whether the credential is tied to a verified natural or legal person depends on the credential the route requests, for example `assurance_level` in the Credential Requirements example. The spec does not mandate it. UNSURE. |
| A1 Proof of possession | 0.5 | The result's proof must be cryptographically valid under the credential and presentation format (Proof Validation 2). That is holder or credential binding, not agent binding. Agent key proof is only via optional layers: Web Bot Auth/HTTP Message Signatures, mTLS, DPoP, SPIFFE (Agent Binding Options). |
| A2 Verifiable key discovery | 0.5 | Issuer trust resolves through federation or trust list (`openid_federation`, `etsi_tl`) and signed requests use `client_id` such as `x509_san_dns`. Agent key discovery exists only in the optional Web Bot Auth `Signature-Agent` key directory. UNSURE. |
| A3 Freshness | 1 | The OpenID4VP `nonce` plus request `exp` are mandatory in the Verifier-composed request (Proof Validation 4; Security Considerations "Replay Prevention"). |
| A4 Principal authentication bound to agent | 0.5 | The Holder authorises the Credential Manager to present, but the result is bound to the Verifier, not the Agent. Agent binding is OPTIONAL (Security Considerations "Agent Binding"). |
| Z1 Explicit grant artefact | 0.5 | The optional Verification Token is a scoped access token (`scope`, `resource`, `satisfied_requirements`) (Verification Token Contents). It records a proof-satisfaction decision, not a grant of what the agent may do for the principal. Delegation artefacts are only suggested (Delegation and Actor Evidence). |
| Z2 Constraints | 0.5 | The token is scoped to Verifier audience, route, method and resource and must expire, but only in the optional OAuth leg. No amount or payee constraints. |
| Z3 Principal-signed | 0 | Nothing is signed by the principal as a grant. Delegation is "Fully Autonomous Delegation", listed as an open question and future work. |
| Z4 Lifecycle | 0.5 | The Verification Token MUST expire, SHOULD be short-lived, and SHOULD support revocation and replay detection (Verification Token Contents). It is optional, and there is no sub-delegation. |
| C1 Action record | 0.5 | The Verification Token records which `request_id`, resource, method and proof time the Verifier accepted. It is not an action or transaction record. Optional. UNSURE. |
| C2 Non-repudiation | 0.5 | The presentation is signed, and the token is a JWT in the common case, but its claim set is "deployment-specific". |
| C3 Redress | 0 | None. Payment and disputes are explicitly out of scope ("Payment Separation"; "Machine Payments and 402" is open). |
| C4 Third-party audit | 0.5 | The Verifier checks credential status, revocation and trust lists (Proof Validation 6). This is credential status, not an after-the-fact audit of actions. UNSURE. |

Totals for x401:

| Dimension | Score |
|---|---|
| Identity | 2.5 |
| Authentication | 2.5 |
| Authorisation | 1.5 |
| Accountability | 1.5 |

Unsure criteria: I1, I2, I4, A2, C1, C4. The x401 spec is a thin layer that composes other standards, so the scores depend on whether credential-level properties count as protocol-level.

## KYA-OS (DIF)

- Version: KYA-OS Protocol Specification v1.0.0, Status "Stable", donated to DIF TAAWG. The spec is `SPEC.md`, with profiles `SPEC-ENTITY-CARD.md` (v1.1, Entity Card profile), `SPEC-MCP-EXTENSION.md`, `SPEC-AUDIT-READ.md` and `AUDITABILITY.md`.
- Read: https://github.com/decentralized-identity/kya-os-mcp `SPEC.md`, `SPEC-ENTITY-CARD.md` and `AUDITABILITY.md` (section 15.3 summary). The latest GitHub release is v1.25.0 (18 Nov 2026), which is the reference implementation package. The wire spec stays at 1.0.0.
- Basis: `spec`.
- Orientation. The spec defines agent DIDs (`did:key`, `did:web`), a handshake, W3C VC delegation chains rooted at a Responsible Party with CRISP constraints and status-list revocation, and detached JWS action proofs. It also defines the Entity Card profile (typed entity, holder-of-key request proof, KYC/KYB attestation) and an audit profile (AAP levels).

| ID | Score | Justification |
|---|---|---|
| I1 Principal conveyed | 1 | The Delegation Credential carries `issuerDid`, and the root issuer is the Responsible Party. The `KYA-OS-Delegation-Credential` header and the Delegation Proof JWT (`sub` = Responsible Party DID) carry it (sections 2, 6.2, 8.1, 8.2). |
| I2 Operator conveyed | 1 | The agent DID is in the handshake `agentDid` and the `KYA-OS-Agent-DID` header. In organisational use the Responsible Party is the employing organisation (section 2 Terminology). The term "operator" is deliberately not used (Entity Card section 2.3). UNSURE whether the rubric treats Responsible Party as the operator. |
| I3 Third-party verified | 0.5 | KYC/KYB rides an `IdentityVerificationCredential` on the `responsibleParty`, from a trusted issuer (SPEC section 6.10 "KYC/KYB"; Entity Card sections 4.1 `attestations`, 10.4). It is optional and part of the Entity Card profile. The core delegation chain is issuer-signed, not third-party-attested. |
| I4 Legal-person grade, checkable | 0.5 | The attestation states a verification fact and level (`verificationLevel` in basic, enhanced, loa3), with no raw PII, and is verified cryptographically via the trusted-issuer, signature and expiry path (section 6.10). It is optional, and tying it to a registered legal entity is by profile, not core. |
| A1 Proof of possession | 1 | The Delegation Proof JWT is holder-of-key and EdDSA-signed (section 8.2). The Layer-1 signature DID must match the agent DID (8.1). The Entity Card profile defines the per-request holder-of-key proof `org.kya-os/proof.v1` (Entity Card section 8). |
| A2 Verifiable key discovery | 1 | The `did:key` and `did:web` resolution rules, and key retrieval by `kid` from `assertionMethod` (sections 4.1 to 4.4, 7.2). |
| A3 Freshness | 1 | Handshake nonce plus a ±120 s timestamp window (5.2), the nonce cache (5.5), a per-proof `nonce` and `ts` (7.2), and `jti` and a 60 s `exp` in the proof JWT (8.2). |
| A4 Principal authentication bound to agent | 1 | `needs_authorization` returns an `authorizationUrl`. The user authenticates and grants, and a DelegationCredential is issued to the agent DID (sections 9.2, 9.3). The authentication method itself is not specified. UNSURE. |
| Z1 Explicit grant artefact | 1 | DelegationCredential, a W3C VC with `credentialSubject.delegation` (6.2). |
| Z2 Constraints | 1 | CRISP: `scopes`, `notBefore`/`notAfter`, `audience`, `budget` with cap, unit and window, and scope matchers (6.3). |
| Z3 Principal-signed | 1 | The chain root is signed by the Responsible Party's DID key. Verifiers check the proof against the issuer DID document (6.2, 6.4.1). Where an authorisation service issues on the user's behalf (9.3), the key may belong to that service. UNSURE. |
| Z4 Lifecycle | 1 | `expirationDate`/`notAfter`, StatusList2021 revocation, cascading revocation (6.5, 6.6) and sub-delegation with subset discipline (6.4). |
| C1 Action record | 1 | The detached proof's `requestHash`, `responseHash`, `delegationRef` and `delegationChainDigest` link each call to the grant (7.2, 7.8). |
| C2 Non-repudiation | 1 | JWS signed by the server DID key, with an optional chained, signed audit ledger (7.4, 15.3). |
| C3 Redress | 0 | There is no dispute, refund or liability path. Section 11.12 defines reputation scope only. |
| C4 Third-party audit | 1 | Status-list revocation (6.6) is core. The Audit Assurance Profile (AAP-1 to AAP-4) adds RFC 9162 signed checkpoints and independent observers (15.3, AUDITABILITY.md). Reputation is scoped to the Responsible Party (11.12). UNSURE whether the rubric wants this at 0.5, since the AAP profile is optional. |

Totals for KYA-OS:

| Dimension | Score |
|---|---|
| Identity | 3.0 |
| Authentication | 4.0 |
| Authorisation | 4.0 |
| Accountability | 3.0 |

Unsure criteria: I2, A4, Z3, C4.

# Task B: untracked protocols (identified, not scored)

Searches used the web search tool, then `gh api` and `curl` against the primary pages. Sections cite only text I read at the primary source.

## 1. AMP — Ant International

- Full name: Agentic Mobile Protocol (AMP). It is sometimes glossed as an "agent payments protocol", but the primary source calls it an "application-layer trust protocol designed for payment scenarios involving AI agents", centred on digital wallets (docs/Overview.md).
- Steward: Ant International (GitHub org `ant-intl`). Licence Apache-2.0.
- What it does: it standardises trust coordination among users, agents, mobile payment providers, merchants, acquirers and credential providers, with mandate chains (three-layer SD-JWT), human-present and human-not-present flows, and evidence logging.
- Status/version/date: no tagged release or version number found. The repo was created on 17 Aug 2026 and last pushed on 23 Sep 2026. Press coverage dates the announcement to about 27 Apr 2026 (Business Wire release, a secondary source for the date only).
- Primary URL: https://github.com/ant-intl/AMP (homepage given as https://amp-protocol.io/, which returned no content to my fetch).
- Public spec: yes, as Markdown in `docs/` (Overview, Intent Trust Domain, Payment Service Domain, Wallet Service Domain, Business Scenarios Processes), plus Python samples.

## 2. Virtuals ACP

- Full name: Agent Commerce Protocol (ACP), Virtuals Protocol. Not the OpenAI/Stripe "Agentic Commerce Protocol", which is a different project.
- Steward: Virtuals Protocol (GitHub org `Virtual-Protocol`).
- What it does: an on-chain agent-to-agent commerce protocol that breaks accounts into jobs and jobs into memos, with a router contract and LayerZero cross-chain transfers. From the `agent-commerce-protocol` README.
- Status/version/date: no versioned spec. The contracts repo has `contracts/acp/v1` and `v2`, created 24 Feb 2026 and last pushed 2 Mar 2026, MIT licence. The SDK moved to `acp-node-v2`, and `acp-node` is marked deprecated. ACP launched in Feb 2025 per secondary sources (not verified at the primary source).
- Primary URLs: https://github.com/Virtual-Protocol/agent-commerce-protocol, https://app.virtuals.io/research/agent-commerce-protocol and https://whitepaper.virtuals.io/acp-product-resources/acp-dev-onboarding-guide. I did not open the research page or the onboarding guide, only the URLs listed by the SDK README.
- Public spec: no formal standalone specification found. The public artefacts are the contract source, the SDKs and the product docs.

## 3. ERC-8183

- Full name: ERC-8183 "Agentic Commerce": job escrow with evaluator attestation for agent commerce.
- Authors: Davide Crapis, Bryan Lim, Tay Weixiong, Chooi Zuhwa (the first is Ethereum Foundation dAI per secondary press, the other three Virtuals per the author handles and press; affiliation not stated in the EIP header).
- What it does: a smart-contract interface for jobs with client, provider and evaluator roles, escrowed ERC-20 payment, and states Open, Funded, Submitted, then Completed, Rejected or Expired.
- Status/date: Draft, Standards Track ERC. Created 2026-02-25. Requires EIP-20.
- Primary URL: https://eips.ethereum.org/EIPS/eip-8183 (discussion: https://ethereum-magicians.org/t/erc-8183-agentic-commerce/27902).
- Public spec: yes. The EIP text is public.

## 4. EMV Agentic Payments framework (EMVCo)

- Full name: "EMV® Agentic Payments – Framework for Specifications", v1.0 draft.
- Steward: EMVCo.
- What it does: a framework (not a specification) for card-based agentic payments. It introduces "Intent Services", a shared layer to register, reference, retrieve and manage consumer-authorised intent. Know Your Agent and agentic transaction indicators are listed as possible future work.
- Status/date: draft for public review, published 1 Sep 2026, comment period closed 30 Sep 2026.
- Primary URLs: https://www.emvco.com/news/emvco-requests-feedback-on-framework-for-secure-interoperable-and-scalable-card-based-agentic-payments/ and https://www.emvco.com/resources/emv-agentic-payments-framework-for-specifications-v1-0-draft-comment-period-ends-30-sept-2026/ (the resource page is linked from the news item and returns HTTP 200; I did not confirm that the draft PDF is downloadable without registration).
- Public spec: partially. A public-comment draft was offered, but the document itself is a framework, and the news item does not confirm a permanent public download.

## 5. AEP — A-Comm Evidence Protocol

- Full name: A-Comm Evidence Protocol (AEP).
- Steward: A-Comm Technologies, Inc. (GitHub org `A-Comm-Tech`). Apache-2.0. Governance says A-Comm stewards in a bootstrap phase.
- What it does: a tamper-evident hash chain of typed evidence artifacts (discovery, referral, intent, delegation, policy, cart, authorisation, then fulfilment and refund), sealed with Ed25519 and exported as a DisputeBundle for dispute evidence. It wraps other protocols (AP2, Visa TAP, Web Bot Auth and others) and says it assigns no liability.
- Status/version/date: v1.0.3-rc.2 draft, pre-release tagged 2026-07-02, repo last pushed 2026-11-14. A search result reported a v1.1.0 page and a v1.0.1 page, but the vercel site `aep-spec.vercel.app` now returns "deployment not found", so I did not verify those. The repo is the authority: v1.0.3-rc.2.
- Primary URL: https://github.com/A-Comm-Tech/a-comm-evidence-protocol (spec file `spec/aep-v1.0.3-rc.2.html`).
- Public spec: yes (draft, in the repo with test vectors). Press says the "full" specification is restricted to implementers during a patent filing, which I could not verify.

## 6. A2WP

- Full name: Agent-to-Wallet Protocol for Digital Credentials (A2WP). Not a payments protocol.
- Author: Thilina Shashimal Senarath, individual submission (no affiliation stated in the draft).
- What it does: lets an AI agent pass a credential offer or presentation request unchanged to a wallet. The wallet decides, obtains principal approval and does issuance or presentation, so credentials and keys never reach the agent.
- Status/date: individual IETF Internet-Draft `draft-senarath-a2wp-01`, dated 17 Oct 2026 (the -00 revision is September 2026). Intended Standards Track, no IETF standing, expires 20 Apr 2027.
- Primary URL: https://datatracker.ietf.org/doc/draft-senarath-a2wp/
- Public spec: yes, as the Internet-Draft.

## 7. HAPS

- Full name: Human Approval and Presence Specification (HAPS). Not found under any payments name. The match is on the exact acronym.
- Steward: iProov (GitHub `iProov/HAPS`, reference implementation in `iProov/HAPS-reference`). Apache-2.0.
- What it does: binds a provider's assertion of human presence and approval to a machine-readable action, as a signed Consent Credential carrying `intent_hash`, `presentation_hash`, `aud`, `challengeId`, `exp`, single-use `jti` and `assurance`.
- Status/date: "experimental draft specification and partial reference implementation; not production-ready". Repo created and last pushed 2026-09-17. No releases.
- Primary URL: https://github.com/iProov/HAPS (spec under `specification/draft`).
- Public spec: yes (draft, with schemas and formal models). Caveat: this identification relies on the acronym alone. Related but different: IETF draft "HTTP Agent Profile (HAP)" and the "Human Agent Protocol (HAP)" are not HAPS.

## 8. Mastercard Agent Pay

- Full name: Mastercard Agent Pay (the Agentic Payments Program, using Agentic Tokens).
- Steward: Mastercard.
- What it does: a programme that registers and verifies agents and issues dynamic Agentic Tokens so agents can transact on a consumer's behalf. Merchants recognise trusted agents through Web Bot Auth. A separate "Agent Pay for Machines" offering exists (2026).
- Status/date: announced April 2025. Acceptance Framework October 2025. Agent identity and trust services expanded in September to October 2026.
- Primary URLs: https://newsroom.mastercard.com/news/press/2025/april/mastercard-unveils-agent-pay-pioneering-agentic-payments-technology-to-power-commerce-in-the-age-of-ai and https://developer.mastercard.com/mastercard-checkout-solutions/documentation/use-cases/agent-pay/ (the developer page only came back as an empty shell to my fetch, so its content is from the search tool's description, not read by me). Merchant guide: https://developer.mastercard.com/merchant-cloud/documentation/tutorials-and-guides/agentic-commerce-guide/
- Public spec: partial. Developer documentation and a merchant guide are public. The programme requires registering with Mastercard, and I found no open protocol specification or version number.
