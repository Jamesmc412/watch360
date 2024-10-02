<?php
// This PHP file renders a Friends page styled like the Xbox app

// Include your back-end logic here, e.g., fetching a list of friends from a database.
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

        .settings-btn {
            background-color: transparent;
            border: none;
            color: black;
            cursor: pointer;
            font-size: 18px;
            display: flex;
            align-items: center;
        }

        .settings-btn i {
            margin-right: 8px;
            font-size: 24px;
        }

        .settings-btn:hover {
            text-decoration: underline;
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

    </style>
</head>
<body>

    <div class="header">
        <h1>Watch360</h1>
        <button class="settings-btn" onclick="location.href='settings.php'">
           Settings
        </button>
    </div>

    <div class="sidebar">
        <h3>Search People</h3>
        <form action="search_results.php" method="get">
            <input type="text" name="friend_name" placeholder="search by username" required>
            <button type="submit">Search</button>
        </form>
    </div>

    <div class="main-content">
        <h2>Your Friends</h2>
        <div class="friend-list">
            <!-- Example of friend card -->
            <div class="friend-card">
                <h2>Friend 1</h2>
                <p>Online</p>
            </div>
            <div class="friend-card">
                <h2>Friend 2</h2>
                <p>Offline</p>
            </div>
            <div class="friend-card">
                <h2>Friend 3</h2>
                <p>Online</p>
            </div>
            <!-- Add more friends here -->
        </div>
    </div>

</body>
</html>
