# GRAVISU Duration Display Feature Implementation

## Overview
This implementation adds a duration display feature to GRAVISU that shows the time taken by the model to process images. After processing completes, a popup displays the duration in "XX m XX s" format.

## Changes Made

### Backend Changes (`/workspace/back-end/server.py`)

1. **Added timing to `/run-gradcam` endpoint:**
   ```python
   import time
   start_time = time.time()

   # ... existing processing code ...

   end_time = time.time()
   duration_seconds = end_time - start_time
   ```

2. **Modified response to include duration:**
   ```python
   return {
       'image_paths': result,
       'max_value': max_column_id,
       'histogram': histogram_path[8:],
       'duration_seconds': duration_seconds
   }
   ```

3. **Updated test endpoint for consistency:**
   - Added mock duration (125.5 seconds) to `/test` endpoint

### Frontend Changes (`/workspace/front-end/script.js`)

1. **Added duration formatting function:**
   ```javascript
   function formatDuration(seconds) {
       const minutes = Math.floor(seconds / 60);
       const remainingSeconds = Math.floor(seconds % 60);
       return `${minutes} m ${remainingSeconds} s`;
   }
   ```

2. **Added popup display function:**
   ```javascript
   function showDurationPopup(duration) {
       const formattedDuration = formatDuration(duration);
       alert(`GRAVISU processing completed!\nDuration: ${formattedDuration}`);
   }
   ```

3. **Modified `function3` to show duration popup:**
   ```javascript
   // Show duration popup if duration is available
   if (data.duration_seconds !== undefined) {
       showDurationPopup(data.duration_seconds);
   }
   ```

## Testing

### Test Files Created

1. **`/workspace/tests/test_duration_feature.py`**
   - Unit tests for duration formatting
   - API endpoint structure validation
   - Mock response testing

2. **`/workspace/test_server.py`**
   - Standalone test server for feature validation
   - Simulates processing time and returns duration

3. **`/workspace/test_client.py`**
   - Client to test API endpoints
   - Validates duration formatting and response structure

4. **`/workspace/tests/test_frontend_duration.html`**
   - Frontend testing interface
   - Interactive duration formatting tests

5. **`/workspace/demo_duration_popup.html`**
   - Complete demo of the duration feature
   - Shows implementation details and examples

### Test Results

All tests pass successfully:
- ✅ Duration formatting works correctly for various time values
- ✅ Backend includes `duration_seconds` in response
- ✅ Frontend properly formats and displays duration
- ✅ Popup appears with correct "XX m XX s" format

## Feature Behavior

1. **When model processing starts:**
   - Timer begins tracking processing time
   - User sees "Running..." status

2. **When model processing completes:**
   - Timer stops and calculates duration
   - Duration is included in API response
   - Frontend receives duration and shows popup

3. **Duration format examples:**
   - 30 seconds → "0 m 30 s"
   - 90 seconds → "1 m 30 s"
   - 125 seconds → "2 m 5 s"
   - 3661 seconds → "61 m 1 s"

## Files Modified

- `/workspace/back-end/server.py` - Added timing and duration response
- `/workspace/front-end/script.js` - Added duration formatting and popup

## Files Added

- `/workspace/tests/test_duration_feature.py` - Unit tests
- `/workspace/test_server.py` - Test server
- `/workspace/test_client.py` - Test client
- `/workspace/tests/test_frontend_duration.html` - Frontend tests
- `/workspace/demo_duration_popup.html` - Feature demo

## Deployment Notes

- No additional dependencies required
- Feature is backward compatible
- Works with existing GRAVISU infrastructure
- Duration popup only appears when `duration_seconds` is present in response

## Usage

After uploading images and model, when user clicks "Run Gra-Visu":
1. Processing begins and button shows "Running..."
2. Model processes images (timing tracked automatically)
3. When complete, popup shows: "GRAVISU processing completed! Duration: X m Y s"
4. User clicks OK to dismiss popup
5. Results are displayed as normal

The feature enhances user experience by providing feedback on processing time without disrupting the existing workflow.
