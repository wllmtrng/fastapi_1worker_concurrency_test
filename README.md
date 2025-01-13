# FastAPI Concurrency Test

## Problem Statement
This project demonstrates FastAPI's concurrency behavior by simulating a heavy workload endpoint. The goal is to understand how FastAPI handles multiple concurrent requests with a slow endpoint (10-second delay) and observe the process/thread behavior with a single worker.

## Test Setup
- Endpoint: GET `/`
- Simulated workload: 10-second sleep
- Each request logs:
  - Process ID
  - Thread ID
  - Start time
  - End time
- Environment: Local Python with 1 worker process

## Running the Test
1. Start the FastAPI server:
```bash
uvicorn app:app --host 0.0.0.0 --port 8000 --workers 1
```

2. In a separate terminal, run the benchmark:
```bash
python benchmark.py
```

## Expected Behavior
When running with a single worker (--workers 1):
1. The server uses 1 worker process that handles all requests
2. Concurrent requests are processed sequentially
3. Each request takes 10 seconds to complete
4. With multiple concurrent requests and 1 worker, total completion time will be approximately (number_of_requests * 10) seconds
5. All requests will show the same process ID but may have different thread IDs

## Key Findings
1. **Sequential Processing**: With a single worker, FastAPI processes requests one at a time
2. **Blocking Behavior**: Each 10-second sleep blocks the entire worker process
3. **Response Time**: Total processing time is the sum of all request times
4. **Process ID Consistency**: All requests share the same process ID as they're handled by the single worker

## Test Results
```
Test Configuration:
- Total Requests: 100
- Concurrent Connections: 100
- Simulated Delay: 10 seconds per request

Results:
- Total Duration: 30.15 seconds
- Successful Requests: 100
- Failed Requests: 0
- Requests per Second: 3.32
- Process ID: All requests shared same PID (45574)
- Request Duration Pattern:
  * First batch: ~10 seconds
  * Second batch: ~20 seconds
  * Third batch: ~30 seconds

Key Observations:
1. Single worker processed requests in batches
2. All requests used the same process ID, confirming single-worker behavior
3. Requests were processed in groups of ~33 (100 requests / 3 batches)
4. Each batch took approximately 10 seconds to process
5. Total processing time (30.15s) ≈ (number of batches × delay time)
``` 