<?php
// Start the session
session_start();

// Check if the user is not logged in, then redirect the user to the login page
if (!isset($_SESSION["userid"]) || empty($_SESSION["userid"])) {
    header("location: login.php");
    exit;
}
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Welcome <?php echo htmlspecialchars($_SESSION["user"]); ?></title>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css">
</head> 
<body>
    <div class="container">
        <div class="row">
            <div class="col-md-12">
                <h1>Hello, <strong><?php echo htmlspecialchars($_SESSION["user"]); ?></strong>. Welcome to the demo site.</h1>
            </div>
            <p>
                <a href="logout.php" class="btn btn-secondary btn-lg active" role="button" aria-pressed="true">Log Out</a>
            </p>
        </div>
    </div>
</body>
</html>
