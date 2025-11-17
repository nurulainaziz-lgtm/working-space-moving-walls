# POI Data Classification Project

A high-performance data engineering project for classifying Points of Interest (POI) into 7 comprehensive categories. Optimized for large datasets (1M+ records) with extensive coverage of Japanese POI data.

## 🚀 Recent Updates (v2.0)

- ✅ **Enhanced Classification**: Expanded from 4 to 7 categories for better granularity
- ✅ **Performance Optimized**: 120K+ records/second processing speed using set-based lookups
- ✅ **100% Coverage**: Comprehensive Japanese POI dataset support (1M+ records)
- ✅ **Environment Classifier**: NEW - Classify coordinates as urban/suburban/rural based on POI analysis
- ✅ **Large Dataset Support**: Updated Jupyter notebook with batch processing capabilities
- ✅ **New Categories**: Added Residential and Infrastructure classification
- ✅ **Extensive POI Types**: 200+ POI type combinations supported
- ✅ **Command-line Tools**: Flexible demo.py with file input arguments

## Project Structure

```
working-space-moving-walls/
├── data/
│   ├── poi_data.csv                  # Sample POI data (17 records)
│   ├── cleaned_JP_POI_part1.csv      # Large Japanese dataset Part 1 (508K records)
│   ├── cleaned_JP_POI_part2.csv      # Large Japanese dataset Part 2 (508K records)
│   └── *_classified.csv              # Classified POI data (generated)
├── notebooks/
│   └── poi_classification.ipynb      # Enhanced Jupyter notebook with large dataset support
├── src/
│   ├── __init__.py
│   └── poi_classifier.py             # Optimized classification module
├── classify_environment.py           # Environment classifier (urban/suburban/rural)
├── demo.py                           # Quick demonstration script
├── verify_setup.py                   # Setup verification script
├── test_classifier_performance.py    # Performance testing script
├── requirements.txt                  # Python dependencies
└── README.md                         # This file
```

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Classify Environment from Coordinates

```bash
# Classify environment at specific coordinates
python classify_environment.py 24.4519 122.9440

# Use custom radius (in kilometers)
python classify_environment.py 24.4519 122.9440 2.0

# Specify custom data file
python classify_environment.py 24.4519 122.9440 1.0 data/cleaned_JP_POI_part1.csv
```

### 3. Run the Jupyter Notebook

```bash
cd notebooks
jupyter notebook poi_classification.ipynb
```

### 3. Use the Classifier Module

```python
from src.poi_classifier import classify_poi

# Classify a single POI
category = classify_poi('amenity', 'restaurant')
print(category)  # Output: business
```

## POI Categories

The system classifies POIs into **seven main categories**:

### 1. **Business**
Commercial establishments and services:
- Shops (convenience, supermarket, retail, etc.)
- Restaurants, cafes, pubs, bars, fast food
- Banks, ATMs, pharmacies
- Vending machines, fuel stations
- Retail buildings

### 2. **Tourism**
Tourism-related facilities:
- Hotels, guest houses, motels, hostels
- Information centers
- Museums, attractions, viewpoints
- Theme parks, galleries

### 3. **Public Services**
Government and community services:
- Police stations, fire stations
- Post offices, social facilities
- Places of worship
- Schools, universities, kindergarten, libraries
- Hospitals, clinics, healthcare
- Public amenities (benches, toilets, shelters)
- Public service buildings

### 4. **Transportation**
Transportation infrastructure:
- Roads (highways, residential, unclassified, tertiary, etc.)
- Traffic infrastructure (signals, crossings, stop signs)
- Railways (rail, stations, level crossings)
- Public transport (platforms, bus stops)
- Parking facilities
- Airports and aeroways

### 5. **Residential**
Housing and residential buildings:
- Houses, apartments
- Residential buildings
- Dormitories, bungalows
- Greenhouses, barns

### 6. **Infrastructure**
Utilities, landuse, and industrial facilities:
- Landuse (farmland, forests, orchards, grass)
- Industrial buildings and warehouses
- Generic buildings
- Construction sites
- Cemeteries

### 7. **Other**
Uncategorized POIs (typically <0.1% of dataset)

## Data Format

### Input Data (poi_data.csv)
```csv
POI_type,POI,latitude,longitude
highway,traffic_signals,24.4519523,122.9439556
amenity,police,24.4511259,122.9459816
```

### Output Data (poi_data_classified.csv)
```csv
POI_type,POI,latitude,longitude,category
highway,traffic_signals,24.4519523,122.9439556,transportation
amenity,police,24.4511259,122.9459816,public_services
```

## Classification Logic

The classifier uses a priority-based approach:

1. **Tourism** (highest priority) - Direct tourism-related POIs
2. **Transportation** - Infrastructure for movement
3. **Public Services** - Government and community services
4. **Business** - Commercial establishments
5. **Fallback** - Based on POI_type if no specific match found

## Usage Examples

### Classify from CSV using pandas

```python
import pandas as pd
from src.poi_classifier import classify_poi

# Load data
df = pd.read_csv('data/poi_data.csv')

# Apply classification
df['category'] = df.apply(
    lambda row: classify_poi(row['POI_type'], row['POI']),
    axis=1
)

# Save results
df.to_csv('data/poi_data_classified.csv', index=False)
```

### Analyze distribution

```python
# Count by category
category_counts = df['category'].value_counts()
print(category_counts)

# Percentage distribution
percentages = (df['category'].value_counts(normalize=True) * 100).round(2)
print(percentages)
```

## Performance

The enhanced classifier delivers exceptional performance on large datasets:

- **Processing Speed**: 120,000+ records/second
- **Dataset Coverage**: 100% classification rate (tested on 1M+ Japanese POI records)
- **Full Dataset Time**: Process 1M records in ~8.4 seconds
- **Memory Efficient**: Set-based lookups for O(1) performance
- **Scalable**: Handles multi-file datasets with batch processing

### Performance Test Results

```bash
python test_classifier_performance.py 5000
```

Sample output:
```
✓ Classification completed in 0.04 seconds
  Processing rate: 120,688 records/second
✓ Classification Coverage: 5,000 / 5,000 (100.00%)

Estimated full dataset processing time: 8.4 seconds (0.1 minutes)
```

## Features

- ✅ **7 comprehensive categories** with 200+ POI type combinations
- ✅ **High-performance classification** (120K+ records/sec)
- ✅ **100% coverage** on Japanese POI datasets
- ✅ **Environment classification** - Classify coordinates as urban/suburban/rural
- ✅ **Large dataset support** in Jupyter notebook
- ✅ **Extensible design** - Easy to add new categories or POI types
- ✅ **Multiple testing scripts** (demo, verify, performance test)
- ✅ **Reusable module** for integration into other projects
- ✅ **Detailed documentation** and examples

## Environment Classification

The project includes a powerful environment classification tool that analyzes POI density and characteristics around given coordinates to determine if an area is urban, suburban, or rural.

### Usage

```bash
python classify_environment.py <latitude> <longitude> [radius_km]
```

### Examples

```bash
# Urban area (high POI density)
python classify_environment.py 24.4519 122.9440

# Output: 🏙️ URBAN (Confidence: 100%)
# Reasoning: Very high POI density: 205.6 POIs/km²

# Suburban area (moderate density)
python classify_environment.py 24.465 122.956 0.5

# Output: 🏘️ SUBURBAN (Confidence: 70%)
# Reasoning: Moderate POI density: 52.2 POIs/km²

# Rural area (low density)
python classify_environment.py 24.35 122.85

# Output: 🌾 RURAL (Confidence: 80%)
# Reasoning: Very low POI density
```

### Classification Criteria

| Environment | POI Density | Key Characteristics |
|-------------|-------------|---------------------|
| **Urban** | >100 POIs/km² | High commercial activity, diverse POI types, dense infrastructure |
| **Suburban** | 20-100 POIs/km² | Mixed residential/commercial, moderate density, balanced categories |
| **Rural** | <20 POIs/km² | Low density, agricultural landuse, dominated by infrastructure |

### Output Information

The classifier provides:
- **Environment Type**: Urban, Suburban, or Rural
- **Confidence Score**: 0-100% based on clarity of indicators
- **Reasoning**: Detailed explanation of classification factors
- **Area Statistics**: POI counts, density, category distribution
- **Nearest POIs**: List of closest points of interest

## Development

### Adding New POI Types

Edit `src/poi_classifier.py` and add the new POI to the appropriate category dictionary:

```python
business_pois = {
    'shop': ['convenience', 'supermarket', 'your_new_type'],
    'amenity': ['restaurant', 'cafe']
}
```

### Testing

Run the module directly to test:

```bash
python src/poi_classifier.py
```

## Requirements

- Python 3.7+
- pandas >= 1.3.0
- numpy >= 1.21.0
- jupyter >= 1.0.0
- notebook >= 6.4.0

## License

This project is for educational and demonstration purposes.

## Contributing

Feel free to extend the classification rules or add new features!
