from pipeline import DataPipeline

def test_filter():
    data = [{"name": "A", "age": 20}, {"name": "B", "age": 15}]
    result = DataPipeline().extract_list(data).filter(lambda r: r["age"] >= 18).result()
    assert len(result) == 1

def test_aggregate():
    data = [{"city": "NYC", "val": "10"}, {"city": "NYC", "val": "20"}, {"city": "LA", "val": "30"}]
    result = DataPipeline().extract_list(data).aggregate("city", "sum:val").result()
    nyc = [r for r in result if r["city"] == "NYC"][0]
    assert nyc["sum_val"] == 30

def test_sort():
    data = [{"n": 3}, {"n": 1}, {"n": 2}]
    result = DataPipeline().extract_list(data).sort("n").result()
    assert [r["n"] for r in result] == [1, 2, 3]

if __name__ == "__main__":
    test_filter()
    test_aggregate()
    test_sort()
    print("All tests passed!")
