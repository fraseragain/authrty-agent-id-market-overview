# Rubric: four-dimension coverage of agentic commerce protocols

Scores one protocol on four dimensions, each 0 to 4, so it can be shown as a Harvey ball (0 = empty, 1 = quarter, 2 = half, 3 = three-quarter, 4 = full). Each dimension has four yes/no criteria. Each criterion scores:

- **1** — met by the protocol's core specification.
- **0.5** — met only by an optional extension or profile the same spec defines, or met in part (say which part is missing).
- **0** — not met, or the spec delegates it entirely to something outside the protocol (for example "the payment network handles disputes" with no protocol artefact).

Score from the specification text, not from marketing or roadmaps. A roadmap item, "future work" or "out of scope" note scores 0. If you cannot find or read the spec, say so and score from the best primary documentation you can find, marking the basis as `docs` rather than `spec`.

## Identity — the natural or legal person behind the agent, and how that person is verified

- **I1 Principal conveyed.** A protocol artefact carries an identifier for the person or organisation the agent acts for to the counterparty (a user ID, account link, subject claim, buyer object).
- **I2 Operator conveyed.** The operator or deployer of the agent (the company running it) is identified to the counterparty by a protocol artefact, not just by a bilateral onboarding contract.
- **I3 Third-party verified.** The principal's or operator's identity is attested by a third party (credential issuer, KYC/KYB provider, certificate authority, card network, identity provider), not self-asserted.
- **I4 Legal-person grade, checkable.** That attestation is tied to a real-world legal identity (a verified natural person or a registered legal entity) and the counterparty can verify it cryptographically itself.

## Authentication — how the principal or their agent proves it is them

- **A1 Proof of possession.** The agent (or its operator) proves control of a private key bound to its identity or credential.
- **A2 Verifiable key discovery.** The verifier can obtain the key from a published, resolvable source (JWKS URL, DID, certificate chain, key directory) rather than a bilateral exchange.
- **A3 Freshness.** Replay protection on each request or session (nonce, timestamp window, `jti`, DPoP).
- **A4 Principal authentication bound to the agent.** The human or organisation authenticates (OAuth sign-in, passkey, issuer step-up) and the protocol binds that result to the agent or its credential.

## Authorisation — how the agent proves it has authority to act for the principal

- **Z1 Explicit grant artefact.** A defined object or token states what the agent may do (mandate, scoped token, delegation credential).
- **Z2 Constraints.** The grant can express limits: amount, merchant or payee, time window, scope of operations.
- **Z3 Principal-signed.** The grant is signed by the principal's own key or authenticator, so the counterparty can verify it without trusting the agent or its operator. A token issued by a platform or payment provider on the principal's behalf scores 0.5.
- **Z4 Lifecycle.** The grant expires or can be revoked, or can be sub-delegated with narrower scope.

## Accountability — who resolves customer issues, redress and liability

- **C1 Action record.** The protocol produces a record that links the action or transaction to the grant or the identity behind it (receipt, signed order, action proof).
- **C2 Non-repudiation.** That record is signed or otherwise tamper-evident.
- **C3 Redress.** The protocol defines a dispute, refund or chargeback path, or allocates liability between parties.
- **C4 Third-party audit.** An independent party can check after the fact: a transparency log, public registry, reputation record, or status list.

## What to return per protocol

For each protocol: spec name, version and URL read; basis (`spec` or `docs`); then a table of the 16 criteria with score (1 / 0.5 / 0) and a one-line justification that cites the section, field or heading in the source. Then the four dimension totals. Flag any criterion where you are unsure.
