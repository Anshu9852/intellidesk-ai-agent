# queue_setup.py
from redis import Redis
from rq import Queue

redis_conn = Redis(host="localhost", port=6379)
pdf_queue = Queue("pdf_jobs", connection=redis_conn)