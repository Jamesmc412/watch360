<?php
// updateVideoInfo.php
header("Content-Type: application/json");

// Connect to MySQL database
$host = 'localhost';
$db = 'watch360';
$user = 'root'; // Replace with your DB user
$pass = '';     // Replace with your DB password

$conn = new mysqli($host, $user, $pass, $db);

// Check connection
if ($conn->connect_error) {
    die(json_encode(['success' => false, 'message' => 'Database connection failed']));
}

// Get the POST data from the extension
$userId = $_POST['user_id'];
$videoId = $_POST['video_id'];
$title = $_POST['title'];
$channel = $_POST['channel'];
$length = $_POST['length'];
$currentTime = $_POST['current_time'];

// Insert or update the video information
$sql = "INSERT INTO videos (user_id, video_id, title, channel, length, current_time)
        VALUES ('$userId', '$videoId', '$title', '$channel', '$length', '$currentTime')
        ON DUPLICATE KEY UPDATE
        title = '$title', channel = '$channel', length = '$length', current_time = '$currentTime'";

if ($conn->query($sql) === TRUE) {
    echo json_encode(['success' => true, 'message' => 'Video info updated']);
} else {
    echo json_encode(['success' => false, 'message' => 'Failed to update video info']);
}

$conn->close();
?>
