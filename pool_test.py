from sqlalchemy import create_engine
import time
from datetime import datetime

# Create engine with a small pool and max_overflow
engine = create_engine(
    'sqlite:///test.db',
    pool_size=2,           # Start with 2 connections
    max_overflow=3,        # Allow 3 more connections
    pool_timeout=30,       # Wait up to 30s for a connection
    echo_pool=True         # Print pool events
)

def get_connection():
    print(f"\n[{datetime.now()}] Requesting connection...")
    conn = engine.connect()
    print(f"[{datetime.now()}] Got connection, sleeping...")
    time.sleep(5)  # Hold the connection for 5 seconds
    conn.close()
    print(f"[{datetime.now()}] Released connection")
    return True

# Test the pool behavior
if __name__ == "__main__":
    print("Testing SQLAlchemy connection pool behavior")
    print("------------------------------------------")
    print(f"Pool size: {engine.pool._pool.maxsize}")
    print(f"Max overflow: {engine.pool._max_overflow}")
    
    # Create multiple concurrent connections
    from concurrent.futures import ThreadPoolExecutor
    with ThreadPoolExecutor(max_workers=6) as executor:
        # Try to get more connections than pool_size + max_overflow
        futures = [executor.submit(get_connection) for _ in range(6)]
        results = [f.result() for f in futures]
    
    print("\nPool stats after test:")
    print(f"Pool size: {engine.pool._pool.maxsize}")
    print(f"Current connections: {engine.pool._pool.qsize()}")
    print(f"Current overflow: {engine.pool._overflow}") 