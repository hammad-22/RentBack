# RentBack — Roadmap

> **PRIVATE — DO NOT COMMIT**
> This file is in .gitignore. Keep it local only.

---

## Vision

RentBack is the **operating system for renters** in NYC — and eventually, every major US city.

**Positioning:** "Built for renters, not landlords."

**The wedge:** AI-powered rent negotiation letters backed by real comparable listings.
**The long game:** Own the full renter lifecycle — Hunt → Negotiate → Sign → Live → Move Out.

---

## The Renter Lifecycle (5 Stages)

### Stage 1 — Hunt
> Features that help renters find and evaluate apartments before signing.

- **Neighborhood Profiles** — Comprehensive neighborhood pages with rent data, transit, crime, schools, amenities, and environmental info (see Neighborhood Feature Strategy below)
- **Neighborhood Rent Intelligence** — Median prices, YoY trends, supply/demand signals by neighborhood and bedroom count (RentCast data)
- **Landlord Reputation Score** — Aggregate HPD violations, 311 complaints, court filings, and user reviews into a trust score per building/landlord
- **Fair Rent Estimator** — Input an address, get a data-backed fair market price and confidence interval

### Stage 2 — Negotiate
> The current MVP. Expand depth here first.

- **AI Negotiation Letter Generator** (live) — Personalized, data-backed letters with specific comps
- **Counter-Offer Calculator** — Given an ask price, suggest an optimal counter and confidence that landlord will accept
- **Renewal Negotiation Flow** — Separate flow for lease renewals vs. new leases (different leverage points)
- **Negotiation Outcome Tracker** — Users report results; trains our model on what works

### Stage 3 — Sign
> Features for lease review and signing safely.

- **AI Lease Analyzer** — Upload a PDF lease, get plain-English summary of unusual clauses, red flags, missing tenant protections, and illegal terms
- **NYC Rent Stabilization Checker** — Is this unit stabilized? What's the legal max increase? Pull from DHCR/HPD data
- **Lease Template Library** — Know what a fair lease looks like vs. what you got
- **Addendum Generator** — AI-drafted addendums for pets, roommates, early termination, etc.

### Stage 4 — Live
> Features for the duration of tenancy.

- **Know Your Rights AI** — Chat-style Q&A for tenant rights questions (heat requirements, repairs, lockouts, harassment, eviction defense)
- **Repair Request Letter Generator** — Documented, certified-mail-ready letters for habitability issues
- **Rent Payment Tracker** — Log payments, flag late fees, track lease terms
- **Rent Increase Alert** — Notify user when their building files for a rent increase
- **Document Vault** — Encrypted storage for lease, move-in photos, repair requests, correspondence

### Stage 5 — Move Out
> Features for end-of-lease protection.

- **Move-Out Letter Generator** — 30/60-day notice templates
- **Security Deposit Recovery Guide** — Step-by-step with letter templates and small claims court filing help
- **Landlord Report Card** — Submit a review after move-out; feeds the Stage 1 reputation score

---

## Neighborhood Feature Strategy

### Why This Matters

Neighborhood profiles serve three strategic purposes:

1. **Top-of-funnel SEO** — NYC has ~250+ named neighborhoods, each becoming an indexable page targeting long-tail queries ("average rent in Astoria", "is Bed-Stuy safe", "best neighborhoods near the G train"). This compounds over time.
2. **Solves the retention gap** — Renters negotiate once a year. Neighborhood data gives them a reason to come back between negotiations — browsing for a future move, sharing with friends, checking market shifts.
3. **Natural conversion pipeline** — Someone researching neighborhoods is pre-lease, the perfect moment to introduce the negotiation tool. Flow: browse neighborhood → see fair rent data → use analysis tool.

### Data Sources

| Data | Source | Cost | Complexity |
|------|--------|------|------------|
| Rent data & deals | RentCast (already integrated) | Existing | Low |
| Transit lines | MTA GTFS static feeds | Free, public | Moderate parsing |
| Crime stats | NYPD CompStat / NYC Open Data | Free, public | Normalization needed |
| School ratings | NYC DOE / GreatSchools API | Free/cheap | Straightforward |
| Grocery / amenities | Google Places or Yelp API | Paid, rate-limited | Moderate |
| Environmental hazards | NYC DEP, EPA Superfund data | Free | Messy/inconsistent |
| Neighborhood descriptions | AI-generated + editorial review | Time-intensive | Moderate |

### Implementation Phases

#### Phase 1 — Enrich Results Page (Start Here)
> Lowest effort, highest signal. Ships in 1-2 weeks.

When someone runs a rent analysis for "456 DeKalb Ave, Brooklyn", the results page automatically includes a neighborhood summary for Clinton Hill. No new pages, no new routes — just context added to the existing flow.

- Pull neighborhood name from address (map to NYC neighborhood boundaries)
- Show median rent for the neighborhood (from RentCast data we already fetch)
- AI-generated 2-3 sentence neighborhood description (can be cached/static)
- "What's a good deal" threshold (e.g., below 25th percentile for that bed count)
- CTA: "Explore more about [Neighborhood]" (placeholder for Phase 2)

**Why start here:** Validates whether users engage with neighborhood context before building standalone pages. Minimal new backend work — enriches existing API response.

#### Phase 2 — Standalone Neighborhood Pages
> SEO play. 2-3 weeks of work.

- `/neighborhoods` directory page — browsable list of all NYC neighborhoods
- `/neighborhoods/[slug]` — individual profile pages
- Per-neighborhood data: median rent by bedroom count, YoY trend direction, "good deal" threshold
- Static neighborhood descriptions (AI-generated, then human-edited for quality)
- Hard link to "Analyze your rent in [Neighborhood]" CTA on every page
- Basic filtering: by borough, by budget range

**Data needed:** RentCast (have it), neighborhood boundary mapping, cached descriptions.

#### Phase 3 — Transit & Livability Layer
> Adds the data that differentiates us. 2-3 weeks on top of Phase 2.

- MTA GTFS data: subway lines, bus routes, ferry stops per neighborhood
- NYPD CompStat: crime stats normalized per capita, by precinct/neighborhood
- NYC DOE / GreatSchools: school ratings for family-oriented neighborhoods
- "Livability score" — composite rating combining transit access, safety, schools
- Filter neighborhoods by: budget + transit line + safety score

**Data needed:** MTA GTFS feeds, NYC Open Data API, GreatSchools API.

#### Phase 4 — Full Neighborhood Profiles
> The premium layer. Longer-term build.

- Grocery store / amenity density via Google Places API
- Environmental hazards: flood zones (FEMA), Superfund proximity (EPA), air quality
- User-contributed neighborhood reviews (feeds into Landlord Report Card ecosystem)
- "Neighborhood match" quiz — answer lifestyle questions, get ranked recommendations
- Comparison tool: compare two neighborhoods side by side

**Data needed:** Google Places API (paid), FEMA flood maps, EPA data, user review system (requires auth + DB).

### Design Principle

Neighborhood features must stay **in service of the negotiation tool**, not become a StreetEasy competitor. Every neighborhood page should funnel users toward analyzing their rent or exploring fair market rates. The data exists to empower negotiation, not to be a listings platform.

---

## Paywall Structure

### Free Tier
- 1 negotiation letter per month
- Basic neighborhood price data (no trend history)
- Know Your Rights Q&A (limited to 5 questions/month)
- Neighborhood profiles with basic rent data (Phase 1-2 content)

### Pro — $12/month or $99/year
- Unlimited negotiation letters
- Full RentCast comp data with trend history
- Lease analyzer (up to 3 leases/month)
- Rent stabilization checker
- Document vault (1GB)
- Landlord reputation scores
- Full neighborhood profiles with transit, crime, schools (Phase 3-4 content)
- Livability scores and neighborhood comparison tool

### Premium — $29/month or $249/year
- Everything in Pro
- Unlimited lease analysis
- Counter-offer calculator with confidence scores
- Priority AI response times
- Phone/email consultation credit (1x/quarter with tenant rights org partner)
- Negotiation outcome coaching (personalized tips based on your specific landlord/building history)

### Pay-per-report — $7-9
- One-time purchase for users who don't want a subscription
- Full analysis + neighborhood context included

The paywall hits after the first free report — the product earns trust on run one, converts on run two.

---

## B2B Revenue Paths

1. **Tenant Unions & Advocacy Orgs** — White-label platform (Met Council, UHAB, etc.), flat SaaS fee, anonymized aggregate data
2. **Legal Aid Organizations** — Bulk access at discounted rates, co-branded letters
3. **Real Estate Brokers (Tenant-Side)** — License data layer via API, $299-999/month per brokerage
4. **Employers / HR Benefits** — Corporate bulk subscriptions at $8/employee/month
5. **Relocation Services** — Affiliate or flat-fee per referral from corporate relocation firms

---

## MRR Targets

| Milestone | Users | Mix | MRR |
|-----------|-------|-----|-----|
| Month 3 | 500 total / 50 Pro | 90% free | ~$600 |
| Month 6 | 2,000 total / 300 Pro | 15% paid | ~$3,600 |
| Month 12 | 8,000 total / 1,200 Pro / 2 B2B | — | ~$15,000 |
| Month 18 | 25,000 total / 4,000 Pro / 10 B2B | — | ~$55,000 |

*Assumes: Pro at $12/mo, B2B at $500/mo avg. Does not include Premium tier uplift.*

---

## Monetization Notes

### Highest-leverage early moves
1. **Usage gate** — Ship the freemium wall first, lowest-effort path to any MRR
2. **B2B licensing** — Tenant advocacy orgs and attorneys, $50-200/month, much higher LTV than individual renters
3. **Referral/affiliate** — Renter's insurance (Lemonade, etc.) or moving companies, zero marginal cost

### LTV Consideration
Individual renters negotiate roughly once a year — low natural retention. Neighborhood profiles + alerts + history loop and the B2B angle create recurring reasons to stay subscribed beyond the one-time negotiation event.

---

## Growth Strategy

### NYC First, Own It
- Hyper-local content: neighborhood guides (Phase 2+), HPD data, rent stabilization explainers
- NYC-specific SEO: "how to negotiate rent in Brooklyn", "is my apartment rent stabilized", "average rent in [neighborhood]"
- Partner with NYC-focused media (Curbed, Gothamist, The City)
- Reach out to r/NYCapartments, r/AskNYC, local Facebook groups

### Distribution Levers
1. **SEO** — Long-tail tenant rights and rent negotiation queries; neighborhood pages as content engine
2. **Reddit/Community** — Organic engagement in tenant communities
3. **Influencer** — NYC lifestyle creators who rent (huge audience overlap)
4. **Employer Benefits** — Cold outreach to NYC startup HR teams
5. **Legal Referral Network** — Build relationships with tenant attorneys who refer clients
6. **Press** — Housing affordability is a perennial NYC news cycle; pitch data stories

### Expansion Playbook (After NYC)
1. NYC → San Francisco / LA (high-rent, renter-friendly law markets)
2. SF/LA → Boston, Chicago, Seattle, DC
3. National: generic lease analyzer, rights guides, negotiation tools
4. International: London, Toronto (similar renter protection frameworks)

---

## Competitive Moat

| Competitor | Gap We Fill |
|------------|-------------|
| Zillow/StreetEasy | No negotiation help, no tenant advocacy |
| Avail/TurboTenant | Built for landlords, not renters |
| HelloSign/DocuSign | No intelligence, just signing |
| Generic ChatGPT | No local data, no NYC-specific knowledge |

**Our moat:** Proprietary outcome data (what negotiations succeed and why) + NYC regulatory data integration + network effects from landlord reputation scores + hyper-local neighborhood intelligence.

---

## Technical Roadmap

### Near-term (next 3 months)
- [ ] **Neighborhood context on results page (Phase 1)** — Enrich analysis results with neighborhood summary
- [ ] Auth system (Clerk or Supabase Auth)
- [ ] Database (Supabase Postgres) for user accounts, saved letters, usage tracking
- [ ] Usage metering for free tier limits
- [ ] Stripe integration for Pro subscriptions
- [ ] Lease PDF upload + parsing (LangChain + PDF parser)
- [ ] Backend CI/CD — Cloud Build trigger for auto-deploy on push

### Medium-term (3-9 months)
- [ ] **Standalone neighborhood pages (Phase 2)** — `/neighborhoods` directory + individual profiles
- [ ] **Transit & livability data (Phase 3)** — MTA, NYPD, school ratings integration
- [ ] HPD violation data integration
- [ ] DHCR rent stabilization data integration
- [ ] Landlord reputation score (v1)
- [ ] Renewal negotiation flow
- [ ] Counter-offer calculator

### Long-term (9-18 months)
- [ ] **Full neighborhood profiles (Phase 4)** — Amenities, environmental, user reviews, comparison tool
- [ ] Document vault with encryption
- [ ] Know Your Rights AI (RAG on NYC housing law)
- [ ] Outcome tracker + model feedback loop
- [ ] B2B API tier
- [ ] Mobile app (React Native)

### Feature Ideas (Unscheduled)
- PDF export of analysis reports
- Email report delivery (Resend or Postmark)
- Shareable report links (UUID-based public URL, requires DB)
- Lease renewal reminders (email 60/30/14 days before lease end)
- Re-analyze button (one-click refresh for market rate shifts)
- Market shift alerts (notify when neighborhood median drops by X%)
- Landlord response coach (paste landlord reply, AI suggests counter-response)
- Multi-unit comparison (compare two apartments side by side)
- Expand beyond NYC (RentCast covers entire US; largely a config/copy change)
