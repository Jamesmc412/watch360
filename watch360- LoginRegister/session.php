<?php
// Start the session
session_start();

// If user is already logged in, then redirect the user to the welcome page
if (isset($_SESSION["userid"]) && !empty($_SESSION["userid"])) {
    header("location: welcome.php");
    exit;
}
?>
