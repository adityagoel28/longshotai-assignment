def individual_serial(item_type) -> dict:
    return {
        "_id": str(item_type["_id"]),
        "name": item_type["name"],
        "requires_refrigeration": item_type["requires_refrigeration"],
    }

def list_serial(item_types) -> list:
    return [individual_serial(item_type) for item_type in item_types]