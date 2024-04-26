from tenacity import (
    RetryCallState,
    RetryError,
    Retrying,
    stop_after_attempt,
    wait_exponential,
)


class RetryManager:
    def __init__(self) -> None:
        self.retry_error = RetryError
        self.retrying = Retrying(
            wait=wait_exponential(multiplier=1, min=4, max=10),
            stop=stop_after_attempt(5),
            reraise=True,
            before=self.before,
            after=self.after,
        )

    def before(self, retry_state: RetryCallState):
        ...

    def after(self, retry_state: RetryCallState):
        ...

    def make_retry(self):
        return self.retrying
