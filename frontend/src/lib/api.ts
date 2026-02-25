/* API client for communicating with the backend */

const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export interface ApartmentInput {
    address: string;
    city: string;
    state: string;
    zip_code: string;
    bedrooms: number;
    bathrooms: number;
    sqft: number | null;
    floor_level: number | null;
    current_rent: number;
    lease_end_date: string | null;
    amenities: string[];
    building_type: string | null;
    year_built: number | null;
}

export interface ComparableListing {
    address: string;
    distance_miles: number;
    rent: number;
    bedrooms: number;
    bathrooms: number;
    sqft: number | null;
    floor_level: number | null;
    amenities: string[];
    building_type: string | null;
    listing_url: string | null;
    source: string;
    description: string | null;
    date_listed: string | null;
    adjusted_rent: number | null;
    adjustment_notes: string[];
}

export interface MarketAnalysis {
    market_rate: number;
    market_rate_low: number;
    market_rate_high: number;
    user_rent: number;
    difference: number;
    difference_percent: number;
    is_overpaying: boolean;
    potential_monthly_savings: number;
    potential_annual_savings: number;
    confidence_score: number;
    num_comparables: number;
    suggested_rent: number;
    negotiation_strength: string;
}

export interface TimingAdvice {
    days_until_lease_end: number | null;
    optimal_window: string;
    urgency: string;
    tips: string[];
}

export interface NegotiationScript {
    opening_statement: string;
    key_data_points: string[];
    comparison_summary: string;
    suggested_ask: string;
    closing_statement: string;
    full_script: string;
    email_subject: string;
    email_body: string;
    timing_advice: TimingAdvice;
}

export interface AnalysisResponse {
    apartment: ApartmentInput;
    comparables: ComparableListing[];
    analysis: MarketAnalysis;
    negotiation: NegotiationScript | null;
    sentiment: null;
}

export async function analyzeApartment(input: ApartmentInput): Promise<AnalysisResponse> {
    const response = await fetch(`${API_BASE}/api/analyze`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(input),
    });

    if (!response.ok) {
        const error = await response.json().catch(() => ({ detail: 'Analysis failed' }));
        throw new Error(error.detail || 'Analysis failed');
    }

    return response.json();
}

export async function healthCheck(): Promise<{ status: string }> {
    const response = await fetch(`${API_BASE}/api/health`);
    return response.json();
}

export interface Stats {
    avg_annual_savings: number;
    avg_overpayment_rate: number;
    neighborhoods_covered: number;
}

export async function getStats(): Promise<Stats> {
    const response = await fetch(`${API_BASE}/api/stats`);
    if (!response.ok) throw new Error('Failed to fetch stats');
    return response.json();
}
