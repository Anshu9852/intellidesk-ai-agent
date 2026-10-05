import os
import streamlit as st
from rq.job import Job

from graph import graph
from queue_setup import pdf_queue, redis_conn
from tasks import process_pdf_task

st.set_page_config(page_title="IntelliDesk", page_icon="💬")
st.title("IntelliDesk - HR Document Assistant")
st.caption("Company policy PDF se sawal poochhiye")

# ---- PDF upload + queue mein job bhejna + status ----
with st.sidebar:
    st.header("PDF upload karo")
    uploaded_file = st.file_uploader("Apni PDF chuno", type="pdf")

    if uploaded_file is not None and st.button("Process karo"):
        os.makedirs("data", exist_ok=True)
        save_path = os.path.join("data", uploaded_file.name)
        with open(save_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        job = pdf_queue.enqueue(process_pdf_task, save_path)
        st.session_state.job_id = job.id
        st.success("Processing shuru ho gayi! Job ID: " + job.id)

    # Naya hissa: status check
    if "job_id" in st.session_state:
        if st.button("Status check karo"):
            try:
                job = Job.fetch(st.session_state.job_id, connection=redis_conn)
                if job.is_finished:
                    st.success("Ho gayi! Ab sawal pooch sakti ho.")
                elif job.is_failed:
                    st.error("Job fail ho gayi. Worker terminal mein error dekho.")
                elif job.is_started:
                    st.info("Processing chal rahi hai...")
                else:
                    st.warning("Queue mein wait kar rahi hai. Worker chal raha hai?")
            except Exception:
                st.warning("Job nahi mili (shayad bahut purani ho gayi).")

# ---- Chat (bilkul waisa hi) ----
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

question = st.chat_input("Apna sawal yahan likhiye...")

if question:
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.write(question)

    with st.chat_message("assistant"):
        with st.spinner("Soch rahe hain..."):
            result = graph.invoke(
                {"question": question, "route": "", "answer": "", "memory_context": ""}
            )
        st.write(result["answer"])

    st.session_state.messages.append({"role": "assistant", "content": result["answer"]})