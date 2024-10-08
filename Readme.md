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

## Git hooks

En el directorio `.git/hooks` se pueden colocar scripts (sh por ejemplo) que modifiquen el comportamiento de git ante ciertas acciones.

### Pre-commit

Para ejecutar un script previo a realizar un commit, el fichero debe tener nombre `pre-commit`

Un ejemplo en `/.git/hooks/pre-commit` que revisa el formato con flake8 y ejecuta un test simple con pytest

```bash
#!/usr/bin/env bash
# If any command fails, exit immediately with that command's exit status
set -eo pipefail

# Activar entorno de Anaconda para poder usar las librerias
eval "$(conda shell.bash hook)" # Esta linea lanza un hook que exporta las rutas de anaconda y lo hace disponible por el script
conda activate testenv
# Otro metodo
# source /home/glpazos/anaconda3/bin/activate testenv

# Ejecuta flake8 en el directorio raiz
flake8 . --statistics
if [ $? -ne 0 ]; then # 
 echo "Comprobacion flake8 erronea. Abortando el commit."
 exit 1
fi

# Ejecuta pytest en el directorio local
pytest
if [ $? -ne 0 ]; then # 
 echo "Comprobacion con pytest erronea. Abortando el commit."
 exit 1
fi
echo "pytest tests resueltos con exito!"
```