(() => {
    let youtubePlayer;
  
    // Function to get current video info
    const getCurrentVideoInfo = () => {
      const videoTitle = document.querySelector('h1.title.style-scope.ytd-video-primary-info-renderer')?.innerText;
      const channelName = document.querySelector('#text-container a')?.innerText;
      const videoLength = youtubePlayer?.duration;
      const currentTime = youtubePlayer?.currentTime;
  
      return {
        title: videoTitle || "Unknown title",
        channelName: channelName || "Unknown channel",
        videoLength: getTime(videoLength), // Convert seconds to HH:MM:SS format
        currentTime: getTime(currentTime)
      };
    };
  
    // Utility function to format time as HH:MM:SS
    const getTime = (t) => {
      if (!t) return "00:00:00";
      const date = new Date(0);
      date.setSeconds(t);
      return date.toISOString().substr(11, 8);
    };
  
    // Send video information to background.js
    const sendVideoInfoToBackground = () => {
      const videoInfo = getCurrentVideoInfo();
  
      chrome.runtime.sendMessage({
        type: 'UPDATE_VIDEO_INFO',
        videoInfo: videoInfo
      });
    };
  
    // Listen for video state updates
    setInterval(() => {
      youtubePlayer = document.getElementsByClassName('video-stream')[0];
      if (youtubePlayer) {
        sendVideoInfoToBackground();  // Send updated video info to background.js
      }
    }, 1000);  // Update every second
  })();
  