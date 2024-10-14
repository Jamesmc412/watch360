<?php
// Database configuration
define('DB_SERVER', 'localhost');  // Database server (usually localhost)
define('DB_USERNAME', 'root');     // Database username
define('DB_PASSWORD', '');         // Database password (leave blank if no password is set)
define('DB_NAME', 'watch360');     // Database name (change if necessary)

// Attempt to connect to MySQL database
$db = mysqli_connect(DB_SERVER, DB_USERNAME, DB_PASSWORD, DB_NAME);

// Check connection
if($db === false){
    die("ERROR: Could not connect. " . mysqli_connect_error());
}
?>
