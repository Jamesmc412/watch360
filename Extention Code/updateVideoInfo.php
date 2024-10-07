<?php
// Database connection settings
$host = 'localhost';             // Database host
$user = 'root';        // Database username
$password = '';// Database password
$database = 'watch360';           // Database name

// Create connection to the MySQL database
$conn = new mysqli($host, $user, $password, $database);

// Check the connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

// Get the raw POST data from the request
$postData = file_get_contents("php://input");

// Decode the JSON data
$data = json_decode($postData, true);

// Validate data
if (!isset($data['userId']) || !isset($data['videoId'])) {
    echo json_encode(['error' => 'Invalid data']);
    exit;
}

// Extract variables from decoded JSON data
$userId = intval($data['userId']);
$videoId = $conn->real_escape_string($data['videoId']);
$videoTitle = $conn->real_escape_string($data['videoTitle']);
$channelName = $conn->real_escape_string($data['channelName']);
$videoLength = intval($data['videoLength']);
$currentTime = intval($data['currentTime']);

// Prepare the SQL statement to insert or update video data
$sql = "INSERT INTO videos (user_id, video_id, video_title, channel_name, video_length, current_time)
        VALUES (?, ?, ?, ?, ?, ?)
        ON DUPLICATE KEY UPDATE
        video_title = VALUES(video_title),
        channel_name = VALUES(channel_name),
        video_length = VALUES(video_length),
        current_time = VALUES(current_time)";

// Prepare the statement and bind the parameters
$stmt = $conn->prepare($sql);
$stmt->bind_param("isssii", $userId, $videoId, $videoTitle, $channelName, $videoLength, $currentTime);

// Execute the statement
if ($stmt->execute()) {
    echo json_encode(['status' => 'success', 'message' => 'Video info updated']);
} else {
    echo json_encode(['status' => 'error', 'message' => 'Failed to update video info']);
}

// Close the connection
$stmt->close();
$conn->close();
?>
