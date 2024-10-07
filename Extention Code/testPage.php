<?php
// Database connection settings
$host = 'localhost'; // or your server's IP
$user = 'your_mysql_user';
$password = 'your_mysql_password';
$database = 'watch360';

// Create connection to the database
$conn = new mysqli($host, $user, $password, $database);

// Check the connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

// Get the user ID from the URL or set a default user ID
$userId = isset($_GET['user_id']) ? intval($_GET['user_id']) : 1; // Replace 1 with the actual user ID if needed

// SQL query to fetch videos for the given user ID
$sql = "SELECT video_id, channel_name, video_title, video_length, current_time FROM videos WHERE user_id = ?";
$stmt = $conn->prepare($sql);
$stmt->bind_param("i", $userId);
$stmt->execute();
$result = $stmt->get_result();

// Fetch video data
$videos = [];
while ($row = $result->fetch_assoc()) {
    $videos[] = $row;
}

$stmt->close();
$conn->close();
?>

<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Video Data</title>
</head>
<body>
  <h1>User Video Data</h1>
  <div id="videos">
    <?php if (count($videos) > 0): ?>
      <?php foreach ($videos as $video): ?>
        <div>
          <h2><?php echo htmlspecialchars($video['video_title']); ?></h2>
          <p>Channel: <?php echo htmlspecialchars($video['channel_name']); ?></p>
          <p>Video Length: <?php echo htmlspecialchars($video['video_length']); ?> seconds</p>
          <p>Current Time: <?php echo htmlspecialchars($video['current_time']); ?> seconds</p>
        </div>
        <hr>
      <?php endforeach; ?>
    <?php else: ?>
      <p>No videos found.</p>
    <?php endif; ?>
  </div>
</body>
</html>
