<!DOCTYPE html>
<html lang="es" xml:lang="es">
	<head>
		<title>Mantenimiento DB - Víctor Arcas</title>
		<meta charset="utf-8">
		<link rel="stylesheet" href="assets/css/bootstrap.min.css">
		<link rel="stylesheet" href="assets/css/main.css">
	</head>
	<body>
		<?php require "src/views/layouts/navigation.php" ?>
		<section id="main" class="container-fluid">
			<?php if(isset($error_message)): ?>
				<div class="row">
					<div class="alert alert-danger col-lg-8 col-lg-offset-2">
						<strong>ERROR: </strong><?= $error_message ?>
					</div>
				</div>
			<?php 
			endif; 
			if(isset($success_message)): ?>
				<div class="row">
					<div class="alert alert-success col-lg-8 col-lg-offset-2">
						<strong>ÉXITO: </strong><?= $success_message ?>
					</div>
				</div>
			<?php endif; ?>
			<?= $content ?>		
		</section>
		<script src="assets/js/jquery.min.js" type="text/javascript"></script>
		<script src="assets/js/bootstrap.min.js" type="text/javascript"></script>
	</body>
</html>
