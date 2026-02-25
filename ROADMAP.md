# RentCoach NYC — Roadmap & Product Notes

---

## Hosting

### Recommended Stack (no Vercel)

**Option A — Single platform (simplest)**
Host both frontend and backend on **Railway**. Next.js runs as a Node.js process (`next start`), FastAPI runs as a Python process. One dashboard, one bill, auto-deploys on git push. ~$10–15/month total at hobby scale.

**Option B — Split platform**
- Frontend: **Netlify** — closest Vercel alternative, native Next.js support, free tier, deploys from GitHub in minutes.
- Backend: **Railway** — best for FastAPI, built-in PostgreSQL add-on when you need it, ~$5/month.

**Option C — If you want more control**
- Frontend + Backend: **Render** — free tier available (note: free instances sleep after inactivity, causing slow cold starts — use paid tier for a real product).
- Or containerize both with **Fly.io** for global edge deployment if latency becomes a concern.

### Environment Variables to Set at Deploy Time

**Frontend:**
```
NEXT_PUBLIC_API_URL=https://your-backend-url.com
```

**Backend:**
```
CORS_ORIGINS=https://your-frontend-url.com
LLM_PROVIDER=groq
GROQ_API_KEY=...
DATA_SOURCE=rentcast
RENTCAST_API_KEY=...
```

---

## Database

**Not required for the current MVP.** The app is fully stateless — RentCast and Groq are called on demand, results pass through sessionStorage client-side, nothing needs to persist.

### When to add one

Add a database when you need any of the following:
- User accounts and saved report history
- Real aggregated homepage stats (currently served as constants from `/api/stats`)
- RentCast result caching — their API has call limits; caching by address + bedroom count avoids redundant calls and cuts costs
- Lease renewal reminders and alerts
- Usage analytics

### Recommended: Supabase (PostgreSQL)

Free tier, easy setup, works as a standalone service alongside Railway or Netlify. No infrastructure to manage.

---

## Features to Build

### High impact, low effort
- **PDF export** — generate a branded PDF of the analysis report
- **Email report** — send the report to the user's inbox (Resend or Postmark, ~$0 at MVP scale)
- **Shareable report link** — store result in DB, generate a UUID-based public URL
- **Lease renewal reminders** — user enters lease end date, gets email 60/30/14 days before
- **Re-analyze** — one-click refresh to check if market rates have shifted since the last report

### Medium effort, high retention
- **Saved report history** — requires auth + DB; lets users track rent trends over time
- **Market shift alerts** — notify users when neighborhood median rent drops by X%
- **Expand beyond NYC** — RentCast covers the entire US; removing the NYC constraint is largely a config and copy change

### Larger bets
- **Landlord response coach** — user pastes landlord's reply, AI suggests a counter-response
- **Multi-unit comparison** — compare two apartments side by side before signing
- **Lease clause analyzer** — user uploads lease PDF, AI flags unusual or risky clauses

---

## Monetization

### Model: Freemium with usage gate

| Tier | Price | What's included |
|---|---|---|
| Free | $0 | 1 analysis per month, basic report |
| Pro | $12–15/month | Unlimited analyses, PDF export, report history, alerts |
| Pay-per-report | $7–9 | One-time purchase for users who don't want a subscription |

The paywall hits after the first free report — the product earns trust on run one, converts on run two.

### Highest-leverage early moves

1. **Usage gate** — ship the freemium wall first, it's the lowest-effort path to any MRR
2. **B2B licensing** — tenant advocacy orgs, renter's unions, and real estate attorneys would pay $50–200/month for white-labeled access for their clients. Much higher LTV than individual renters, far fewer customers needed to hit meaningful MRR
3. **Referral/affiliate** — partner with renter's insurance providers (Lemonade, etc.) or moving companies for a referral fee per conversion. Zero marginal cost once the integration is live

### LTV consideration

Individual renters negotiate their lease roughly once a year — low natural retention. The "alerts + history" loop and the B2B angle both solve this by creating recurring reasons to stay subscribed beyond the one-time negotiation event.
