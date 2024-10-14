<?php
// Include the database configuration file
require_once 'config.php';

// Check if data is received via POST
if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    // Get the JSON input
    $data = json_decode(file_get_contents('php://input'), true);

    // Extract video data
    $user_id = $data['user_id'];
    $video_id = $data['video_id'];
    $title = $data['title'];
    $channel = $data['channel'];
    $length = $data['length'];
    $current_time = $data['current_time'];

    // Prepare the SQL statement
    $sql = "INSERT INTO videos (user_id, video_id, title, channel, length, current_time) 
            VALUES (?, ?, ?, ?, ?, ?)
            ON DUPLICATE KEY UPDATE current_time = ?";

    // Prepare and bind parameters
    if ($stmt = mysqli_prepare($db, $sql)) {
        mysqli_stmt_bind_param($stmt, "sssssss", $user_id, $video_id, $title, $channel, $length, $current_time, $current_time);

        // Execute the statement
        if (mysqli_stmt_execute($stmt)) {
            echo json_encode(['status' => 'success']);
        } else {
            echo json_encode(['status' => 'error', 'message' => 'Failed to save data']);
        }

        // Close the statement
        mysqli_stmt_close($stmt);
    }
}

// Close the connection
mysqli_close($db);
?>
