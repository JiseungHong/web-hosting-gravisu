#!/usr/bin/env python3
"""
Simple test server to verify the duration feature works
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import time

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Test server for GRAVISU duration feature"}

@app.post("/test")
async def test():
    # Simulate some processing time
    time.sleep(2)

    result = ['dog1.png', 'dog2.png', 'dog3.png', 'dog4.png']
    max_column_id = [6, 6, 8]
    histogram_path = 'heatmap/histogram/histogram_1.png'
    # Mock duration for testing (e.g., 125.5 seconds = 2m 5s)
    mock_duration = 125.5
    return {
        'image_paths': result,
        'max_value': max_column_id,
        'histogram': histogram_path[8:],
        'duration_seconds': mock_duration
    }

@app.post("/run-gradcam")
async def run_gradcam():
    # Simulate processing time
    start_time = time.time()
    time.sleep(3)  # Simulate 3 seconds of processing
    end_time = time.time()
    duration_seconds = end_time - start_time

    result = ['processed1.png', 'processed2.png', 'processed3.png', 'processed4.png']
    max_column_id = [4, 5, 6]
    histogram_path = 'histogram/histogram_1.png'

    return {
        'image_paths': result,
        'max_value': max_column_id,
        'histogram': histogram_path,
        'duration_seconds': duration_seconds
    }

if __name__ == "__main__":
    print("Starting test server on http://localhost:8000")
    print("Test the duration feature by calling POST /test or POST /run-gradcam")
    uvicorn.run(app, host="0.0.0.0", port=8000)
