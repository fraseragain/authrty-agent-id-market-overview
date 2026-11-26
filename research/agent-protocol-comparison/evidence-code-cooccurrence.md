# Agent protocol co-occurrence in open-source code

Date run: 2026-11-25 (UTC). Tools: `gh api` (authenticated), npm registry, PyPI, deps.dev. Nothing was created or edited on GitHub.

## Headline caveats (read first)

- **GitHub code search is per file, not per repo, and is not exact.** `total_count` is a file count, capped at 1,000 retrievable results and 100 per page. I read only page 1 (100 results) per query, so "repos" below are distinct repos in that sample (exact only when total_files <= 100; marked `lower bound` otherwise). Forks are excluded by GitHub default. Monorepos with several manifests, and repos with deps split across manifests (e.g. MCP in one package.json, x402 in another), are undercounted or double counted.
- **Marker noise.** Code search tokenises terms, so `"x402"` also matches `@x402/core`, `x402-fetch`, names, descriptions and examples (12,256 package.json files vs 269 npm dependents of the `x402` package on deps.dev). Python `mcp` is a very short token (121,088 pyproject files) and matches far more than the PyPI `mcp` dependency. Treat MCP, x402 and A2A single counts as inflated; pairs involving rare markers (UCP, ACP, KYA, x401, TAP, L402, MPP, WBA) are precise but small.
- **Vendor/sample repos inflate counts**: e.g. google-agentic-commerce/AP2 and a2a-x402, wevm/mppx, x402-foundation/x402, cloudflare/agents, solana-foundation/pay, the A2A/MCP SDK example repos. Several single-author crypto-agent mega-repos (nirholas/*, LeoYeAI/agent-master-skills) pull in many protocols at once.
- **Spam/mass-generated repos** are present (agent-skill collections, scaffolds). I did not filter them.
- **Topic counts** are self-labelled and include repos with no code dependency. Topics `ucp`, `acp`, `mpp`, `a2a` are ambiguous (other meanings); the specific alias (`universal-commerce-protocol`, `agentic-commerce-protocol`) gives much smaller numbers. Topic counts for aliases overlap, so I report the maximum, not the sum.
- **Not covered by manifests**: AP2 (the PyPI/npm `ap2` packages are unrelated third-party projects, so I used the marker `google-agentic-commerce` in pyproject.toml/requirements.txt only, i.e. git dependencies on that org; AP2 via imports is not captured), ACP (`delegate_payment` is code, not a manifest; only `@agentic-commerce-protocol/specification` searched, 1 package.json hit), Visa TAP (npm `trusted-agent-protocol` unpublished; 3 package.json hits), ERC-8004 npm marker `erc-8004` only (contract-level use via Solidity is not captured), KYA-OS marker `@kya-os` (prefix; tokenised). PyPI has no packages for ACP, ERC-8004, KYA-OS, MPP, TAP, x401 markers I could verify, so those were npm-only.
- **Dependents cross-check (step 2):** libraries.io returns "Disabled for performance reasons" without a key; npmjs.com dependents pages return 403. deps.dev v3alpha gives dependent *counts* per package version (not lists, so no pair cross-check is possible). Counts on 2026-11-25 (latest version): @modelcontextprotocol/sdk 88,024 (78,339 direct); @a2a-js/sdk 126 (75 direct); x402 269 (83 direct); @coinbase/x402 61 (59 direct); l402 1; web-bot-auth 11 (7 direct); mppx and @kya-os/mcp-i not found. These are packages (not repos) depending on the package, so consistent in scale with the MCP and A2A code search counts and show the x402 code search count is inflated by roughly 40x by tokenisation and non-dependency mentions. PyPI download volume for x402 (pypistats): ~324k last month.

## Markers used (verified against registries)

| Protocol | npm marker (package.json) | PyPI marker (pyproject.toml, requirements.txt) | Notes |
|---|---|---|---|
| MCP | `@modelcontextprotocol/sdk` (v1.32.2) | `mcp` | PyPI token very noisy |
| A2A | `@a2a-js/sdk` (1.3.0) | `a2a-sdk` | |
| AP2 | none (npm `ap2` is unrelated) | `google-agentic-commerce` (git deps) | PyPI `ap2` is a third-party package (whillhill/ap2), not Google |
| UCP | `@ucp-js/sdk` (from Universal-Commerce-Protocol/js-sdk) | `ucp-sdk` | |
| ACP | `@agentic-commerce-protocol/specification` | none | spec repo only |
| x402 | `x402` (matches x402-*, @x402/*, @coinbase/x402 by tokenisation) | `x402` | |
| MPP | `mppx` | none | |
| L402 | `l402` | `l402` | |
| Web Bot Auth | `web-bot-auth` | `web-bot-auth` | |
| KYA-OS | `@kya-os` | none | |
| x401 | `@proof.com/x401-node` | none | |
| Visa TAP | `trusted-agent-protocol` | none | |
| ERC-8004 | `erc-8004` | none | |

## Single-protocol manifest counts (files, GitHub code search)

| Protocol | package.json | pyproject.toml | requirements.txt |
|---|---|---|---|
| MCP | 129280 | 121088 | 82048 |
| A2A | 1190 | 4728 | 2464 |
| AP2 | - | 48 | 10 |
| UCP | 18 | 56 | 7 |
| ACP | 1 | - | - |
| x402 | 12256 | 1114 | 382 |
| MPP | 673 | - | - |
| L402 | 194 | 53 | 8 |
| WBA | 163 | 7 | 0 |
| KYA | 26 | - | - |
| x401 | 6 | - | - |
| TAP | 3 | - | - |
| ERC8004 | 509 | - | - |

Exact query form: `gh api -X GET search/code -f q='"<term>" filename:<file>' -f per_page=100`.

## Pair matrix (all 78 pairs with any signal, sorted by manifest files)

Manifest files = sum across package.json/pyproject.toml/requirements.txt where both terms are in the same file. Repos = distinct repos in the first 100 results per query (lower bound when files > 100 per query). Topic = max over alias topics.

| A | B | manifest files | manifest repos (sample) | lower bound? | topic repos |
|---|---|---|---|---|---|
| MCP | A2A | 2984 | 254 | yes | 1589 |
| MCP | x402 | 1670 | 164 | yes | 2086 |
| x402 | ERC8004 | 191 | 89 | yes | 214 |
| x402 | MPP | 160 | 85 | yes | 106 |
| MCP | MPP | 94 | 87 | no | 47 |
| A2A | x402 | 70 | 60 | no | 269 |
| MCP | ERC8004 | 61 | 59 | no | 121 |
| x402 | L402 | 51 | 31 | no | 48 |
| MCP | WBA | 35 | 35 | no | 8 |
| MCP | L402 | 24 | 19 | no | 66 |
| AP2 | x402 | 24 | 24 | no | 55 |
| A2A | AP2 | 18 | 16 | no | 34 |
| MCP | AP2 | 14 | 13 | no | 53 |
| MCP | KYA | 12 | 4 | no | 2 |
| MCP | UCP | 10 | 9 | no | 81 |
| AP2 | UCP | 8 | 5 | no | 20 |
| A2A | ERC8004 | 6 | 6 | no | 31 |
| x402 | WBA | 6 | 6 | no | 6 |
| A2A | UCP | 4 | 2 | no | 14 |
| A2A | MPP | 4 | 4 | no | 8 |
| A2A | KYA | 4 | 1 | no | 0 |
| UCP | x402 | 3 | 3 | no | 17 |
| A2A | WBA | 3 | 3 | no | 1 |
| MPP | L402 | 2 | 2 | no | 6 |
| x402 | x401 | 2 | 2 | no | 1 |
| MPP | ERC8004 | 2 | 2 | no | 1 |
| x402 | KYA | 2 | 1 | no | 0 |
| MPP | WBA | 2 | 1 | no | 0 |
| A2A | L402 | 1 | 1 | no | 7 |
| UCP | WBA | 1 | 1 | no | 1 |
| L402 | ERC8004 | 1 | 1 | no | 1 |
| MCP | x401 | 1 | 1 | no | 0 |
| A2A | x401 | 1 | 1 | no | 0 |
| x402 | TAP | 1 | 1 | no | 0 |
| WBA | ERC8004 | 1 | 1 | no | 0 |
| MCP | ACP | 0 | 0 | no | 363 |
| A2A | ACP | 0 | 0 | no | 53 |
| UCP | ACP | 0 | 0 | no | 34 |
| AP2 | ACP | n/a | n/a | no | 27 |
| ACP | x402 | 0 | 0 | no | 20 |
| AP2 | MPP | n/a | n/a | no | 8 |
| AP2 | L402 | 0 | 0 | no | 2 |
| AP2 | TAP | n/a | n/a | no | 2 |
| AP2 | ERC8004 | n/a | n/a | no | 2 |
| UCP | MPP | 0 | 0 | no | 2 |
| ACP | MPP | 0 | 0 | no | 2 |
| ACP | L402 | 0 | 0 | no | 2 |
| UCP | ERC8004 | 0 | 0 | no | 1 |
| ACP | WBA | 0 | 0 | no | 1 |

Pairs with zero in both measures are listed in the JSON. Per-pair exact queries are in `cooccurrence.json` (`method`, `topic_variants`) and the raw cache `cache.json`/`topics.json`.

## Topic-pair detail for the largest pairs (exact query, count)

- MCP+x402: `topic:mcp topic:x402` = 2086; `topic:model-context-protocol topic:x402` = 698
- MCP+A2A: `topic:mcp topic:a2a` = 1589; `topic:mcp topic:a2a-protocol` = 222; `topic:model-context-protocol topic:a2a` = 358; `topic:model-context-protocol topic:a2a-protocol` = 63
- MCP+ACP: `topic:mcp topic:agentic-commerce-protocol` = 8; `topic:mcp topic:acp` = 363; `topic:model-context-protocol topic:agentic-commerce-protocol` = 2; `topic:model-context-protocol topic:acp` = 48
- A2A+x402: `topic:a2a topic:x402` = 269; `topic:a2a-protocol topic:x402` = 25
- x402+ERC8004: `topic:x402 topic:erc-8004` = 214; `topic:x402 topic:erc8004` = 24
- MCP+ERC8004: `topic:mcp topic:erc-8004` = 121; `topic:mcp topic:erc8004` = 7; `topic:model-context-protocol topic:erc-8004` = 31; `topic:model-context-protocol topic:erc8004` = 0
- x402+MPP: `topic:x402 topic:mpp` = 106
- MCP+UCP: `topic:mcp topic:universal-commerce-protocol` = 28; `topic:mcp topic:ucp` = 81; `topic:model-context-protocol topic:universal-commerce-protocol` = 11; `topic:model-context-protocol topic:ucp` = 21
- MCP+L402: `topic:mcp topic:l402` = 66; `topic:model-context-protocol topic:l402` = 23
- AP2+x402: `topic:ap2 topic:x402` = 55
- MCP+AP2: `topic:mcp topic:ap2` = 53; `topic:model-context-protocol topic:ap2` = 10
- A2A+ACP: `topic:a2a topic:agentic-commerce-protocol` = 2; `topic:a2a topic:acp` = 53; `topic:a2a-protocol topic:agentic-commerce-protocol` = 0; `topic:a2a-protocol topic:acp` = 4

## Top ten pairs by manifest files: five most-starred repos (from the sampled manifest results)

Sample = first 100 results per query, so for large pairs these are the most-starred repos *in the sample*, not provably the global top five. "Org" does not mean independent; vendor/sample repos flagged by me.

**MCP+A2A** (2984 files; 254+ repos in sample)
- langflow-ai/langflow (156,937 stars, Organization) - independent/OSS product
- google-gemini/gemini-cli (109,104 stars, Organization) - vendor product
- datawhalechina/hello-agents (87,946 stars, Organization)
- microsoft/ai-agents-for-beginners (80,957 stars, Organization) - vendor tutorial
- QwenLM/qwen-code (30,935 stars, Organization)

**MCP+x402** (1670 files; 164+ repos in sample)
- superdesigndev/treg (8,915 stars, Organization)
- x402-foundation/x402 (6,827 stars, Organization) - protocol reference repo
- crestalnetwork/intentkit (6,514 stars, Organization)
- cloudflare/agents (6,142 stars, Organization) - vendor framework
- google-agentic-commerce/AP2 (3,286 stars, Organization) - vendor sample/spec (Google)

**x402+ERC8004** (191 files; 89+ repos in sample)
- LeoYeAI/agent-master-skills (2,224 stars, User)
- hashgraph-online/standards-sdk (1,285 stars, Organization)
- nirholas/three.ws (286 stars, User)
- nirholas/crypto-vision (97 stars, User)
- AgentlyHQ/aixyz (81 stars, Organization)

**x402+MPP** (160 files; 85+ repos in sample)
- TryGhost/Ghost (55,907 stars, Organization) - independent OSS product (real use of @x402/* and mppx)
- solana-foundation/pay (1,810 stars, Organization) - foundation project
- nirholas/three.ws (286 stars, User)
- daydreamsai/lucid-agents (202 stars, Organization)
- wevm/mppx (195 stars, Organization) - protocol reference SDK

**MCP+MPP** (94 files; 87 repos in sample)
- elie222/rakazo (9,776 stars, User)
- nirholas/three.ws (286 stars, User)
- wevm/mppx (195 stars, Organization) - protocol reference SDK
- orkbot-run/ork (148 stars, Organization)
- xlnfinance/xln (102 stars, Organization)

**A2A+x402** (70 files; 60 repos in sample)
- google-agentic-commerce/AP2 (3,286 stars, Organization) - vendor sample/spec (Google)
- google-agentic-commerce/a2a-x402 (572 stars, Organization) - vendor sample (Google)
- dabit3/a2a-x402-typescript (105 stars, User)
- key0ai/key0 (96 stars, Organization)
- AgentlyHQ/aixyz (81 stars, Organization)

**MCP+ERC8004** (61 files; 59 repos in sample)
- nirholas/three.ws (286 stars, User)
- AgentlyHQ/aixyz (81 stars, Organization)
- keep-starknet-strange/starknet-agentic (80 stars, Organization)
- Eversmile12/create-8004-agent (52 stars, User)
- Sperax/bnb-chain-toolkit (40 stars, Organization)

**MCP+WBA** (35 files; 35 repos in sample)
- every-app/open-seo (28,886 stars, Organization)
- CopilotKit/OpenDuet (2,153 stars, Organization)
- NSHipster/sosumi.ai (496 stars, Organization)
- wevm/mppx (195 stars, Organization) - protocol reference SDK
- datalayer/agent-runtimes (25 stars, Organization)

**x402+L402** (51 files; 31 repos in sample)
- getAlby/js-lightning-tools (49 stars, Organization)
- msaleme/red-team-blue-team-agent-fabric (34 stars, User)
- peacprotocol/peac (15 stars, Organization)
- lightningfaucet/lightning-wallet-mcp (11 stars, Organization)
- clankwright/satring (7 stars, User)

**AP2+x402** (24 files; 24 repos in sample)
- google-agentic-commerce/AP2 (3,286 stars, Organization) - vendor sample/spec (Google)
- google-agentic-commerce/a2a-x402 (572 stars, Organization) - vendor sample (Google)
- x402agent/solana-clawd (26 stars, User)
- ChaosChain/chaoschain (25 stars, Organization)
- cianfhoghlaim/cianfhoghlaim (4 stars, User)

Topic-based top five (true star order, `sort=stars`) for the same pairs:

- MCP+A2A `topic:mcp topic:a2a` (1589): cheaper-inference/OmniRoute (90,271), a2ui-project/a2ui (18,633), google/adk-go (9,009), EvoMap/evolver (8,750), ag2ai/ag2 (5,088)
- MCP+x402 `topic:mcp topic:x402` (2086): vAPI-Network/vapi-network (5,862), daydreamsai/daydreams (628), qntx/bot (572), moov-io/awesome-fintech (413), BlockRunAI/blockrun-mcp (391)
- x402+ERC8004 `topic:x402 topic:erc-8004` (214): internet-court/internet-court-skill (7,205), bolivian-peru/os-moda (122), tenequm/skills (38), cascade-protocol/sati (19), satohubai/onchain-agents (16)
- x402+MPP `topic:x402 topic:mpp` (106): devlab-group/agent-commerce (83), solana-foundation/pay-kit (78), faremeter/faremeter (70), MikeyPetrillo/Agent402 (54), tenequm/skills (38)
- MCP+MPP `topic:mcp topic:mpp` (47): devlab-group/agent-commerce (83), MikeyPetrillo/Agent402 (54), agents-txt/agents-txt (16), winsznx/remlo (13), Custena/agent-payment-protocols (10)
- A2A+x402 `topic:a2a topic:x402` (269): internet-court/internet-court-skill (7,205), qntx/bot (572), daydreamsai/lucid-agents (202), qntx-labs/ra2a (169), bolivian-peru/os-moda (122)
- MCP+ERC8004 `topic:mcp topic:erc-8004` (121): bolivian-peru/os-moda (122), unibaseio/aip-agent (17), satohubai/onchain-agents (16), hashgraph-online/hashnet-mcp-js (13), Abstraxn-Labs/agent-kit (11)
- MCP+WBA `topic:mcp topic:web-bot-auth` (8): tragent-io/acurl (3), angeo-dev/module-agent-activity (2), Merlin-Bedford/noodle (1), agentbouncer/agentbouncer-js (0), KirkeLabs/agent-readiness-scan (0)
- x402+L402 `topic:x402 topic:l402` (48): nikoSchoinas/routeweiler-python-sdk (34), msaleme/red-team-blue-team-agent-fabric (34), lightningfaucet/lightning-wallet-mcp (11), Custena/agent-payment-protocols (10), Mike-io-hash/satsgate (7)
- AP2+x402 `topic:ap2 topic:x402` (55): sthamann/awesome-agentic-commerce (100), devlab-group/agent-commerce (83), longcipher/ledgerflow (19), tsubasakong/awesome-agent-payments-protocol (16), hummusonrails/x402-demo-arbitrum (9)

## Three-protocol combinations (npm package.json, same file; and topic triples)

| Combination | package.json files | repos in sample | topic repos |
|---|---|---|---|
| MCP + A2A + x402 | 12 | 11 | 203 |
| MCP + x402 + ERC8004 | 34 | 32 | 94 |
| MCP + x402 + MPP | 41 | 40 | 37 |
| x402 + MPP + ERC8004 | 2 | 2 | 1 |
| MCP + A2A + ERC8004 | 3 | 3 | 23 |
| MCP + x402 + L402 | 4 | 3 | 33 |
| x402 + MPP + L402 | 2 | 2 | 6 |
| A2A + x402 + ERC8004 | 5 | 5 | 22 |
| MCP + A2A + MPP | 2 | 2 | 7 |
| MCP + x402 + WBA | 3 | 3 | 1 |

Queries: `"<npm-marker-1>" "<npm-marker-2>" "<npm-marker-3>" filename:package.json`; topic: `topic:a topic:b topic:c`. Triples are in `/triples.json` in the same directory with repo lists.

## Reading the results

- MCP is the hub: it is the most common co-dependency for every other protocol (MCP+A2A, MCP+x402 far ahead). That mostly reflects MCP being near-universal in agent repos, so the informative signal is lift, not raw count.
- The x402 cluster is the strongest *payments* stack: x402 with MCP (paid MCP tools), with ERC-8004 (agent identity/reputation on EVM), with MPP and L402 (competing/complementary payment rails), and with A2A (Google a2a-x402 extension).
- AP2 pairs almost only with x402 and A2A, dominated by Google vendor repos.
- UCP, ACP, KYA-OS, x401 and Visa TAP have too few dependents (single or low double digits) for meaningful pairing in manifests. UCP+MCP is 10 package.json files.
- Web Bot Auth appears with MCP mostly through a few apps (every-app/open-seo, CopilotKit/OpenDuet, NSHipster/sosumi.ai, wevm/mppx).