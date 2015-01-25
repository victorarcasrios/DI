<div class="panel panel-default">
	<div class="panel-heading">
		Datos actuales del registro a modificar
	</div>
	<table class="table table-striped table-bordered">
		<thead>
			<tr>
				<th>#</th>
				<th>Nombre</th>
				<th>Apellidos</th>
				<th>E-mail</th>
			</tr>
		</thead>
		<tbody>
			<tr>
				<td><?= $person["id"] ?></td>
				<td><?= $person["nombre"] ?></td>
				<td><?= $person["apellidos"] ?></td>
				<td><?= $person["email"] ?></td>
			</tr>
		</tbody>
	</table>
</div>

<form action="?r=modify" method="POST">
	<div class="form-group col-lg-6 col-lg-offset-3">
		<input type="hidden" name="id" value="<?= $person['id'] ?>">
		<label for="name">Nombre</label>
		<input type="text" name="name" class="form-control" placeholder="Introduce el nuevo nombre" autofocus>
		<label for="surname">Apellidos</label>
		<input type="text" name="surname" class="form-control" placeholder="Introduce los nuevos apellidos">
		<label for="email">Email</label>
		<input type="email" name="email" class="form-control" placeholder="Introduce el nuevo correo electrónico">
	</div>
	<div class="col-lg-4 col-lg-offset-8">
		<input type="submit" class="btn btn-default" name="submit" value="Guardar cambios">
	</div>
</form>
