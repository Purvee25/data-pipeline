import csv
import json
from collections import defaultdict

class DataPipeline:
    def __init__(self):
        self.data = []
        self.steps = []

    def extract_csv(self, filepath):
        with open(filepath, 'r') as f:
            reader = csv.DictReader(f)
            self.data = list(reader)
        return self

    def extract_json(self, filepath):
        with open(filepath, 'r') as f:
            self.data = json.load(f)
        return self

    def extract_list(self, data):
        self.data = [row.copy() for row in data]
        return self

    def filter(self, predicate):
        self.data = [row for row in self.data if predicate(row)]
        return self

    def map(self, transform):
        self.data = [transform(row) for row in self.data]
        return self

    def select(self, columns):
        self.data = [{k: row.get(k) for k in columns} for row in self.data]
        return self

    def rename(self, mapping):
        def _rename(row):
            return {mapping.get(k, k): v for k, v in row.items()}
        self.data = [_rename(row) for row in self.data]
        return self

    def aggregate(self, group_by, operation="count"):
        groups = defaultdict(list)
        for row in self.data:
            key = row.get(group_by, "")
            groups[key].append(row)
        result = []
        for key, rows in groups.items():
            entry = {group_by: key}
            if operation == "count":
                entry["count"] = len(rows)
            elif operation.startswith("sum:"):
                field = operation.split(":")[1]
                entry[f"sum_{field}"] = sum(float(r.get(field, 0)) for r in rows)
            elif operation.startswith("avg:"):
                field = operation.split(":")[1]
                vals = [float(r.get(field, 0)) for r in rows]
                entry[f"avg_{field}"] = sum(vals) / len(vals) if vals else 0
            result.append(entry)
        self.data = result
        return self

    def sort(self, key, reverse=False):
        self.data.sort(key=lambda r: r.get(key, ""), reverse=reverse)
        return self

    def limit(self, n):
        self.data = self.data[:n]
        return self

    def load_csv(self, filepath):
        if not self.data:
            return self
        with open(filepath, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=self.data[0].keys())
            writer.writeheader()
            writer.writerows(self.data)
        return self

    def load_json(self, filepath):
        with open(filepath, 'w') as f:
            json.dump(self.data, f, indent=2)
        return self

    def result(self):
        return self.data

if __name__ == "__main__":
    sample = [{"name": "Alice", "city": "NYC", "age": "30"}, {"name": "Bob", "city": "LA", "age": "25"}, {"name": "Charlie", "city": "NYC", "age": "35"}, {"name": "Diana", "city": "LA", "age": "28"}]
    p = DataPipeline()
    result = p.extract_list(sample).filter(lambda r: int(r["age"]) > 26).aggregate("city", "count").result()
    print("Result:", result)
