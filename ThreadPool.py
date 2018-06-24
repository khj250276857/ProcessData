import os
from concurrent.futures.thread import ThreadPoolExecutor


jobs = list(range(10000000))
with ThreadPoolExecutor(max_workers=os.cpu_count() * 2) as executor:
    for job in jobs:
        executor.submit(job)
    # for executor.

