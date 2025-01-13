import aiohttp
import asyncio
import time
from datetime import datetime
import statistics

async def make_request(session, url, request_id):
    start_time = datetime.now()
    try:
        async with session.get(url) as response:
            response_data = await response.json()
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            print(f"Request {request_id:4d} - Start: {start_time.strftime('%H:%M:%S.%f')} - End: {end_time.strftime('%H:%M:%S.%f')} - Duration: {duration:.2f}s")
            print(f"           Process ID: {response_data['process_id']}, Thread ID: {response_data['thread_id']}")
            return True
    except Exception as e:
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        print(f"Request {request_id:4d} - Start: {start_time.strftime('%H:%M:%S.%f')} - End: {end_time.strftime('%H:%M:%S.%f')} - Duration: {duration:.2f}s - Error: {str(e)}")
        return False

async def run_benchmark(num_requests, concurrent_limit):
    print(f"\nStarting batch of {num_requests} requests with concurrency limit of {concurrent_limit}")
    print("=" * 80)
    
    connector = aiohttp.TCPConnector(limit=concurrent_limit)
    async with aiohttp.ClientSession(connector=connector) as session:
        tasks = []
        for i in range(num_requests):
            task = asyncio.create_task(make_request(session, 'http://localhost:8000', i+1))
            tasks.append(task)
        
        start_time = time.time()
        results = await asyncio.gather(*tasks)
        end_time = time.time()
        
        successful_requests = sum(1 for r in results if r)
        failed_requests = sum(1 for r in results if not r)
        duration = end_time - start_time
        rps = num_requests / duration
        
        print("\nBatch Summary:")
        print("-" * 40)
        print(f"Total Requests: {num_requests}")
        print(f"Successful Requests: {successful_requests}")
        print(f"Failed Requests: {failed_requests}")
        print(f"Total Duration: {duration:.2f} seconds")
        print(f"Requests per second: {rps:.2f}")
        print("=" * 80 + "\n")
        
        return {
            'total_requests': num_requests,
            'successful_requests': successful_requests,
            'failed_requests': failed_requests,
            'duration': duration,
            'requests_per_second': rps
        }

async def main():
    print(f"Starting benchmark at {datetime.now()}")
    print("Testing FastAPI concurrent connections capacity...")
    print("-" * 50)
    
    # Test with 100 concurrent connections
    concurrent_limits = [100]
    num_requests = 100  # Total number of requests
    
    results = []
    for limit in concurrent_limits:
        print(f"\nTesting with {limit} concurrent connections...")
        result = await run_benchmark(num_requests, limit)
        results.append(result['requests_per_second'])
    
    print("\nFinal Summary:")
    print("-" * 50)
    print(f"Average RPS: {statistics.mean(results):.2f}")
    print(f"Max RPS: {max(results):.2f}")
    print(f"Min RPS: {min(results):.2f}")
    if len(results) > 1:
        print(f"Standard Deviation: {statistics.stdev(results):.2f}")

if __name__ == "__main__":
    asyncio.run(main()) 