#!/usr/bin/env python3
"""
Minimal test server to verify duration feature without heavy dependencies.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import time
import uvicorn

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/hello")
def hello():
    return {'message': 'HELLO CS492 TAs!'}

@app.post("/test")
async def test():
    result = ['dog1.png', 'dog2.png', 'dog3.png', 'dog4.png']
    max_column_id = [6, 6, 8]
    histogram_path = 'heatmap/histogram/histogram_1.png'
    # Mock duration for testing (simulate 2 minutes and 30 seconds)
    mock_duration = 150.0
    return {'image_paths': result, 'max_value': max_column_id, 'histogram': histogram_path[8:], 'duration_seconds': mock_duration}

@app.post("/run-gradcam")
async def run_gradcam():
    # Start timing the processing
    start_time = time.time()

    # Simulate some processing time
    time.sleep(0.1)  # 100ms of simulated processing

    # End timing the processing
    end_time = time.time()
    duration_seconds = end_time - start_time

    result = ['test1.png', 'test2.png', 'test3.png', 'test4.png']
    max_column_id = [4, 4, 4]
    histogram_path = 'histogram/histogram_1.png'

    print(f"Processing duration: {duration_seconds:.2f} seconds")
    return {'image_paths': result, 'max_value': max_column_id, 'histogram': histogram_path, 'duration_seconds': duration_seconds}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8001)
