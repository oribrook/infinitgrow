"""
NOTES:
    * Task example results contains mistake, "NewCustomer" instead of "New Customer"
    * If metric M1 shares filter F1 with metric M2 and filter F2 with M3,  two entries
       need to be created, [M1, M2] for F1 and [M1, M3] for F2 etc..       
"""
import json
from helpers import sort_obj_recursive


def format_results(data: dict) -> list:
    """given algorithm result, convert it to the task-required format"""

    filters_by_metrics = {}
    for filter, metrics in data.items():
        metrics_json = json.dumps(sorted(metrics))
        if metrics_json in filters_by_metrics:
            filters_by_metrics[metrics_json].append(filter)
        else:
            filters_by_metrics[metrics_json] = [filter]

    res = []
    for k, v in filters_by_metrics.items():
        res.append(
            {
                "metrics": json.loads(k),
                "filters": [json.loads(filter) for filter in v],
            }
        )
    return res


def create_dataset(data: dict) -> list:
    data = data["metricsCustomFilters"]
    data = sort_obj_recursive(data)  # identical filters should be looks exact similar

    metrics_by_filter = {}
    for metric, filters in data.items():
        for filter in filters:
            filter_json = json.dumps(filter)
            if filter_json in metrics_by_filter:
                metrics_by_filter[filter_json].append(metric)
            else:
                metrics_by_filter[filter_json] = [metric]

    return format_results(metrics_by_filter)


## test ##
if __name__ == "__main__":
    # load test input data:
    with open("task1_input.json", "r") as F:
        data = json.load(F)

    # run algo
    algo_res = create_dataset(data)

    # load test required output
    with open("task1_output.json", "r") as F:
        real_res = json.load(F)

    # sort the two dicts in order to compare them
    real_res = sort_obj_recursive(real_res)
    algo_res = sort_obj_recursive(algo_res)

    # compare results
    res = "PASSED" if real_res == algo_res else "FAILED"
    print(res)
