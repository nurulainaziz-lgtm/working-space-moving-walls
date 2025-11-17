"""POI Classification Module

This module provides functions to classify Points of Interest (POI) into categories.
"""

def classify_poi(poi_type, poi):
    """
    Classify a POI into one of four categories:
    - business
    - tourism
    - public_services
    - transportation

    Parameters:
    -----------
    poi_type : str
        The type category of the POI (e.g., 'amenity', 'tourism', 'shop')
    poi : str
        The specific POI subcategory (e.g., 'restaurant', 'guest_house')

    Returns:
    --------
    str
        The classified category
    """

    # Business establishments
    business_pois = {
        'shop': ['convenience', 'supermarket', 'bakery', 'butcher', 'clothes'],
        'amenity': ['restaurant', 'cafe', 'pub', 'bar', 'fast_food', 'bank', 'pharmacy']
    }

    # Tourism facilities
    tourism_pois = {
        'tourism': ['guest_house', 'hotel', 'motel', 'information', 'museum', 'attraction', 'viewpoint']
    }

    # Public services
    public_service_pois = {
        'amenity': ['police', 'post_office', 'social_facility', 'place_of_worship',
                    'post_box', 'townhall', 'library', 'hospital', 'clinic', 'school', 'university']
    }

    # Transportation infrastructure
    transportation_pois = {
        'highway': ['traffic_signals', 'bus_stop', 'crossing'],
        'amenity': ['ferry_terminal', 'bus_station', 'taxi', 'parking'],
        'public_transport': ['platform', 'station', 'stop_position']
    }

    # Classification logic with priority
    # 1. Check tourism first (most specific)
    if poi_type in tourism_pois and poi in tourism_pois[poi_type]:
        return 'tourism'

    # 2. Check transportation
    if poi_type in transportation_pois and poi in transportation_pois[poi_type]:
        return 'transportation'

    # 3. Check public services
    if poi_type in public_service_pois and poi in public_service_pois[poi_type]:
        return 'public_services'

    # 4. Check business
    if poi_type in business_pois and poi in business_pois[poi_type]:
        return 'business'

    # 5. Default fallback based on poi_type
    if poi_type == 'tourism':
        return 'tourism'
    elif poi_type in ['highway', 'public_transport']:
        return 'transportation'
    elif poi_type == 'shop':
        return 'business'
    else:
        return 'other'


if __name__ == "__main__":
    # Test cases
    test_cases = [
        ('amenity', 'restaurant'),
        ('tourism', 'guest_house'),
        ('amenity', 'police'),
        ('highway', 'traffic_signals'),
        ('public_transport', 'platform'),
        ('shop', 'convenience'),
        ('amenity', 'cafe'),
        ('amenity', 'post_office')
    ]

    print("POI Classification Test Results:")
    print("=" * 60)
    for poi_type, poi in test_cases:
        category = classify_poi(poi_type, poi)
        print(f"{poi_type:20} | {poi:20} | {category}")
