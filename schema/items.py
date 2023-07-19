def individual_serial(item) -> dict:
    return {
        "_id": str(item["_id"]),
        "name": item["name"],
        "max_limit": item["max_limit"],
        "is_refrigerated": item["is_refrigerated"],
        "items": item["items"]
    }

def list_serial(items) -> list:
    return [individual_serial(item) for item in items]