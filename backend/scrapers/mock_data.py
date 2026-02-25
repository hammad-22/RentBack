"""Mock data for realistic NYC rental listings demo."""

import random
from backend.models import ComparableListing


def generate_nyc_mock_comparables(
    bedrooms: int,
    bathrooms: float,
    sqft: int | None,
    base_rent: float,
    neighborhood: str = "Manhattan",
) -> list[ComparableListing]:
    """Generate realistic mock comparable listings for NYC.
    
    Produces 8-15 comparable rentals with realistic variations
    in rent, square footage, amenities, and distances.
    """
    
    # NYC neighborhood rent multipliers (relative to median)
    neighborhood_data = {
        "Upper East Side": {"base": 3200, "variance": 500, "addresses": [
            "221 E 76th St", "345 E 82nd St", "178 E 71st St", "402 E 79th St",
            "156 E 85th St", "289 E 73rd St", "433 E 80th St", "167 E 77th St",
        ]},
        "Upper West Side": {"base": 3100, "variance": 450, "addresses": [
            "155 W 72nd St", "290 W 86th St", "412 W 79th St", "178 W 68th St",
            "345 W 83rd St", "221 W 75th St", "467 W 81st St", "133 W 70th St",
        ]},
        "Midtown": {"base": 3500, "variance": 600, "addresses": [
            "350 W 50th St", "245 E 44th St", "178 W 56th St", "412 E 52nd St",
            "289 W 48th St", "156 E 54th St", "433 W 57th St", "201 E 46th St",
        ]},
        "East Village": {"base": 2800, "variance": 400, "addresses": [
            "156 E 7th St", "245 E 11th St", "89 E 4th St", "312 E 9th St",
            "178 E 6th St", "267 E 13th St", "134 E 3rd St", "389 E 10th St",
        ]},
        "West Village": {"base": 3300, "variance": 500, "addresses": [
            "89 Bedford St", "156 Christopher St", "245 W 4th St", "312 Bleecker St",
            "178 Grove St", "267 W 11th St", "134 Perry St", "389 Hudson St",
        ]},
        "Chelsea": {"base": 3100, "variance": 450, "addresses": [
            "245 W 20th St", "312 W 23rd St", "178 W 17th St", "156 W 26th St",
            "389 W 21st St", "134 W 19th St", "267 W 24th St", "412 W 18th St",
        ]},
        "Williamsburg": {"base": 2900, "variance": 400, "addresses": [
            "156 N 7th St", "289 Bedford Ave", "412 Metropolitan Ave", "178 Berry St",
            "345 Wythe Ave", "221 N 6th St", "467 Driggs Ave", "133 N 9th St",
        ]},
        "Brooklyn Heights": {"base": 3000, "variance": 400, "addresses": [
            "89 Montague St", "156 Henry St", "245 Clinton St", "312 Hicks St",
            "178 Joralemon St", "267 Columbia Heights", "134 Pineapple St", "389 Remsen St",
        ]},
        "Manhattan": {"base": 3200, "variance": 500, "addresses": [
            "245 E 34th St", "178 W 42nd St", "312 E 28th St", "156 W 37th St",
            "389 E 31st St", "134 W 45th St", "267 E 39th St", "412 W 33rd St",
        ]},
    }
    
    # Determine neighborhood
    hood = neighborhood_data.get(neighborhood, neighborhood_data["Manhattan"])
    
    # Amenities pool
    amenities_pool = [
        "Doorman", "Elevator", "Laundry In-Unit", "Laundry In Building",
        "Dishwasher", "Central AC", "Gym", "Roof Deck", "Pet Friendly",
        "Storage", "Bike Room", "Package Room", "Concierge",
        "Hardwood Floors", "Stainless Steel Appliances", "Renovated Kitchen",
        "Natural Light", "City Views", "Balcony", "Outdoor Space",
    ]
    
    building_types = ["walk-up", "elevator", "high-rise", "brownstone", "pre-war", "new-construction"]
    sources = ["zillow", "streeteasy", "apartments.com", "renthop"]
    
    descriptions = [
        "Bright and spacious apartment with great natural light. Recently renovated kitchen and bathroom. Close to subway.",
        "Charming unit in well-maintained building. Quiet tree-lined street. Available immediately. No fee!",
        "Must see! Beautiful apartment with modern finishes. Flexible lease terms. Pet-friendly building.",
        "Sun-drenched apartment with city views. Great closet space. Steps from restaurants and shopping.",
        "Renovated apartment featuring stainless steel appliances and hardwood floors throughout. Great location!",
        "Cozy apartment in the heart of the neighborhood. Close to parks and public transit. Won't last!",
        "Spacious layout with separate kitchen and living area. Natural light in every room. Landlord pays heat.",
        "Top-floor unit with skyline views. Updated bathroom. Laundry in building. Great value!",
        "Price reduced! Owner eager to rent. Modern kitchen, good closets, pet-friendly. Flexible move-in.",
        "Stunning apartment with exposed brick and high ceilings. Washer/dryer in unit. Rare find!",
    ]
    
    num_listings = random.randint(8, 15)
    comparables = []
    
    # Bedroom count adjustments
    bedroom_rent_adj = {0: -400, 1: 0, 2: 600, 3: 1200, 4: 2000}
    base_adj = bedroom_rent_adj.get(bedrooms, 0)
    
    for i in range(num_listings):
        address = random.choice(hood["addresses"])
        apt_num = random.choice(["1A", "2B", "3C", "4D", "5E", "6F", "PH", "1R", "3F", "2A", "7B"])
        full_address = f"{address}, Apt {apt_num}, New York, NY"
        
        # Rent variation based on bedrooms and neighborhood
        rent_base = hood["base"] + base_adj
        rent_variation = random.gauss(0, hood["variance"])
        listing_rent = round(max(rent_base + rent_variation, 1200), -1)  # Round to nearest 10
        
        # Square footage
        sqft_base = {0: 450, 1: 650, 2: 900, 3: 1200, 4: 1500}.get(bedrooms, 700)
        listing_sqft = sqft_base + random.randint(-100, 200)
        
        # Floor level
        floor = random.randint(1, 25) if random.random() > 0.3 else random.randint(1, 6)
        
        # Random amenities
        num_amenities = random.randint(3, 8)
        listing_amenities = random.sample(amenities_pool, num_amenities)
        
        building = random.choice(building_types)
        source = random.choice(sources)
        desc = random.choice(descriptions)
        
        # Distance (within 0.5 miles, with some just outside)
        distance = round(random.uniform(0.05, 0.55), 2)
        
        comparable = ComparableListing(
            address=full_address,
            distance_miles=distance,
            rent=listing_rent,
            bedrooms=bedrooms,
            bathrooms=bathrooms,
            sqft=listing_sqft,
            floor_level=floor,
            amenities=listing_amenities,
            building_type=building,
            listing_url=f"https://www.{source}.com/listing/{random.randint(100000, 999999)}",
            source=source,
            description=desc,
            date_listed=f"2025-{random.randint(1,2):02d}-{random.randint(1,28):02d}",
        )
        comparables.append(comparable)
    
    return comparables
