<?php

function error_404(){
	echo "ERROR 404: La página buscada no existe";
	die;
}

function render($view, $args = array()) {
    if(count($args) >= 2)
    	extract($args);

    ob_start();
    require "src/views/{$view}.php";
    $content = ob_get_clean();
    require "src/views/layouts/default.php";
}