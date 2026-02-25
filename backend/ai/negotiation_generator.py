"""AI-powered negotiation script and email generator.

Supports multiple LLM providers: OpenAI, Groq, Mistral, Ollama, or mock fallback.
"""

from datetime import datetime, timedelta
from backend.models import (
    ApartmentInput, MarketAnalysis, ComparableListing,
    NegotiationScript, TimingAdvice
)
from backend.config import settings


def _get_timing_advice(lease_end_date: str | None) -> TimingAdvice:
    """Calculate timing advice based on lease end date."""
    tips = [
        "Start negotiations 60-90 days before your lease ends for maximum leverage",
        "Landlords prefer to avoid turnover costs ($2,000-5,000+ per unit)",
        "Winter months (Nov-Feb) typically have less demand — better for negotiating",
        "If your lease is month-to-month, you have more flexibility but less urgency",
    ]
    
    if not lease_end_date:
        return TimingAdvice(
            days_until_lease_end=None,
            optimal_window="Start as soon as possible — 60-90 days before renewal is ideal",
            urgency="unknown",
            tips=tips,
        )
    
    try:
        end_date = datetime.strptime(lease_end_date, "%Y-%m-%d")
        days_left = (end_date - datetime.now()).days
        
        if days_left < 0:
            return TimingAdvice(
                days_until_lease_end=days_left,
                optimal_window="Your lease has already ended. You may be on month-to-month — negotiate now!",
                urgency="urgent",
                tips=tips,
            )
        elif days_left < 30:
            return TimingAdvice(
                days_until_lease_end=days_left,
                optimal_window=f"Only {days_left} days left! Act immediately — but don't panic. Present data calmly.",
                urgency="urgent",
                tips=tips,
            )
        elif days_left < 90:
            return TimingAdvice(
                days_until_lease_end=days_left,
                optimal_window=f"Perfect timing! You have {days_left} days — this is the optimal negotiation window.",
                urgency="optimal",
                tips=tips,
            )
        else:
            return TimingAdvice(
                days_until_lease_end=days_left,
                optimal_window=f"You have {days_left} days — start preparing your case. Best to initiate 60-90 days before renewal.",
                urgency="early",
                tips=tips,
            )
    except ValueError:
        return TimingAdvice(
            days_until_lease_end=None,
            optimal_window="Start as soon as possible — 60-90 days before renewal is ideal",
            urgency="unknown",
            tips=tips,
        )


def _generate_template_script(
    apartment: ApartmentInput,
    analysis: MarketAnalysis,
    comparables: list[ComparableListing],
) -> NegotiationScript:
    """Generate a negotiation script using templates (no LLM needed)."""
    
    timing = _get_timing_advice(apartment.lease_end_date)
    
    # Build key data points
    sorted_comps = sorted(comparables, key=lambda c: c.adjusted_rent or c.rent)[:5]
    avg_comp_rent = sum(c.adjusted_rent or c.rent for c in sorted_comps) / len(sorted_comps) if sorted_comps else apartment.current_rent
    
    key_data_points = [
        f"Market analysis of {analysis.num_comparables} comparable units within 0.5 miles",
        f"Average comparable rent: ${avg_comp_rent:,.0f}/month",
        f"Your current rent: ${apartment.current_rent:,.0f}/month",
    ]
    
    if analysis.is_overpaying:
        key_data_points.append(
            f"You are paying ${analysis.difference:,.0f}/month ({analysis.difference_percent:.1f}%) above market average"
        )
        key_data_points.append(
            f"Potential annual savings: ${analysis.potential_annual_savings:,.0f}"
        )
    
    # Comparison summary
    comp_lines = []
    for i, comp in enumerate(sorted_comps[:3], 1):
        rent = comp.adjusted_rent or comp.rent
        comp_lines.append(
            f"  {i}. {comp.address} — ${rent:,.0f}/mo ({comp.bedrooms}BR, {comp.sqft or 'N/A'} sqft, {comp.distance_miles:.2f} mi away)"
        )
    comparison_summary = "Most comparable units:\n" + "\n".join(comp_lines)
    
    # Opening statement
    opening = (
        f"Hi, I'm reaching out regarding my lease renewal at {apartment.address}. "
        f"I've been a great tenant and I'd love to continue living here. "
        f"Before we discuss renewal terms, I did some research on the current rental market "
        f"in our area and wanted to share what I found."
    )
    
    # Suggested ask
    if analysis.is_overpaying:
        suggested_ask = (
            f"Based on my research, I'd like to propose a renewal rate of ${analysis.suggested_rent:,.0f}/month, "
            f"which reflects the current market conditions. This is a reduction of "
            f"${apartment.current_rent - analysis.suggested_rent:,.0f}/month from my current rent of ${apartment.current_rent:,.0f}. "
            f"I believe this is a fair rate that's still competitive for the area."
        )
    else:
        suggested_ask = (
            f"My research shows that my current rent of ${apartment.current_rent:,.0f}/month is at or below market rate. "
            f"I'd like to discuss keeping my rent at the current level, or at most a modest increase below the typical 3-5% range."
        )
    
    # Closing
    closing = (
        "I value living here and want to make this work for both of us. "
        "I've been reliable with rent payments and take good care of the unit. "
        "Finding a new tenant and turnover typically costs landlords $2,000-5,000+, "
        "so keeping a good tenant at a fair rate is beneficial for everyone. "
        "I'd love to discuss this further at your convenience."
    )
    
    # Full script
    full_script = f"""NEGOTIATION SCRIPT
==================

{opening}

KEY FINDINGS:
{chr(10).join(f'• {dp}' for dp in key_data_points)}

{comparison_summary}

MY PROPOSAL:
{suggested_ask}

{closing}
"""
    
    # Email template
    tenant_name = "Tenant"
    email_subject = f"Lease Renewal Discussion — {apartment.address}"
    email_body = f"""Dear [Landlord/Property Manager Name],

I hope this email finds you well. I'm writing regarding the upcoming renewal of my lease at {apartment.address}.

I've thoroughly enjoyed living here and would very much like to continue as your tenant. As we approach the renewal period, I wanted to share some market research I've conducted that I believe will be helpful for our discussion.

After analyzing {analysis.num_comparables} comparable rental listings within a 0.5-mile radius, I found that the current market rate for similar units in our area averages ${analysis.market_rate:,.0f}/month. My current rent of ${apartment.current_rent:,.0f}/month is {'above' if analysis.is_overpaying else 'in line with'} this market average.

Comparable listings I reviewed include:
{chr(10).join(comp_lines)}

{"Given these findings, I'd like to propose a renewal rate of $" + f"{analysis.suggested_rent:,.0f}/month, which reflects the current market conditions while still being a competitive rate for the area." if analysis.is_overpaying else "I believe my current rate is fair, and I would appreciate keeping it at the same level for the renewal period."}

As a tenant, I've consistently paid rent on time, maintained the apartment well, and been considerate of neighbors. I understand that tenant turnover involves significant costs and downtime, and I'm confident that continuing our arrangement is mutually beneficial.

I'd welcome the opportunity to discuss this further at your convenience. Please let me know a good time to connect.

Thank you for your consideration.

Best regards,
[Your Name]
{apartment.address}"""
    
    return NegotiationScript(
        opening_statement=opening,
        key_data_points=key_data_points,
        comparison_summary=comparison_summary,
        suggested_ask=suggested_ask,
        closing_statement=closing,
        full_script=full_script,
        email_subject=email_subject,
        email_body=email_body,
        timing_advice=timing,
    )


async def _generate_llm_script(
    apartment: ApartmentInput,
    analysis: MarketAnalysis,
    comparables: list[ComparableListing],
) -> NegotiationScript:
    """Generate a negotiation script using an LLM provider."""
    
    # Build context for the LLM
    comp_summaries = []
    sorted_comps = sorted(comparables, key=lambda c: c.adjusted_rent or c.rent)[:5]
    for comp in sorted_comps:
        comp_summaries.append(
            f"- {comp.address}: ${comp.adjusted_rent or comp.rent:,.0f}/mo, "
            f"{comp.bedrooms}BR/{comp.bathrooms}BA, {comp.sqft or 'N/A'} sqft, "
            f"{comp.distance_miles:.2f} mi away ({comp.source})"
        )
    
    prompt = f"""You are an expert rent negotiation coach. Generate a personalized, natural-sounding 
negotiation script for a tenant who wants to negotiate their rent. Be specific with data points 
and make it sound conversational, NOT robotic.

TENANT'S APARTMENT:
- Address: {apartment.address}, {apartment.city}, {apartment.state}
- Current Rent: ${apartment.current_rent:,.0f}/month
- Unit: {apartment.bedrooms}BR/{apartment.bathrooms}BA, {apartment.sqft or 'N/A'} sqft
- Floor: {apartment.floor_level or 'N/A'}
- Amenities: {', '.join(apartment.amenities) if apartment.amenities else 'Not specified'}

MARKET ANALYSIS:
- Market Rate: ${analysis.market_rate:,.0f}/month (range: ${analysis.market_rate_low:,.0f}-${analysis.market_rate_high:,.0f})
- Overpaying: {'Yes, by $' + f'{analysis.difference:,.0f}/month ({analysis.difference_percent:.1f}%)' if analysis.is_overpaying else 'No'}
- Suggested Rent: ${analysis.suggested_rent:,.0f}/month
- Negotiation Strength: {analysis.negotiation_strength}
- Based on {analysis.num_comparables} comparable listings

TOP COMPARABLES:
{chr(10).join(comp_summaries)}

Please generate:
1. A natural opening statement
2. 4-5 specific data-backed talking points
3. A clear proposal with the suggested rent amount
4. A confident but respectful closing
5. A professional email to the landlord

Format your response as JSON with these keys:
- opening_statement
- key_data_points (array of strings)
- comparison_summary
- suggested_ask
- closing_statement
- full_script (complete script combining all above)
- email_subject
- email_body
"""
    
    try:
        response_text = await _call_llm(prompt)
        
        # Try to parse as JSON
        import json
        import re
        # Try to extract JSON from the response
        json_start = response_text.find("{")
        json_end = response_text.rfind("}") + 1
        if json_start >= 0 and json_end > json_start:
            json_str = response_text[json_start:json_end]
            # Strip control characters that LLMs sometimes emit in string values
            json_str = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f]', ' ', json_str)
            data = json.loads(json_str)
            
            timing = _get_timing_advice(apartment.lease_end_date)
            
            return NegotiationScript(
                opening_statement=data.get("opening_statement", ""),
                key_data_points=data.get("key_data_points", []),
                comparison_summary=data.get("comparison_summary", ""),
                suggested_ask=data.get("suggested_ask", ""),
                closing_statement=data.get("closing_statement", ""),
                full_script=data.get("full_script", ""),
                email_subject=data.get("email_subject", f"Lease Renewal Discussion — {apartment.address}"),
                email_body=data.get("email_body", ""),
                timing_advice=timing,
            )
    except Exception as e:
        print(f"LLM generation failed: {e}, falling back to template")
    
    # Fallback to template
    return _generate_template_script(apartment, analysis, comparables)


async def _call_llm(prompt: str) -> str:
    """Call the configured LLM provider."""
    provider = settings.LLM_PROVIDER.lower()
    
    if provider == "openai":
        from openai import AsyncOpenAI
        client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        response = await client.chat.completions.create(
            model=settings.OPENAI_MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
        )
        return response.choices[0].message.content or ""
    
    elif provider == "groq":
        from openai import AsyncOpenAI
        client = AsyncOpenAI(
            api_key=settings.GROQ_API_KEY,
            base_url="https://api.groq.com/openai/v1",
        )
        response = await client.chat.completions.create(
            model=settings.GROQ_MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
        )
        return response.choices[0].message.content or ""
    
    elif provider == "mistral":
        from openai import AsyncOpenAI
        client = AsyncOpenAI(
            api_key=settings.MISTRAL_API_KEY,
            base_url="https://api.mistral.ai/v1",
        )
        response = await client.chat.completions.create(
            model=settings.MISTRAL_MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
        )
        return response.choices[0].message.content or ""
    
    elif provider == "ollama":
        import httpx
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{settings.OLLAMA_BASE_URL}/api/generate",
                json={"model": settings.OLLAMA_MODEL, "prompt": prompt, "stream": False},
                timeout=120.0,
            )
            return response.json().get("response", "")
    
    else:
        raise ValueError(f"Unknown LLM provider: {provider}")


async def generate_negotiation(
    apartment: ApartmentInput,
    analysis: MarketAnalysis,
    comparables: list[ComparableListing],
) -> NegotiationScript:
    """Generate a negotiation script using the configured provider.
    
    Falls back to template-based generation if LLM is unavailable or set to 'mock'.
    """
    if settings.LLM_PROVIDER.lower() == "mock":
        return _generate_template_script(apartment, analysis, comparables)
    
    return await _generate_llm_script(apartment, analysis, comparables)
