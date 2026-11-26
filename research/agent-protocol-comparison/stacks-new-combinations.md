# Stack joins for the chain rubric: three non-purchase stacks

Scope: three stacks built on Web Bot Auth (WBA) and PAP/Poppy 1.0, with KYA-OS, AP2, or both. Only the joins between protocols are assessed. Member scores are taken as reviewed in `scores.json` (`chain_scores`) and are not re-scored. Format follows `chain-stacks.md`. Read on 2026-11-25. No repository was edited.

## Sources and versions

| Short name | What was read | Version / revision |
|---|---|---|
| WBA | `draft-ietf-webbotauth-httpsig-protocol-01` (IETF archive text, 29 Oct 2026) | -01 |
| PAP | personalagentprotocol.org `/docs/1.0/spec.md`, `/docs/1.0/extensions.md` and every extension page (`ucp`, `operations`, `links`, `disclosures`, `mediated-sign-in`, `browser-control`), `/docs/1.0/guides.md`, `/docs/introduction.md`, `/docs/changelog.md`, draft `/docs/1.1/spec.md` | 1.0 (published) |
| PAP issues | all 121 issues of `personal-agent-protocol/personal-agent-protocol`, searched for AP2, KYA, Verifiable Intent, Web Bot Auth. Community proposals, not spec. Proposal text for #61 read from its attached revision 3 (24 Nov 2026) | open |
| KYA | `decentralized-identity/kya-os-mcp` at `ffe1810` (19 Nov 2026): `SPEC.md` (1.0.0, Stable), `SPEC-ENTITY-CARD.md` (profile 1.1), `SPEC-MCP-EXTENSION.md` (1.0.0-draft), `CONFORMANCE.md`, `submission/` | 1.0.0 core |
| AP2 | `google-agentic-commerce/AP2` at `e1ea56d` (29 Apr 2026): `docs/ap2/*.md`, `code/sdk/schemas/ap2/*.json` | v0.2.0 |
| UCP | `Universal-Commerce-Protocol/ucp` at `c20aa35`, read only to check what carries an AP2 mandate | v2026-08-25 line |

Local copies of the sources were kept and are not committed. A grep for the other protocols' names across every spec file, in both directions, is the basis for each "no reference" statement below. Patterns used: `poppy|personal.agent.protocol|\bPAP\b|Personal Agent`, `web.?bot.?auth|Signature-Agent|9421`, `\bAP2\b|Agent Payments|mandate`, `\bKYA\b|kya-os|know.your.agent|did:`, `client_id|jwks_uri|CIMD`.

Member scores used (from `scores.json` `chain_scores`):

| | L1 | L2 | L3 | L4 | L5 | L6 | L7 | L8 | L9 | L10 | Chain | Total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| WBA | 0 | 1 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 2 |
| PAP | 0 | 1 | 1 | 1 | 1 | 1 | 0 | 0 | 1 | 1 | 0 | 7 |
| KYA-OS | 1 | 1 | 1 | 2 | 1 | 2 | 1 | 0 | 1 | 1 | 0 | 11 |
| AP2 | 1 | 1 | 1 | 1 | 1 | 2 | 1 | 1 | 1 | 2 | 1 | 12 |

## Summary

| # | Stack | Documented? | "Documented today" chain / total | "If joined" chain / total (upper bound) | Single most important missing join |
|---|---|---|---|---|---|
| 1 | WBA + PAP + KYA-OS | WBA+PAP: yes (PAP spec 5.3). KYA-OS with either: no, in either direction | 0 / 7 | 0 / 11 (L8 stays 0) | A carrier that puts a KYA-OS delegation chain and proof on a PAP request, bound to the Session, with a key relationship between KYA-OS's Ed25519 DID key and PAP's ES256 keys |
| 2 | WBA + PAP + AP2 | WBA+PAP: yes. AP2 with either: no in any published spec. Open PAP issue #61 is a community proposal that would do it | 0 / 7 | 1 / 12 | A PAP extension that carries the AP2 mandates and ties the mandate `cnf` key and the PAP Session to the same action |
| 3 | WBA + PAP + KYA-OS + AP2 | WBA+PAP: yes. Everything else: no | 0 / 7 | 1 / 13 | The KYA-OS to AP2 link: nothing makes an AP2 open mandate reference the KYA-OS delegation chain (or the reverse), so the grant exists twice with no common anchor |

Reading of "documented today": a layer is credited to the best member only where a documented join carries it. The only documented join in any of the three stacks is PAP to WBA, which adds nothing to PAP's own scores (WBA scores 0 or equal on every layer). KYA-OS and AP2 artefacts never appear on a PAP request under any published spec, so they earn no credit. If the rows were instead scored by "the member that owns each layer, standalone", they would equal the "if joined" rows apart from L10, which is why L10 is the cell that actually depends on a join (see each stack).

## Pairwise join map

| Pair | Documented? | Citations |
|---|---|---|
| PAP and WBA | Yes, one-sided in PAP. WBA does not mention PAP | PAP spec 5.3 "Operator signatures": "A Personal Agent SHOULD also sign requests carrying the Session header ... using Web Bot Auth"; the signature "MUST cover `poppy-session`, and `authorization` when present". PAP guides "Operator signatures and bot defenses". PAP UCP extension section 4. WBA: no hit for Poppy or PAP |
| WBA and KYA-OS | Informal, one-sided in KYA-OS. WBA does not mention KYA-OS or DIDs | `SPEC-ENTITY-CARD.md` 8.5: "A stock RFC 9421 verifier (SEP-1960, Cloudflare Web Bot Auth) reconstructs this base and verifies `httpSig` against the resolved DID key with zero new code". A compatibility claim, not a join definition, and it does not hold against draft-01 (see stack 1). WBA D.1: "Delegation and chaining are out of scope for this document" |
| PAP and KYA-OS | No | No hit in the KYA-OS repo for Poppy, PAP or "Personal Agent". No hit in PAP 1.0, the 1.1 draft, the changelog or the guides for KYA, `did:` or DID identifiers. PAP issues: the only "kya" string is a branch name (`kya-mandate-spec`) in a third party's repository, linked from #71; no link to `decentralized-identity/kya-os-mcp` |
| PAP and AP2 | No in published specs. Proposal only | PAP introduction roadmap "Signed approvals": "Mandates, where the User signs once for a class of actions with limits ... would build on it" (concept; AP2 not named). Roadmap "Payments": "How payment works with the Operations extension is open." Open PAP issue #61 (payments extension, revision 3 of 24 Nov 2026) adopts AP2 and Verifiable Intent as the approval-evidence format (`mandate_formats: ["ap2", "verifiable-intent"]`). AP2 docs and schemas: no hit for Poppy or PAP |
| AP2 and WBA | No | AP2 docs and schemas: no hit for Web Bot Auth, Signature-Agent or RFC 9421. `implementation_considerations.md` "Agent Identification": "Merchants or Trusted Surfaces MAY wish to only work with trusted Agents. These details are left to the Commerce Protocol layer." Open AP2 issue #268 (non-normative) says WBA "is being adopted as the HTTP transport identity layer across agentic commerce" and reports a key-algorithm clash (Ed25519 for WBA, ECDSA for the checkout JWT, `specification.md` "Payment Mandate") |
| AP2 and KYA-OS | No | No hit for AP2 or Agent Payments in the KYA-OS repo (the word "mandate" appears only in KYA-OS's own `mandate-VC` shorthand and in "spec-mandated"). No hit for KYA, DIDs or decentralized identity in the AP2 docs or code. AP2 `specification.md` leaves agent-to-agent delegation "outside the scope of the current specification" |

## Facts used by all three stacks

PAP (spec 1.0):
- Agent identity is a URL: `client_id` is an HTTPS URL returning client metadata, with `jwks_uri` on the same domain (4.1). Keys in `jwks_uri` sign client assertions (ES256 or PS384; "Companies MUST accept" both) and delegations. They do not sign Session JWTs.
- The `Poppy-Session` JWT: `typ` `poppy-session+jwt`, `alg` MUST be `ES256`, header `poppy_dlg` (the delegation), claims `iss` (= `client_id`), `aud`, `sid`, `sub` (the User ID), optional `agent_id`, `htm`, `htu`, `iat`, `jti`, `ath` (5.2).
- "Delegation" in PAP is key delegation. A `poppy-delegation+jwt` signed by a `jwks_uri` key vouches for a short-lived key (`cnf.jwk`; `exp` at most 24 hours after `iat`). The Personal Agent "MUST NOT put a User ID, an Agent ID, a Company's issuer, or anything else about the User or the Companies they use in a delegation" (5.2). It conveys no authority to act, and "can't be withdrawn before it expires" (10.7).
- A delegated key is used "for one User ID only", and a Company MAY reject a key that has signed for a second User ID (5.2, 10.7).
- User IDs are pairwise: "opaque and different for each Company", and MUST NOT contain or derive from personal information (5.1).
- Extension points: domain-named extensions in `poppy.json` `extensions` and the `Poppy-Extensions` header (3.3); "Personal Agents and Companies MUST ignore extensions and versions they don't support and fields they don't recognize" (3.3); API types include `mcp` (7), where the Session header rides the MCP request; the Operations approval is a `Poppy-Approval` Dictionary field with `operation_id`, `revision`, `approver`, `approved_at`, `input_type`, `reference` (Operations 6).
- Approval strength: the Company relies on the Personal Agent's word (Operations 8.1; introduction roadmap "Signed approvals"). A User signature is roadmap.
- Operator signature: SHOULD, WBA-based, MUST cover `poppy-session` and `authorization` (5.3). Guides: "Keep operator keys separate from delegated Session keys. Publishing every User's delegated key in an operator directory is not equivalent to verifying a delegation, and exposes a new key mapping." Spec 5.3: "A shared origin alone does not establish that two client metadata URLs name the same client."

WBA (draft-01):
- The identifier is the `Signature-Agent` URL, resolved as a JWK Set (4.1); it "says nothing about who operates the Agent". `keyid` MUST be the base64url JWK SHA-256 thumbprint (RFC 7638) (5.2). `tag` MUST be `web-bot-auth`; at least one of `@authority` or `@target-uri` MUST be covered; `Signature-Agent` MUST be present and its member covered (5.2, 5.2.1). No body coverage unless `Content-Digest` is sent and covered (5.2). Extra covered components are allowed (5.2.4). Several signatures may be present, each with its own `Signature-Agent` member (5.2.2).
- Out of scope: "does not authenticate human users, does not provide anonymous authentication, and does not define authorization or delegation" (4.6). Key reuse across purposes: SHOULD NOT (6.5). Privacy: "Agents whose identifier would be associated with an individual human ... This protocol is not suited to such deployments" (7.1).

KYA-OS (1.0.0 core, Entity Card profile 1.1, MCP binding 1.0.0-draft):
- Keys: "KYA-OS uses Ed25519 ... for all cryptographic operations" (`SPEC.md` 4.2); `did:key` derivation is Ed25519 only (4.3). The Entity Card proof allows `EdDSA` or `ES256` (`SPEC-ENTITY-CARD.md` 8.2, 8.4). Delegation hops carry a `DataIntegrityProof` with `eddsa-jcs-2022` (10.5 item 3).
- CIMD on-ramp (7): `client_id` IS the entity's `did:web` in HTTPS form (`https://host/a/b` is `did:web:host:a:b`, 7.1); `jwks_uri` "MUST serve a JWKS that is a mechanical projection of the DID document's" `authentication` methods, and "Non-Ed25519 methods ... are skipped" (7.2); the CIMD document carries `_meta["org.kya-os/did"]` (7.3); fail-closed bind: `did:web` origin = `client_id` origin = `jwks_uri` origin, plus a reciprocal `alsoKnownAs` listing the `client_id` (7.4); `cnf.jkt` is the RFC 7638 thumbprint (7.5, 8.6).
- `proof.v1` (8.2): fields `prf`, `alg`, `did`, `kid`, `audience`, `nonce`, `created`, `expires` (at most 60 s), `requestHash`, optional `cnf.jkt`, `jws`, `httpSig`. Carrier is `_meta["org.kya-os/request-proof"]` in JSON-RPC `params` (`SPEC-MCP-EXTENSION.md` 6). `requestHash` covers `{method, params}` minus `_meta`, JCS then SHA-256 (8.3). It is defined only for JSON-RPC.
- The `httpSig` sibling (8.5): a raw signature by the same DID key over a base of `content-digest`, `kya-audience`, `kya-nonce`, optional `kya-cnf` and `@signature-params`, label `kyaos`. It "carries no delegation statement".
- The proof names its chain by digest in the JWS protected header `org.kya-os/delegation` (8.4).
- Delegation: `DelegationCredential` (VC 2.0 + ZCAP-LD, `SPEC.md` 6.10): `issuer`, `credentialSubject.invoker`, `allowedAction` (example `payments.transfer`), `caveats` (`ValidUntil`, `MaxAmount` with `limit` and `currency`), `parentCredentialDigest`, `credentialStatus` (Bitstring Status List). A caveat of an unknown type "MUST be replicated verbatim" down the chain (6.10). Carried in `_meta["org.kya-os/delegation-chain"]` (Entity Card 10.5), or over HTTP in `KYA-OS-Delegation-Credential`, `KYA-OS-Delegation-Proof` (JWT: `iss`, `sub` = root responsible party DID, `aud` = target hostname, `exp` = `iat` + 60 s, `scope`) and `KYA-OS-Agent-DID` (`SPEC.md` 8.1). The verifier "MUST check it equals the Layer-1 signature's resolved DID"; "Layer-1 signature" is not defined anywhere in the spec set.
- Privacy: a persistent DID "is a pseudonym; reuse across recipients enables correlation. Privacy-sensitive Entities SHOULD consider per-recipient DID rotation" (Entity Card 13). KYC/KYB is a fact and level, "never raw PII" (10.4).

AP2 (v0.2.0):
- Open mandates (`mandate.checkout.open.1`, `mandate.payment.open.1`) MUST carry the agent's public key as `cnf` (`specification.md` "Autonomous"); the schema describes `cnf` as "Confirmation claim as defined in RFC 7800 section 3.1" (`open_payment_mandate.json`). Examples use P-256 (`payment_mandate.md`). Closed mandates are signed by the agent key (Autonomous) or by the user through a User Credential or a Trusted Agent Provider (`agent_authorization.md`).
- No user identifier appears in any mandate schema (`vct`, `constraints`, `cnf`, `iat`, `exp`, `payee`, `payment_amount`, `payment_instrument`, `pisp`, `execution_date`, `risk_data`, `transaction_id`). The user is identified through the credential or provider that signed.
- Extension points (`specification.md`): new constraint `type` ("a uniquely defined `type`", a schema, an evaluation algorithm), checkout object, payment instrument, VDC format. `agent_authorization.md` verification: "Any unknown Constraints MUST be treated as failing evaluation" (error `unresolved_constraint`). So an extension constraint is not ignorable: a verifier that does not implement it rejects the mandate.
- AP2 defines no transport. Agent trust is left "to the Commerce Protocol layer", and the "trust list of Agent Providers" is not defined (`specification.md` Modes; `implementation_considerations.md`). The only documented carrier is UCP (`ap2.checkout_mandate`, `payment.instruments[*].credential.token`), which is not a member of any of these stacks and does not mention PAP, WBA or KYA-OS.

---

## Stack 1: WBA + PAP + KYA-OS

### Documented?
Only the PAP to WBA edge. No spec in the set refers to another across the PAP/KYA-OS or WBA/KYA-OS boundary in a way that defines a join. The one KYA-OS reference to WBA (`SPEC-ENTITY-CARD.md` 8.5) is a compatibility claim, and it fails against draft-01:
- WBA 5.2 requires `tag` `web-bot-auth`, at least one of `@authority` or `@target-uri`, and a covered `Signature-Agent`. The KYA-OS `httpSig` base is `content-digest`, `kya-audience`, `kya-nonce`, `kya-cnf` and `@signature-params`: no `@authority`, no `Signature-Agent`, and no tag stated. A draft-01 verifier "MAY discard signatures for which the tag is not set to web-bot-auth" (WBA 5.4), and the signature does not meet the 5.2 MUSTs anyway.

Nearest documented alternative: none for KYA-OS on a PAP request. KYA-OS's own documented HTTP carrier is the outbound `KYA-OS-*` header set (`SPEC.md` 8.1), defined for an MCP server calling a downstream service, not for a Personal Agent calling a Company.

### Feasibility of the joins

**Could a KYA-OS delegation credential or `proof.v1` ride on a PAP request?** Mechanically yes, on three surfaces, none defined.

| Surface | What would carry what | Why it works | Limit |
|---|---|---|---|
| PAP `mcp` API (spec 7) | `_meta["org.kya-os/request-proof"]` and `_meta["org.kya-os/delegation-chain"]` in the JSON-RPC `params`, beside `Poppy-Session` in the HTTP header | KYA-OS's native binding (`SPEC-MCP-EXTENSION.md` 6, 7.1); `requestHash` is defined for exactly this body. PAP 3.3 ignores unrecognised fields | Nothing ties the KYA-OS proof to the Session JWT. `_meta` is outside `requestHash` and "intermediary-mutable" (`SPEC-MCP-EXTENSION.md` 6 item 2), and the proof names its chain by digest only (`SPEC-ENTITY-CARD.md` 8.4). Binding to the Session needs a new field |
| PAP `openapi` API or any REST path | HTTP headers `KYA-OS-Delegation-Credential`, `KYA-OS-Delegation-Proof`, `KYA-OS-Agent-DID` (`SPEC.md` 8.1), covered by the operator signature | PAP 5.3 requires the operator signature to cover only `poppy-session` and `authorization`, but WBA 5.2.4 lets an agent cover extra headers, so the KYA-OS headers could be signed into the same WBA signature as the Session | `requestHash` is JSON-RPC only, so a REST body has no KYA-OS binding except the `httpSig` sibling, which fails WBA and carries no chain statement. The delegation proof JWT has `aud` = hostname and a 60 s life, no method or path, so it is replayable across endpoints of one host inside the window. EdDSA only (`SPEC.md` 8.2) |
| A PAP Session JWT claim | A claim naming the chain digest (the `sha256:` digest of the last credential, `SPEC.md` 7.8) | PAP 3.3 ignores unrecognised fields | Not recommended. PAP 5.2 defines no extension claims. A chain digest in a per-request JWT would be a stable cross-request handle, which the Session design avoids |

Best fit: the `mcp` path, with the KYA-OS proof and chain in `_meta` and the WBA signature covering the HTTP-level `Poppy-Session`. That yields two independent signatures on one request, linked only by timing and a shared audience unless a new field links them.

**Can PAP's `client_id` / `jwks_uri` keys and a KYA-OS agent DID be the same key or be bound?** Bound, yes. The same key, no.

- Binding is already specified on the KYA-OS side: `client_id` ⇄ `did:web` (7.1), `jwks_uri` ⇄ DID keys (7.2), origin equality plus reciprocal `alsoKnownAs` (7.4). A PAP `client_id` such as `https://agent.example/agent.json` maps to `did:web:agent.example:agent.json`. PAP 4.1 already requires a CIMD-style `client_id` URL with `jwks_uri` on the same domain, which matches KYA-OS's origin-equality rule. A Company running a KYA-OS verifier could apply `verifyCimdBind` to a PAP client without any PAP change. That is a stronger test than the shared origin that PAP 5.3 refuses to treat as sufficient.
- Same key fails on algorithm. PAP: the Session JWT `alg` MUST be `ES256` (5.2); client assertions and delegations are `ES256` or `PS384` and Companies MUST accept those two (4.1, 5.2). KYA-OS: Ed25519 "for all cryptographic operations" (`SPEC.md` 4.2); `did:key` is Ed25519 only (4.3); delegation hops are `eddsa-jcs-2022` (Ed25519); the CIMD `jwks_uri` projection drops non-Ed25519 methods (`SPEC-ENTITY-CARD.md` 7.2). The only P-256 allowance in KYA-OS is the `proof.v1` signature itself (8.4). So the Ed25519 key in a KYA-OS `jwks_uri` is not one a PAP Company must accept, and an ES256 key in a PAP `jwks_uri` is not one KYA-OS projects.
- Workaround inside the specs: one controller, two keys. The DID document carries the Ed25519 key (projected into `jwks_uri`) plus a P-256 method used only for `proof.v1` `ES256`. PAP still needs ES256 keys in the same `jwks_uri`, making it a superset of the DID projection. KYA-OS 7.2 says "mechanical projection" but only the origin and `alsoKnownAs` checks are enforced, so it would probably verify while contradicting the wording.
- PAP's Session key is a delegated key, not a `jwks_uri` key. The KYA-OS analogue is the one-off `did:key` delegate (`SPEC-ENTITY-CARD.md` 1.4; `SPEC.md` 6.9). It is Ed25519, so it cannot equal PAP's ES256 delegated key. A binding would be asserted, for example the PAP delegated key's JWK thumbprint placed in a KYA-OS caveat. No spec defines this.
- PAP's `poppy-delegation+jwt` and a KYA-OS `DelegationCredential` share a word only. One vouches for a key, the other grants authority. Neither can stand in for the other, and PAP forbids putting anything about the User or Company in its delegation (5.2), so a KYA-OS reference cannot go there.

**Is WBA's `Signature-Agent` bindable to either?**
- To KYA-OS: yes, cleanly, because both use the RFC 7638 thumbprint. WBA `keyid` MUST be the JWK thumbprint (5.2); KYA-OS `cnf.jkt` is the same thumbprint (8.6). The `Signature-Agent` value could be the KYA-OS CIMD `jwks_uri` (a JWKS over HTTPS serving Ed25519 `OKP` keys, which WBA accepts), so the URL-to-keys association WBA requires (4.4) coincides with the DID-to-keys association KYA-OS requires (7.4). Constraint: WBA 6.5 says a key SHOULD NOT be reused for another purpose, and a `jwks_uri` key would then sign HTTP requests and serve as DID `authentication`. A separate operator key listed in the same DID document is the compliant route.
- To PAP: only by Company policy. PAP deliberately does not bind them: "A verified operator signature establishes control of its key source. It does not establish every client metadata URL on the same origin" (guides). A defined bind would be: `Signature-Agent` URL equals the client's `jwks_uri` exactly and the signing key is in that set. PAP does not say this, and its guides say to keep operator keys separate from delegated Session keys.
- The human principal is excluded: WBA 7.1 says it is "not suited" to identifiers tied to "an individual human". `Signature-Agent` can bind only to the operator (a KYA-OS `agent` or `client` entity), never to the human root issuer.

**Conflicts**
1. Pairwise anonymous User ID versus an identifiable principal. PAP `sub` is pairwise and not derivable from personal data (5.1). KYA-OS's root issuer is the accountable principal (`SPEC-ENTITY-CARD.md` 10.2) and L1 needs it identifiable. A persistent root DID reused across Companies recreates the cross-Company handle PAP removes. It is compatible only if the principal uses a per-Company KYA-OS DID (Entity Card 13 allows "per-recipient DID rotation"; one-off `did:key` delegates, `SPEC.md` 12.5), so the Company sees two pairwise identifiers (PAP `sub`, KYA-OS root or delegate DID) and the Personal Agent holds the mapping. That works for pseudonymity. It gives the Company no resolvable real-world identity unless a KYC/KYB attestation (`SPEC-ENTITY-CARD.md` 10.4) is also shown, which PAP's design intends to avoid.
2. DID versus URL identifiers. PAP `iss` = `client_id` URL; KYA-OS `did` = `did:web`. The bijection covers host and path, not query strings, and `did:key` (the KYA-OS default for delegates and `human` principals) has no URL form, so it cannot be a PAP `client_id`.
3. Algorithms: Ed25519 versus ES256 (above).
4. Carrier: `proof.v1` is bound to a JSON-RPC body; PAP also serves REST and web pages.
5. Naming: "delegation" and "session" mean different things in each. KYA-OS has its own session handshake (`SPEC.md` 5, legacy 1.x profile) that PAP does not know.

### Score

| | L1 | L2 | L3 | L4 | L5 | L6 | L7 | L8 | L9 | L10 | Chain | Total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Documented today | 0 | 1 | 1 | 1 | 1 | 1 | 0 | 0 | 1 | 1 | 0 | 7 |
| If joined as proposed (upper bound) | 1 | 1 | 1 | 2 | 1 | 2 | 1 | 0 | 1 | 1 | 0 | 11 |

Documented row: PAP leads, WBA adds nothing, KYA-OS is credited nowhere.

Extension point or basis for each "if joined" cell that differs from the documented row:
- L1 = 1: the KYA-OS root `responsibleParty` DID, with the optional in-spec KYC/KYB `IdentityVerificationCredential` (`SPEC-ENTITY-CARD.md` 10.4). Partial under I1' because nothing names who resolves the DID to a real party on request. Carried in `_meta["org.kya-os/delegation-chain"]`. Capped by conflict 1.
- L4 = 2: the `DelegationCredential` (D1 `allowedAction`; D2 `caveats` including `MaxAmount`; D3 signed by the root issuer; D4 `validUntil` plus Bitstring Status List; D5 attenuation), carried as above. Only a KYA-OS verifier at the Company can check it.
- L6 = 2 on the `mcp` path only: the delegation digest in the proof's protected header (`org.kya-os/delegation`) and the caveat checks (`SPEC-ENTITY-CARD.md` 8.4, 11.4). On a REST path the best is 1, because the `httpSig` sibling carries no chain statement (8.5).
- L7 = 1: KYA-OS signed proofs as audit records (Entity Card 13 "Proof retention"); no accountable timestamp and no defined retention.
- L8 stays 0: neither PAP nor KYA-OS allocates liability or defines a dispute path. This is what holds the chain at 0.
- L10 stays 1: KYA-OS's own link from grant to identity is a DID match, not a hash (rule B); PAP's `sub` is pairwise and appears in no KYA-OS artefact; neither protocol's artefact hashes the other's. Adding `poppy-session` or the Session `jti` to what the KYA-OS proof covers would add a request-level link, not a record step.

### What this stack covers that purchase stacks do not
Purchase stacks (AP2 with UCP, TAP with WBA, PAP with UCP and WBA) cover paying. This one is built for non-purchase actions.

| Action class | Coverage | Basis |
|---|---|---|
| Read data | Yes | PAP scopes with `changes` and `personal_data` hints (4.7); KYA-OS `allowedAction` and CRISP scope matchers (`SPEC.md` 6.3) |
| Communicate on the principal's behalf | Yes, through PAP only | PAP conversations with the Company Agent (8). KYA-OS has no message semantics; a grant to send is generic `allowedAction` |
| Change account state | Yes | PAP Operations approves exact terms by revision; KYA-OS `allowedAction` and caveats. The approval is agent-attested, not user-signed (PAP roadmap) |
| Legally significant act | Partial | Generic only. A KYA-OS grant can name an action but defines no consent or signing semantics, and PAP approvals rest on the Personal Agent's word |
| Pay | Partial at best | KYA-OS `MaxAmount` and `payments.transfer` in the example (`SPEC.md` 6.10) bound a spend, but there is no payee caveat, no checkout binding and no receipt. PAP defers payment to UCP |
| Delegate onward | Yes, through KYA-OS | Multi-hop attenuating chains with `parentCredentialDigest` (6.10). PAP does not: an agent run by another company "connects under its own `client_id`" (5.1) |

---

## Stack 2: WBA + PAP + AP2

### Documented?
Only PAP to WBA. AP2 is not mentioned in any PAP 1.0 page, the 1.1 draft, the changelog or the guides, and PAP, WBA and Poppy are not mentioned in any AP2 doc or schema. Two sideways signals:
- PAP issue #61, an open community proposal, not part of the published spec. A comment of 2026-10-30 proposes reusing "the AP2 / Verifiable Intent mandate model"; the author agreed on the same day. Revision 3 (24 Nov 2026) defines `mandate_formats: ["ap2", "verifiable-intent"]`, a `poppy` object bound inside every mandate (`payee_domain`, `client_id`, `operation_id`, `revision`, `operation_ref`, `display_hash`, `offer`), a `Poppy-Payment` header for APIs, a `_meta` entry for MCP, and "User identifiers in the mandate MUST be pairwise". Open question 10 asks which payer the mandate binds. A proposal scores 0 under the rubric.
- AP2 issue #268 (open, non-normative): WBA is "being adopted as the HTTP transport identity layer"; AP2's "Checkout JWT MUST be signed ... ECDSA and not ... Ed25519" (`specification.md` "Payment Mandate") forces two keypairs where the WBA convention is Ed25519. Correction (26 Nov): Ed25519 is a deployment convention, not a WBA requirement; draft-01 allows any IANA-registered RFC 9421 algorithm (5.2), so an ECDSA WBA key can satisfy both. AP2's own security section also allows Ed25519 when the checkout carries a salt, so AP2 is internally inconsistent here.

Nearest documented alternative: PAP's UCP extension plus UCP's AP2 Mandates extension, each documented separately and not joined end to end. PAP's UCP page names the UCP checkout as the approval and does not mention mandates. UCP is not a member of this stack.

### Feasibility of the joins

**Could an AP2 mandate ride a PAP request?** Yes, on PAP's extension surface, with no AP2 change. AP2 defines no transport.

| What | Where on a PAP request | Basis |
|---|---|---|
| Open and closed checkout and payment mandates (SD-JWT with disclosures) | A domain-named PAP extension listed in `poppy.json` `extensions` and the `Poppy-Extensions` header (3.3); body or header on APIs, `_meta` on `mcp`, a message field on conversations. Adjacent field: `Poppy-Approval` (Operations 6) | PAP 3.3 allows domain-named extensions and requires unknown ones to be ignored. This is the approach in PAP #61 revision 3 ("Delivering the credential to the Payee") |
| Receipts | PAP response body or conversation message | AP2 receipts (`reference` = hash of the mandate) are signed by the verifier. PAP has no carrier |
| The action itself | A PAP Operation (`operation_id`, `revision`) carried as AP2's merchant-signed checkout | Proposed in #61 ("The Poppy Operation is carried as AP2's merchant-signed checkout"); AP2's "Checkout Object" extension point allows it |

**Could an AP2 mandate's `cnf` be the PAP delegated key?** Mechanically yes, and it is the best binding on offer.
- The algorithm fits: the PAP delegated key is P-256 (`cnf.jwk` `kty` `EC`, `crv` `P-256`, 5.2) and AP2 `cnf` is an RFC 7800 JWK with P-256 in every example. AP2's ECDSA rule applies to the merchant checkout JWT, not the agent key.
- Setting the open mandate's `cnf.jwk` equal to the delegated key's `cnf.jwk` means the Session JWT and the closed mandates are signed by the same key. A Company can check that the Session's signer is the key the user-signed open mandate named. That is a key-level link, which counts toward C1 only under rule B.
- Frictions:
  1. Lifetime. The delegation lasts at most 24 hours and the Personal Agent MUST NOT sign a Session JWT after it lapses (5.2). An open mandate can outlive it. The agent must keep the key and obtain fresh delegations for it. PAP lets the agent decide "when to create a new delegated key" and guides say to get a new delegation before expiry, but they do not say a new delegation may name the same key.
  2. Exposure. An AP2 mandate also goes to the credential provider, the network and the payment processor, so the key becomes visible to payment parties. It is a per-Company pseudonym with no User ID attached.
  3. Operator signature. The WBA operator key must not be this key: PAP's guides keep operator keys separate from delegated Session keys and warn that publishing delegated keys in a directory "exposes a new key mapping".
- An alternative that avoids key equality is the #61 design: `client_id` and the Operation go inside the signed mandate (`poppy` object). That ties the mandate to the PAP agent identity but not to a key.

**Is WBA's `Signature-Agent` bindable to either?**
- To AP2 `cnf`: not as key equality (friction 3; WBA 6.5). The workable bind is coverage. The WBA signature covers the field that carries the mandate, for example a `Content-Digest` of the body that holds the closed mandate or the extension header (WBA 5.2, 5.2.4). The operator named by `Signature-Agent` then attests "I sent these mandate bytes". It does not make the operator an AP2 party.
- To PAP: as in stack 1, Company policy only.

**Conflicts**
1. Pairwise anonymous User ID versus an identifiable principal. AP2 has no user identifier in any mandate; the user is whoever the credential issuer or Trusted Agent Provider vouches for. PAP's `sub` enters no AP2 artefact under any spec, and #61 itself lists "which identifier binds the payer" as open. An AP2 User Credential with selective disclosure can stay hidden from the Company, so pseudonymity survives, but then the Company cannot resolve the principal. L1 stays partial.
2. Trusted Surface versus agent-attested approval. AP2 requires the user's signature on a Trusted Surface; PAP's Company relies on the Personal Agent and the signed approval is roadmap. For one action, a PAP Operation approved by the agent and an AP2 mandate signed by the user are grants of different strength. Under #61 revision 3 a Payee can set `requires_mandate`, which resolves it for payment only.
3. DID versus URL identifiers: not engaged. AP2 uses neither for the agent; the Agent Provider is a `kid` (for example `agent-provider-key-1`) on a trust list that AP2 does not define.
4. Three signature layers on one request (the PAP Session JWT, the WBA operator signature, AP2's key-binding JWT per mandate). None references another by hash.

### Score

| | L1 | L2 | L3 | L4 | L5 | L6 | L7 | L8 | L9 | L10 | Chain | Total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Documented today | 0 | 1 | 1 | 1 | 1 | 1 | 0 | 0 | 1 | 1 | 0 | 7 |
| If joined as proposed (upper bound) | 1 | 1 | 1 | 1 | 1 | 2 | 1 | 1 | 1 | 2 | 1 | 12 |

Documented row: as stack 1.

Extension point or basis for each "if joined" cell that differs from the documented row:
- L1 = 1: the AP2 User Credential issuer verifies the principal (OpenID4VP, `agent_authorization.md`); partial under I1' because there is no resolve-on-request wording and no accredited-issuer rule.
- L3 and L4 stay 1: AP2's open mandate, signed by the user, binds the agent key (`cnf`), but its only validity control is `exp`, and AP2 has no revocation. PAP's delegation adds none ("can't be withdrawn before it expires", 10.7).
- L6 = 2: the closed mandate hashes the checkout and chains to the open mandate by `sd_hash` (A1), and the merchant verifies `payment.allowed_payees`, `amount_range`, `budget` (A2). Payments only. Needs the PAP extension above to carry the mandates.
- L7 = 1, L8 = 1: AP2 signed receipts and the "Dispute Evidence" verification steps (`specification.md`), credited as rule C. Needs the receipt to reach the Personal Agent, which PAP does not carry.
- L10 = 2: reachable only with an extension that (a) sets the open mandate's `cnf` equal to the PAP delegated key (key link, C1) and (b) has the operator signature cover the carrier of the closed mandate (action references grant by signature coverage). AP2 then supplies closed to open by `sd_hash` and receipt to mandate by hash (`reference`). Today, with no join, it is 1.

### What this stack covers that purchase stacks do not
It adds PAP's non-payment surface to AP2's payment evidence. AP2 itself is payment and checkout only; its authorisation model "could be applied more generally in the future" (`agent_authorization.md`).

| Action class | Coverage | Basis |
|---|---|---|
| Read data | Yes (PAP) | OAuth scopes with hints (4.7) |
| Communicate on the principal's behalf | Yes (PAP) | Conversations (8) |
| Change account state | Yes (PAP), agent-attested | Operations approvals. An AP2 mandate does not cover it: no constraint type for account changes, though the "Mandate Constraints" extension point would allow one |
| Legally significant act | Partial | Neither defines consent or signing semantics. AP2 mandates are user-signed but typed to checkout and payment |
| Pay | Yes (AP2) | Open and closed payment mandates, constraints, receipts |
| Delegate onward | No | AP2: agent-to-agent delegation "is outside the scope of the current specification". PAP: key delegation only |

---

## Stack 3: WBA + PAP + KYA-OS + AP2

### Documented?
No. It inherits the PAP to WBA edge only. There is no documented path between KYA-OS and AP2 in either direction. The nearest alternatives do not overlap: PAP issue #61 proposes AP2 for PAP; nothing proposes KYA-OS for PAP or for AP2. The two grants are independent:
- the KYA-OS `DelegationCredential` (authority chain, `allowedAction` and caveats, Ed25519, DID identifiers, `credentialStatus`);
- the AP2 open mandate (SD-JWT, constraint array, P-256, `cnf`, expiry only).
Each could be the grant for a different class of action. KYA-OS lists `payments.transfer` and `MaxAmount` in its own example (`SPEC.md` 6.10), so the two overlap on payments with no stated precedence.

### Feasibility of the joins
The stack 1 and stack 2 findings carry over. The new joins are between KYA-OS and AP2.

**Could a KYA-OS credential or `proof.v1` ride on an AP2 mandate, or the reverse?** Extension points exist on both sides, with different failure behaviour.
- AP2 "Mandate Constraints": a new constraint needs a unique `type`, a schema and an evaluation algorithm (`specification.md`). A constraint such as `kya.delegation_ref` holding the chain digest (`SPEC.md` 7.8) would put the digest inside the user-signed open mandate. AP2 says "Any unknown Constraints MUST be treated as failing evaluation" (`agent_authorization.md`), so every verifier on the path (merchant, credential provider, network) would have to implement it or reject the mandate. The binding is therefore safe but must be negotiated.
- KYA-OS caveats: a caveat of an unknown type "MUST be replicated verbatim" (`SPEC.md` 6.10). A caveat such as `{type: "AP2OpenMandate", sdHash: ...}` would put the hash of the AP2 open mandate inside the KYA-OS grant. It would be a signed commitment only, because KYA-OS defines no evaluation for it.
- Either gives a hash link, which is what C2 needs (rule B). One direction is enough for a one-way chain. The AP2 constraint is the more natural, because the user's signature on the mandate then covers the delegation chain.
- KYA-OS `proof.v1` is a per-request proof over a JSON-RPC body (`requestHash`). It cannot sign an AP2 closed mandate; a new proof of the closed mandate would be needed.

**Could an AP2 mandate's `cnf` be the KYA-OS agent key or the PAP delegated key?**
- AP2 does not restrict the algorithm of the agent key. An Ed25519 `OKP` JWK is a valid RFC 7800 `cnf`; the examples and the OpenID4VP sample (`kb-jwt_alg_values: ["ES256"]`) use P-256, and AP2 does not say verifiers must accept EdDSA key-binding JWTs.
- Equating `cnf` with the KYA-OS leaf delegate key (the `did:key` named in `credentialSubject.invoker`) would make the KYA-OS leaf join (`leafInvoker === proof.did`, 10.2) and the AP2 mandate signature name the same key; `cnf.jkt` (8.6) is the comparison value.
- One agent key cannot be all three of the AP2 `cnf`, the KYA-OS leaf delegate (Ed25519 under the core spec) and the PAP Session key (ES256). The workable split is: AP2 `cnf` = PAP delegated key (as in stack 2); the KYA-OS delegate key bound to the AP2 mandate by the hash constraint above; the KYA-OS proof used on the MCP path only.

**Is WBA's `Signature-Agent` bindable?** As in stack 1 (to KYA-OS, through the shared thumbprint and `jwks_uri`) and stack 2 (to AP2, by coverage and not by key). The best compliant arrangement uses three distinct keys: the operator key (WBA), the KYA-OS agent key, and the PAP delegated key.

**Conflicts**: those in stacks 1 and 2, plus:
1. Two grants for one purchase. A KYA-OS `MaxAmount` caveat and an AP2 `payment.amount_range` can disagree, and neither spec says which wins. A Company that checks only one is exposed to the other's looser limit.
2. Three principal identifiers (KYA-OS root issuer DID, the AP2 credential subject, the PAP pairwise `sub`) with no spec saying they name one person.
3. Revocation: KYA-OS has cascading Bitstring Status Lists (`SPEC.md` 6.5, 6.6); AP2 has expiry only; PAP delegations cannot be revoked. Revoking the KYA-OS chain does not revoke an issued AP2 open mandate.

### Score

| | L1 | L2 | L3 | L4 | L5 | L6 | L7 | L8 | L9 | L10 | Chain | Total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Documented today | 0 | 1 | 1 | 1 | 1 | 1 | 0 | 0 | 1 | 1 | 0 | 7 |
| If joined as proposed (upper bound) | 1 | 1 | 1 | 2 | 1 | 2 | 1 | 1 | 1 | 2 | 1 | 13 |

Documented row: as stacks 1 and 2.

Basis for each "if joined" cell beyond stacks 1 and 2:
- L4 = 2 comes from KYA-OS (best member) and only for the actions its grant covers. The AP2 mandate (L4 = 1, no revocation) covers purchases. No cell takes the weaker of two overlapping grants.
- L8 = 1 comes from AP2 alone. KYA-OS and PAP add nothing.
- L10 = 2 needs three links: (a) the AP2 open mandate carries the KYA-OS chain digest as a new constraint (grant to authority by hash, which also closes KYA-OS's own gap, where the grant refers to identity by DID match only); (b) the AP2 `cnf` is the PAP delegated key, and the operator signature covers the mandate carrier (action to grant); (c) AP2 receipts reference the closed mandate by hash (record to action). All three rest on extensions that no spec defines. If one is omitted L10 falls to 1 and the total to 12.
- The chain stays at 1 because L8 is 1 and no member scores 2 on L1, L2, L3, L5, L7, L8 or L9.

### What this stack covers that purchase stacks do not
Everything in stacks 1 and 2: the grant for non-purchase and onward-delegated actions comes from KYA-OS and the grant for purchases from AP2.

| Action class | Coverage | Basis |
|---|---|---|
| Read data | Yes | PAP scopes; KYA-OS `allowedAction` and scope matchers |
| Communicate on the principal's behalf | Yes (PAP) | Conversations. No signed grant for it in AP2; KYA-OS has only generic `allowedAction` |
| Change account state | Yes | PAP Operations plus a KYA-OS grant. The approval is still agent-attested unless the user's signature on the AP2 or KYA-OS artefact is made to cover the Operation (the #61 `operation_ref` idea) |
| Legally significant act | Partial | No defined semantics in any of the four |
| Pay | Yes (AP2), with KYA-OS `MaxAmount` as a second, unreconciled limit | AP2 mandates; conflict 1 |
| Delegate onward | Yes (KYA-OS) | Attenuating chains. AP2 delegation to another agent is out of scope, so onward delegation of a purchase mandate is not covered |

---

## Notes on method and limits
- "If joined" cells are upper bounds. They assume the proposed extension is built as described and the Company's verifier runs every check named. No stack was tested against running implementations.
- KYA-OS version: the brief named v1.0.0. `SPEC.md` is 1.0.0 (Stable). The Entity Card profile (1.1) and the MCP binding (1.0.0-draft) are separate documents in the same repository, and the `proof.v1`, CIMD on-ramp and `httpSig` material used here sits in those two. If only `SPEC.md` 1.0.0 is in scope, the legacy session-handshake proof (`SPEC.md` 5, 7) and the `KYA-OS-*` headers (8) apply and the CIMD binding does not.
- AP2 was read as the v0.2.0 repository tree, not the published web docs.
- PAP issues #61, #69, #71, #74 and #102 discuss mandates. They show intent, not a defined join, and score nothing (roadmap or future work is 0). #71's "kya" string is a branch name in another project's repository.
- UCP was checked only to confirm that UCP, not AP2, defines how a mandate rides a request. UCP does not mention PAP, WBA key binding to AP2, or KYA-OS.
- Under an alternative reading of "documented today", where KYA-OS or AP2 is credited standalone as owner of each layer, the totals would be 11, 12 and 13 for stacks 1 to 3, equal to the "if joined" rows. The difference is that no published spec lets those artefacts be presented to a PAP Company.
