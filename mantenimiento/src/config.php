<?php

class db extends PDO{

	private static $instance;

	public function __construct(){
		$db = array(
			"host" => "localhost",
			"name" => "mantenimiento",
			"user" => "root",
			"pass" => "root",
			array(
				PDO::ATTR_EMULATE_PREPARES => false,
				PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION
				)
		);
		parent::__construct(
			"mysql:host={$db['host']};dbname={$db['name']}",
			$db['user'], 
			$db['pass'],
			array(PDO::MYSQL_ATTR_INIT_COMMAND => 'SET NAMES utf8')
		);
	}

	public static function singleton(){
		if( self::$instance == null )
			self::$instance = new self();
		return self::$instance;
	}
}