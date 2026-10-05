# test_queue.py
from queue_setup import pdf_queue
from tasks import process_pdf_task

job = pdf_queue.enqueue(process_pdf_task, "data/company_policy.pdf")
print("Job ID:", job.id)
print("Status:", job.get_status())