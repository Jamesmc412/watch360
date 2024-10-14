<?php
// Start the session
session_start();

// Destroy the session
$_SESSION = array(); // Clear session data

if (session_destroy()) {
    // Redirect to the login page
    header("Location: login.php");
    exit;
}
?>
