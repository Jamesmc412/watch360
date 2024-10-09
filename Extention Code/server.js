// server.js
const express = require('express');
const mysql = require('mysql');
const app = express();
const bodyParser = require('body-parser');

app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

const db = mysql.createConnection({
  host: 'localhost',
  user: 'root',
  password: '',
  database: 'watch360'
});

db.connect(err => {
  if (err) throw err;
  console.log('Connected to MySQL');
});

app.post('/updateVideoInfo', (req, res) => {
  const { user_id, video_id, title, channel, length, current_time } = req.body;

  const sql = `INSERT INTO videos (user_id, video_id, title, channel, length, current_time)
               VALUES (?, ?, ?, ?, ?, ?)
               ON DUPLICATE KEY UPDATE
               title = VALUES(title), channel = VALUES(channel), length = VALUES(length), current_time = VALUES(current_time)`;

  db.query(sql, [user_id, video_id, title, channel, length, current_time], (err, result) => {
    if (err) {
      return res.json({ success: false, message: 'Failed to update video info' });
    }
    res.json({ success: true, message: 'Video info updated' });
  });
});

app.listen(3000, () => {
  console.log('Server running on port 3000');
});
