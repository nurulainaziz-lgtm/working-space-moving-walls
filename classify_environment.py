#!/usr/bin/env python3
"""
Environment Classification Script

This script analyzes POI data around given coordinates to classify the environment
as urban, suburban, or rural based on POI density and characteristics.

Usage:
    python classify_environment.py <latitude> <longitude> [radius_km] [data_file]

Examples:
    python classify_environment.py 24.4519 122.9440                    # Uses default 1km radius
    python classify_environment.py 24.4519 122.9440 2.0                # 2km radius
    python classify_environment.py 24.4519 122.9440 1.0 data/poi_data.csv  # Custom data file
"""

import pandas as pd
import sys
import math
from pathlib import Path
from src.poi_classifier import classify_poi


def haversine_distance(lat1, lon1, lat2, lon2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees).
    Returns distance in kilometers.
    """
    # Convert decimal degrees to radians
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))

    # Radius of earth in kilometers
    r = 6371

    return c * r


def classify_environment(lat, lon, pois_df, radius_km=1.0):
    """
    Classify the environment around given coordinates as urban, suburban, or rural.

    Parameters:
    -----------
    lat : float
        Latitude of the point
    lon : float
        Longitude of the point
    pois_df : DataFrame
        DataFrame with POI data (must have 'latitude', 'longitude', 'POI_type', 'POI' columns)
    radius_km : float
        Radius in kilometers to search around the point (default: 1.0 km)

    Returns:
    --------
    dict
        Classification results with environment type and analysis details
    """

    # Calculate distances to all POIs
    pois_df = pois_df.copy()
    pois_df['distance_km'] = pois_df.apply(
        lambda row: haversine_distance(lat, lon, row['latitude'], row['longitude']),
        axis=1
    )

    # Filter POIs within radius
    nearby_pois = pois_df[pois_df['distance_km'] <= radius_km].copy()

    # Classify POIs if not already classified
    if 'category' not in nearby_pois.columns:
        nearby_pois['category'] = nearby_pois.apply(
            lambda row: classify_poi(row['POI_type'], row['POI']),
            axis=1
        )

    # Calculate statistics
    total_pois = len(nearby_pois)
    area_km2 = math.pi * radius_km ** 2
    poi_density = total_pois / area_km2 if area_km2 > 0 else 0

    # Category distribution
    category_counts = nearby_pois['category'].value_counts().to_dict()

    # Calculate percentages
    category_percentages = {}
    for category, count in category_counts.items():
        category_percentages[category] = (count / total_pois * 100) if total_pois > 0 else 0

    # Urban indicators
    business_pct = category_percentages.get('business', 0)
    public_services_pct = category_percentages.get('public_services', 0)
    transportation_pct = category_percentages.get('transportation', 0)
    infrastructure_pct = category_percentages.get('infrastructure', 0)
    residential_pct = category_percentages.get('residential', 0)

    # Infrastructure type analysis
    infrastructure_pois = nearby_pois[nearby_pois['category'] == 'infrastructure']
    landuse_count = len(infrastructure_pois[infrastructure_pois['POI_type'] == 'landuse'])
    farmland_count = len(infrastructure_pois[
        (infrastructure_pois['POI_type'] == 'landuse') &
        (infrastructure_pois['POI'].isin(['farmland', 'forest', 'farm', 'orchard', 'meadow']))
    ])

    # Classification logic
    environment_type = None
    confidence = 0
    reasoning = []

    # Urban classification criteria
    if poi_density > 100:
        environment_type = 'urban'
        confidence = min(100, poi_density / 2)
        reasoning.append(f"Very high POI density: {poi_density:.1f} POIs/km²")
    elif poi_density > 50:
        # Check composition for urban/suburban distinction
        urban_score = business_pct + public_services_pct + (transportation_pct * 0.5)

        if urban_score > 40 or business_pct > 20:
            environment_type = 'urban'
            confidence = 75
            reasoning.append(f"High POI density: {poi_density:.1f} POIs/km²")
            reasoning.append(f"Significant commercial activity: {business_pct:.1f}% business POIs")
        else:
            environment_type = 'suburban'
            confidence = 70
            reasoning.append(f"Moderate POI density: {poi_density:.1f} POIs/km²")
            reasoning.append(f"Mixed residential and commercial: {residential_pct:.1f}% residential")

    elif poi_density > 20:
        # Suburban or rural distinction
        rural_indicators = farmland_count / total_pois if total_pois > 0 else 0

        if rural_indicators > 0.3 or infrastructure_pct > 60:
            environment_type = 'rural'
            confidence = 65
            reasoning.append(f"Low POI density: {poi_density:.1f} POIs/km²")
            reasoning.append(f"High infrastructure/landuse: {infrastructure_pct:.1f}%")
            if farmland_count > 0:
                reasoning.append(f"Agricultural area: {farmland_count} farmland POIs")
        else:
            environment_type = 'suburban'
            confidence = 70
            reasoning.append(f"Moderate POI density: {poi_density:.1f} POIs/km²")
            reasoning.append(f"Residential focus: {residential_pct:.1f}% residential POIs")

    else:
        # Low density - likely rural
        environment_type = 'rural'
        confidence = 80
        reasoning.append(f"Very low POI density: {poi_density:.1f} POIs/km²")
        if farmland_count > 0:
            reasoning.append(f"Agricultural presence: {farmland_count} farmland POIs")
        if infrastructure_pct > 50:
            reasoning.append(f"Dominated by infrastructure/landuse: {infrastructure_pct:.1f}%")

    # If still not classified, use fallback
    if environment_type is None:
        if total_pois == 0:
            environment_type = 'rural'
            confidence = 90
            reasoning.append("No POIs found in area - likely uninhabited or rural")
        else:
            environment_type = 'suburban'
            confidence = 50
            reasoning.append("Inconclusive - defaulting to suburban")

    return {
        'environment': environment_type,
        'confidence': confidence,
        'reasoning': reasoning,
        'statistics': {
            'total_pois': total_pois,
            'area_km2': round(area_km2, 2),
            'poi_density': round(poi_density, 1),
            'category_distribution': category_percentages,
            'category_counts': category_counts
        },
        'nearby_pois': nearby_pois
    }


def main():
    # Show help
    if len(sys.argv) < 3 or sys.argv[1] in ['-h', '--help', 'help']:
        print(__doc__)
        print("\nExample coordinates from dataset:")
        print("  Latitude: 24.4519, Longitude: 122.9440  (Ishigaki, Japan)")
        print("\nRadius options:")
        print("  0.5  - 500m radius (very local)")
        print("  1.0  - 1km radius (default, neighborhood)")
        print("  2.0  - 2km radius (broader area)")
        print("  5.0  - 5km radius (district/region)")
        sys.exit(0)

    # Parse arguments
    try:
        latitude = float(sys.argv[1])
        longitude = float(sys.argv[2])
    except ValueError:
        print("❌ Error: Latitude and longitude must be numeric values")
        print("Example: python classify_environment.py 24.4519 122.9440")
        sys.exit(1)

    radius_km = float(sys.argv[3]) if len(sys.argv) > 3 else 1.0
    data_file = sys.argv[4] if len(sys.argv) > 4 else None

    # Validate coordinates
    if not (-90 <= latitude <= 90):
        print(f"❌ Error: Latitude must be between -90 and 90 (got {latitude})")
        sys.exit(1)

    if not (-180 <= longitude <= 180):
        print(f"❌ Error: Longitude must be between -180 and 180 (got {longitude})")
        sys.exit(1)

    # Find available data file
    if data_file is None:
        # Try to find the largest available dataset
        data_dir = Path('data')
        candidates = [
            'cleaned_JP_POI_part1.csv',
            'cleaned_JP_POI_part2.csv',
            'poi_data.csv'
        ]

        for candidate in candidates:
            candidate_path = data_dir / candidate
            if candidate_path.exists():
                data_file = str(candidate_path)
                break

        if data_file is None:
            print("❌ Error: No POI data files found in data/ directory")
            sys.exit(1)

    # Check if file exists
    if not Path(data_file).exists():
        print(f"❌ Error: Data file not found: {data_file}")
        sys.exit(1)

    print("=" * 80)
    print("ENVIRONMENT CLASSIFICATION")
    print("=" * 80)
    print()
    print(f"Coordinates: {latitude}, {longitude}")
    print(f"Search radius: {radius_km} km")
    print(f"Data source: {data_file}")
    print()

    # Load data
    print("Loading POI data...")
    try:
        df = pd.read_csv(data_file)
        print(f"✓ Loaded {len(df):,} POI records")
    except Exception as e:
        print(f"❌ Error loading data: {e}")
        sys.exit(1)

    print()

    # Classify environment
    print("Analyzing environment...")
    result = classify_environment(latitude, longitude, df, radius_km)

    # Display results
    print()
    print("=" * 80)
    print("CLASSIFICATION RESULTS")
    print("=" * 80)
    print()

    env = result['environment'].upper()
    conf = result['confidence']

    # Color coding (if terminal supports it)
    env_color = {
        'URBAN': '🏙️',
        'SUBURBAN': '🏘️',
        'RURAL': '🌾'
    }

    print(f"Environment Type: {env_color.get(env, '')} {env}")
    print(f"Confidence: {conf:.0f}%")
    print()

    print("Reasoning:")
    for i, reason in enumerate(result['reasoning'], 1):
        print(f"  {i}. {reason}")
    print()

    # Statistics
    stats = result['statistics']
    print("=" * 80)
    print("AREA STATISTICS")
    print("=" * 80)
    print()
    print(f"Total POIs in area: {stats['total_pois']:,}")
    print(f"Search area: {stats['area_km2']:.2f} km²")
    print(f"POI density: {stats['poi_density']:.1f} POIs/km²")
    print()

    if stats['total_pois'] > 0:
        print("Category Distribution:")
        print("-" * 80)

        category_order = ['business', 'residential', 'public_services', 'transportation',
                         'tourism', 'infrastructure', 'other']

        for category in category_order:
            if category in stats['category_counts']:
                count = stats['category_counts'][category]
                pct = stats['category_distribution'][category]
                bar_length = int(pct / 2)
                bar = "█" * bar_length
                print(f"  {category:20}: {count:>6,} ({pct:>5.1f}%) {bar}")

        print("-" * 80)

        # Show nearest POIs
        nearby = result['nearby_pois'].nsmallest(10, 'distance_km')
        if len(nearby) > 0:
            print()
            print(f"Nearest POIs (within {radius_km} km):")
            print("-" * 80)
            for idx, row in nearby.iterrows():
                print(f"  • {row['POI_type']:15} | {row['POI']:20} | "
                      f"{row['distance_km']:.3f} km | {row.get('category', 'N/A')}")

            if len(result['nearby_pois']) > 10:
                print(f"  ... and {len(result['nearby_pois']) - 10} more POIs")
    else:
        print("⚠ No POIs found within search radius")
        print("Try increasing the radius or checking if coordinates are correct")

    print()
    print("=" * 80)
    print("CLASSIFICATION COMPLETE")
    print("=" * 80)

    # Return exit code based on confidence
    return 0 if conf >= 60 else 1


if __name__ == "__main__":
    sys.exit(main())
