chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
  // Only act when the page is fully loaded and is a YouTube video page
  if (tab.url && tab.url.includes("youtube.com/watch") && changeInfo.status === 'complete') {
    const queryParameters = tab.url.split("?")[1];
    const urlParameters = new URLSearchParams(queryParameters);
    const videoId = urlParameters.get("v");

    // Inject the content script dynamically
    chrome.scripting.executeScript({
      target: { tabId: tabId },
      files: ['contentScript.js']
    }).then(() => {
      console.log("Content script injected successfully");

      // After the content script is injected, send the message
      chrome.tabs.sendMessage(tabId, {
        type: "GET_VIDEO_INFO",
        videoId: videoId
      }, (response) => {
        if (chrome.runtime.lastError) {
          console.error("Error while sending message:", chrome.runtime.lastError.message);
        } else {
          // Send video data to your backend to update the record
          fetch('http://your-backend-url.com/api/updateVideoInfo', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify({
              userId: '1', // Replace with the actual user ID
              videoId: videoId,
              videoTitle: response.videoTitle,
              channelName: response.channelName,
              videoLength: response.videoLength,
              currentTime: response.currentTime
            })
          }).then(response => response.json())
            .then(data => {
              console.log('Video info updated in backend:', data);
            })
            .catch(error => {
              console.error('Error updating video info in backend:', error);
            });
        }
      });
    }).catch((err) => {
      console.error('Failed to inject content script:', err);
    });
  }
});

// Listener for tab close events
chrome.tabs.onRemoved.addListener((tabId, removeInfo) => {
  // Logic to handle when a tab is closed
  console.log(`Tab ${tabId} was closed`);
  
  // Optionally, you could send a message to your backend to delete or update video data
  fetch('http://your-backend-url.com/api/removeVideoInfo', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      userId: '1', // Replace with the actual user ID
      tabId: tabId // You could track the video info per tab if needed
    })
  }).then(response => response.json())
    .then(data => {
      console.log('Video info removed in backend:', data);
    })
    .catch(error => {
      console.error('Error removing video info in backend:', error);
    });
});

chrome.tabs.onRemoved.addListener((tabId, removeInfo) => {
  console.log(`Tab ${tabId} was closed`);

  // Send a request to your backend to delete video info when the tab is closed
  fetch('http://your-server-url/api/removeVideoInfo.php', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      userId: '1', // Replace with actual user ID
      tabId: tabId  // Optional, if you are tracking by tab
    })
  }).then(response => response.json())
    .then(data => {
      console.log('Video info removed in backend:', data);
    })
    .catch(error => {
      console.error('Error removing video info:', error);
    });
});
