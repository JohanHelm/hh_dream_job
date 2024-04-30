from api_requests.retry import RetryManager

retry_manager: RetryManager = RetryManager()

for attempt in retry_manager.make_retry():
    with attempt:
        print(attempt)
        raise Exception

