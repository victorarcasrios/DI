<form action="?r=delete" method="POST">
	
	<div class="panel panel-default">
		<div class="panel-heading">
			<input type="submit" name="submit" value="Borrar" class="btn btn-danger">
		</div>
		<table class="table table-striped table-bordered">
			<thead>
				<tr>
					<th>#</th>
					<th>Nombre</th>
					<th>Apellidos</th>
					<th>E-mail</th>
					<th>Borrar</th>
				</tr>
			</thead>
			<tbody>

				<?php 
				if( isset($list) ):
					foreach($list as $row):
				?>
					<tr>
						<td><?= $row['id'] ?></td>
						<td><?= $row['nombre'] ?></td>
						<td><?= $row['apellidos'] ?></td>
						<td><?= $row['email'] ?></td>
						<td><input type="checkbox" name="checkboxes[]" value="<?= $row['id'] ?>"></td>
					</tr>
				<?php
					endforeach; 
				endif;
				?>
				
			</tbody>
		</table>
	</div>
</form>