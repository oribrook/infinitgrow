def sort_obj_recursive(obj):
    if isinstance(obj, dict):
        sorted_dict = {}
        for key in sorted(obj.keys()):
            sorted_dict[key] = sort_obj_recursive(obj[key])
        return sorted_dict
    elif isinstance(obj, list):
        # Check if the list contains dictionaries, and sort them recursively
        if all(isinstance(item, dict) for item in obj):
            return sorted(
                [sort_obj_recursive(item) for item in obj], key=lambda x: str(x)
            )
        else:
            # Sort non-dictionary items (e.g., metrics)
            return sorted(obj, key=lambda x: str(x))
    else:
        return obj
