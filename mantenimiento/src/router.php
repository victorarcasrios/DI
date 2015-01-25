<?php
	require "src/models/People.php";
	require "src/controllers/MainController.php";
	$controller = new MainController();

if(!isset($_GET['r'])){
	$controller->listAll();
}
else{

	$r = $_GET['r'];

	if(!method_exists($controller, $r))
		error_404();

	$controller->$r();
}	