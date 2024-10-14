<?php
// Database connection settings
$host = 'localhost';
$user = 'root';
$password = '';
$database = 'watch360';

// Create connection to the database
$conn = new mysqli($host, $user, $password, $database);

// start session
session_start();

// Check the connection
if ($conn->connect_error) {
    error_log("Connection failed: " . $conn->connect_error);
    die("Connection failed: " . $conn->connect_error);
}

// Get the user ID from the URL or set a default user ID
$userId = $_SESSION["userid"]; // Replace 1 with the actual user ID if needed
// echo $_SESSION["userid"];

// Check if the form has been submitted
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    // Get the username and password from the form
    $newUsername = $conn->real_escape_string($_POST['changeUsername']);
    $newPassword = $conn->real_escape_string($_POST['changePassword']);

    // Update query to change the username and password
    $updateQuery = "UPDATE users SET username='$newUsername', password='$newPassword' WHERE id=$userId";
    
    if ($conn->query($updateQuery) === TRUE) {
        // Redirect to the login page after successful update
        header("Location: login.php");
        exit;
    } else {
        echo "Error updating record: " . $conn->error;
    }
}

// Query to get the current username and password of the user
$query = "SELECT username, password FROM users WHERE id = $userId";
$result = $conn->query($query);

// Fetch user details
if ($result && $result->num_rows > 0) {
    $user = $result->fetch_assoc();
} else {
    die("User not found");
}

$conn->close();

?>


<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta http-equiv="X-UA-Compatible" content="IE=edge" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <link rel="stylesheet" href="./app.css" />
    <title>Settings Panel</title>
  </head>
  <body>
    <div class="settings-panel" id="SettingsPanel">
      <header>
          <h1>Settings</h1>
		  <button onclick="history.back()">Go Back</button>
      </header>
      <div class="settings" id="Settings">
        <form method="POST" action="">
          <div class="setting">
              <label for="onlineOffline">
                  <span>Online/Offline Visibility</span>
                  <span>Allow friends to be able to see whether or not you are online</span>
              </label>
              <input type="checkbox" id="onlineOffline">
          </div>
          <div class="setting">
              <label for="lightDarkMode">
                  <span>Light/Dark Mode</span>
                  <span>Set the app to a Light Theme or Dark Theme</span>
              </label>
              <input type="checkbox" id="lightDarkMode">
          </div>
          <div class="setting">
              <label for="changeUsername">
                  <span>Change Your Username</span>
                  <span>Alter your current username to a new one</span>
              </label>
              <input type="text" placeholder="Change Your Username" id="changeUsername">
          </div>
          <div class="setting">
              <label for="changePassword">
                  <span>Change Your Password</span>
                  <span>Alter your current password to a new one</span>
              </label>
              <input type="password" placeholder="Change Your Password" id="changePassword">
          </div>
          <div class="setting">
                <label for="submitButton">
                <input type="submit" class="save" value="Save Changes" id="submitButton">
          </div>
        </form>  
      </div>
    </div>
  
    <script src="./app.js"></script>
  </body>
</html>
