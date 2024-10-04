<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>YouTube Video Data</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            padding: 20px;
            background-color: #f4f4f4;
        }
        #youtube-data {
            background-color: #fff;
            padding: 15px;
            border: 1px solid #ddd;
            border-radius: 8px;
            max-width: 500px;
            margin: 0 auto;
        }
        h2 {
            margin-top: 0;
        }
    </style>
</head>
<body>
    <h1>Current YouTube Video Information</h1>
    <div id="youtube-data">
        <!-- YouTube video information will be displayed here -->
        <p>No video data available yet...</p>
    </div>

    <script>
        // Listen for messages from the content script
        window.addEventListener('message', (event) => {
            if (event.data.type === 'YOUTUBE_VIDEO_INFO') {
                const videoInfo = event.data.videoInfo;
                const container = document.getElementById('youtube-data');
                
                // Display the YouTube data on the webpage
                container.innerHTML = `
                    <h2>${videoInfo.title}</h2>
                    <p><strong>Channel:</strong> ${videoInfo.channelName}</p>
                    <p><strong>Video Length:</strong> ${videoInfo.videoLength}</p>
                    <p><strong>Current Time:</strong> ${videoInfo.currentTime}</p>
                `;
            }
        });
    </script>
</body>
</html>
