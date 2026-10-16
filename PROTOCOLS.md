# Protocols tracked

Every protocol that appears in the capability map ([`generate.py`](./generate.py)), with who stewards it, where it is documented and how firm the ratings are. Ratings are the author's assessment (October 2026).

**Rating basis:** *Spec* means the specification was read. *Secondary* means rated from announcements, blog posts or press. *Provisional* protocols render with dashed chips on the map.

| Protocol | Steward | What it does | Status | Documentation | Rating basis |
|---|---|---|---|---|---|
| A2A | `a2aproject` (Linux Foundation) | Agent Card discovery, messages, tasks, extensions | v1.0.1 (28 May 2026) | [github.com/a2aproject/A2A](https://github.com/a2aproject/A2A) | Spec |
| MCP | Anthropic-originated open standard | Tool and data access for agents | Released | [modelcontextprotocol.io](https://modelcontextprotocol.io) | Secondary |
| KYA-OS | Decentralized Identity Foundation | Entity Card, `proof.v1`, delegation credentials, `cnf` binding | `@kya-os/mcp` 1.16.2 | [github.com/decentralized-identity/kya-os-mcp](https://github.com/decentralized-identity/kya-os-mcp) | Spec |
| KYAPay | Not stated on the page read | `kya`, `pay` and `kya-pay` JWTs | Not recorded | [kyapay.org](https://kyapay.org/overview/the-agentic-protocol-stack) | Secondary |
| Baselayer KYA | Baselayer (commercial) | Who deployed an agent, whom it represents, what it may do | Closed, no public spec found | [Crunchbase coverage](https://news.crunchbase.com/ai/verifying-ai-agents-baselayer-35m-raise/) | Secondary |
| ANS | Independent submission | DNS-anchored agent names, identity certificates, transparency log, assurance tiers | Internet-Draft `draft-narajala-courtney-ansv2-01`, expired | [datatracker.ietf.org](https://datatracker.ietf.org/doc/draft-narajala-courtney-ansv2/) | Spec |
| Web Bot Auth | IETF working group | RFC 9421 request signatures, `Signature-Agent`, JWKS key directory | Internet-Draft `draft-ietf-webbotauth-httpsig-protocol-00` | [datatracker.ietf.org](https://datatracker.ietf.org/doc/draft-ietf-webbotauth-httpsig-protocol/) | Spec |
| **PAP (Poppy)** | Sierra and Meta (authors Bret Taylor, Clay Bavor) | Business-hosted `/.well-known/poppy.json` discovery, guest and signed-in sessions via OAuth, customer-approved access | Draft 0.1, published 9 Oct 2026; 35 design partners | [personalagentprotocol.org](https://personalagentprotocol.org/), [Sierra announcement](https://sierra.ai/blog/poppy) | Secondary, provisional |
| **x401** | Proof | HTTP 401 identity challenge answered with Verifiable Credential presentations and a user-signed authorisation mandate; complements x402 | Emerging, open; Proof's Digital ID is the first live implementation | [x401.id](https://x401.id), [Proof launch post](https://www.proof.com/blog/introducing-x401) | Secondary, provisional |
| AP2 | Google | Intent, checkout and payment mandates, `cnf` key binding | v0.2.0 (28 Apr 2026) | [github.com/google-agentic-commerce/AP2](https://github.com/google-agentic-commerce/AP2) | Spec |
| UCP | Google | Business capability manifest, checkout and order semantics | Not recorded | Google developer blog (link not recorded) | Secondary |
| ACP | OpenAI | Checkout in ChatGPT | Not recorded | Link not recorded | Secondary |
| TAP | Visa | Card-network agent payments | Not recorded | Link not recorded | Secondary |
| x402 | Not recorded | HTTP 402 payment request, stablecoin settlement | Not recorded | [x402.org](https://x402.org) | Secondary |
| MPP | Not recorded | Session and streaming payments, multiple payment methods | Not recorded | Link not recorded | Secondary |
| L402 | Lightning Labs | HTTP 402 with Lightning and macaroons | Not recorded | Link not recorded | Secondary |
| cheqd | cheqd | `did:cheqd`, DID-Linked Resources, status lists, trust registries | Live network | [docs.cheqd.io](https://docs.cheqd.io) | Spec |

## Notes

- **PAP and Poppy are the same protocol.** Poppy is the nickname; PAP is the formal name. Meta's Muse agent was the live-demo agent at Sierra Summit (6 Oct 2026). It is not a separate protocol.
- **x401 proves the human principal, not the agent.** The agent inherits the human's identity. On the map that is why x401 owns owner verification and human-to-agent authority but not agent identity credential.
- **Revisit when specs are read.** PAP draft 0.1 and the x401 specification at x401.id have not been read. Every PAP and x401 rating should be checked against them.
- **Source repo:** the map and its history come from [`cheqd/agent-toolkit`](https://github.com/cheqd/agent-toolkit/tree/main/docs/research/tools/capability-map). Rows marked "not recorded" were not captured in that repo's landscape notes.
