def validate_schema(data, schema):
    errors = []
    for i, row in enumerate(data):
        for field, ftype in schema.items():
            if field not in row:
                errors.append(f"Row {i}: missing field '{field}'")
            elif not isinstance(row[field], ftype):
                errors.append(f"Row {i}: '{field}' expected {ftype.__name__}, got {type(row[field]).__name__}")
    return errors

def validate_not_null(data, fields):
    errors = []
    for i, row in enumerate(data):
        for f in fields:
            if row.get(f) is None or row.get(f) == "":
                errors.append(f"Row {i}: '{f}' is null/empty")
    return errors
