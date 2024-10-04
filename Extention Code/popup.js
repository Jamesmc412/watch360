document.addEventListener("DOMContentLoaded", () => {
    const bookmarksElement = document.getElementById("bookmarks");
  
    // Function to display video information
    const displayCurrentVideoInfo = (videoInfo) => {
      bookmarksElement.innerHTML = ""; // Clear previous content
  
      if (videoInfo) {
        const { title, channelName, videoLength, currentTime } = videoInfo;
  
        // Create and display video information elements
        const videoInfoElement = document.createElement("div");
        videoInfoElement.innerHTML = `
          <div class="video-info">
            <strong>Title:</strong> ${title}<br>
            <strong>Channel:</strong> ${channelName}<br>
            <strong>Video Length:</strong> ${videoLength}<br>
            <strong>Current Time:</strong> ${currentTime}
          </div>
        `;
        bookmarksElement.appendChild(videoInfoElement);
      } else {
        bookmarksElement.innerHTML = '<i class="row">No video information available</i>';
      }
    };
  
    // Request the current video information from the background
    chrome.runtime.sendMessage({ type: 'REQUEST_VIDEO_INFO' }, (response) => {
      if (chrome.runtime.lastError || !response) {
        console.log("Error:", chrome.runtime.lastError?.message || "No response from background.");
        bookmarksElement.innerHTML = '<i class="row">No video information available</i>';
      } else {
        displayCurrentVideoInfo(response);
      }
    });
  });
  