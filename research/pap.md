# Personal Agent Protocol (PAP, "Poppy"): research note

Researched 16 Oct 2026 and updated 19 Nov 2026. The update is the next section. Everything after it is the original note on draft 0.1, kept as a record, with corrections marked where 1.0 changed the picture.

## Update, 19 Nov 2026: version 1.0 is published

**PAP is no longer a draft.** Version 1.0 was published and frozen on 14 Nov 2026, five weeks after draft 0.1. The changelog says to build against 1.0, and that later 1.x versions add features without breaking 1.0 implementations. Draft 1.1 opened on 17 Nov.

| Version | Published | Notes |
|---|---|---|
| 0.1 | 9 Oct 2026 | First draft, as reviewed below |
| 0.2 | 24 Oct 2026 | Security considerations section, standard OAuth metadata for scopes and sign-in types, Session Keys, Mediated Sign-In marked transitional |
| 0.3 | 4 Nov 2026 | UCP extension, skills index, auth-disabled Companies |
| 0.4 | 10 Nov 2026 | Published as the 1.0 release candidate: version negotiation, Browser Control extension, Operations version 3 |
| **1.0** | **14 Nov 2026** | 0.4 plus fixes: optional Pushed Authorization Requests (RFC 9126), PS384 required alongside ES256, consent shown for every scope, same DPoP key at refresh |
| 1.1 (draft) | opened 17 Nov 2026 | Replacing a User ID, Web Bot Auth operator signatures at OAuth endpoints, `offline_access` handling |

Sources: [`content/versions/versions.json`](https://github.com/personal-agent-protocol/personal-agent-protocol/blob/main/content/versions/versions.json) and the [changelog](https://personalagentprotocol.org/docs/changelog) in the spec repository, read 19 Nov 2026, and [Sierra's 1.0 post](https://sierra.ai/blog/releasing-poppy).

### What changed that matters for the capability map

Sections 1, 4.1, 5.2 to 5.3, 8.1 and 10 of the 1.0 spec, the changelog for 0.2 to 1.1 and the Operations extension's section 8.1 were read.

- **Agent identity is still a URL with keys.** The `client_id` is still an HTTPS Client ID Metadata Document with a `jwks_uri`. Two additions: Session JWTs are now signed by short-lived **delegated keys**, one per User ID, vouched for by a delegation JWT signed with a `jwks_uri` key (5.2); and the agent SHOULD add a **Web Bot Auth operator signature** (RFC 9421) so bot-management at the edge can recognise the operator (5.3). There is still no credential, attestation of the operator, registry or reputation signal. Which agents a Company accepts remains outside the spec (4.1). The map's ratings for agent identity (partial) and holder-of-key binding (full) stand.
- **Approvals are still unsigned.** In the Operations extension an approval is "user approved" or "agent approved", and the Company relies on the agent's word for how it was given (Operations 8.1). Signed approvals and mandates (for example "transfers of up to $50 a week") are first on the roadmap, not in 1.0. The map does not rate PAP on mandate authorisation or spend limits.
- **Payments go through UCP.** The UCP extension, which Sierra says Shopify co-authored, hands carts, checkout and payment to UCP while PAP handles discovery and sign-in. Payments in general remain a roadmap item. The map does not rate PAP on commerce capabilities UCP already owns.
- **Conversations are still PAP's own format.** `poppy` is the only defined conversation type in 1.0 (8.1). A2A is not listed.
- **Mediated Sign-In is now an extension, marked transitional,** with removal planned for 17 Mar 2027. Direct Sign-In is the preferred type.

No rating on the map changes. The rating basis moves from draft 0.1 to version 1.0.

### Review findings from October: what 1.0 did with them

| Finding (Oct 2026) | In 1.0 |
|---|---|
| No Security Considerations section (#4) | Section 10 added: content from Companies treated as untrusted, secrets kept out of model context, what a domain vouches for, assertion audiences, delegated-key security, sign-ins someone else started |
| Mediated Sign-In hands the agent the user's password (#5) | Moved to an extension, transitional, with a removal date of 17 Mar 2027 |
| One issuer shared by many companies merges them (#3) | One issuer per Company required (commit #54), plus a guide for hosting several Companies |
| Client-assertion `aud` unspecified (#2) | `aud` MUST be the Company's issuer as a single string, compared character for character; assertions last at most 5 minutes (4.1) |
| Contradictory signed-out sign-in rules (#8) | Signed-out rules gathered in one section; not rechecked against the original report |

These are the spec authors' fixes as described in the changelog. I did not ask the original reviewer whether they consider them closed.

### Partners and governance

- **Design partners: 102 listed** on the spec site's introduction page (19 Nov), up from 43 on 16 Oct. Sierra's post says 60 joined with 1.0, "bringing the total to more than 100". Technology providers are no longer listed separately. New names include Affirm, Checkout.com, Cisco, Delta Air Lines, Descope, Intuit, Manus, Mercury, Persona, Ping Identity, Salesforce (Fin, Commerce Cloud and Agentforce), Socure, Turkish Airlines, Twilio, Wayfair, WorkOS and Zoom.
- **Still absent:** Anthropic, Google, Amazon, Apple, Microsoft and JPMorgan are not on the list.
- **Governance: unchanged.** No standards body, foundation or governance structure is named in the spec repository or in Sierra's 1.0 post, and searches found no announcement of one. Development now happens in a private repository: only `main` is mirrored to the public one (commit #171), so pull-request numbers in public commits point to the private repository. The public repository has three committers (one Sierra-side author with 148 commits, one with 10 on the site and demos, and the author of the UCP extension, which Sierra says Shopify co-authored).
- **Spec repository:** 158 stars, 23 forks, 159 commits on `main`, 112 issues filed (19 Nov), against 20 stars and 10 issues on 16 Oct.

### Adoption: the first live files

On 16 Oct no partner domain served a `poppy.json`. On 19 Nov I requested `/.well-known/poppy.json` from 36 partner and project domains plus a few claimed deployments.

| Domain | Result |
|---|---|
| **Shopify stores** (Allbirds, Kylie Cosmetics and Brooklinen checked) | Live, version 0.4. Each file is the same shape: a UCP agent endpoint, the UCP extension and one scope, `dev.ucp.shopping.checkout:manage`. This matches Sierra's claim that every Shopify store now publishes a file automatically. `shopify.com` itself returns 404 |
| **Mercury** (`mercury.com`, `app.mercury.com`) | Live, version 0.4. An MCP API at `mcp.mercury.com` with scopes for reading accounts, requesting transactions and transfers, budgets and receipts |
| **Rocket** (`rocket.com`, `rocketmortgage.com`) | Live, version 0.3. Signed out only: one MCP API for mortgage education and sample rates, and a feedback endpoint. No sign-in |
| Stacktree (`stacktr.ee`) | Live, version 1.0, with 0.3 and 0.4 also offered. Not a listed design partner |
| Demo stores (Cliffside Retail, Print with Poppy) | Live, versions 1.0 and 0.4. Listed on the spec site as community demos; Print with Poppy takes real orders |
| Turkish Airlines | Not reachable from here (timed out), so Sierra's "live" claim is unchecked |
| Synchrony | 404. Sierra's post describes Synchrony's work as exploratory, not live |
| Other partners checked | 404 from Sierra, Meta, OpenAI, Bank of America, Walmart, Target, Hertz, Nordstrom, Wells Fargo, Stripe, Cloudflare, Zapier, Notion, Wayfair, Lemonade, Wix, PayPal, BBVA, Cigna and others. 403 (unknown) from GEICO, Chime, Hyatt, SoFi, Intuit and Comcast |

On the agent side, Sierra says Poppy "is now on for everyone who uses Muse", Meta's agent, which "automatically looks for Poppy first on every site it visits". That is Sierra's claim; I found no Meta post on 1.0 and did not test Muse. No other personal agent (OpenAI, Instinct, Manus) was found announcing support.

There is still **no official SDK or reference implementation**. The spec site offers an implementation kit and a validator, and lists three community demos (none endorsed). Community repositories remain small: Datalayer's SDK has 5 stars, the Poppy Demo Agent 3, Print with Poppy 2. GitHub search returns 36 repositories for "poppy personal agent protocol".

**Reading, 19 Nov:** PAP has moved from announced to deployed at scale on one platform. If Sierra's claim holds for every Shopify store (I checked three), a very large number of stores now serve `poppy.json`, but those files only point to UCP. Outside Shopify, two named design partners (Mercury, Rocket) serve real files, one of them signed-out only. Most of the 102 partners serve nothing yet. Governance is still a single vendor's project.

## Original note, 16 Oct 2026 (draft 0.1)

Draft 0.1 of the specification was read in the [source repository](https://github.com/personal-agent-protocol/personal-agent-protocol) (commit of 15 Oct 2026): sections 1 to 6, 7.1 to 7.2 and 7.8 to 7.9 in detail, plus the path-to-1.0, extensions, operations and guides pages. Conversation message formats (7.3 to 7.7, 7.10 to 7.13) were skimmed, not reviewed. Section numbers in this part refer to draft 0.1.

### What it is

A protocol for a **personal agent acting for one user** to work with **a company** (a business that implements it). It is business-facing: it covers how an agent finds a company, identifies itself, gets the user's permission and then uses the company's website, APIs or its own agent. It is not an agent-to-agent protocol like A2A, and it does not define payments.

| Part | What the draft says |
|---|---|
| Discovery | The company publishes `/.well-known/poppy.json` over HTTPS. The `organization.domain` must match the host requested. It lists sign-in types, APIs (OpenAPI or MCP), a company agent, and a web browser-session endpoint |
| Company identity | The company's OAuth issuer, checked against `poppy_domains` in its RFC 8414 metadata. This stops one domain claiming another company's issuer |
| Agent identity | The agent's `client_id` is an HTTPS URL returning a metadata document (the OAuth Client ID Metadata Document draft, also used by MCP) with a `jwks_uri` and redirect URIs. Companies may require registration, allowlist or block by `client_id`, and rate-limit by it. Registration is out of scope |
| User identity | A per-company opaque **User ID** chosen by the agent, so a company recognises a returning user while signed out but companies cannot link users. It must not derive from personal information |
| Sessions | One user, one company, one agent. Starts signed out via an RFC 7523 JWT bearer assertion. Session tokens are short-lived and **DPoP-bound** (RFC 9449) on every API and conversation request; Bearer tokens are allowed only for MCP |
| Sign-in | Direct (OAuth in the user's browser), Device (RFC 8628 code) or **Mediated** (the agent sends the user's credentials to the company). Scopes `poppy:read` and `poppy:write`, plus company-defined scopes. The long-lived **Account Token** is an OAuth refresh token, revocable at an RFC 7009 endpoint |
| Web browsing | The agent's browser posts a signed `poppy-browser+jwt` assertion and the company sets its own cookie for the same session |
| Conversations | Messages to the company's agent over HTTPS with a `sender` field saying whether a human or an AI wrote each message; handoff to a person; Direct Conversations where the user talks to the company |
| Extensions | Named extensions advertised in `poppy.json` and in the agent's metadata. One is defined: **operations** (propose, approve exact terms, confirm, track; at-most-once) |

Standards reused: OAuth 2.0 and its RFCs, JWT, DPoP, OpenAPI 3.1, MCP 2025-06-18, RFC 9728. It defines almost no new cryptography of its own.

### Who is behind it

- **Sierra** (announcement credits Bret Taylor and Clay Bavor) and **Meta**, announced 6 Oct 2026 at Sierra Summit, [draft 0.1 published 9 Oct](https://sierra.ai/blog/poppy). The specification, site and repository name no authors or editors.
- The GitHub organisation was created on 13 Oct 2026, has no public members, and the repository's only commit history visible to me was from one committer. Licence is Apache-2.0 and contributions fall under separate terms on the site (not read).
- **No standards body or governance structure is named** anywhere I found. [Constellation Research](https://www.constellationr.com/insights/news/meta-sierra-pitch-personal-agent-protocol-govern-how-personal-ai-agents-deal-business) also notes this. Contrast: A2A is a Linux Foundation project, x402 is under a foundation, AP2 was reported donated to the FIDO Alliance.
- Stated motive, from Sierra and Meta: businesses currently either block agents or let them do anything the user can; PAP gives a middle path. Meta's Muse agent was the live-demo agent (with Rocket) at Sierra Summit.

### Design partners

The [path-to-1.0 page](https://personalagentprotocol.org/docs/path-to-1) lists 43 partners that agreed to be listed. Sierra's post says 35 were added with the draft on top of those announced earlier, so the totals differ by source.

- **Personal agents (3):** Instinct, Meta, OpenAI.
- **Companies (21):** Bank of America, BBVA, Chime, Cigna, Comcast, DIRECTV, FOX, Gap Inc., GEICO, Hertz, Insurify, Liberty Mutual, Nordstrom, PayPal/Venmo, Rocket, SiriusXM, Synchrony, Target, United Airlines, Walmart, Wells Fargo.
- **Technology providers (19):** 1Password, Adyen, Atomic, Cloudflare, ElevenLabs, Genesys, Klaviyo, Mastercard, NiCE, Notion, Okta, OneSignal, Plaid, Shopify, Sierra, Stripe, Visa, Zapier, Zendesk.

Notable absences: Anthropic and Google are not listed (one source says Anthropic is absent). JPMorgan is not listed. Reported on 15 Oct, [JPMorgan's Jamie Dimon said the bank blocks outside AI agents from accounts](https://finance.yahoo.com/technology/ai/articles/don-t-want-rogue-agents-181013092.html) ("You don't want rogue agents"), and Meta pointed to Poppy as its answer. Amazon was reportedly blocking Muse in September (single source).

### Adoption evidence, 16 Oct (all within days of publication)

| Signal | Finding |
|---|---|
| Live `poppy.json` files | I requested `/.well-known/poppy.json` on 18 partner and project domains on 16 Oct. **None returned a poppy.json document.** Twelve returned 404, three (Rocket, GEICO, Chime) returned 403 so are unknown, one redirected, one was unreachable, one returned an unrelated HTML page. Even the protocol's own domains had none |
| Official reference implementation | None yet. Promised "over the next month". The site has no JSON Schema or conformance suite (per a third-party README) |
| Community implementations | All created 9 to 10 Oct: [datalayer/personal-agent-protocol](https://github.com/datalayer/personal-agent-protocol) (Python and TypeScript SDK, 3 stars), [pi-poppy](https://github.com/richardanaya/pi-poppy) (1), [poppyseed](https://github.com/akshay5995/poppyseed) (Next.js, with a conformance checker, 0 stars, self-described as unaffiliated), plus experimental pull requests in an auth framework and an agent harness, and several zero-star validators |
| Spec repo | 20 stars, 1 fork, 10 issues and 1 pull request in the first two days, mostly review feedback |
| Production use | None found. One live demo (Muse and Rocket mortgage pre-approval) |

Reading: heavy launch-week interest from the ecosystem, a large announced partner list, and no evidence yet of any company actually publishing a file or a personal agent shipping against it.

### Review findings already filed against the draft

Ten issues were open within two days. Five are security reports from one reviewer. I read the summaries of #2 to #5 and #8:

- The draft has **no Security Considerations section**. The reviewer's first example is prompt injection between agents: everything a company returns goes into the personal agent's model, which holds the user's context and other open sessions (#4).
- **Mediated Sign-In** gives the agent the user's raw password, and its endpoint comes only from `poppy.json`, which can be served through a redirect, not from the issuer-checked OAuth metadata (#5).
- A hosting provider using one issuer for many companies merges them into one "company" and links users across them (#3; a pull request on company isolation is open).
- Possible replay of a client assertion at another company if `aud` is unspecified for client assertions (#2; section 4.2 does fix `aud` for the session assertion, so this concerns the client assertion only).
- Contradictory rules about whether a signed-out session can sign in to a different account (#8).

These are one reviewer's claims against a day-old draft. I checked that the draft has no Security Considerations section and that Mediated Sign-In works as described. I did not verify the other findings.

### Where it overlaps and differs in the capability map

- **Agent identity is thin by design.** An agent is a URL with keys. There is no credential, no attestation of who operates it, no registry, and no trust or reputation signal. Companies decide who to allow themselves, by `client_id`.
- **Strong on per-request proof.** DPoP gives holder-of-key binding, per-request proof and replay protection with `jti` and optional server nonce. This is more than most protocols in the map specify.
- **Delegation is coarse.** The user grants account scopes and the agent holds a refresh token. There is no signed, constrained delegation credential. The operations extension adds approval of exact terms per action; I did not read how that approval is recorded or whether it is signed.
- **Payments are explicitly out of scope** (an open topic). It could sit above x402, AP2 or UCP rather than compete with them. UCP overlaps on business capability discovery.
- **Agent-to-agent conversation uses its own `poppy` protocol.** A2A is not a listed conversation type in 0.1, though the list is extensible.

### Not checked

- Conversation message formats and error handling in full, and the operations extension beyond its overview.
- The site's contribution terms and any governance statement beyond the pages read.
- Whether the 403 and redirect responses from partner domains hide a real file.
- Claims in secondary coverage that I could not trace to Sierra or Meta (Amazon blocking Muse; Anthropic absent from the partner list).
