from front_end.script import function3

import pytest

# Test for the duration alert in the front-end script

def test_duration_alert(monkeypatch):
    # Simulate the performance.now() function
    monkeypatch.setattr("time.perf_counter", lambda: 1000)  # Start time

    # Simulate the alert function
    alert_called = False
    def mock_alert(message):
        nonlocal alert_called
        alert_called = True
        assert "Processing time:" in message

    monkeypatch.setattr("builtins.print", mock_alert)

    # Call the function that triggers the alert
    function3(None)  # Call the function directly

    assert alert_called, "Alert was not called"
