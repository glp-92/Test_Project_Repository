# Programa minimo para probar proteccion de Ramas y ejecutar Actions

## Testing

Incluir `pyproject.toml` indicando el PythonPath en la raiz, de esta manera, los imports desde el directorio `./src/tests/*` a `./src/main` no dan error

```bash
pytest
```

## Linting

Para ejecutar linting sobre el codigo completo dentro de `./src/main` debe incluirse un fichero `__init__.py` vacio

```bash
pylint ./src/main/
```

Si se quiere modificar alguna configuracion de pylint se puede generar un fichero `.pylintrc`

```bash
pylint --generate-rcfile > ./.pylintrc
```

Al fichero se añadio la siguiente linea en `[MAIN]`
```bash
disable=
    C0103 # variables tienen como convencion minuscula, constante mayuscula, pero pylint no lo determina correctamente
```

## Actions

Para hacer un setup de pipelines de actions, se sigue los siguientes pasos

1. `git init` para iniciar repositorio
2. Creando un directorio `.github/workflows` donde almacenar las pipelines. De 2 formas:
  1. Creando un fichero `yml` dentro de un directorio `.github/workflows` en la raiz del proyecto
  2. A través de la interfaz de Github a traves de `New Workflow`

### Ejemplo de Pipeline para Python

```yaml
name: Example Python Pipeline

on:
  push:
    branches: [ "main", "develop" ] # Ramas que ejecutaran la accion en caso de un push
  pull_request:
    branches: [ "main", "develop" ] # Ramas que ejecutaran la accion en caso de un pull request

permissions:
  contents: read

jobs:
  check-app:

    runs-on: ubuntu-latest # Maquina que ejecutara la tarea

    steps:
    - uses: actions/checkout@v4 # checkout permite que la maquina acceda a los ficheros del repositorio
    - name: Listar todos los ficheros de la raiz
      run: ls -la
    - name: Instalar Python3
      uses: actions/setup-python@v5
      with:
        python-version: "3.10" # Especificar aqui la version de Python
    - name: Instalar librerias de pip
      run: |
        python -m pip install --upgrade pip
        if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
    - name: Control de formato con Flake8
      run: |
        flake8 . --exit-zero --statistics # exit-zero devuelve error en caso de no superar el test de formato
    - name: Control de errores en escritura de codigo con Pylint
      run: |
        pylint ./src/main/
    - name: Ejecucion de tests con Pytest
      run: |
        pytest
```

## Proteccion de ramas

Proteger las ramas de develop y main es una forma de evitar inclusion de errores en las mismas y poder revisar el codigo antes de actualizarlas

Para una proteccion minima que exija revision de codigo antes de hacer un `merge` a una rama dada

1. Repositorio en Github => settings => branches => `Add Branch Ruleset`
2. Rellenar el formulario:
  - Enforcement status `enabled` para forzar la aplicacion de reglas
  - Targets => Add Target (añadir ramas) => Include by pattern => `main` y `develop` 
  - [x] Require a pull request before merging => seleccionar el numero minimo de aprobaciones de codigo (por parte de colaboradores diferentes a los que han realizado la pr)

Para proteger ramas de commits pusheados de forma directa.
  - [x] Require status checks (los commits se deben "pushear" a otra rama, para despues ser "mergeados" o "pusheados" directamente a una rama que tenga esta regla despues de que los checks hayan sido superados). Seleccionar `jobs` de workflows que se hayan declarado en github actions para el repositorio

  De esta forma, se notificara que la rama (por ejemplo feature/...) que se pretende mergear no ha superado la pipeline de tests y si se ha marcado el check como requerido no permitira realizar el merge
