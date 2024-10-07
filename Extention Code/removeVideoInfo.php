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

// Get the user ID and tab ID (if you want to track it)
$userId = intval($data['userId']);
$tabId = intval($data['tabId']); // If you are using tabId, otherwise you can ignore

// Remove the video data for the user (or by tab if you are tracking it)
$sql = "DELETE FROM videos WHERE user_id = ?";
$stmt = $conn->prepare($sql);
$stmt->bind_param("i", $userId);
$stmt->execute();
$stmt->close();

$conn->close();

echo json_encode(["status" => "success"]);
?>
