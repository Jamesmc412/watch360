const express = require('express');
const mysql = require('mysql');
const app = express();
const port = 80;

// Create connection to MySQL database
const db = mysql.createConnection({
  host: 'localhost',
  user: 'root',
  password: '',
  database: 'watch360'
});

db.connect((err) => {
  if (err) {
    console.error('Error connecting to the database:', err);
    return;
  }
  console.log('Connected to MySQL');
});

// Middleware to parse JSON requests
app.use(express.json());

// Route to handle video info submissions from the extension
app.post('/api/saveVideoInfo', (req, res) => {
  const { userId, videoId, channelName, videoTitle, videoLength, currentTime } = req.body;

  const query = `
    INSERT INTO videos (user_id, video_id, channel_name, video_title, video_length, current_time)
    VALUES (?, ?, ?, ?, ?, ?)
  `;

  db.query(query, [userId, videoId, channelName, videoTitle, videoLength, currentTime], (err, result) => {
    if (err) {
      console.error('Error inserting video data:', err);
      res.status(500).send('Error inserting video data');
      return;
    }
    res.send('Video info saved successfully');
  });
});

app.listen(port, () => {
  console.log(`Server running on http://localhost:${port}`);
});


app.get('/api/getVideos/:userId', (req, res) => {
    const userId = req.params.userId;
  
    const query = `SELECT * FROM videos WHERE user_id = ?`;
  
    db.query(query, [userId], (err, results) => {
      if (err) {
        console.error('Error fetching videos:', err);
        res.status(500).send('Error fetching videos');
        return;
      }
      res.json(results);
    });
  });
  