# Data Pipeline

ETL data pipeline framework for batch and stream processing with configurable transformations.

## Features
- Extract from CSV, JSON, and API sources
- Transform with map, filter, aggregate operations
- Load to CSV, JSON, or database targets
- Pipeline chaining and error handling

## Usage
```python
from pipeline import DataPipeline
p = DataPipeline()
p.extract_csv("input.csv").filter(lambda r: r["age"] > 18).aggregate("city", "count").load_csv("output.csv")
```
