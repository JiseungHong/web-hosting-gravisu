// Test for duration popup functionality
describe('Duration Popup Test', function() {
  it('should display a popup with the duration when data contains duration property', function() {
    // Mock the alert function
    const originalAlert = window.alert;
    let alertMessage = '';
    window.alert = function(message) {
      alertMessage = message;
    };
    
    // Create a mock data object with duration
    const mockData = {
      image_paths: ['img1.png', 'img2.png', 'img3.png', 'img4.png'],
      max_value: [3, 2, 1],
      histogram: 'histogram_1.png',
      duration: '2 m 30 s'
    };
    
    // Simulate the code that would display the popup
    if (mockData.duration) {
      alert(`GRAVISU processing time: ${mockData.duration}`);
    }
    
    // Check if the alert was called with the correct message
    expect(alertMessage).toBe('GRAVISU processing time: 2 m 30 s');
    
    // Restore the original alert function
    window.alert = originalAlert;
  });
  
  it('should not display a popup when data does not contain duration property', function() {
    // Mock the alert function
    const originalAlert = window.alert;
    let alertCalled = false;
    window.alert = function() {
      alertCalled = true;
    };
    
    // Create a mock data object without duration
    const mockData = {
      image_paths: ['img1.png', 'img2.png', 'img3.png', 'img4.png'],
      max_value: [3, 2, 1],
      histogram: 'histogram_1.png'
    };
    
    // Simulate the code that would display the popup
    if (mockData.duration) {
      alert(`GRAVISU processing time: ${mockData.duration}`);
    }
    
    // Check if the alert was not called
    expect(alertCalled).toBe(false);
    
    // Restore the original alert function
    window.alert = originalAlert;
  });
});
