# Chain rubric: an end-to-end trust chain for agentic commerce

The four-heading rubric ([rubric.md](rubric.md)) asks whether a protocol has each piece. This rubric asks whether the pieces form a chain that a merchant, an auditor or a court could follow from the person behind an agent to the money that moved. It also asks whether each party in that chain can be identified and held responsible.

## Scoring

Each link scores:

- **2 — met.** Every test for the link is met by the protocol's core specification. A normative (MUST) dependency on an external standard counts as core.
- **1 — partial.** Some tests are met, or tests are met only by an optional extension, profile or SHOULD/MAY requirement.
- **0 — absent.** No test is met, or the spec says the link is out of scope or leaves it to another party without naming how.

Cite the section, field or heading for every link. A roadmap item or "future work" scores 0. Say which tests are met and which are not.

The **chain score** is the lowest link score: one missing link means the chain is not complete. Totals are also reported to show breadth.

## Links

**L1 Principal identity**
- P1 The principal (the person or organisation the agent acts for) is *identifiable*. The counterparty can tell who it is, or a named party can resolve a pseudonymous identifier to a real party on request, such as in a dispute. A self-asserted name or email does not meet P1.
- P2 The principal's identity is verified by a third party (issuer, KYC/KYB provider, identity provider, card issuer).
- P3 The verifying party is itself accountable: it is named in the artefact and accredited or listed under a trust framework, registry or scheme.

**L2 Operator identity** (the company running the agent, or the agent provider)
- O1 The operator is identifiable in the same sense as P1. A bare domain or URL with no attestation of who controls it is partial.
- O2 The operator's identity is verified by a third party.
- O3 The verifying party is accountable, as in P3.

**L3 Agent key binding**
- K1 The agent's signing key is bound to the operator or principal by a statement from an accountable party, not only self-published.
- K2 The key's validity (rotation, revocation, expiry) can be checked as at the time of use, including after the fact.

**L4 Delegation**
- D1 An explicit grant artefact states what the agent may do.
- D2 The grant can carry constraints: amount, payee or merchant, time window, scope.
- D3 The grant is signed by the principal or the principal's own authenticator. A token issued by a platform or payment provider on the principal's behalf is partial.
- D4 The grant expires or can be revoked.
- Note separately (not required for a 2): D5, multi-hop sub-delegation with narrowing scope.

**L5 Session authentication**
- S1 Proof of possession of the agent's key per request or per session.
- S2 Replay protection (nonce, timestamp window, `jti`, DPoP).
- S3 Human presence or consent is captured, with an assurance level, when the grant is made or before a high-risk action.

**L6 Action conformance**
- A1 The action or transaction references the grant it relies on.
- A2 The counterparty can verify, before acting, that the action falls within the grant's constraints.

**L7 Evidence**
- E1 A record of the action is signed by an identifiable, accountable party.
- E2 The record carries a time that a third party can rely on (trusted timestamp, ledger time, or a signed time from an accountable party).
- E3 The record can be re-verified later: the spec addresses retention, or the key and credential status needed to verify it stay available.

**L8 Redress**
- R1 Liability is allocated between named roles (principal, operator, agent provider, issuer, merchant, payment provider).
- R2 There is a dispute or refund path: native to the protocol, or delegated to a named rulebook (for example card scheme rules) with the protocol's evidence mapped to it. Delegation to a named rulebook without that evidence mapping is partial.

**L9 Trust anchor**
- T1 The spec references a registry, trust list or governance framework that says which issuers, operators or agents are trusted.
- T2 There is a revocation or status mechanism for the credentials or keys the chain relies on.

**L10 Continuity**
- C1 The same principal, by identifier or cryptographic link, appears in the identity, the grant and the action record.
- C2 Each artefact cryptographically references the one before it: the grant references the identity credential, the action references the grant, and the record references the action (by hash or signature over the predecessor).

## Stacks

Protocols are deployed together, so stacks are scored too. For links L1 to L9, a stack scores the best score any member achieves, *provided the specs define how the members fit together*. For L10, score whether continuity holds across the members' boundaries: does an artefact from one protocol reference the other's artefact, by a mechanism defined in at least one of the specs?
