<?php
require_once "config.php";
require_once "session.php";

$error = ''; // Initialize the error variable
if ($_SERVER["REQUEST_METHOD"] == "POST" && isset($_POST['submit'])) {
    $fullname = trim($_POST['name']);
    $username = trim($_POST['username']);
    $password = trim($_POST['password']);
    $confirm_password = trim($_POST["confirm_password"]);
    $password_hash = password_hash($password, PASSWORD_BCRYPT);

    // Check if the username already exists
    if ($query = $db->prepare("SELECT * FROM users WHERE username = ?")) {
        $query->bind_param('s', $username);
        $query->execute();
        $query->store_result();

        if ($query->num_rows > 0) {
            $error .= '<p class="error">The username is already taken!</p>';
        } else {
            // Validate password length
            if (strlen($password) < 6) {
                $error .= '<p class="error">Password must have at least 6 characters.</p>';
            }

            // Validate confirm password
            if (empty($confirm_password)) {
                $error .= '<p class="error">Please enter confirm password.</p>';
            } else {
                if ($password !== $confirm_password) {
                    $error .= '<p class="error">Passwords do not match.</p>';
                }
            }

            // If no errors, insert the user into the database
            if (empty($error)) {
                $insertQuery = $db->prepare("INSERT INTO users (name, username, password) VALUES (?, ?, ?);");
                $insertQuery->bind_param("sss", $fullname, $username, $password_hash);
                $result = $insertQuery->execute();

                if ($result) {
                    // Optionally log the user in after successful registration
                    $_SESSION["userid"] = $db->insert_id; // Get the last inserted id
                    $_SESSION["user"] = $fullname; // Store the user's name

                    $error = '<p class="success">Your registration was successful! Redirecting to login...</p>';
                    // Redirect to login page or welcome page
                    header("Refresh: 3; url=login.php");
                    exit;
                } else {
                    $error = '<p class="error">Something went wrong! Please try again.</p>';
                }

                $insertQuery->close();
            }
        }
        $query->close();
    }

    // Close DB connection
    mysqli_close($db);
}
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Register</title>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css">
    <style>
        body {
            background-color: black;
            color: white;
        }

        /* Make the "Login here" link green */
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
    </style>
</head>
<body>
    <div class="container">
        <div class="row">
            <div class="col-md-12">
                <h2>Register</h2>
                <p>Please fill in this form to create an account.</p>
                <?php
                // Display errors, if any
                if (!empty($error)) {
                    echo '<div class="alert alert-danger">' . $error . '</div>';
                }
                ?>
                <form action="" method="post">
                    <div class="form-group">
                        <label>Full Name</label>
                        <input type="text" name="name" class="form-control" required>
                    </div>
                    <div class="form-group">
                        <label>Username</label>
                        <input type="text" name="username" class="form-control" required>
                    </div>
                    <div class="form-group">
                        <label>Password</label>
                        <input type="password" name="password" class="form-control" required>
                    </div>
                    <div class="form-group">
                        <label>Confirm Password</label>
                        <input type="password" name="confirm_password" class="form-control" required>
                    </div>
                    <div class="form-group">
                        <input type="submit" name="submit" class="btn btn-primary" value="Register">
                    </div>
                    <p>Already have an account? <a href="login.php">Login here</a>.</p>
                </form>
            </div>
        </div>
    </div>
</body>
</html>
