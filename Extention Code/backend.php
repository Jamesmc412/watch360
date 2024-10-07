<?php
// Database connection settings
$host = 'localhost';
$user = 'root';
$password = '';
$database = 'watch360';

// Create connection to the database
$conn = new mysqli($host, $user, $password, $database);

// Check the connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

// Get the raw POST data from the request
$postData = file_get_contents("php://input");
$data = json_decode($postData, true);

// Get the user ID and video information from the POST data
$userId = intval($data['userId']);
$videoId = $conn->real_escape_string($data['videoId']);
$videoTitle = $conn->real_escape_string($data['videoTitle']);
$channelName = $conn->real_escape_string($data['channelName']);
$videoLength = intval($data['videoLength']);
$currentTime = intval($data['currentTime']);

// Check if the user already has a video entry in the database
$sql = "SELECT id FROM videos WHERE user_id = ?";
$stmt = $conn->prepare($sql);
$stmt->bind_param("i", $userId);
$stmt->execute();
$stmt->store_result();

if ($stmt->num_rows > 0) {
    // If the user has a video entry, update it
    $updateSql = "UPDATE videos SET video_id = ?, video_title = ?, channel_name = ?, video_length = ?, current_time = ? WHERE user_id = ?";
    $updateStmt = $conn->prepare($updateSql);
    $updateStmt->bind_param("sssiis", $videoId, $videoTitle, $channelName, $videoLength, $currentTime, $userId);
    $updateStmt->execute();
} else {
    // If the user does not have a video entry, insert a new record
    $insertSql = "INSERT INTO videos (user_id, video_id, video_title, channel_name, video_length, current_time) VALUES (?, ?, ?, ?, ?, ?)";
    $insertStmt = $conn->prepare($insertSql);
    $insertStmt->bind_param("isssii", $userId, $videoId, $videoTitle, $channelName, $videoLength, $currentTime);
    $insertStmt->execute();
}

$conn->close();

echo json_encode(["status" => "success"]);
?>
