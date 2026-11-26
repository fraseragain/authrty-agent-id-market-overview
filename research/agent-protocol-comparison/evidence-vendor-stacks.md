# Agent protocol stacks deployed or announced together, as of 25 Nov 2026

Evidence key: [P] primary (vendor doc, blog, press release, spec); [S] secondary press or blog (marked). Status: LIVE, PILOT/PREVIEW, ANNOUNCED. "Not found" means the search did not surface a source. Several primary pages (Visa press release, Mastercard Oct 2026 page, OpenAI March 2026 post) returned 404/403 to fetch, so claims about them rest on search snippets and are marked.

## 1. Per-vendor tables

### Google (Gemini, AI Mode, Agent Payments)
| Combination | How | Status | Date | Source |
|---|---|---|---|---|
| AP2 + A2A + MCP | AP2 designed as an extension of A2A and MCP | Announced (spec/repo) | 16 Sep 2025 | [P] https://cloud.google.com/blog/products/ai-machine-learning/announcing-agents-to-payments-ap2-protocol/ |
| AP2 + A2A + x402 | "A2A x402 extension", with Coinbase, Ethereum Foundation, MetaMask | Reference extension; no consumer product found | Sep 2025 | [P] https://www.coinbase.com/developer-platform/discover/launches/google_x402 |
| UCP + AP2 + A2A + MCP | UCP "compatible with" AP2, A2A, MCP; REST and MCP bindings; A2A as optional transport | UCP checkout LIVE in AI Mode and Gemini for select merchants (US-led); Gemini web app "coming soon" | UCP 11 Jan 2026 | [P] https://developers.google.com/merchant/ucp ; [S] https://9to5google.com/2026/01/11/gemini-ai-mode-checkout/ |
| UCP + Google Pay handler (+ PayPal, Affirm, Klarna) | Payment handlers inside UCP checkout; PayPal "coming soon" | LIVE (Google Pay); others announced | 2026 | [P] https://support.google.com/merchants/answer/16837055 |
| AP2 in Google products | "coming months, starting with Gemini Spark" (undated in results) | Announced | 2026 | [P] https://blog.google/products-and-platforms/products/shopping/shopping-updates-google-marketing-live |
| Mastercard Verifiable Intent aligned with AP2 + UCP | Co-developed with Google | Spec open-sourced; Agent Pay integration "coming months" | Mar 2026 | [P] https://www.mastercard.com/gb/en/news-and-trends/stories/2026/verifiable-intent.html |
| x402 Foundation premier member | Governance only | LIVE | Jul 2026 | [P] https://www.linuxfoundation.org/press/linux-foundation-announces-operational-launch-of-x402-foundation-to-standardize-internet-native-payments-for-ai-agents-and-applications |
| Web Bot Auth | Listed as supporter of the standard (Mastercard dev guide) | Not found as a Google product statement | n/a | [S-ish] https://developer.mastercard.com/merchant-cloud/documentation/tutorials-and-guides/agentic-commerce-guide/24/ |

### Shopify
| Combination | How | Status | Date | Source |
|---|---|---|---|---|
| UCP (with Google) over MCP / A2A / REST | UCP co-developed; transports swappable | LIVE (spec 2026-01-11) | 11 Jan 2026 | [P] https://www.shopify.com/ucp |
| UCP + Poppy (PAP) | "Poppy commerce extension" co-authored by Shopify; Poppy handles agent identity/permissions, UCP handles shopping; every Shopify store auto-publishes a Poppy file | LIVE | 13 Nov 2026 | [P] https://sierra.ai/blog/releasing-poppy |
| ChatGPT/ACP via Shopify Catalog | Shopify merchants reached through Shopify Catalog; approval requirement removed 17 Jun 2026 | Reported live | 2026 | [S] https://gigacommerce.co/insights/ai-channels/chatgpt-instant-checkout-ended (no primary found) |
| Copilot Checkout | Launch partner (auto-enrolment after opt-out) | LIVE (US) | Jan 2026 | [S] https://www.retailtouchpoints.com/news/etsy-shopify-among-early-partners-for-microsofts-copilot-checkout/156346 |
| x402 Foundation premier member | Governance | LIVE | Jul 2026 | Linux Foundation link above |

### OpenAI (ChatGPT checkout, Apps SDK)
| Combination | How | Status | Date | Source |
|---|---|---|---|---|
| ACP + Stripe SPT | Instant Checkout used ACP; SPT is first Delegated Payment Spec implementation | Launched Sep 2025; then scaled back | 29 Sep 2025 | [P] https://openai.com/index/buy-it-in-chatgpt/ ; https://developers.openai.com/commerce/guides/key-concepts |
| ACP + product discovery/feeds, cart, orders, MCP | Spec release 17 Apr 2026 adds cart, feed, orders, auth, MCP support (as reported) | Live spec | Apr 2026 | [S] https://anatta.io/agentic-commerce/shopify/ucp-vs-acp/ |
| Apps SDK (MCP-based) for merchant-owned checkout | After 24 Mar 2026 OpenAI lets merchants use own checkout; deeper integration via ChatGPT apps | LIVE (direction) | 24 Mar 2026 | [S] https://www.digitalcommerce360.com/2026/03/24/openai-agentic-commerce-updates-chatgpt-walmart/ (quotes OpenAI post; OpenAI primary not retrieved) |
| ACP + Web Bot Auth signatures on ChatGPT agent requests | Not found |  | n/a | Not found |

### Stripe
| Combination | How | Status | Date | Source |
|---|---|---|---|---|
| ACP + SPT | Co-developed with OpenAI; SPT as payment primitive | LIVE | Sep 2025 | [P] https://docs.stripe.com/agentic-commerce/acp |
| SPT + Visa Intelligent Commerce + Mastercard Agent Pay | SPT extended to agentic network tokens | Announced as supported; live scope not verified | 2025-26 | [P] https://stripe.com/br/blog/supporting-additional-payment-methods-for-agentic-commerce |
| MPP + SPT + cards/Klarna/Affirm | MPP accepted via PaymentIntents, stablecoin or fiat via SPT | Sessions says "available now"; Stripe MPP docs earlier said private preview | 18 Mar 2026; Apr 2026 | [P] https://docs.stripe.com/payments/machine/mpp ; https://stripe.com/blog/everything-we-announced-at-sessions-2026 |
| UCP (with Google) | Buy in AI Mode and Gemini "soon" | Announced | 29 Apr 2026 | Sessions link above |
| Meta native checkout in ads; Link agent wallet | Partnership; Link wallet available | Mixed | Apr 2026 | Sessions link above |
| Stripe MCP | Preview of subscription metrics via Stripe MCP | Preview | Apr 2026 | Sessions link above |
| Copilot Checkout (SPT) | Stripe merchants apply to onboard | LIVE (US) | Jan 2026 | [P] https://stripe.com/en-ca/newsroom/news/microsoft-copilot-and-stripe |
| AWS AgentCore Payments (Stripe/Privy wallet) | Wallet provider | GA | 2026 | AWS docs below |
| PAP/Poppy design partner; x402 Foundation premier | | LIVE/partner | Oct-Nov 2026 | Sierra, Linux Foundation links |

### PayPal
| Combination | How | Status | Date | Source |
|---|---|---|---|---|
| ACP (via Braintree delegated tokens) + UCP (Google Pay handler) + AP2 collaboration | Agent Ready / Store Sync | ACP integration documented; UCP "will support"; AP2 collaboration | Oct 2025 - Jan 2026 | [P] https://developer.paypal.com/agent-ready/overview ; https://newsroom.paypal-corp.com/2026-01-22-Making-Sense-of-the-AI-Shopping-Protocol-Moment |
| Perplexity checkout | PayPal/Venmo in-chat checkout, Instant Buy | LIVE | May and Nov 2025 | [P] https://newsroom.paypal-corp.com/2025-11-PayPal-Launches-Agentic-Shopping-with-Perplexity |
| Copilot Checkout | Launch partner | LIVE (US) | Jan 2026 | [S] https://www.windowscentral.com/artificial-intelligence/microsoft-copilot/microsoft-and-paypals-copilot-checkout-allows-users-to-make-purchases-without-leaving-the-chatbot |

### Visa
| Combination | How | Status | Date | Source |
|---|---|---|---|---|
| TAP + Web Bot Auth (Cloudflare) | TAP built on HTTP Message Signatures, Web Bot Auth as authentication layer, adds tag and nonce | Spec published; Cloudflare says SDK support "over coming months" | 14-24 Oct 2025 | [P] https://blog.cloudflare.com/secure-agentic-commerce/ ; https://developer.visa.com/capabilities/trusted-agent-protocol/overview |
| Intelligent Commerce Connect: TAP + MPP + ACP + UCP | One merchant integration accepting all four | Launched Apr 2026 (date from [S]); press release page not retrievable | Apr 2026 | [P] https://corporate.visa.com/en/sites/visa-perspectives/press-releases/visa-intelligent-commerce-connect-ai-shopping-for-businesses.html (404 on fetch; text via search snippet); [S] https://worldpay.com/insights/articles/agentic-commerce-what-it-means-for-your-business |
| MPP card spec + SDK on VIC and TAP, "complements x402" | `mpp-card` npm; Visa design partner of MPP | LIVE spec | 18 Mar 2026 | [P] https://corporate.visa.com/en/sites/visa-perspectives/innovation/visa-card-specification-sdk-for-machine-payments-protocol.html |
| Akamai + TAP | Behavioural bot intelligence plus TAP | Announced | Dec 2025 | [P] https://corporate.visa.com/en/sites/visa-perspectives/press-releases/akamai-visa-collaborate-to-build-trust-in-agentic-commerce.html |
| Visa MCP server / agent acceptance toolkit | MCP | Exists; detail not read | 2026 | [P] https://corporate.visa.com/en/sites/visa-perspectives/innovation/visa-mcp-server-agent-acceptance-toolkit.html |
| x402 Foundation premier member | | LIVE | Jul 2026 | Linux Foundation link |

### Mastercard
| Combination | How | Status | Date | Source |
|---|---|---|---|---|
| Agent Pay + Web Bot Auth | Same layering as TAP; Mastercard hosts key directory | Announced/rolling out | Oct 2025 | Cloudflare blog above |
| Verifiable Intent aligned to AP2 + UCP; to be integrated into Agent Pay intent APIs | Open-source spec (FIDO, EMVCo, IETF, W3C based) | Spec open; Agent Pay integration "coming months" (Mar 2026) | Mar 2026 | [P] https://www.mastercard.com/gb/en/news-and-trends/stories/2026/verifiable-intent.html |
| Agent Pay for Machines + x402 | Builds on x402 plus network trust layer; early-access APIs, sandbox | PILOT (Decrypt: not commercially available); demoed at Cloudflare Connect Oct 2026 | Launch Jun 2026; demo Oct 2026 | [P] https://www.mastercard.com/us/en/business/artificial-intelligence/mastercard-agent-pay/agent-pay-for-machines.html ; [S] https://decrypt.co/381373. MPP link: not found. |
| Stripe SPT; Checkout.com; Adyen quote | Network tokens via PSPs | Announced/partial | 2025-26 | Stripe and Checkout.com links |
| Anthropic blueprint partner | Merchant network distribution | Announced | 2 Sep 2026 | [S] https://www.pymnts.com/news/artificial-intelligence/2026/anthropic-built-the-shopping-brain-and-skipped-the-wallet/ |

### American Express
| Combination | How | Status | Date | Source |
|---|---|---|---|---|
| ACE developer kit + Agent Purchase Protection + Intent Intelligence | Own stack; registered agents | Kit Apr 2026; Intent Intelligence framework 13 Oct 2026 with no ACE integrations using it yet | Apr/Oct 2026 | [P] https://www.americanexpress.com/en-us/company/agentic-commerce/ ; [S] https://www.digitalcommerce360.com/2026/10/16/american-express-ai-framework/ |
| Web Bot Auth foundation | "will be leveraging" | Announced | Oct 2025 | Cloudflare blog above |
| x402 Foundation premier member | | LIVE | Jul 2026 | Linux Foundation link |

### Adyen
| Combination | How | Status | Date | Source |
|---|---|---|---|---|
| ACP + UCP (tokenization handler) + AP2 | "Adyen Agentic" | ACP and UCP docs exist; broader availability "later" | Jun 2026 | [P] https://docs.adyen.com/online-payments/agentic-commerce.md ; [S] https://www.crowdfundinsider.com/2026/06/287393-global-fintech-adyen-launches-conversational-ai-and-autonomous-commerce-agentic-solutions/ |
| Visa/Mastercard programmes | Quotes only; specific integration not confirmed | Not found | | https://www.adyen.com/press-and-media/adyen-agentic |
| x402 Foundation premier; AMP acquirer | | LIVE | 2026 | Linux Foundation; Ant links |

### Checkout.com
| Combination | How | Status | Date | Source |
|---|---|---|---|---|
| ACP + UCP/AP2 + VIC + Agent Pay, with TAP and Verifiable Intent as trust layers | Single connectivity layer | ACP adoption announced Nov 2025; live status of whole page unclear | Nov 2025- 2026 | [P] https://www.checkout.com/agentic-commerce ; https://www.checkout.com/newsroom/checkout-adopts-acp-backed-by-openai-to-power-agentic-commerce-for-enterprise-merchants |
| AMP acquirer | | Reported | Apr 2026 | [P] https://www.businesswire.com/news/home/20260427209524/en/Ant-International-Launches-Open-Sourced-Agentic-Mobile-Protocol-to-Drive-AI-Commerce |

### Coinbase
| Combination | How | Status | Date | Source |
|---|---|---|---|---|
| x402 + A2A + AP2 | A2A x402 extension | Reference extension | Sep 2025 | Coinbase link above |
| x402 inside MCP (Bazaar MCP server in AWS AgentCore) | 10,000+ x402 endpoints via Gateway | LIVE (GA) | 2026 | AWS docs below |
| x402 Foundation (Linux Foundation) | Founder | LIVE | Apr intent, Jul 2026 | [P] https://docs.cdp.coinbase.com/x402/support/x402-foundation |
| ERC-8004 + x402 (Base docs recommend CDP facilitator) | Identity/Reputation registries on Base; payment-agnostic | LIVE contracts (mainnet Jan 2026); Validation Registry in revision | 2026 | [P] https://docs.base.org/ai-agents/reference/contracts ; https://eips.ethereum.org/EIPS/eip-8004 |

### Cloudflare
| Combination | How | Status | Date | Source |
|---|---|---|---|---|
| Web Bot Auth + Visa TAP + Mastercard Agent Pay (+ Amex plan) | Verification of signed agents for merchants | Sample TAP implementation and Agent SDK available; managed rulesets "will be created" | 24 Oct 2025 (page updated Jul 2026) | https://blog.cloudflare.com/secure-agentic-commerce/ |
| x402 + Web Bot Auth + (planned) MCP tool charging: Monetization Gateway | Stablecoin settlement over x402; Web Bot Auth optional | ANNOUNCED (waitlist) | 1 Jul 2026 | [P] https://blog.cloudflare.com/monetization-gateway/ |
| MPP + x402 + MCP | Guides for accepting and paying MPP on Workers and MCP tools; "MPP is backwards-compatible with x402" | Documented (status not stated) | updated 5 Aug 2026 | [P] https://developers.cloudflare.com/agents/agentic-payments/mpp |
| x402 in Agents SDK/MCP client | Pay for x402-protected MCP tools | Documented | 2025-26 | [P] https://developers.cloudflare.com/agents/agentic-payments/x402/pay-from-agents-sdk |
| Mastercard Agent Pay for Machines demo | Cloudflare Connect | PILOT | Oct 2026 | Mastercard page above |

### AWS (AgentCore)
| Combination | How | Status | Date | Source |
|---|---|---|---|---|
| x402 + MPP + MCP (Gateway) + AgentCore Identity/Browser; wallets Coinbase CDP or Stripe/Privy | AgentCore Payments manages 402 flow, session budgets, signs via wallet; Coinbase Bazaar MCP server; AWS Marketplace billing connector | Preview May 2026, GA Aug 2026 | May / Aug 2026 | [P] https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/payments.html ; https://aws.amazon.com/about-aws/whats-new/2026/08/bedrock-agentcore-payments-ga/ |
| A2A, AP2, TAP, ACP | Not found in AgentCore Payments docs | Not found | | |
| x402 Foundation premier | | LIVE | Jul 2026 | Linux Foundation link |

### Microsoft (Copilot Checkout)
| Combination | How | Status | Date | Source |
|---|---|---|---|---|
| Stripe SPT/ACP + PayPal + Shopify (merchant of record stays merchant) | Checkout inside Copilot; Microsoft describes UCP as transaction layer atop Merchant Center feeds | LIVE (US) | 8 Jan 2026 | [P] https://about.ads.microsoft.com/en/solutions/technology/agentic-commerce ; https://stripe.com/en-ca/newsroom/news/microsoft-copilot-and-stripe ; [S] https://www.axios.com/2026/01/08/microsoft-ai-copilot-checkout |
| MCP/A2A in Copilot Checkout | Not found | | | |

### Salesforce (Agentforce Commerce)
| Combination | How | Status | Date | Source |
|---|---|---|---|---|
| ACP (with Stripe) + UCP | Agentforce Commerce merchants get ACP Instant Checkout and native UCP | ACP announced Oct 2025; UCP supported 2026 | Oct 2025, 2026 | [P] https://www.salesforce.com/ap/news/press-releases/2025/10/17/salesforce-announces-support-for-agentic-commerce-protocol-in-collaboration-with-stripe/ ; https://www.salesforce.com/news/stories/google-universal-commerce-protocol-support-announcement/ |
| A2A | Mentioned in interview as separate | [S] https://www.digitalcommerce360.com/2026/07/08/salesforce-agentic-ai-landscape/ | | |
| Poppy participant | Joined as one of 64 later companies | LIVE partner | 13 Nov 2026 | Sierra link |

### Sierra and Meta (Muse)
| Combination | How | Status | Date | Source |
|---|---|---|---|---|
| PAP/Poppy built on MCP + OpenAPI + UCP + OAuth | Discovery at /.well-known/poppy.json; agent identifies itself and learns permissions; Muse checks Poppy first on every site; Shopify publishes file for all stores | LIVE v1.0 | 13 Nov 2026 (announced 6 Oct 2026) | [P] https://sierra.ai/blog/releasing-poppy |
| Payments (ACP/AP2/Web Bot Auth) | Poppy post does not mention them; secondary says it sits above settlement | Not found | | [S] https://www.pymnts.com/?p=4302401 |
| Stripe ACP: Meta named co-creator on a Stripe page; Meta checkout in Stripe ads | | Reported | 2026 | https://stripe.com/en-at/blog/developing-an-open-standard-for-agentic-commerce ; Sessions link |

### Anthropic
| Combination | How | Status | Date | Source |
|---|---|---|---|---|
| Claude Commerce Agents blueprint; checkout handed to merchant; Visa and Mastercard as distribution partners | No payment processing in Claude | ANNOUNCED/published blueprint | 2 Sep 2026 | [S] https://www.pymnts.com/news/artificial-intelligence/2026/anthropic-built-the-shopping-brain-and-skipped-the-wallet/ (Anthropic primary not found) |
| MCP as base | Anthropic originated MCP; x402 / MPP / KYA-OS / Poppy / ACP all layer on it | n/a | | multiple |
| Claude-native x402 or SPT | Not found | | | |

### Perplexity
| Combination | How | Status | Date | Source |
|---|---|---|---|---|
| PayPal/Venmo checkout + Store Sync | In-chat purchase | LIVE | Nov 2025 | PayPal newsroom link above |
| Comet as agentic browser to be verified via Web Bot Auth | Mastercard merchant guide lists Comet as an agentic browser, advises validating signatures | Guidance only; no Perplexity statement found | 2026 | [S-ish] https://developer.mastercard.com/merchant-cloud/documentation/tutorials-and-guides/agentic-commerce-guide/24/ |
| Visa TAP, ACP, UCP with Perplexity | Not found | | | |

### Klarna
| Combination | How | Status | Date | Source |
|---|---|---|---|---|
| Agentic Product Protocol (discovery) + UCP + AP2; "complements ACP" | Product data layer works alongside others | APP launched; UCP backing announced | 2 Feb 2026 | [P] https://www.businesswire.com/news/home/20260202720690/en/Klarna-Backs-Googles-Universal-Commerce-Protocol-UCP-to-Enable-Agentic-Commerce-Across-Platforms ; https://klarna.com/international/enterprise/agentic-product-protocol/ |
| Klarna as BNPL via SPT; Google Pay | Payment method | Announced | 2026 | Stripe and Google links |

### Worldpay / FIS
| Combination | How | Status | Date | Source |
|---|---|---|---|---|
| Worldpay: ACP + TAP (with Visa, Cloudflare); ACP/UCP via modular credential mgmt | | ACP support announced 29 Oct 2025; TAP collaboration | 2025-26 | [P] https://worldpay.com/press-releases/worldpay-unlock-new-commerce-channels-merchants-openai-agentic ; https://www.worldpay.com/en/news/worldpay-collaborates-visa-and-cloudflare-advance-trusted-agent |
| FIS: issuer-side KYA with Visa and Mastercard; "proprietary protocol" | | Announced; detail not retrieved | 2026 | [S] https://www.paymentsdive.com/news/fis-teams-with-visa-mastercard-on-agentic-commerce/809472/ ; https://www.emarketer.com/content/paypal-integrates-google-s-latest-agentic-commerce-standard--fis-launches-proprietary-protocol |

### Akamai
| Combination | How | Status | Date | Source |
|---|---|---|---|---|
| Visa TAP + Akamai bot/behavioural intelligence | Edge verification | Announced | Dec 2025 | Visa/Akamai link above |
| Skyfire KYA tokens natively supported in Bot and Agent Control; KYAPay | Skyfire + Akamai agentic transactions (figure in blog title/URL inconsistent: 2.5M vs 25M) | Live per Akamai blog | 2025-26 | [P] https://www.akamai.com/blog/security/how-skyfire-akamai-enabled-25-million-agentic-transactions |
| Web Bot Auth | Not found as separate Akamai statement | | | |

### Vercel
| Combination | How | Status | Date | Source |
|---|---|---|---|---|
| x402 inside MCP: `x402-mcp` (createPaidMcpHandler, withPayment) with AI SDK; x402 AI Starter on CDP | Library and template | LIVE (testnet default) | 2025 | [P] https://vercel.com/blog/introducing-x402-mcp-open-protocol-payments-for-mcp-tools ; https://vercel.com/changelog/402-mcp-enables-x402-payments-in-mcp |
| A2A, ACP, AP2 | Not found | | | |

### Other in-scope protocols (no vendor-product pairing beyond above)
| Protocol | Status | Source |
|---|---|---|
| MPP (Stripe+Tempo) | Launched 18 Mar 2026; Visa card spec; Lightspark Lightning extension; Cloudflare and AWS support | [P] https://stripe.com/blog/machine-payments-protocol ; Visa link above |
| L402 (Lightning Labs) | Agent tools 11 Feb 2026 incl. MCP server and Aperture proxy; third-party MCP servers pair L402 + x402. No big-vendor pairing found | [P] https://lightning.engineering/posts/2026-02-11-ln-agent-tools/ |
| ERC-8004 | Mainnet Jan 2026; Base deploys; pairs with A2A/MCP/x402 conceptually; no production MCP/A2A dependency confirmed | [P] https://eips.ethereum.org/EIPS/eip-8004 |
| ANS | Linux Foundation intent 23 Jun 2026; welcomed 10 Nov 2026; DNS-based; AGNTCY directory supports verifying ANS identities | [P] https://www.linuxfoundation.org/press/linux-foundation-welcomes-agent-name-service-to-bring-verifiable-identity-and-discovery-to-ai-agents |
| AGNTCY | Donated to Linux Foundation Jul 2025; Webex integrated Directory and Identity | [P] https://outshift.cisco.com/the-internet-of-agents/agntcy |
| KYA-OS (DIF/Vouched) | MCP-I donated Mar 2026, renamed Apr 2026, reported v1.0.0 Jul 2026 (dates conflict); prepends identity/delegation preamble to MCP messages; sparse production use | [P] https://github.com/decentralized-identity/kya-os-mcp ; https://www.vouched.id/learn/vouched-and-the-decentralized-identity-foundation-launch-kya-os-an-open-trust-layer-for-ai-agents |
| KYAPay (Skyfire) | Live with Akamai KYA token support | Akamai link above |
| x401 (Proof) | Draft (v0.1 then v0.2); explicitly separate from payment (use 402 for payment); to go to FIDO workgroup; no big-vendor pairing found | [P] https://x401.proof.com/ |
| EMVCo agentic framework | Draft published 1 Sep 2026, comment closed 30 Sep; Intent Services; KYA possible later | [S] https://www.pymnts.com/?p=4269674 ; https://fidoalliance.org/fintech-global-emvco-drafts-framework-for-agentic-card-payments/ |
| Ant International AMP (Agentic Mobile Protocol; note: "AMP" = Agentic Mobile Protocol) | Announced 28 Apr 2026; open source; Alipay+ wallets plus acquirers incl. Adyen, Checkout.com, Fiserv, Worldline; Ant is also AP2 launch partner (Sep 2025) | [P] https://www.businesswire.com/news/home/20260427209524/en/Ant-International-Launches-Open-Sourced-Agentic-Mobile-Protocol-to-Drive-AI-Commerce |
| iProov HAPS (Human Approval and Presence Specification) | Experimental spec Sep 2026; hosted service Oct 2026 with Cerbos and agentgateway | [S] https://idtechwire.com/iproov-launches-human-approval-service-for-ai-agents-with-cerbos-and-agentgateway/ |
| A-Comm AEP (Evidence Protocol) | Draft v1.1.0; consortium; public comment rounds; wraps other protocols; no major-vendor adoption found | [S] https://www.greensheet.com/newswire&newswire_id=64255 |
| Amex Intent Intelligence | See Amex table | |

## 2. Recurring stacks (more than one vendor)

| # | Stack | Vendors | Status | Strongest source |
|---|---|---|---|---|
| 1 | x402 as payment rail (with MCP as tool surface), via x402 Foundation | Coinbase, Cloudflare, AWS, Vercel, Google (A2A x402 ext.), Mastercard (Agent Pay for Machines), Visa (complements), Stripe, Adyen, Amex, Shopify (foundation members) | Software LIVE (AWS GA, Vercel library, Coinbase); Cloudflare gateway ANNOUNCED; Mastercard PILOT | https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/payments.html |
| 2 | x402 + MPP (+ MCP) dual-protocol 402 stack | AWS AgentCore, Cloudflare, Visa (MPP card, ICC), Stripe, Tempo | LIVE docs (AWS GA); Stripe MPP LIVE per Sessions | https://developers.cloudflare.com/agents/agentic-payments/mpp |
| 3 | UCP over MCP/A2A/REST with AP2 compatibility; Google Pay and PSP handlers | Google, Shopify, Salesforce, Klarna, PayPal, Adyen, Stripe, Visa (ICC), Microsoft (described), Poppy | Google/Shopify LIVE (select merchants); others announced or documented | https://developers.google.com/merchant/ucp |
| 4 | ACP + Stripe SPT (delegated payment token) | OpenAI, Stripe, Salesforce, Microsoft Copilot (Stripe path), Worldpay, Checkout.com, Adyen, PayPal (Braintree), Visa ICC | Protocol live; OpenAI native Instant Checkout withdrawn Mar 2026 (see section 3); Copilot LIVE | https://docs.stripe.com/agentic-commerce/acp |
| 5 | Web Bot Auth as agent authentication under card-network protocols (Visa TAP, Mastercard Agent Pay, Amex plan) | Cloudflare, Visa, Mastercard, Amex, Akamai (TAP), Worldpay | Specs published Oct 2025; Cloudflare tooling partial/"coming months"; no vendor-primary statement of full production | https://blog.cloudflare.com/secure-agentic-commerce/ |
| 6 | Multi-protocol acceptance layer (one integration for ACP, UCP, TAP, MPP, AP2, plus network tokens) | Visa ICC, Adyen, Checkout.com, Worldpay, Stripe, PayPal | Visa ICC launched Apr 2026; PSP layers LIVE in part | Visa press release (404 on fetch) and https://www.checkout.com/agentic-commerce |
| 7 | AP2-aligned trust: Mastercard Verifiable Intent + AP2 + UCP | Mastercard, Google, Adyen (quote), Checkout.com (page) | Spec open; Agent Pay integration pending | https://www.mastercard.com/gb/en/news-and-trends/stories/2026/verifiable-intent.html |
| 8 | Network tokens via PSP: Stripe SPT with Visa Intelligent Commerce and Mastercard Agent Pay | Stripe, Visa, Mastercard, Checkout.com, Adyen | Announced; live scope unverified | https://stripe.com/br/blog/supporting-additional-payment-methods-for-agentic-commerce |
| 9 | Poppy/PAP identity layer with UCP and MCP | Sierra, Meta (Muse), Shopify, Stripe, Salesforce, Walmart and 100+ | LIVE v1.0 (13 Nov 2026) | https://sierra.ai/blog/releasing-poppy |
| 10 | Skyfire KYA/KYAPay with edge bot control | Skyfire, Akamai | Live per Akamai | Akamai blog above |
| 11 | AP2 + A2A + MCP | Google, Coinbase, Ant, PayPal (collab) | Spec; little product evidence | https://cloud.google.com/blog/products/ai-machine-learning/announcing-agents-to-payments-ap2-protocol/ |

Weak or single-vendor: Amex ACE and Intent Intelligence (own stack), Anthropic blueprint, L402, ERC-8004, ANS/AGNTCY, KYA-OS, x401, HAPS, AEP, EMVCo, AMP. None has a second major vendor shipping it with another protocol in one flow.

## 3. Announced but contradicted, scaled back, or unverified

1. OpenAI Instant Checkout: launched Sep 2025 on ACP; OpenAI said on 24 Mar 2026 that merchants may use their own checkout while it focuses on product discovery. Reported adoption tiny (around 30 Shopify stores live, single outlet, unverified). OpenAI primary post not retrieved; cited via https://www.digitalcommerce360.com/2026/03/24/openai-agentic-commerce-updates-chatgpt-walmart/. Some sources say Instant Checkout still appears for approved partners.
2. Shopify-ChatGPT: "every merchant via Shopify Catalog" is secondary only.
3. Stripe MPP: docs said private preview; Sessions (29 Apr 2026) says available now. Check current access.
4. Visa and Mastercard network support in Stripe SPT: Stripe's Sessions 2026 recap does not mention either network; no independent live evidence.
5. Amex: protection depends on Intent Intelligence, yet Amex said no ACE integrations use it yet (as at Oct 2026).
6. Mastercard Agent Pay for Machines: "launched" June 2026, but reported pilot-only. Verifiable Intent in Agent Pay APIs promised "in coming months" (Mar 2026); shipping not confirmed.
7. Cloudflare Web Bot Auth with Visa/Mastercard: Oct 2025 announcement; page still says SDK support "over the coming months" and managed rulesets "will be created".
8. Cloudflare Monetization Gateway: waitlist, future-tense; MCP charging planned.
9. PayPal UCP support: "will support"; PayPal in Google Pay marked "coming soon".
10. Google AP2 in products: "coming months, starting with Gemini Spark" (undated); UCP Gemini web app "coming soon".
11. Microsoft: one outlet lists Microsoft as x402 Foundation supporter; Linux Foundation July premier list omits it.
12. Anthropic: nothing from Anthropic primary retrieved; blueprint explicitly excludes payment and checkout.
13. ERC-8004 + MCP/A2A production use: only a community sketch; Validation Registry still being revised.
14. Lowe's/Coinbase A2A x402 demo: simulated, not live ([P] Coinbase launch page).
15. Akamai blog title says 2.5M transactions, URL says 25M; do not cite a figure.
16. Sources conflict on KYA-OS dates and A-Comm comment dates.

## Gaps
Primary pages not retrievable: Visa ICC press release, Mastercard Oct 2026 page, OpenAI March 2026 post, Anthropic announcement. Not found: Web Bot Auth on ChatGPT agent requests; any Perplexity-TAP/ACP link; Vercel pairing beyond x402+MCP; MCP/A2A in Microsoft Copilot Checkout.
