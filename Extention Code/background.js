chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
  // Only act when the page is fully loaded and is a YouTube video page
  if (tab.url && tab.url.includes("youtube.com/watch") && changeInfo.status === 'complete') {
    const queryParameters = tab.url.split("?")[1];
    const urlParameters = new URLSearchParams(queryParameters);

    // Inject the content script dynamically
    chrome.scripting.executeScript({
      target: { tabId: tabId },
      files: ['contentScript.js']
    }).then(() => {
      console.log("Content script injected successfully");

      // After the content script is injected, send the message
      chrome.tabs.sendMessage(tabId, {
        type: "GET_VIDEO_INFO",
        videoId: urlParameters.get("v")
      }, (response) => {
        if (chrome.runtime.lastError) {
          console.error("Error while sending message:", chrome.runtime.lastError.message);
        } else {
          console.log("Video Info:", response);
        }
      });
    }).catch((err) => {
      console.error('Failed to inject content script:', err);
    });
  }
});

// Listener for messages from content script
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.type === 'UPDATE_VIDEO_INFO') {
    chrome.storage.local.set({ videoInfo: message.videoInfo }, () => {
      console.log('Video info updated:', message.videoInfo);
    });
  }

  if (message.type === 'REQUEST_VIDEO_INFO') {
    chrome.storage.local.get('videoInfo', (data) => {
      sendResponse(data.videoInfo || null);
    });

    // Return true to indicate async response
    return true;
  }
});
