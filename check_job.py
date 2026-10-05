# check_job.py
from redis import Redis
from rq.job import Job

redis_conn = Redis(host="localhost", port=6379)

job = Job.fetch("3a70c79c-9816-4eb5-aceb-0b6b74ea6edf", connection=redis_conn)

print("Status:", job.get_status())
print("Result:", job.result)