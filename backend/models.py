"""Pydantic models for the RentBack API."""

from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum


class ApartmentInput(BaseModel):
    """User's apartment details for analysis."""
    address: str = Field(..., description="Full street address")
    city: str = Field(default="New York", description="City name")
    state: str = Field(default="NY", description="State abbreviation")
    zip_code: str = Field(default="", description="ZIP code")
    
    # Unit specs
    bedrooms: int = Field(..., ge=0, le=10, description="Number of bedrooms (0 = studio)")
    bathrooms: float = Field(..., ge=0.5, le=5, description="Number of bathrooms")
    sqft: Optional[int] = Field(None, ge=100, le=10000, description="Square footage")
    floor_level: Optional[int] = Field(None, ge=0, le=100, description="Floor level")
    
    # Rent info
    current_rent: float = Field(..., gt=0, description="Current monthly rent in USD")
    lease_end_date: Optional[str] = Field(None, description="Lease end date (YYYY-MM-DD)")
    
    # Amenities
    amenities: list[str] = Field(default_factory=list, description="List of amenities")
    
    # Building info
    building_type: Optional[str] = Field(None, description="e.g., 'walk-up', 'elevator', 'high-rise'")
    year_built: Optional[int] = Field(None, description="Year the building was built")


class ComparableListing(BaseModel):
    """A comparable rental listing found in the market."""
    address: str
    distance_miles: float = Field(..., description="Distance from user's apartment")
    rent: float = Field(..., description="Monthly rent in USD")
    bedrooms: int
    bathrooms: float
    sqft: Optional[int] = None
    floor_level: Optional[int] = None
    amenities: list[str] = Field(default_factory=list)
    building_type: Optional[str] = None
    listing_url: Optional[str] = None
    source: str = Field(..., description="Data source (e.g., 'zillow', 'apartments.com')")
    description: Optional[str] = None
    date_listed: Optional[str] = None
    
    # Adjusted rent (after accounting for differences)
    adjusted_rent: Optional[float] = None
    adjustment_notes: list[str] = Field(default_factory=list)


class SentimentScore(BaseModel):
    """Sentiment analysis of listing description."""
    flexibility_score: float = Field(..., ge=0, le=1, description="0-1 score of landlord flexibility")
    urgency_signals: list[str] = Field(default_factory=list)
    positive_indicators: list[str] = Field(default_factory=list)
    negative_indicators: list[str] = Field(default_factory=list)


class MarketAnalysis(BaseModel):
    """Market analysis results."""
    market_rate: float = Field(..., description="Estimated fair market rent")
    market_rate_low: float = Field(..., description="Low end of market range")
    market_rate_high: float = Field(..., description="High end of market range")
    
    user_rent: float = Field(..., description="User's current rent")
    difference: float = Field(..., description="Difference: user_rent - market_rate")
    difference_percent: float = Field(..., description="Percentage difference")
    
    is_overpaying: bool = Field(..., description="Whether user is overpaying")
    potential_monthly_savings: float = Field(..., ge=0)
    potential_annual_savings: float = Field(..., ge=0)
    
    confidence_score: float = Field(..., ge=0, le=1, description="Confidence in the analysis")
    num_comparables: int = Field(..., description="Number of comparables used")
    
    # Recommendation
    suggested_rent: float = Field(..., description="Suggested asking price")
    negotiation_strength: str = Field(..., description="'strong', 'moderate', 'weak'")


class TimingAdvice(BaseModel):
    """Advice on when to negotiate."""
    days_until_lease_end: Optional[int] = None
    optimal_window: str = Field(..., description="When to start negotiating")
    urgency: str = Field(..., description="'urgent', 'optimal', 'early', 'unknown'")
    tips: list[str] = Field(default_factory=list)


class NegotiationScript(BaseModel):
    """AI-generated negotiation script."""
    opening_statement: str
    key_data_points: list[str]
    comparison_summary: str
    suggested_ask: str
    closing_statement: str
    full_script: str
    
    # Email template
    email_subject: str
    email_body: str
    
    # Timing
    timing_advice: TimingAdvice


class AnalysisResponse(BaseModel):
    """Complete analysis response sent to the frontend."""
    apartment: ApartmentInput
    comparables: list[ComparableListing]
    analysis: MarketAnalysis
    negotiation: Optional[NegotiationScript] = None
    sentiment: Optional[SentimentScore] = None
