<?php

class MainController{

	public function listAll(){
		$list = People::getAll();
		if( !sizeof( $list ) )
			self::alertEmptyDB();
		else
			render( "list", array( "aux", "list" => $list ) );
	}

	// TODO error message if email exists yet
	public function insert(){
		if( !isset($_POST['submit']))
			render( "insert-form", array());
		else if( isset($_POST['name']) && isset($_POST['surname']) && isset($_POST['email']) ){
			People::insert($_POST['name'], $_POST['surname'], $_POST['email']);
			render( "insert-form", array( "aux", "success_message" => "Nuevo registro creado satisfactoriamente" ) );
		}
		else
			render( "insert-form", array( "aux", "error_message" => "Los datos introducidos no son correctos" ) );
	}

	public function delete(){
		if( isset($_POST['submit']) && !empty($_POST['checkboxes']) )
			self::deleteRecords($_POST['checkboxes']);
		else
			self::showDeletionView();			
	}

	## INNER deleteAction FUNCTIONS
		private function deleteRecords($ids){
			People::delete($ids);
			$list = People::getAll();
			if( !sizeof($list) )
				self::alertEmptyDB();
			else
				render( "delete", array("list" => $list, "success_message" => "Registros borrados satisfactoriamente") );
		}

		private function showDeletionView(){
			$list = People::getAll();
			if( !sizeof( $list ) )
				self::alertEmptyDB();
			else
				render( "delete", array("aux", "list" => $list) );
		}
	## END INNER deleteAction FUNCTIONS

	// TODO check if id exists + check if email exists
	public static function modify(){
		if( isset($_POST['submit']) && isset($_POST['id']) && (isset($_POST['name']) || isset($_POST['surname'])
			|| isset($_POST['email'])) ){
				People::update( $_POST['id'], array( 
					( isset($_POST['name']) ) ? $_POST['name'] : false, 
					( isset($_POST['surname']) ) ? $_POST['surname'] : false, 
					( isset($_POST['email']) ) ? $_POST['email'] : false
					)
				);
			render("update-form", array("aux", "person" => People::getById($_POST['id']), "success_message" => "Registro modificado satisfactoriamente" ) );						
		}else if( isset($_POST['radio']) )
			render("update-form", array("aux", "person" => People::getById($_POST['radio'])) );
		else
			render('update', array("aux", "list" => People::getAll()) );
	}

	public function search(){
		if( !isset($_POST['submit']) && trim($_POST['data']) ){
			$data = $_POST['data'];
			$list = People::search($data);
			if( !sizeof($list) )
				render( "index", array( "aux", 
					"message" => "No se encontraron coincidencias con los siguientes términos de búsqueda:<br> <i>{$data}</i>") );
			else
				render( "list", array( "list" => $list, "success_message" => "Búsqueda: {$data}") );
		}

	}

	public function truncate(){
		$list = People::getAll();
		if( !sizeof( $list ) )
			self::alertEmptyDB();
		else if( !isset($_POST['submit']))
			render( "truncate-form", array() );
		else{
			People::truncate();
			render( "index", array( "aux", "message" => "Acaba de VACIAR la base de datos" ) );
		}
	}

	public function update(){
		$list = People::getAll();
		if( !sizeof( $list ) )
			self::alertEmptyDB();
		else if( isset($_POST['submit']) && !empty($_POST['radio']) )
			render("update-form", array("aux", "person" => People::getById($_POST['radio'])) );
		else
			render('update', array("aux", "list" => $list) );
	}

	private function alertEmptyDB(){
		render( "index", array( "aux", "message" => "La base de datos esta vacía. No hay registros que mostrar" ) );
	}
}