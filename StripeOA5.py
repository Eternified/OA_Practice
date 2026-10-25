def has_rate_limit_violation(request_timestamps, max_requests, window_size):
    if request_timestamps == [] or len(request_timestamps) <= max_requests:
        return False

    stop_index = len(request_timestamps) - max_requests

    for i in range(stop_index):

        current_request_time = request_timestamps[i]
        boundary_request_time = request_timestamps[i + max_requests]

        time_difference = boundary_request_time - current_request_time

        if time_difference <= window_size:
            return True


print(has_rate_limit_violation([1, 2, 5, 8, 9, 10, 14], 2, 5))