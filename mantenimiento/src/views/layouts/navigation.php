<nav class="navbar navbar-default">
  <div class="container-fluid">
    <div class="navbar-header">
      <button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#bs-example-navbar-collapse-1">
        <span class="sr-only">Toggle navigation</span>
        <span class="icon-bar"></span>
        <span class="icon-bar"></span>
        <span class="icon-bar"></span>
      </button>
      <a class="navbar-brand" href="#">Administrador DB</a>
    </div>

    <div class="collapse navbar-collapse" id="bs-example-navbar-collapse-1">
      <ul class="nav navbar-nav">
        <li><a href="?r=listAll">Listar</a></li>
        <li><a href="?r=insert">Insertar</a></li>
        <li><a href="?r=update">Modificar</a></li>
        <li><a href="?r=delete">Borrar</a></li>
        <li><a href="?r=truncate">Borrar todo</a></li>
      </ul>
      <form class="navbar-form navbar-right" role="search" method="POST" action="?r=search">
        <div class="form-group">
          <input type="text" name="data" class="form-control" placeholder="Buscador" required>
        </div>
        <button type="submit" class="btn btn-default">Buscar</button>
      </form>
        </li>
      </ul>
    </div>
  </div>
</nav>