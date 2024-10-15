<?php
// Include config.php for database connection and session.php to start the session
require_once "config.php"; // Ensure this file sets up the $db variable
require_once "session.php"; // Ensure this file calls session_start()

// Check if the session is started and if the user is logged in
if (!isset($_SESSION['userid'])) {
    header("Location: login.php");
    exit;
}

$error = ''; // Variable to store errors
// Fetch friends of the logged-in user
$loggedInUserId = $_SESSION['userid'];

// Prepare the SQL query to fetch friends
if ($stmt = $db->prepare("SELECT u.id, u.name, u.username, 
        IFNULL(f.status, 'not_friends') AS friendship_status 
        FROM users u
        LEFT JOIN friendships f 
        ON (u.id = f.friend_id AND f.user_id = ?) 
        OR (u.id = f.user_id AND f.friend_id = ?)
        WHERE u.id != ?")) {

    // Bind the parameters
    $stmt->bind_param('iii', $loggedInUserId, $loggedInUserId, $loggedInUserId);

    // Execute the query
    $stmt->execute();

    // Get the result
    $result = $stmt->get_result();
    $friends = $result->fetch_all(MYSQLI_ASSOC);

    // Close the statement
    $stmt->close();
} else {
    $error = "Database error: Unable to prepare query.";
}
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Watch360</title>
    <style>
        body {
            margin: 0;
            font-family: Arial, sans-serif;
            background-color: #ffffff; 
            color: #1b1b1b; 

        .header {
            background-color: #107c10; /* Xbox Green */
            padding: 10px 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .header h1 {
            font-size: 24px;
        }

         .header-buttons {
            display: flex;
            gap: 10px; /* Space between buttons */
        }

        .header-buttons .settings-btn, .header-buttons .logout-btn {
            background-color: transparent;
            border: none;
            color: black;
            cursor: pointer;
            font-size: 18px;
            display: flex;
            align-items: center;
        }

        .header-buttons .settings-btn i, .header-buttons .logout-btn i {
            margin-right: 8px;
            font-size: 24px;
        }

        .sidebar {
            width: 200px;
            background-color: #242424;
            height: 100vh;
            position: fixed;
            top: 79px;
            left: 0;
            padding: 10px;
        }

        .sidebar h3 {
            color: white;
            margin-bottom: 10px;
        }

        .sidebar form input {
            width: 90%;
            padding: 10px;
            margin-bottom: 10px;
            border: black;
            border-radius: 5px;
        }

        .sidebar form button {
            width: 100%;
            padding: 10px;
            background-color: #107c10;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }

        .main-content {
            margin-left: 220px;
            padding: 20px;
        }

        .friend-list {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
            gap: 20px;
        }

        .friend-card {
            background-color: #333;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
        }

        .friend-card h2 {
            font-size: 18px;
            margin-bottom: 5px;
        }

        .friend-card p {
            font-size: 14px;
            color: #bbb;
        }

        .currently-watching {
            font-size: 14px;
            color: #ccc; /* Lighter color for "Currently watching" */
            margin-top: 10px;
        }


    </style>
</head>
<body>

    <div class="header">
        <h1>Watch360</h1>
         <div class="header-buttons">
            <button class="settings-btn" onclick="location.href='settings.php'">
                Settings
            </button>
            <button class="logout-btn" onclick="location.href='logout.php'">
                Logout
            </button>
        </div>
    </div>

    <div class="sidebar">
        <h3>Search People</h3>
        <form action="search_results.php" method="get">
            <input type="text" name="friend_name" placeholder="Search by username" required>
            <button type="submit">Search</button>
        </form>
    </div>

    <div class="main-content">
    <h2>Your Friends</h2>
    
    <div class="friend-list">
        <?php if (!empty($friends)): ?>
            <?php foreach ($friends as $friend): ?>
                <div class="friend-card">
                    <h2><?php echo htmlspecialchars($friend['name']); ?></h2>
                    <p>
                        <?php 
                        // Display friendship status
                        if ($friend['friendship_status'] == 'accepted') {
                            echo 'Online';  // Placeholder, replace with real online status if available
                        } elseif ($friend['friendship_status'] == 'pending') {
                            echo 'Friend Request Pending';
                        } else {
                            echo 'Not Friends';
                        }
                        ?>
                    </p>
                    <p class="currently-watching">Currently watching: ?</p> <!-- Add dynamic watching info if available -->
                </div>
            <?php endforeach; ?>
        <?php else: ?>
            <p>You have no friends to display.</p>
        <?php endif; ?>
    </div>
</div>


</body>
</html>
