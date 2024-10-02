<!DOCTYPE html>
<html lang="en">
	<head>
		<meta charset="UTF-8">
		<title>Sign Up</title>
		<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.ccs">
	</head>
	<body>
		<div class="container">
			<div class="row">
				<div class="col-md-12">
					<h2>Sign Up</h2>
					<p>Please fill out this form to create an account</p>
					<form action="" method="post">
						<div class="form-group">
							<label>Full Name</label>
							<input type="text" name="name" class="form-control" required>
						</div>
						<div class="form-group">
							<label>Username</label>
							<input type="username" name="username" class="form-control" required>
						</div>
						<div class="form-group">
							<label>Password</label>
							<input type="password" name="password" class="form-control" required>
						</div>
						<div class="form-group">
							<label>Confirm Password</label>
							<input type="password" name="confirm_password" class="form-control" required>
						</div>
						<div>
						<div class="form-group">
							<input type="submit" name="submit" class="btn btn-primary" value="Submit">
						</div>
						<p>Already have an account? <a href="login.php">Login here</a>.</p>
					</form>
				</div>
			</div>
		</div>
	</body>