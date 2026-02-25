"""Market analysis engine for comparing rental listings."""

import statistics
from backend.models import ApartmentInput, ComparableListing, MarketAnalysis


def analyze_market(
    apartment: ApartmentInput,
    comparables: list[ComparableListing],
) -> MarketAnalysis:
    """Perform comparative market analysis.
    
    Adjusts comparable rents for differences in features
    and calculates a fair market rate.
    """
    if not comparables:
        # No comps found — return user's own rent as market rate
        return MarketAnalysis(
            market_rate=apartment.current_rent,
            market_rate_low=apartment.current_rent * 0.95,
            market_rate_high=apartment.current_rent * 1.05,
            user_rent=apartment.current_rent,
            difference=0,
            difference_percent=0,
            is_overpaying=False,
            potential_monthly_savings=0,
            potential_annual_savings=0,
            confidence_score=0.0,
            num_comparables=0,
            suggested_rent=apartment.current_rent,
            negotiation_strength="weak",
        )
    
    # Adjust each comparable's rent to account for differences
    adjusted_comps = []
    for comp in comparables:
        adjusted_rent = comp.rent
        notes = []
        
        # Square footage adjustment ($1.50-2.50 per sqft difference)
        if apartment.sqft and comp.sqft:
            sqft_diff = apartment.sqft - comp.sqft
            per_sqft_rate = 2.0
            sqft_adj = sqft_diff * per_sqft_rate
            adjusted_rent += sqft_adj
            if abs(sqft_adj) > 20:
                notes.append(f"Sq ft adjustment: ${sqft_adj:+.0f} ({sqft_diff:+d} sqft)")
        
        # Floor level adjustment (~$25-50 per floor)
        if apartment.floor_level and comp.floor_level:
            floor_diff = apartment.floor_level - comp.floor_level
            floor_adj = floor_diff * 35
            adjusted_rent += floor_adj
            if abs(floor_adj) > 20:
                notes.append(f"Floor adjustment: ${floor_adj:+.0f} ({floor_diff:+d} floors)")
        
        # Amenity adjustments
        user_amenities = set(a.lower() for a in apartment.amenities)
        comp_amenities = set(a.lower() for a in comp.amenities)
        
        premium_amenities = {
            "doorman": 150, "concierge": 200, "gym": 75, "laundry in-unit": 100,
            "roof deck": 50, "balcony": 75, "central ac": 50, "outdoor space": 60,
            "city views": 40, "natural light": 30, "elevator": 40,
        }
        
        # Comp has amenities that user doesn't → comp is worth less comparatively
        for amenity in comp_amenities - user_amenities:
            if amenity in premium_amenities:
                adj = -premium_amenities[amenity]
                adjusted_rent += adj
                notes.append(f"Comp has {amenity}: ${adj:+.0f}")
        
        # User has amenities that comp doesn't → user's unit is worth more
        for amenity in user_amenities - comp_amenities:
            if amenity in premium_amenities:
                adj = premium_amenities[amenity]
                adjusted_rent += adj
                notes.append(f"User has {amenity}: ${adj:+.0f}")
        
        # Distance weighting — closer comps get more weight
        distance_weight = max(0.3, 1.0 - (comp.distance_miles / 0.5) * 0.5)
        
        comp.adjusted_rent = round(adjusted_rent, 2)
        comp.adjustment_notes = notes
        adjusted_comps.append((comp, distance_weight))
    
    # Calculate weighted market rate
    weighted_rents = [comp.adjusted_rent * w for comp, w in adjusted_comps if comp.adjusted_rent]
    total_weight = sum(w for _, w in adjusted_comps)
    
    if total_weight > 0:
        market_rate = sum(weighted_rents) / total_weight
    else:
        market_rate = statistics.mean([c.adjusted_rent or c.rent for c in comparables])
    
    # Statistical spread
    raw_rents = [c.adjusted_rent or c.rent for c in comparables]
    try:
        rent_stdev = statistics.stdev(raw_rents)
    except statistics.StatisticsError:
        rent_stdev = 0
    
    market_rate_low = max(0, market_rate - rent_stdev)
    market_rate_high = market_rate + rent_stdev
    
    # Metrics
    difference = apartment.current_rent - market_rate
    difference_percent = (difference / market_rate * 100) if market_rate > 0 else 0
    is_overpaying = difference > 50  # Threshold for "overpaying"
    
    potential_monthly_savings = max(0, difference) if is_overpaying else 0
    potential_annual_savings = potential_monthly_savings * 12
    
    # Confidence score based on number and consistency of comps
    num_comps = len(comparables)
    comp_score = min(1.0, num_comps / 10)  # More comps = higher confidence
    consistency_score = max(0, 1.0 - (rent_stdev / market_rate)) if market_rate > 0 else 0
    confidence_score = round((comp_score * 0.4 + consistency_score * 0.6), 2)
    
    # Suggested rent and negotiation strength
    if is_overpaying:
        # Suggest 5-10% below current rent, but not below market
        suggested_reduction = min(difference * 0.8, apartment.current_rent * 0.10)
        suggested_rent = round(apartment.current_rent - suggested_reduction, -1)
        
        if difference_percent > 15:
            negotiation_strength = "strong"
        elif difference_percent > 8:
            negotiation_strength = "moderate"
        else:
            negotiation_strength = "moderate"
    else:
        suggested_rent = apartment.current_rent
        negotiation_strength = "weak"
    
    return MarketAnalysis(
        market_rate=round(market_rate, 2),
        market_rate_low=round(market_rate_low, 2),
        market_rate_high=round(market_rate_high, 2),
        user_rent=apartment.current_rent,
        difference=round(difference, 2),
        difference_percent=round(difference_percent, 1),
        is_overpaying=is_overpaying,
        potential_monthly_savings=round(potential_monthly_savings, 2),
        potential_annual_savings=round(potential_annual_savings, 2),
        confidence_score=confidence_score,
        num_comparables=num_comps,
        suggested_rent=round(suggested_rent, 2),
        negotiation_strength=negotiation_strength,
    )
