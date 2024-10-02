<?php
require_once "config.php";
require_once "session.php"; // Make sure this starts the session

$error = '';
if ($_SERVER["REQUEST_METHOD"] == "POST" && isset($_POST['submit'])) {
    $username = trim($_POST['username']);
    $password = trim($_POST['password']);

    // Validate if username is empty
    if (empty($username)) {
        $error .= '<p class="error">Please enter username.</p>';
    }

    // Validate if password is empty
    if (empty($password)) {
        $error .= '<p class="error">Please enter password.</p>';
    }

    // Proceed only if there are no validation errors
    if (empty($error)) {
        if ($query = $db->prepare("SELECT * FROM users WHERE username = ?")) {
            $query->bind_param('s', $username);
            $query->execute();
            $result = $query->get_result();
            $row = $result->fetch_assoc();
            
            // Check if the user exists
            if ($row) {
                // Verify password
                if (password_verify($password, $row['password'])) {
                    // Store user session
                    $_SESSION["userid"] = $row['id'];
                    $_SESSION["user"] = $row['name']; // Store the user's name if needed

                    // Redirect to the welcome page
                    header("location: welcome.php");
                    exit;
                } else {
                    $error .= '<p class="error">The password is not valid.</p>';
                }
            } else {
                $error .= '<p class="error">No user exists with that username.</p>';
            }
            $query->close(); // Close query
        } else {
            $error .= '<p class="error">Database error: Unable to prepare query.</p>';
        }
    }
    
    // Close connection
    mysqli_close($db);
}
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Login</title>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css">
    <style>
        body {
            background-color: white;
            color: black;
            position: relative;
            min-height: 100vh; /* Ensure the body covers full viewport height */
            margin: 0;
            padding-bottom: 100px; /* Space for image */
        }

        /* Make the "Register here" link green */
        a {
            color: green;
        }

        /* Make the "Submit" button green */
        .btn-primary {
            background-color: green;
            border-color: green;
        }

        /* Change button color on hover */
        .btn-primary:hover {
            background-color: darkgreen;
            border-color: darkgreen;
        }

        /* Style for the image at the bottom */
        .bottom-image {
            position: absolute;
            bottom: 0;
            left: 50%;
            transform: translateX(-50%);
            width: 200px; /* Increased size to make the image larger */
            height: auto; /* Maintain aspect ratio */
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="row">
            <div class="col-md-12">
                <h2>Login</h2>
                <p>Please fill in your username and password.</p>
                <?php
                // Display errors, if any
                if (!empty($error)) {
                    echo '<div class="alert alert-danger">' . $error . '</div>';
                }
                ?>
                <form action="" method="post">
                    <div class="form-group">
                        <label>Username</label>
                        <input type="text" name="username" class="form-control" required />
                    </div>
                    <div class="form-group">
                        <label>Password</label>
                        <input type="password" name="password" class="form-control" required>
                    </div>
                    <div class="form-group">
                        <input type="submit" name="submit" class="btn btn-primary" value="Submit">
                    </div>
                    <p>Don't have an account? <a href="register.php">Register here</a>.</p>
                </form>
            </div>
        </div>
    </div>

    <!-- XBOX Image positioned at the bottom of the page -->
    <img src="smallxbox.png" alt="Small Xbox" class="bottom-image">
</body>
</html>
