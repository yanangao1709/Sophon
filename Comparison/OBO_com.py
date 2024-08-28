from Examples.OneByOne import *

def OBO_run(requests, request_required_data, candidate_routes):
    total_time_costs = 0
    total_time_costs += OneByOne(requests, request_required_data, candidate_routes, False)
    return total_time_costs
