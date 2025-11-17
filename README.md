# POI Data Classification Project

A data engineering project for classifying Points of Interest (POI) into business, tourism, public services, and transportation categories.

## Project Structure

```
working-space-moving-walls/
├── data/
│   ├── poi_data.csv              # Original POI data
│   └── poi_data_classified.csv   # Classified POI data (generated)
├── notebooks/
│   └── poi_classification.ipynb  # Main Jupyter notebook for analysis
├── src/
│   ├── __init__.py
│   └── poi_classifier.py         # Core classification module
├── requirements.txt              # Python dependencies
└── README.md                     # This file
```

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the Jupyter Notebook

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

The system classifies POIs into four main categories:

### 1. **Business**
Commercial establishments and services:
- Shops (convenience stores, supermarkets, etc.)
- Restaurants, cafes, pubs, bars
- Banks, pharmacies

### 2. **Tourism**
Tourism-related facilities:
- Hotels, guest houses, motels
- Information centers
- Museums, attractions, viewpoints

### 3. **Public Services**
Government and community services:
- Police stations
- Post offices
- Places of worship
- Schools, universities, libraries
- Hospitals, clinics
- Social facilities

### 4. **Transportation**
Transportation infrastructure:
- Traffic signals, crossings
- Ferry terminals, bus stations
- Public transport platforms

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

## Features

- **Comprehensive classification rules** covering common POI types
- **Extensible design** - Easy to add new categories or POI types
- **Jupyter notebook** with full analysis workflow
- **Reusable module** for integration into other projects
- **Detailed documentation** and examples

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
