(() => {
  let youtubePlayer;

  // Function to get current video info
  const getCurrentVideoInfo = () => {
    const videoTitle = document.querySelector('h1.title.style-scope.ytd-video-primary-info-renderer')?.innerText;
    const videoLength = youtubePlayer?.duration;
    const currentTime = youtubePlayer?.currentTime;
    const videoId = new URLSearchParams(window.location.search).get("v");
    const channelName = document.querySelector('ytd-channel-name a')?.innerText || "Unknown Channel";

    return {
      title: videoTitle || "Unknown title",
      videoId: videoId || "Unknown video ID",
      channel: channelName,
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

  // Send video information to the background script
  const sendVideoInfoToBackground = () => {
    const videoInfo = getCurrentVideoInfo();

    chrome.runtime.sendMessage({
      type: 'UPDATE_VIDEO_INFO',
      videoInfo: videoInfo
    });

    sendVideoInfoToDatabase(videoInfo);  // Also send the data to the backend database
  };

  // Send video info to backend API (PHP)
  const sendVideoInfoToDatabase = (videoInfo) => {
    const userId = "123";  // Replace with the actual user ID logic

    fetch('http://localhost/path/to/save_video.php', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        user_id: userId,
        video_id: videoInfo.videoId,
        title: videoInfo.title,
        channel: videoInfo.channel,
        length: videoInfo.videoLength,
        current_time: videoInfo.currentTime
      })
    })
    .then(response => response.json())
    .then(data => {
      if (data.status === 'success') {
        console.log('Video info saved successfully');
      } else {
        console.error('Failed to save video info:', data.message);
      }
    })
    .catch(error => console.error('Error:', error));
  };

  // Listen for video state updates every second
  setInterval(() => {
    youtubePlayer = document.getElementsByClassName('video-stream')[0];
    if (youtubePlayer) {
      sendVideoInfoToBackground();  // Send updated video info to background.js
    }
  }, 1000);  // Update every second
})();
