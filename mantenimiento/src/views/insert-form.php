<form action="?r=insert" method="POST">
	<div class="form-group col-lg-6 col-lg-offset-3">
		<label for="name">Nombre</label>
		<input type="text" name="name" class="form-control" placeholder="Introduce el nombre" required autofocus>
		<label for="surname">Apellidos</label>
		<input type="text" name="surname" class="form-control" placeholder="Introduce los apellidos" required>
		<label for="email">Email</label>
		<input type="email" name="email" class="form-control" placeholder="Introduce el correo electrónico" required>
	</div>
	<div class="col-lg-4 col-lg-offset-8">
		<input type="submit" class="btn btn-default" name="submit" value="Insertar">
	</div>
</form>