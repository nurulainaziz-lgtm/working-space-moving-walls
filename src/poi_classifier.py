"""POI Classification Module

This module provides functions to classify Points of Interest (POI) into categories.
Optimized for large datasets with comprehensive Japanese POI coverage.
"""

def classify_poi(poi_type, poi):
    """
    Classify a POI into one of seven main categories:
    - business: Commercial establishments and retail
    - tourism: Tourism facilities and attractions
    - public_services: Government, education, healthcare, community services
    - transportation: Roads, transit, traffic infrastructure
    - residential: Housing and residential buildings
    - infrastructure: Utilities, landuse, industrial facilities
    - other: Uncategorized POIs

    Parameters:
    -----------
    poi_type : str
        The type category of the POI (e.g., 'amenity', 'tourism', 'shop', 'highway', 'building')
    poi : str
        The specific POI subcategory (e.g., 'restaurant', 'guest_house', 'house', 'residential')

    Returns:
    --------
    str
        The classified category

    Performance:
    -----------
    Uses set-based lookups for O(1) performance on large datasets (1M+ records)
    """

    # Business establishments (shops, restaurants, commercial services)
    # Using sets for O(1) lookup performance
    business_shops = {
        'convenience', 'supermarket', 'bakery', 'butcher', 'clothes', 'mall',
        'department_store', 'kiosk', 'general', 'car', 'bicycle', 'books',
        'gift', 'jewelry', 'mobile_phone', 'electronics', 'alcohol', 'beverages',
        'variety_store', 'wholesale', 'chemist', 'beauty', 'hairdresser',
        'laundry', 'dry_cleaning', 'seafood', 'greengrocer', 'florist'
    }

    business_amenities = {
        'restaurant', 'cafe', 'pub', 'bar', 'fast_food', 'food_court', 'ice_cream',
        'bank', 'atm', 'bureau_de_change', 'pharmacy', 'marketplace', 'vending_machine',
        'fuel', 'car_wash', 'car_rental', 'charging_station'
    }

    business_buildings = {
        'retail', 'commercial', 'supermarket', 'kiosk', 'shop', 'office'
    }

    # Tourism facilities
    tourism_pois = {
        'guest_house', 'hotel', 'motel', 'hostel', 'apartment', 'camp_site',
        'information', 'museum', 'attraction', 'viewpoint', 'theme_park',
        'zoo', 'artwork', 'gallery', 'picnic_site', 'camp_pitch'
    }

    # Public services (education, healthcare, government, community)
    public_service_amenities = {
        'police', 'post_office', 'social_facility', 'place_of_worship', 'post_box',
        'townhall', 'library', 'hospital', 'clinic', 'doctors', 'dentist', 'pharmacy',
        'school', 'university', 'college', 'kindergarten', 'childcare', 'community_centre',
        'public_building', 'courthouse', 'embassy', 'fire_station', 'grave_yard',
        'nursing_home', 'recycling', 'shelter', 'toilets', 'waste_basket',
        'waste_disposal', 'veterinary', 'animal_shelter', 'drinking_water', 'fountain',
        'bench', 'shower', 'telephone', 'boat_storage'  # Public amenities
    }

    public_service_buildings = {
        'school', 'hospital', 'civic', 'government', 'public', 'college',
        'university', 'kindergarten', 'library', 'fire_station'
    }

    # Transportation infrastructure (roads, rails, transit, parking)
    transportation_highways = {
        'traffic_signals', 'bus_stop', 'crossing', 'stop', 'street_lamp',
        'motorway', 'motorway_link', 'trunk', 'trunk_link', 'primary', 'primary_link',
        'secondary', 'secondary_link', 'tertiary', 'tertiary_link', 'unclassified',
        'residential', 'service', 'track', 'footway', 'path', 'steps', 'pedestrian',
        'cycleway', 'bridleway', 'turning_circle', 'turning_loop', 'mini_roundabout',
        'motorway_junction', 'rest_area', 'speed_camera', 'give_way', 'elevator'
    }

    transportation_amenities = {
        'ferry_terminal', 'bus_station', 'taxi', 'parking', 'bicycle_parking',
        'parking_entrance', 'parking_space', 'motorcycle_parking'
    }

    transportation_public_transport = {
        'platform', 'station', 'stop_position', 'stop_area', 'halt'
    }

    transportation_railway = {
        'rail', 'subway', 'tram', 'light_rail', 'monorail', 'narrow_gauge',
        'funicular', 'level_crossing', 'crossing', 'switch', 'signal', 'buffer_stop',
        'platform', 'station', 'halt', 'tram_stop'
    }

    transportation_aeroway = {
        'aerodrome', 'helipad', 'terminal', 'gate', 'apron', 'taxiway', 'runway'
    }

    # Residential buildings
    residential_buildings = {
        'house', 'apartments', 'residential', 'detached', 'terrace', 'dormitory',
        'bungalow', 'static_caravan', 'cabin', 'hut', 'farm_auxiliary', 'barn',
        'greenhouse', 'roof'  # roof often indicates residential structures
    }

    # Infrastructure (landuse, utilities, industrial)
    infrastructure_landuse = {
        'farmland', 'farm', 'orchard', 'vineyard', 'forest', 'wood', 'meadow',
        'grass', 'industrial', 'commercial', 'retail', 'residential', 'cemetery',
        'reservoir', 'basin', 'construction', 'railway', 'military', 'quarry',
        'landfill', 'plant_nursery', 'allotments', 'recreation_ground', 'village_green'
    }

    infrastructure_buildings = {
        'industrial', 'warehouse', 'construction', 'garages', 'garage', 'shed',
        'service', 'transformer_tower', 'water_tower', 'storage_tank', 'silo',
        'ruins', 'bunker', 'bridge', 'transportation', 'train_station', 'parking',
        'hangar', 'container'
    }

    infrastructure_amenities = {
        'waste_transfer_station', 'wastewater_plant', 'water_works'
    }

    # General buildings (default to infrastructure if not otherwise classified)
    general_buildings = {'yes', 'building'}  # Generic building tag

    # ==========================================
    # Classification logic with priority
    # ==========================================

    # Priority 1: Tourism (highest specificity for tourism-related facilities)
    if poi_type == 'tourism' and poi in tourism_pois:
        return 'tourism'

    # Priority 2: Residential buildings
    if poi_type == 'building' and poi in residential_buildings:
        return 'residential'

    # Priority 3: Transportation infrastructure
    if poi_type == 'highway' and poi in transportation_highways:
        return 'transportation'
    if poi_type == 'amenity' and poi in transportation_amenities:
        return 'transportation'
    if poi_type == 'public_transport' and poi in transportation_public_transport:
        return 'transportation'
    if poi_type == 'railway' and poi in transportation_railway:
        return 'transportation'
    if poi_type == 'aeroway' and poi in transportation_aeroway:
        return 'transportation'

    # Priority 4: Public services
    if poi_type == 'amenity' and poi in public_service_amenities:
        return 'public_services'
    if poi_type == 'building' and poi in public_service_buildings:
        return 'public_services'

    # Priority 5: Business
    if poi_type == 'shop' and poi in business_shops:
        return 'business'
    if poi_type == 'amenity' and poi in business_amenities:
        return 'business'
    if poi_type == 'building' and poi in business_buildings:
        return 'business'

    # Priority 6: Infrastructure
    if poi_type == 'landuse' and poi in infrastructure_landuse:
        return 'infrastructure'
    if poi_type == 'building' and poi in infrastructure_buildings:
        return 'infrastructure'
    if poi_type == 'amenity' and poi in infrastructure_amenities:
        return 'infrastructure'

    # Priority 7: Generic buildings (default to infrastructure)
    if poi_type == 'building' and poi in general_buildings:
        return 'infrastructure'

    # ==========================================
    # Fallback classification based on poi_type
    # ==========================================
    if poi_type == 'tourism':
        return 'tourism'
    elif poi_type in {'highway', 'public_transport', 'railway', 'aeroway'}:
        return 'transportation'
    elif poi_type == 'shop':
        return 'business'
    elif poi_type == 'building':
        return 'infrastructure'
    elif poi_type == 'landuse':
        return 'infrastructure'
    else:
        return 'other'


if __name__ == "__main__":
    # Comprehensive test cases covering all categories
    test_cases = [
        # Business
        ('amenity', 'restaurant'),
        ('shop', 'convenience'),
        ('amenity', 'cafe'),
        ('amenity', 'vending_machine'),
        ('amenity', 'fuel'),
        ('shop', 'supermarket'),
        ('building', 'retail'),

        # Tourism
        ('tourism', 'guest_house'),
        ('tourism', 'hotel'),
        ('tourism', 'information'),
        ('tourism', 'museum'),

        # Public Services
        ('amenity', 'police'),
        ('amenity', 'post_office'),
        ('amenity', 'school'),
        ('amenity', 'kindergarten'),
        ('amenity', 'social_facility'),
        ('amenity', 'place_of_worship'),
        ('building', 'school'),
        ('amenity', 'toilets'),

        # Transportation
        ('highway', 'traffic_signals'),
        ('highway', 'unclassified'),
        ('highway', 'residential'),
        ('highway', 'tertiary'),
        ('highway', 'crossing'),
        ('public_transport', 'platform'),
        ('railway', 'rail'),
        ('railway', 'level_crossing'),
        ('amenity', 'parking'),

        # Residential
        ('building', 'house'),
        ('building', 'apartments'),
        ('building', 'residential'),
        ('building', 'greenhouse'),

        # Infrastructure
        ('building', 'yes'),
        ('landuse', 'farmland'),
        ('landuse', 'grass'),
        ('landuse', 'cemetery'),
        ('landuse', 'forest'),
        ('building', 'industrial'),
    ]

    print("\n" + "=" * 80)
    print("POI CLASSIFICATION TEST RESULTS - Enhanced Classifier")
    print("=" * 80)
    print(f"{'POI Type':<25} {'POI':<25} {'Category':<20}")
    print("-" * 80)

    # Track category counts
    category_counts = {}

    for poi_type, poi in test_cases:
        category = classify_poi(poi_type, poi)
        category_counts[category] = category_counts.get(category, 0) + 1
        print(f"{poi_type:<25} {poi:<25} {category:<20}")

    print("=" * 80)
    print("\nCategory Distribution:")
    print("-" * 40)
    for category, count in sorted(category_counts.items(), key=lambda x: x[1], reverse=True):
        percentage = (count / len(test_cases)) * 100
        print(f"  {category:<20}: {count:>3} ({percentage:>5.1f}%)")
    print("-" * 40)
    print(f"  {'Total':<20}: {len(test_cases):>3}")
    print("=" * 80 + "\n")
