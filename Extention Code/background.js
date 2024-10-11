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

      // After the content script is injected, send the message to get video info
      chrome.tabs.sendMessage(tabId, {
        type: "GET_VIDEO_INFO",
        videoId: videoId
      }, (response) => {
        if (chrome.runtime.lastError) {
          console.error("Error while sending message:", chrome.runtime.lastError.message);
        } else {
          // Send video data to the backend to update the record
          fetch('http://138.47.155.181/watch360/updateVideoInfo.php', { // Replace with your actual URL
            method: 'POST',
            headers: {
              'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: new URLSearchParams({
              user_id: '1', // Replace with the actual user ID
              video_id: videoId,
              title: response.videoTitle,
              channel: response.channelName,
              length: response.videoLength,
              current_time: response.currentTime
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
  console.log(`Tab ${tabId} was closed`);

  // Send a request to your backend to delete video info when the tab is closed
  fetch('http://138.47.155.181/watch360/removeVideoInfo.php', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
    },
    body: new URLSearchParams({
      user_id: '1', // Replace with the actual user ID
      tab_id: tabId // Optionally track video info per tab
    })
  }).then(response => response.json())
    .then(data => {
      console.log('Video info removed in backend:', data);
    })
    .catch(error => {
      console.error('Error removing video info in backend:', error);
    });
});
