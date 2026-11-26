# Agent protocols: coverage, chain of accountability and compatibility

This note scores 14 agent identity, transport, mandate and payment protocols from our [capability map](../../PROTOCOLS.md). Every score comes from a published rubric applied to the protocol's own specification text, with a citation. The aim is to test what the specifications actually provide, not to add another opinion.

The note has four parts, plus a compatibility study:
- **[Part 1](#part-1-the-four-headings)** scores each protocol on four headings: Identity, Authentication, Authorisation and Accountability.
- **[Part 2](#part-2-the-trust-chain)** goes further. Having every piece is not the same as having a chain that an auditor or a court could follow from the person behind an agent to the money that moved. Part 2 scores that chain, for single protocols and for stacks.
- **[Part 3](#part-3-beyond-payments)** scores the same chain for actions other than buying: reading data, messaging, changing an account, accepting terms, and instructing another agent.
- **[Part 4](#part-4-stacks-seen-in-practice)** checks which stacks vendors and open-source projects actually use, including PAP and Web Bot Auth as Meta's Muse and Shopify deploy them.
- **[compatibility.md](compatibility.md)** looks at which protocols appear to fit together, pair by pair: what the specs describe, what is seen in use, and where keys or signatures may not line up.

**In short:**
- On the four headings, the protocols are strongest on authentication and authorisation, and weakest on accountability and verified identity. Identity is carried more often than it is verified.
- On the chain, no protocol or stack is complete. The best, for payments AP2 alone or with UCP, reach "partial on every link".
- The links nobody covers fully are the ones that make someone answerable: an identifiable, verified principal and operator, accountable key binding, durable evidence, liability allocation and a trust anchor.
- Beyond payments the picture is weaker still. Only KYA-OS keeps a chain with no missing link. No protocol defines a grant for communicating on someone's behalf, and only consent records cover legally significant acts.
- The most common real stacks are x402 + MCP and MCP + A2A, and neither completes the chain. Nothing ties the paying wallet, or the next agent, back to the original caller. PAP with Web Bot Auth is emerging, but as deployed it runs as UCP over MCP, with PAP 0.4 files and no visible PAP sessions or signatures.

# Part 1: the four headings

The Harvey-ball format and the four headings were inspired by OneID's protocol coverage chart (LinkedIn, 11 Nov 2026). The original comparison against that chart is kept in [oneid-comparison/](oneid-comparison/README.md).

## Method

**Headings.** Identity covers the natural or legal person behind an agent and how that person is verified. Authentication, Authorisation and Accountability follow the criteria below.

**Rubric.** Each heading has four yes/no criteria, so a heading scores 0 to 4, and 0 to 4 maps onto a Harvey ball (0 empty, 4 full). Each criterion scores 1 if the core specification meets it. It scores 0.5 if only an optional extension or a SHOULD/MAY requirement meets it, or it is met in part. It scores 0 if the spec does not meet it, leaves it out of scope, or hands it to someone else, such as "the card network handles disputes". The full rubric is in [rubric.md](rubric.md).

| Heading | Criteria |
|---|---|
| Identity | I1 principal conveyed · I2 operator conveyed · I3 verified by a third party · I4 legal-person grade and cryptographically checkable |
| Authentication | A1 proof of possession of a key · A2 key discoverable from a published source · A3 replay protection · A4 principal's own authentication bound to the agent |
| Authorisation | Z1 explicit grant artefact · Z2 constraints (amount, payee, time, scope) · Z3 grant signed by the principal · Z4 expiry, revocation or narrowed sub-delegation |
| Accountability | C1 action record linked to the grant or identity · C2 record signed or tamper-evident · C3 dispute, refund or liability path · C4 third-party audit (log, registry, reputation or status list) |

**Scoring.** Four agents scored the protocols independently, in parallel, without seeing any other ratings. Each read the primary specification and cited the section or field for each criterion. Per-criterion scores and citations are in [scores-group-1.md](scores-group-1.md) (PAP, MCP, A2A, Web Bot Auth), [scores-group-2.md](scores-group-2.md) (AP2, Verifiable Intent, UCP, ACP), [scores-group-3.md](scores-group-3.md) (TAP, x402, MPP, ERC-8004) and [scores-group-4.md](scores-group-4.md) (x401, KYA-OS). All scores are also in [scores.json](scores.json).

**Consistency pass.** Afterwards, four cells were changed so that every group applied the rules the same way. The group files show the scores before these changes.

| Protocol | Criterion | From → to | Reason |
|---|---|---|---|
| UCP | A1 | 1 → 0.5 | Request signing is SHOULD, not MUST |
| MCP | I2 | 1 → 0.5 | Client ID Metadata Documents are SHOULD |
| AP2 | C4 | 0.5 → 0 | No log, registry or status list; re-verifiable artefacts alone do not count |
| Verifiable Intent | C4 | 0.5 → 0 | As AP2 |

**Versions read:** PAP 1.0; MCP 2026-07-28 with the Enterprise-Managed Authorization extension; A2A v1.0.1; Web Bot Auth `draft-ietf-webbotauth-httpsig-protocol-01`; AP2 v0.2.0; Verifiable Intent v0.1 draft; UCP v2026-08-25; ACP 2026-04-17; x402 v2 with its extensions; MPP `draft-httpauth-payment-01` with its method drafts; ERC-8004 Draft; x401 Draft 0.2.0; KYA-OS spec v1.0.0. **TAP** has no normative specification, so it was scored from Visa's developer documentation, read through a summarising fetch tool. Treat TAP's scores as provisional.

## Results

Scores are out of 4, on the original criteria. The amended criteria below change Identity and Authentication; the chart uses the amended scores.

| Protocol | Identity | Authentication | Authorisation | Accountability |
|---|---|---|---|---|
| ACP (OpenAI, Stripe) | 1.5 | 2.5 | 3.5 | 1.5 |
| UCP | 3 | 3 | 2 | 1.5 |
| AP2 | 2.5 | 3.5 | 4 | 2.5 |
| Verifiable Intent | 3 | 3.5 | 4 | 2 |
| Visa TAP (provisional) | 3.5 | 4 | 2 | 1 |
| x402 | 1 | 3 | 3.5 | 2.5 |
| MPP | 0.5 | 2 | 2 | 1.5 |
| PAP (Poppy) 1.0 | 2 | 4 | 3.5 | 1 |
| MCP | 1.5 | 2.5 | 3.5 | 0 |
| A2A | 1.5 | 2.5 | 2.5 | 0.5 |
| Web Bot Auth | 1 | 3 | 0 | 1 |
| ERC-8004 | 0.5 | 2.5 | 0 | 2.5 |
| x401 | 2.5 | 2.5 | 1.5 | 1.5 |
| KYA-OS | 3 | 4 | 4 | 3 |

### What the scores show

1. **Authentication and Authorisation are the strongest headings**, averaging 3.0 and 2.6 out of 4. For authorisation, AP2, Verifiable Intent and KYA-OS meet all four criteria. Web Bot Auth and ERC-8004 score 0: both specs exclude delegation.
2. **Identity is carried more often than it is verified.** Several specs convey who is behind an agent:
   - **UCP** (3). Checkout carries a `buyer` object, the `UCP-Agent` header names the platform, and Identity Linking adds a user token.
   - **AP2** (2.5). The User Credential is issued by a third party the verifier trusts, as an SD-JWT VC it can check itself.
   - **TAP** (3.5, provisional). The Consumer Recognition Object carries an issuer-signed ID token, and agents are onboarded to the payment scheme.

   Verification is weaker. No protocol meets I4, *verified, legal-person-grade* identity, in full. Six meet it in part: AP2, Verifiable Intent, UCP, TAP, x401 and KYA-OS.
3. **Accountability is the weakest heading on the original criteria**, averaging 1.6. The cause is C3, redress. Not one of the 14 specs defines a dispute path or allocates liability in full.
   - AP2 and UCP get half: AP2 has dispute-verification steps, and UCP has dispute and refund adjustment records.
   - The rest hand redress to the card network, or say it is out of scope.

   At most, the specs support signed evidence (C1, C2), not redress. MPP's core receipt is not even signed.
4. **x402 scores well for Authorisation** (3.5). The signed EIP-3009 `authorization` is an explicit, payer-signed grant: it states amount, payee and a validity window, and it expires.
5. **MPP's grant-like features sit in its method drafts.** The core receipt is returned only on a SHOULD, is unsigned, and carries no grant or identity. Grant-like features exist only in the payment-method drafts (Tempo `keyAuthorization`, Stripe SPT limits). If the method drafts counted as core, Authorisation would be about 3.5.
6. **A2A records work but not who answers for it** (Accountability 0.5). Task and message objects record the work, but nothing links them to the authenticated identity or a grant, and there is no redress path.
7. **Web Bot Auth authenticates the agent, not the human** (Authentication 3). The spec explicitly excludes authenticating the human (A4).

### The "process identifier" point

Many protocols claim agent identity when what they carry is closer to a process identifier than a legal identity. The specifications bear this out. The agent or operator is identified by a URL, key or token in PAP (`client_id` URL), Web Bot Auth (`Signature-Agent` URL), MCP (client metadata), A2A (Agent Card) and ERC-8004 (an on-chain token ID). None of them attests who the legal person is (I3 = 0 or 0.5). The exceptions all come through third-party credentials, not the agent protocol itself: AP2 and Verifiable Intent (issuer credentials), x401 (verifier-requested digital credentials) and KYA-OS (an optional KYC/KYB credential on the Responsible Party).

### Amended criteria: "identifiable" and "accountable key"

Three criteria were then tightened, and all 14 protocols re-scored on them:
- **I1 and I2** now ask whether the principal and the operator are *identifiable*, not just named. Someone accountable must be able to tell who they are, at least in a dispute. Self-asserted details or a bare domain score half at most.
- **A2** was "key discoverable from a published source". It now asks whether the key is *bound to an accountable party* and *its validity at the time of use can be checked afterwards*. Being able to look a key up publicly says little for audit: anyone who controls a domain can publish one.

| Protocol | Identity (before · amended) | Authentication (before · amended) |
|---|---|---|
| ACP | 1.5 · 1 | 2.5 · 2.5 |
| UCP | 3 · 2 | 3 · 2 |
| AP2 | 2.5 · 2.5 | 3.5 · 3.5 |
| Verifiable Intent | 3 · 2.5 | 3.5 · 3 |
| Visa TAP | 3.5 · 2.5 | 4 · 3.5 |
| x402 | 1 · 0.5 | 3 · 2.5 |
| MPP | 0.5 · 0.5 | 2 · 2 |
| PAP (Poppy) | 2 · 1 | 4 · 3 |
| MCP | 1.5 · 1.5 | 2.5 · 2 |
| A2A | 1.5 · 1 | 2.5 · 1.5 |
| Web Bot Auth | 1 · 0.5 | 3 · 2 |
| ERC-8004 | 0.5 · 0.5 | 2.5 · 2 |
| x401 | 2.5 · 2.5 | 2.5 · 2 |
| KYA-OS | 3 · 2 | 4 · 3.5 |

**Effect:**
- **Identity** falls from an average of 1.9 to 1.5 out of 4. Requiring identifiability rather than naming removes credit for self-asserted details, which makes Identity the weakest heading. The highest, at 2.5, are AP2, Verifiable Intent, TAP and x401.
- **Authentication** falls from 3.0 to 2.5. No protocol binds the agent's key to an accountable party *and* lets its validity be checked later. Web Bot Auth drops to half: its keys are self-published, and the draft defines no revocation.

The amended scores are in [scores.json](scores.json) (`I1p`, `I2p`, `A2p`), with citations in the chain-scores files.

# Part 2: the trust chain

## Why the four headings are not enough

A protocol could answer yes to all 16 questions in Part 1 and still give no chain anyone could rely on:
1. **The headings are scored separately.** Nothing checks that the verified person, the person who authenticated, the signer of the grant and the party named in the record are the same, or that each artefact points to the one before.
2. **Nothing checks that the action stayed within the grant.** A record that mentions the grant is not a check that the purchase stayed within its limits.
3. **Liability belongs to roles.** The principal, operator, agent provider, issuer, merchant and payment provider each carry different exposure. One "is there a dispute path?" question lumps them together.
4. **There is no trust anchor.** A perfectly consistent chain is worthless if nobody accredits the issuers in it.
5. **Evidence must last.** A dispute can come months later, after keys have rotated. Nothing in the headings tests trusted time, retention or later re-verification.
6. **Liability mostly lives in rulebooks, not protocols.** The headings did not separate "delegates disputes to a named rulebook and maps its evidence to it" from "says nothing".

## The chain rubric

[chain-rubric.md](chain-rubric.md) defines ten links. Each scores 2 (met in the core specification), 1 (partial, or only via an optional extension in the same spec set) or 0. The **chain score is the lowest link**, because one missing link means the chain is not complete. The total out of 20 shows breadth.

| Link | Met (2) when |
|---|---|
| L1 Principal identity | The principal is identifiable, verified by a third party, and that verifier is accountable (named, accredited or listed) |
| L2 Operator identity | The same, for the company running the agent |
| L3 Agent key binding | An accountable party binds the agent's key, and its validity at time of use can be checked later |
| L4 Delegation | Explicit grant with constraints, signed by the principal, with expiry or revocation |
| L5 Session authentication | Proof of possession, replay protection, human presence or consent captured with an assurance level |
| L6 Action conformance | The action references the grant, and the counterparty can check it is within the grant before acting |
| L7 Evidence | Signed by an accountable party, trusted time, re-verifiable later |
| L8 Redress | Liability allocated between named roles, and a dispute path (native, or a named rulebook with evidence mapped to it) |
| L9 Trust anchor | Registry, trust list or governance framework, and a revocation or status mechanism |
| L10 Continuity | Same principal throughout, and each artefact hashes or signs over the one before |

## Method

The method was the same as in Part 1:
- Four agents scored the 14 protocols from the primary specifications, citing the section or field for every link. Visa TAP was read from the raw developer pages this time, which corrected two earlier readings.
- A fifth agent checked how the members of each stack are specified to fit together.
- An **independent reviewer** who had not done any scoring then:
  - checked every cell a scorer had marked unsure against the spec text;
  - applied five consistency rules to all protocols;
  - changed 16 cells and one stack score.

The five consistency rules:
- **A.** Only the protocol's own spec set counts. A pointer to another protocol earns nothing unless both are in the stack.
- **B.** A shared identifier is not a cryptographic link.
- **C.** Implicit reliance on card rules is not a dispute path.
- **D.** Unread features are not credited.
- **E.** A self-published key fails accountable binding.

The changes are listed in [chain-review.md](chain-review.md). Per-link scores with citations are in [chain-scores-group-1.md](chain-scores-group-1.md) to [chain-scores-group-4.md](chain-scores-group-4.md), shown before review. The stack joins are in [chain-stacks.md](chain-stacks.md).

## Results: single protocols

After review. 2 = met, 1 = partial, 0 = absent.

| Protocol | L1 | L2 | L3 | L4 | L5 | L6 | L7 | L8 | L9 | L10 | Chain | Total /20 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| AP2 | 1 | 1 | 1 | 1 | 1 | 2 | 1 | 1 | 1 | 2 | **1** | 12 |
| Verifiable Intent | 1 | 1 | 1 | 2 | 1 | 2 | 1 | 1 | 1 | 1 | **1** | 12 |
| KYA-OS | 1 | 1 | 1 | 2 | 1 | 2 | 1 | 0 | 1 | 1 | 0 | 11 |
| UCP | 1 | 1 | 0 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 0 | 9 |
| MPP | 1 | 0 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 0 | 9 |
| x402 | 0 | 1 | 0 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 0 | 8 |
| PAP (Poppy) 1.0 | 0 | 1 | 1 | 1 | 1 | 1 | 0 | 0 | 1 | 1 | 0 | 7 |
| Visa TAP | 1 | 1 | 1 | 0 | 1 | 0 | 1 | 0 | 1 | 1 | 0 | 7 |
| MCP | 1 | 1 | 0 | 1 | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 6 |
| ACP | 1 | 0 | 0 | 1 | 1 | 1 | 0 | 1 | 0 | 1 | 0 | 6 |
| x401 | 1 | 1 | 0 | 1 | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 6 |
| A2A | 0 | 1 | 0 | 1 | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 5 |
| ERC-8004 | 0 | 1 | 1 | 0 | 0 | 0 | 1 | 0 | 1 | 1 | 0 | 5 |
| Web Bot Auth | 0 | 1 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 2 |
| **Best score on the link** | 1 | 1 | 1 | 2 | 1 | 2 | 1 | 1 | 1 | 2 | | |

**Findings:**
- **No protocol has a complete chain.** Only AP2 and Verifiable Intent avoid a missing link, and they get there by being partial on most links.
- **Only three links are ever fully met:** delegation (Verifiable Intent, KYA-OS), action conformance (AP2, Verifiable Intent, KYA-OS) and continuity (AP2). The protocols are good at *what the agent may do* and *whether this action fits it*.
- **Seven links are never fully met by any protocol:**
  - L1, principal identity: no spec has an accountable party that will resolve who the principal is.
  - L2, operator identity.
  - L3, accountable key binding.
  - L5, human presence with an assurance level.
  - L7, evidence with trusted time and retention.
  - L8, redress.
  - L9, trust anchor.

  These are the links that make someone *answerable*. Identity alone is not enough without accountable verifiers, evidence that lasts, and liability rules.
- **Redress is the link most often missing.** Eight of the 14 score 0 on L8. Even the best score only partial: AP2 and Verifiable Intent define dispute-verification steps, and UCP and ACP define refund and dispute records. None allocates liability between named roles.
- **Agent-centric protocols score lowest.** Web Bot Auth, A2A and ERC-8004 identify an agent or its domain, and stop there. Their specs explicitly put human identity, delegation or trust out of scope. That is by design, not a defect, but it is why they cannot carry accountability on their own.

## Results: stacks

Protocols are deployed together, so 13 combinations were scored. They include the most common real-world stacks (see [Part 4](#part-4-stacks-seen-in-practice)) and combinations around PAP.

**Basis ("documented today").** A stack takes a member's score on a link only where a spec defines the join that carries that member's artefact. Otherwise it takes the score of the member that owns that layer. Where members sit on separate agent-to-agent hops with no join, each link takes the weaker hop.

**Two extra kinds of row:**
- **"If joined as proposed"** is an upper bound for joins no spec defines yet, naming the extension point that would carry them. Details are in [stacks-new-combinations.md](stacks-new-combinations.md) and [stacks-common.md](stacks-common.md).
- **"As deployed"** reflects what live deployments actually publish.

| Stack | L1 | L2 | L3 | L4 | L5 | L6 | L7 | L8 | L9 | L10 | Chain | Total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| UCP + AP2 over MCP/A2A | 1 | 1 | 1 | 1 | 1 | 2 | 1 | 1 | 1 | 1 | **1** | 11 |
| ↳ if joined as proposed | 1 | 1 | 1 | 1 | 1 | 2 | 1 | 1 | 1 | 2 | **1** | 12 |
| PAP + Web Bot Auth (+ UCP, MCP), as specified | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | **1** | 10 |
| ↳ as deployed (Shopify, Muse) | 1 | 1 | 0 | 1 | 1 | 1 | 0 | 1 | 1 | 1 | 0 | 8 |
| KYA-OS + MCP (tool calls, not commerce) | 1 | 1 | 1 | 2 | 1 | 2 | 1 | 0 | 1 | 1 | 0 | 11 |
| x402 + MPP + MCP | 1 | 0 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 0 | 9 |
| ↳ if joined as proposed | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | **1** | 10 |
| x402 + ERC-8004 | 0 | 1 | 0 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 0 | 8 |
| x402 + MCP | 0 | 1 | 0 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 0 | 8 |
| ↳ if joined as proposed | 1 | 1 | 0 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 0 | 9 |
| PAP + Web Bot Auth | 0 | 1 | 1 | 1 | 1 | 1 | 0 | 0 | 1 | 1 | 0 | 7 |
| Visa TAP + Web Bot Auth (join not defined; TAP's own scores) | 1 | 1 | 1 | 0 | 1 | 0 | 1 | 0 | 1 | 1 | 0 | 7 |
| Web Bot Auth + PAP + KYA-OS | 0 | 1 | 1 | 1 | 1 | 1 | 0 | 0 | 1 | 1 | 0 | 7 |
| ↳ if joined as proposed | 1 | 1 | 1 | 2 | 1 | 2 | 1 | 0 | 1 | 1 | 0 | 11 |
| Web Bot Auth + PAP + AP2 | 0 | 1 | 1 | 1 | 1 | 1 | 0 | 0 | 1 | 1 | 0 | 7 |
| ↳ if joined as proposed | 1 | 1 | 1 | 1 | 1 | 2 | 1 | 1 | 1 | 2 | **1** | 12 |
| Web Bot Auth + PAP + KYA-OS + AP2 | 0 | 1 | 1 | 1 | 1 | 1 | 0 | 0 | 1 | 1 | 0 | 7 |
| ↳ if joined as proposed | 1 | 1 | 1 | 2 | 1 | 2 | 1 | 1 | 1 | 2 | **1** | 13 |
| ACP + Stripe Shared Payment Tokens | 1 | 0 | 0 | 1 | 1 | 1 | 0 | 1 | 0 | 1 | 0 | 6 |
| MCP + A2A | 0 | 1 | 0 | 1 | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 5 |
| ↳ if joined as proposed | 1 | 1 | 0 | 1 | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 6 |

Two rows in an earlier version of this table were corrected on review:
- **AP2 + UCP:** continuity goes from 2 to 1, total 12 to 11, because UCP has no field that carries AP2's receipts.
- **x402 + ERC-8004:** agent key binding goes from 1 to 0, total 9 to 8, because no documented join binds ERC-8004's registered wallet to the x402 payer.

**Findings:**
- **Stacking does not complete the chain.** The members share the same gaps, so combining them cannot fill those gaps. The best stacks reach "partial on every link", the same as AP2 alone.
- **PAP + Web Bot Auth adds nothing over PAP alone.** Web Bot Auth scores at or below PAP on every link. Its value is access: firewalls and bot-management services can recognise the operator. It does not make the operator accountable. PAP itself says a valid Web Bot Auth signature does not prove the signer is the same client as PAP's `client_id`.
- **Combinations with KYA-OS or AP2 are undocumented.** No spec defines a join between PAP and KYA-OS or AP2, so today they score as PAP alone.
  - **If joined as proposed:**
    - PAP + AP2 reaches a chain of 1. An open PAP issue, #61, proposes exactly this.
    - PAP + KYA-OS does not, because neither defines redress for payments.
  - **Key algorithms clash.** PAP's Session JWT must be ES256, and KYA-OS's core `did:key` delegate is Ed25519 (ES256 is allowed only for its Entity Card per-request proof), so one delegated agent key cannot serve both; they can only be bound. See [compatibility.md](compatibility.md).
- **Joins are weaker than the members.**
  - **AP2 + UCP** is the only stack joined by a normative hash and signature chain. UCP's AP2 Mandates extension uses MUST throughout. Even there, the chain holds only when the user signs the grant. Under UCP's "trusted platform" option the platform signs, and continuity drops to partial. UCP also has no field for AP2's receipts.
  - **Verifiable Intent**'s mapping to AP2 and UCP is informal and out of date. AP2 0.2 now defines the same mandate layer, so the two overlap rather than stack.
  - **TAP and Web Bot Auth** are described as "aligned", but a Web Bot Auth verifier would not accept TAP's signatures. They use different tags and have no `Signature-Agent` header.
  - **PAP + UCP + Web Bot Auth** is well documented. However, PAP's pairwise, deliberately anonymous user ID works against an identifiable principal. Web Bot Auth's key is not bound to PAP's `client_id`, and the stack has no grant signed by the principal.
  - **x402 + ERC-8004** is linked only by an optional, unvalidated transaction hash in ERC-8004's off-chain feedback file. The x402 repository does not mention ERC-8004.
- **"Best member" overstates every stack.** The scores above are an upper bound. [chain-stacks.md](chain-stacks.md) lists, for each stack, where one member's identity or grant is not carried into the other's artefacts.

# Part 3: beyond payments

The chain rubric assumes money throughout: amounts, payees, receipts, chargebacks. Most of what an agent does for someone is not a purchase. It reads a mailbox, sends a message, changes an account, accepts terms, or instructs another agent. [chain-rubric-general-actions.md](chain-rubric-general-actions.md) keeps the same ten links but rewrites the tests that assume money:

| Link | Rewritten test |
|---|---|
| L4 Delegation | Can the grant limit the operation, resource, data scope, recipient, count and time window? |
| L5 Session authentication | Is there a step-up confirmation by the human before any high-risk action? |
| L6 Action conformance | Can the counterparty check that this operation on this resource is within the grant? |
| L7 Evidence | Is there a signed record of what was done, to what, and with which inputs? Is the outcome signed too? |
| L8 Redress | Is responsibility allocated for non-monetary harm? Is there a way to contest, cancel, roll back or revoke? Chargebacks alone score 0. |

Payment-only mechanisms earn nothing on L4 to L8. The rubric also asks which kinds of action a protocol can express: read data, communicate on someone's behalf, change an account, a legally significant act, pay, and instruct another agent.

**Method.** Two scorers covered seven protocols each. An independent reviewer then applied the same rules to all 14:
- Cancelling an action in flight, or revoking a grant, is partial redress.
- An action kind counts as "defined" only where the spec names its scope, operation or constraint.

The full record is in [general-scores-group-a.md](general-scores-group-a.md), [general-scores-group-b.md](general-scores-group-b.md) and [general-review.md](general-review.md).

## Results: single protocols

| Protocol | L1 | L2 | L3 | L4 | L5 | L6 | L7 | L8 | L9 | L10 | Chain | Total /20 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| KYA-OS | 1 | 1 | 1 | 2 | 1 | 2 | 1 | 1 | 1 | 1 | **1** | 12 |
| AP2 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 0 | 1 | 2 | 0 | 10 |
| UCP | 1 | 1 | 0 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 0 | 9 |
| PAP (Poppy) 1.0 | 0 | 1 | 1 | 1 | 1 | 1 | 0 | 1 | 1 | 1 | 0 | 8 |
| Verifiable Intent | 1 | 1 | 1 | 1 | 1 | 1 | 0 | 0 | 1 | 1 | 0 | 8 |
| MCP | 1 | 1 | 0 | 1 | 1 | 1 | 0 | 1 | 1 | 0 | 0 | 7 |
| x401 | 1 | 1 | 0 | 1 | 1 | 1 | 0 | 1 | 1 | 0 | 0 | 7 |
| A2A | 0 | 1 | 0 | 1 | 1 | 1 | 0 | 1 | 1 | 0 | 0 | 6 |
| Visa TAP | 1 | 1 | 1 | 0 | 1 | 0 | 0 | 0 | 1 | 1 | 0 | 6 |
| x402 | 0 | 1 | 0 | 0 | 1 | 0 | 1 | 0 | 1 | 1 | 0 | 5 |
| ERC-8004 | 0 | 1 | 1 | 0 | 0 | 0 | 1 | 0 | 1 | 1 | 0 | 5 |
| MPP | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 1 | 1 | 0 | 4 |
| ACP | 1 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 1 | 0 | 3 |
| Web Bot Auth | 0 | 1 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 2 |

**What an agent can be authorised to do.** "Defined" means the spec names the scope, operation or constraint. "Hook" means only a free-form scope, tool name or custom type exists, with no agreed meaning.

| Protocol | Read data | Communicate | Change an account | Legally significant act | Pay | Instruct another agent |
|---|---|---|---|---|---|---|
| UCP | defined | hook | defined | defined | defined | — |
| KYA-OS | hook | hook | hook | hook | defined | defined |
| A2A | hook | hook | hook | hook | hook | hook |
| AP2 | hook | hook | hook | hook | defined | — |
| PAP (Poppy) 1.0 | hook | hook | defined | hook | hook | — |
| Verifiable Intent | hook | hook | hook | hook | defined | — |
| ERC-8004 | hook | hook | hook | hook | hook | — |
| MCP | hook | hook | hook | hook | hook | — |
| ACP | — | — | — | defined | defined | — |
| x401 | hook | hook | hook | hook | — | — |
| Visa TAP | hook | — | — | — | defined | — |
| MPP | — | — | — | — | defined | — |
| x402 | — | — | — | — | defined | — |
| Web Bot Auth | — | — | — | — | — | — |
| **Protocols defining it** | **1** | **0** | **2** | **2** | **8** | **1** |

**Findings:**
- **Payment protocols cover little else.** Their grants, checks and remedies are payment-only. ACP falls from 6 to 3, MPP from 9 to 4, and x402 from 8 to 5.
- **AP2 and Verifiable Intent lose their chains.** Every mandate and constraint they define is about purchases. A custom constraint type is allowed, but none is defined.
- **KYA-OS is the only protocol with a chain with no missing link.** It names a Responsible Party for any action and can revoke a delegation, both partial.
- **Most kinds of action have no defined grant.** Paying is defined by 8 protocols. Communicating on someone's behalf is defined by none, and a legally significant act only by consent records (UCP's Buyer Consent, ACP's marketing consent).
- **Instructing another agent is barely covered.** Only KYA-OS defines narrowed onward delegation. A2A has a task chain but no scoped onward grant.

## Results: stacks

Same stacks and basis as in Part 2, under the general-actions rubric. A join that is itself a payment mechanism carries nothing here.

| Stack | L1 | L2 | L3 | L4 | L5 | L6 | L7 | L8 | L9 | L10 | Chain | Total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| KYA-OS + MCP | 1 | 1 | 1 | 2 | 1 | 2 | 1 | 1 | 1 | 1 | **1** | 12 |
| PAP + Web Bot Auth (+ UCP, MCP), as specified | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | **1** | 10 |
| ↳ as deployed (Shopify, Muse) | 1 | 1 | 0 | 1 | 1 | 1 | 0 | 1 | 1 | 1 | 0 | 8 |
| UCP + AP2 over MCP/A2A | 1 | 1 | 0 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 0 | 9 |
| ↳ if joined as proposed | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 2 | **1** | 11 |
| PAP + Web Bot Auth | 0 | 1 | 1 | 1 | 1 | 1 | 0 | 1 | 1 | 1 | 0 | 8 |
| Web Bot Auth + PAP + KYA-OS | 0 | 1 | 1 | 1 | 1 | 1 | 0 | 1 | 1 | 1 | 0 | 8 |
| ↳ if joined as proposed | 1 | 1 | 1 | 2 | 1 | 2 | 1 | 1 | 1 | 1 | **1** | 12 |
| Web Bot Auth + PAP + AP2 | 0 | 1 | 1 | 1 | 1 | 1 | 0 | 1 | 1 | 1 | 0 | 8 |
| ↳ if joined as proposed | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 2 | **1** | 11 |
| Web Bot Auth + PAP + KYA-OS + AP2 | 0 | 1 | 1 | 1 | 1 | 1 | 0 | 1 | 1 | 1 | 0 | 8 |
| ↳ if joined as proposed | 1 | 1 | 1 | 2 | 1 | 2 | 1 | 1 | 1 | 2 | **1** | 13 |
| x402 + MCP | 1 | 1 | 0 | 1 | 1 | 1 | 0 | 1 | 1 | 0 | 0 | 7 |
| ↳ if joined as proposed | 1 | 1 | 0 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 0 | 9 |
| x402 + MPP + MCP | 1 | 1 | 0 | 1 | 1 | 1 | 0 | 1 | 1 | 0 | 0 | 7 |
| ↳ if joined as proposed | 1 | 1 | 0 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 0 | 9 |
| Visa TAP + Web Bot Auth | 1 | 1 | 1 | 0 | 1 | 0 | 0 | 0 | 1 | 1 | 0 | 6 |
| MCP + A2A | 0 | 1 | 0 | 1 | 1 | 1 | 0 | 1 | 1 | 0 | 0 | 6 |
| ↳ if joined as proposed | 1 | 1 | 0 | 1 | 1 | 1 | 0 | 1 | 1 | 0 | 0 | 7 |
| x402 + ERC-8004 | 0 | 1 | 0 | 0 | 1 | 0 | 1 | 0 | 1 | 1 | 0 | 5 |
| ACP + Stripe Shared Payment Tokens | 1 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 1 | 0 | 3 |

**Findings:**
- **Chains with no missing link:**
  - **Today:** KYA-OS + MCP, for tool calls, and PAP + Web Bot Auth with UCP, as specified. Both are partial on every link.
  - **If joined as proposed:** all three PAP + Web Bot Auth combinations with KYA-OS or AP2 reach the same level.
  - **Gains most from a join:** Web Bot Auth + PAP + KYA-OS. For payments it still does not complete the chain; beyond payments it would become complete at "partial". That is the strongest case for defining that join.
- **The PAP + UCP chain of 1 is fragile.** It rests on counting UCP's signed order webhooks as evidence for non-payment actions. A strict reading gives 0.
- **The common payment stacks fall away.** x402 + MCP, x402 + MPP + MCP and ACP carry little beyond payment.

# Part 4: stacks seen in practice

Parts 2 and 3 started from combinations the specifications define. This part checks which combinations are actually used, from two directions:
- **Vendors.** About 20 vendors' products and announcements, with sources, are in [evidence-vendor-stacks.md](evidence-vendor-stacks.md).
- **Open-source code.** Repositories whose dependency files include two protocols' packages are counted in [evidence-code-cooccurrence.md](evidence-code-cooccurrence.md).

| Stack | Vendors using it (about 20 checked) | Open-source co-occurrence (package.json files, estimate) |
|---|---|---|
| x402 + MCP | About 10. The most widely live: AWS AgentCore Payments (generally available), Vercel, Cloudflare (waitlist) | About 1,670, the second most common pair |
| MCP + A2A | Google, Microsoft and others | About 2,980, the most common pair |
| UCP over MCP/A2A, alongside AP2 | About 8. Live in Google AI Mode and Gemini; others announced | About 10 |
| ACP + Stripe Shared Payment Tokens | About 8, including Microsoft Copilot Checkout (live). OpenAI scaled back its own Instant Checkout in March 2026 | None found (closed APIs) |
| Payment-provider acceptance layers (ACP, UCP, Visa TAP, MPP and network tokens behind one integration) | 6 | n/a |
| Card networks over Web Bot Auth (Visa TAP, Mastercard Agent Pay) | About 5. Specifications published; production not confirmed | Very little |
| x402 + MPP (+ MCP) | 4 | About 160 for the pair. MCP + x402 + MPP is the clearest three-protocol stack |
| PAP + UCP + MCP (+ Web Bot Auth) | Sierra, Meta (Muse), Shopify | None yet |
| x402 + ERC-8004 | None of the major vendors | About 190, mostly crypto projects |

The code counts are estimates. GitHub code search matches loosely; "x402" matched about 12,000 manifest files against 269 npm packages that actually depend on it. Vendor sample repositories are not filtered out.

**Findings:**
- **Vendor and open-source stacks differ.** UCP, ACP and the card-network stacks run inside closed platforms, so they barely appear in code. Open source is dominated by MCP, A2A and the crypto payment rail (x402, MPP, ERC-8004).
- **x402 + MCP is the one stack strong on both measures.** It does not complete the chain because nothing ties the wallet that pays to the MCP caller who asked. It scores 0 out of 20 at 8 for payments and 0 at 7 beyond payments. The same gap applies to x402 + MPP + MCP.
- **MCP + A2A has no delegation across the hop.** It is the most common combination in code. A2A has no grant artefact, and the MCP token is issued to the A2A server agent, not derived from the original caller.
- **Identity layers are rarely shipped in common stacks.** KYA-OS, x401, ANS and Verifiable Intent are not combined with anything at scale. The only live vendor pairing found is Skyfire's KYA with Akamai. This matches the chain results: who is behind the agent is the weakest part in practice as well as on paper.

## PAP and Web Bot Auth as deployed

PAP with Web Bot Auth, used by Meta's Muse and Shopify stores, looks to be the emerging combination. The deployment was checked against PAP 1.0 on 25 Nov 2026. The raw survey is in [evidence-poppy-survey.json](evidence-poppy-survey.json).

- **Shopify publishes PAP 0.4, not 1.0.** Of 81 domains probed, 45 returned a `/.well-known/poppy.json`, all Shopify storefronts. All 45 declare protocol version 0.4, and PAP 1.0 says a 1.0 agent must not use a 0.4 document. They are identical apart from the store name and host. Each lists a single surface, UCP checkout, with no MCP or OpenAPI entry; MCP is reachable only through the UCP profile.
- **Shopify's UCP profiles publish no keys,** so their signed order webhooks cannot be verified. None offers AP2.
- **Muse signing with Web Bot Auth is unconfirmed.**
  - **Primary:** Meta publishes a live key directory at `www.meta.com` with five Ed25519 keys, but nothing in it names Muse. Meta's crawler page lists five agents, not Muse, and describes only IP-based verification.
  - **Secondary:** a single report of a bot-detection firm's observation that Meta began signing some Muse requests in mid-October.
  - **Not found:** any statement from Meta or Sierra that Muse signs with Web Bot Auth, and any public sign of Muse sending PAP session headers.
- **As deployed, the stack is UCP over MCP.** It scores a chain of 0 at 8 out of 20 under both rubrics, against 1 at 10 for PAP 1.0 as specified. The pieces that would make it accountable are not visibly live: PAP 1.0 sessions, operator signatures and verifiable webhooks.

# What a complete chain would need

Reading across all the tables, the missing pieces sit outside what these protocols try to do:

| Gap | What would close it |
|---|---|
| L1, L2: identifiable, verified principal and operator | A credential from an accredited verifier (KYC or KYB under a named trust framework), carried into the grant, and resolvable to a real party in a dispute |
| L3: accountable key binding | The agent key certified by the operator or a third party, with key status kept so a signature can be checked as at the time it was made |
| L5: human presence | Consent captured with a stated assurance level and bound to the grant (HAPS targets this) |
| L7: evidence | Records signed by an accountable party, with trusted time and a retention rule. AEP targets this |
| L8: redress | A rulebook that allocates liability by role and states which artefacts count as evidence. Card schemes do this for card payments; nothing equivalent covers the agent layer |
| L9: trust anchor | A registry or trust list of accredited issuers and operators, with status and revocation |
| Beyond payments: what may be done | Defined grant types for reading data, communicating on someone's behalf, changing an account and legally significant acts, not just free-form scopes |
| Across agents | A scoped onward grant that each agent hop carries and narrows, tied back to the original principal |
| Across protocols | A binding between the identity at one layer and the payer or signer at another, such as the MCP caller and the x402 wallet, or the PAP session and the AP2 mandate |

No single protocol is likely to cover all of this, and the protocols here do not try to. It is a governance and trust-infrastructure layer that sits across them. The rubric gives a way to test any claim to provide it on the same terms.

# Charts

Rendered by two scripts, which write HTML for headless Chrome to screenshot at 2x:
- [charts/make-charts.py](charts/make-charts.py), from [scores.json](scores.json) and [adoption.json](adoption.json). From the `charts` folder, run `python3 make-charts.py ../scores.json <out-dir> ../scores.json ../adoption.json`.
- [charts/compat-matrix.py](charts/compat-matrix.py), from [compatibility.json](compatibility.json). From the `charts` folder, run `python3 compat-matrix.py ../compatibility.json <out-dir>`.

| Chart | Shows |
|---|---|
| [payments-1-four-headings.png](charts/payments-1-four-headings.png) | Harvey balls on the four headings, amended criteria (Part 1) |
| [payments-2-chain-by-protocol.png](charts/payments-2-chain-by-protocol.png) | The ten links for each protocol, payments, with GitHub stars and downloads (Part 2) |
| [payments-3-chain-by-stack.png](charts/payments-3-chain-by-stack.png) | The ten links for each stack, payments, with "if joined as proposed" rows (Parts 2 and 4) |
| [non-payments-1-action-coverage.png](charts/non-payments-1-action-coverage.png) | Which kinds of action each protocol defines (Part 3) |
| [non-payments-2-chain-by-protocol.png](charts/non-payments-2-chain-by-protocol.png) | The ten links for each protocol, beyond payments, with GitHub stars and downloads (Part 3) |
| [non-payments-3-chain-by-stack.png](charts/non-payments-3-chain-by-stack.png) | The ten links for each stack, beyond payments (Parts 3 and 4) |
| [compatibility-matrix.png](charts/compatibility-matrix.png) | Which protocols appear to fit together, pair by pair ([compatibility.md](compatibility.md)) |

# Reference

## Coverage: what is in one list and not the other

**Related protocols, not in our map.** These were identified from primary sources but not scored. Details are in [scores-group-4.md](scores-group-4.md).

| Protocol | What it is | Status | Primary source |
|---|---|---|---|
| AMP — Ant International | Agentic Mobile Protocol, a wallet-centred agent trust protocol with SD-JWT mandate chains | Public Markdown docs, no version; repo created 17 Aug 2026 | [ant-intl/AMP](https://github.com/ant-intl/AMP) |
| Virtuals ACP | Virtuals' Agent Commerce Protocol, on-chain agent-to-agent jobs and escrow. Not OpenAI/Stripe ACP | Contracts and SDKs; no standalone spec | [Virtual-Protocol/agent-commerce-protocol](https://github.com/Virtual-Protocol/agent-commerce-protocol) |
| ERC-8183 | "Agentic Commerce": job escrow with an evaluator role | ERC Draft, 25 Feb 2026 | [EIP-8183](https://eips.ethereum.org/EIPS/eip-8183) |
| EMV Agentic Payments framework | EMVCo framework for specifications ("Intent Services"); a framework, not a spec | v1.0 draft, comments closed 30 Sep 2026 | [EMVCo](https://www.emvco.com/news/emvco-requests-feedback-on-framework-for-secure-interoperable-and-scalable-card-based-agentic-payments/) |
| AEP — A-Comm Evidence Protocol | Tamper-evident hash chain of transaction evidence, exported for disputes | v1.0.3-rc.2 draft | [A-Comm-Tech/a-comm-evidence-protocol](https://github.com/A-Comm-Tech/a-comm-evidence-protocol) |
| A2WP | Agent-to-Wallet Protocol: an agent relays credential requests to the user's wallet. Not payments | Individual Internet-Draft -01, 17 Oct 2026 | [draft-senarath-a2wp](https://datatracker.ietf.org/doc/draft-senarath-a2wp/) |
| HAPS | Human Approval and Presence Specification (iProov): signed consent credential for an action. Matched on acronym | Experimental draft, 17 Sep 2026 | [iProov/HAPS](https://github.com/iProov/HAPS) |
| Mastercard Agent Pay | Card programme with Agentic Tokens; merchants recognise agents through Web Bot Auth | Programme; registration required, no open spec found | [Mastercard newsroom](https://newsroom.mastercard.com/news/press/2025/april/mastercard-unveils-agent-pay-pioneering-agentic-payments-technology-to-power-commerce-in-the-age-of-ai) |

**In our map, not scored here:** L402, KYAPay (Skyfire), Baselayer KYA, ANS, AGNTCY, Stripe Shared Payment Tokens, Amex Intent Intelligence and cheqd. Several bear directly on the Identity heading:
- Baselayer and KYAPay verify the owner and deployer.
- ANS issues assurance-tiered identity certificates.
- cheqd provides trust registries and status lists.

## What this means for our capability map

The map records which protocol owns each capability (full or partial). It does not list everything each protocol does, so it is not a substitute for this rubric. Comparing the two suggests these candidate additions to the map, each to be confirmed before changing `generate.py`:
- **TAP:** per-request proof and holder-of-key binding (it signs with Web Bot Auth), plus agent identification to the business.
- **x402:** receipts, via the `offer-and-receipt` extension, as partial.
- **KYA-OS:** an append-only transparency log via the optional Audit Assurance Profile, as partial.
- **Verifiable Intent:** signed action evidence under receipts and dispute evidence.

## Limitations

- **Part 1 was scored in one pass; Part 2 had a second, independent review.** For Part 1, the criteria the scorers marked as unsure are flagged in the group files. For Part 2, cells the reviewer still considers contestable are listed in [chain-review.md](chain-review.md). The main ones:
  - x402's grant and trust anchor (L4, L9);
  - MPP's redress (L8);
  - AP2's continuity under its platform-signed mode (L10);
  - KYA-OS's "ultimately accountable" Responsible Party (L8), which would give KYA-OS a chain of 1;
  - whether Verifiable Intent and TAP make the principal identifiable.

  No plausible change to these cells makes any chain complete.
- **Visa TAP has no normative specification.** It was scored from Visa's developer pages. Visa Intelligent Commerce features whose fields were not read are not credited.
- **Stack scores are read from the specifications.** "If joined as proposed" rows are upper bounds for joins that do not exist yet. Only stack 5, PAP + Web Bot Auth with UCP and MCP, was checked against live deployments. Reviewer notes are in [stacks-common-review.md](stacks-common-review.md).
- **Contestable cells beyond payments** are listed in [general-review.md](general-review.md) and [stacks-common-review.md](stacks-common-review.md). The main ones:
  - UCP's order webhooks as evidence for non-payment actions, which the PAP + UCP chain of 1 depends on;
  - treating payment-only joins as carrying nothing;
  - MPP's score combining two of its payment methods.
- **Practice evidence is partly secondary.** Some vendor pages would not load, so a few claims rest on press coverage and are marked as such in [evidence-vendor-stacks.md](evidence-vendor-stacks.md). Code co-occurrence counts are estimates from GitHub code search and include vendor sample repositories.
- **Working-file references.** Some score files mention local working paths (for example `cmp2/src/`). Those were local copies of the sources and are not committed.
- **The rubric is ours.** Its criteria are our reading of the four headings and the ten links. A different, equally reasonable set of criteria would move individual cells. Because the criteria and citations are published, any cell can be challenged on the text.
- **Specifications change.** Scores are as read on 25 Nov 2026.
