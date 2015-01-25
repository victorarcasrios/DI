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

		<?php 
		if( isset($list) ):
			foreach($list as $row):
		?>
			<tr>
				<td><?= $row['id'] ?></td>
				<td><?= $row['nombre'] ?></td>
				<td><?= $row['apellidos'] ?></td>
				<td><?= $row['email'] ?></td>
			</tr>
		<?php
			endforeach; 
		endif;
		?>
		
	</tbody>
</table>