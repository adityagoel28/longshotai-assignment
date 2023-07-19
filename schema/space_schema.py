def individual_serial(space) -> dict:
    return {
        "_id": str(space["_id"]),
        "name": space["name"],
        "max_limit": space["max_limit"],
        "is_refrigerated": space["is_refrigerated"],
        "items": space["items"]
    }

def list_serial(spaces) -> list:
    return [individual_serial(space) for space in spaces]