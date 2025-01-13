from fastapi import FastAPI
import time
import os
import threading
from datetime import datetime

app = FastAPI()

@app.get("/")
def root():
    # Capture start time
    start_time = datetime.now()
    
    # Print process and thread info
    process_id = os.getpid()
    thread_id = threading.get_native_id()
    print(f"[{start_time.strftime('%H:%M:%S.%f')}] Starting request - Process ID: {process_id}, Thread ID: {thread_id}")
    
    # Simulate heavy work with a 10 second delay
    time.sleep(10)
    
    # Capture end time
    end_time = datetime.now()
    print(f"[{end_time.strftime('%H:%M:%S.%f')}] Finishing request - Process ID: {process_id}, Thread ID: {thread_id}")
    
    return {
        "message": "Hello World",
        "process_id": process_id,
        "thread_id": thread_id,
        "start_time": start_time.strftime('%H:%M:%S.%f'),
        "end_time": end_time.strftime('%H:%M:%S.%f')
    } 