<?php

class People{

	const TABLE = "personas";

	public static function delete($ids){
		$delete = "DELETE FROM ".self::TABLE." WHERE id = ?";
		if( sizeof($ids) > 0 ){
			for( $i = 1; $i < sizeof($ids); $i++ )
				$delete .= " OR id = ?";
		}
		$query = db::singleton()->prepare($delete);			
		$query->execute($ids);
	}

	public static function getAll(){
		$select = "SELECT * FROM ".self::TABLE;
		return db::singleton()->query($select)->fetchAll();
	}

	// TODO convert bare query in a prepared one
	public static function getById($id){
		return db::singleton()->query("SELECT * FROM ".self::TABLE." WHERE id = $id")->fetch();
	}

	public static function insert($name, $surname, $email){
		$insert = "INSERT INTO ".self::TABLE." VALUES (NULL, ?, ?, ?)";
		$query = db::singleton()->prepare($insert);
		$query->execute(array($name, $surname, $email));
	}

	// TODO convert bare query in a prepared one
	public static function search($string_data){
		$data = explode(" ", $string_data);
		$select = "SELECT * FROM ".self::TABLE. " WHERE nombre like '%{$data[0]}%' OR apellidos like '%{$data[0]}%' OR email like '%{$data[0]}%'";
		for($i = 1; $i < sizeof($data); $i++)
			$select .= " OR nombre like '%{$data[$i]}%' OR apellidos like '%{$data[$i]}%' OR email like '%{$data[$i]}%'";
		return db::singleton()->query($select)->fetchAll();
	}

	public static function truncate(){
		$truncate = "TRUNCATE TABLE ".self::TABLE;
		return db::singleton()->query($truncate);
	}

	public static function update($id, $new_data){
		$table = self::TABLE; 
		if( trim($name = $new_data[0]) ){
			db::singleton()->prepare("UPDATE {$table} SET nombre = ? WHERE id = ?")->execute(array($name, $id));
		}
		if( trim($surname = $new_data[1]) ){
			db::singleton()->prepare("UPDATE {$table} SET apellidos = ? WHERE id = ?")->execute(array($surname, $id));
		}
		if( trim($email = $new_data[2]) ){
			db::singleton()->prepare("UPDATE {$table} SET email = ? WHERE id = ?")->execute(array($email, $id));
		}
	}
}