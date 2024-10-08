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