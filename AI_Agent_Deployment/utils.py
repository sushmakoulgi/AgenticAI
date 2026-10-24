from collections import deque,defaultdict
import time
class RateLimiter:

    def __init__(self) -> None:
        self.rate_tracker=defaultdict(deque)
        self.time_window=30
        self.request_limit=3

    def is_rate_within_limit(self,clientId:str):
        now=int(time.time())
        print("current_time",now)
        self.remove_old_records(clientId=clientId,current=now)
        count_of_requests=len(self.rate_tracker[clientId])
        print("count of request",count_of_requests)
        if count_of_requests> self.request_limit:
            return False
        self.rate_tracker[clientId].append(now)
        return True

    def remove_old_records(self,clientId,current):
        current_queue=self.rate_tracker[clientId]
        old_time=current-self.time_window
        print("removing records older than ",old_time)
        while current_queue and current_queue[-1]<old_time:
            current_queue.popleft()

        

