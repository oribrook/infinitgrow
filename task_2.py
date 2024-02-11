"""
NOTES:
    * Assuming all identities entry values are immutable
"""
import json
from helpers import sort_obj_recursive


def merge_identities(new_ident: dict, old_ident: dict) -> dict:
    """merge new_ident into old_ident"""

    res = old_ident.copy()

    for k, new_val in new_ident.items():
        if new_val is None:
            # convert old value to list
            res[k] = res[k] if type(res[k]) is list or res[k] is None else [res[k]]
            continue

        if old_ident[k] is None:
            res[k] = [new_val]
            continue

        merged_values = old_ident[k] if type(old_ident[k]) == list else [old_ident[k]]

        if new_val not in merged_values:
            merged_values.append(new_val)
            res[k] = merged_values

    return res


def update_index(index_dict: dict, new_identity: dict, index: int) -> dict:
    for k, v in new_identity.items():
        v = v if k != "email" else v.split("@")[1]
        index_dict[k][v] = index

    return index_dict


def create_dataset(identities: list) -> list:
    if len(identities) == 0:
        return identities

    # initial index_dict
    index_dict = {}
    for k in identities[0]:
        index_dict[k] = {}

    res = []
    for identity in identities:
        is_merged = False
        for k, v in identity.items():
            v = v if k != "email" else v.split("@")[1]

            # check if identity need to be merged
            if v in index_dict[k]:
                index = index_dict[k][v]
                merged_identity = merge_identities(identity, old_ident=res[index])
                index_dict = update_index(index_dict, identity, index)
                res[index] = merged_identity
                is_merged = True
                break

        if is_merged:
            continue

        res.append(identity)
        index_dict = update_index(index_dict, identity, len(res) - 1)

    return res


## test ##
if __name__ == "__main__":
    # load test data:
    with open("task_2_input.json", "r") as F:
        data = json.load(F)

    # run algo
    algo_res = create_dataset(data)

    # load expected result
    with open("task_2_output.json", "r") as F:
        real_res = json.load(F)

    # sort the two dicts in order to compare them
    real_res = sort_obj_recursive(real_res)
    algo_res = sort_obj_recursive(algo_res)

    # compare results
    res = "PASSED" if real_res == algo_res else "FAILED"
    print(res)
