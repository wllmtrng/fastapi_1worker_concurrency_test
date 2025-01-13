# FastAPI Concurrency Test

## Problem Statement
This project demonstrates FastAPI's concurrency behavior by simulating a heavy workload endpoint. While FastAPI is built for async operations, it handles synchronous blocking operations (like `time.sleep()`) using Starlette's threadpool, which explains some surprising concurrency patterns.

## Technical Background
- FastAPI is built on Starlette, which uses a threadpool executor for handling blocking operations
- The ThreadPoolExecutor's default max_workers has evolved across Python versions:
  - Python 3.8+ (current): `max_workers = min(32, os.cpu_count() + 4)`
  - Python 3.5: `max_workers = (os.cpu_count() or 1) * 5`
  - Python 3.13 (upcoming): `max_workers = min(32, (os.process_cpu_count() or 1) + 4)`
- The current default (min(32, os.cpu_count() + 4)) was carefully chosen to:
  - Preserve at least 5 workers for I/O bound tasks
  - Utilize at most 32 CPU cores for CPU bound tasks that release the GIL
  - Avoid using excessive resources on many-core machines
- This means even with a single uvicorn worker process, blocking operations can still achieve some parallelism
- However, this is not true async concurrency, but rather concurrent execution via threads

## Test Setup
- Endpoint: GET `/`
- Simulated workload: 10-second sleep (blocking operation)
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
2. Concurrent requests are handled by Starlette's threadpool
3. Each request takes 10 seconds to complete
4. With multiple concurrent requests, they are processed in batches based on threadpool size
5. All requests will show the same process ID but different thread IDs

## Key Findings
1. **Parallel Processing via Threads**: Despite having a single worker, FastAPI/Starlette handles blocking operations in parallel using a threadpool
2. **Batch Processing**: Requests are processed in batches corresponding to the threadpool size
3. **Response Time**: Total processing time is (number_of_requests / threadpool_size * delay_time)
4. **Process/Thread Behavior**: 
   - Same process ID across all requests (single worker)
   - Different thread IDs within the threadpool

## Test Results
```
Test Configuration:
- Total Requests: 100
- Concurrent Connections: 100
- Simulated Delay: 10 seconds per request
- Default Threadpool Size: ~32 threads

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
1. Requests were processed in batches of ~33 (matching threadpool size)
2. All requests used the same process ID, confirming single-worker behavior
3. Different thread IDs show threadpool utilization
4. Each batch took approximately 10 seconds to process
5. Total processing time (30.15s) = (100 requests / ~33 threads * 10s delay)
```

## Important Notes
- This behavior is specific to blocking operations (like `time.sleep()`, file I/O, or blocking database calls)
- True async operations (using `async/await`) would behave differently
- For production systems with blocking operations, consider:
  1. Converting blocking operations to async where possible
  2. Using multiple worker processes
  3. Implementing proper async patterns instead of relying on the threadpool