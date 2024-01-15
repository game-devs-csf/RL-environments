# Reinforcement Learning (RL) environments

Environments for RL

- [Cartpole](/cartPole/Cartpole.md)

Aquí van los ambientes que se van a usar para el taller y competencia de Reinforcement Learning para juegos.

# Crear el ambiente de desarrollo con Conda
**Si no eres parte del equipo de desarrollo del taller no te preocupes por esta parte :)**

Para importar las dependencias de desarrollo para armar el taller corre el siguiente comando:
```
conda env create --file dev-environment.yml
```
Para activar este ambiente corre:
```
conda activate rl-lab-dev
```

Además de incluir las dependencias que se usan para que el ambiente y y el juego corran (numpy, pygame), se incluyen cosas como pre-commit (para correr ciertos chequeos antes de que se haga un commit) y Ruff (para lintear y formatear el código, se corre con el pre-commit), así nos aseguramos que el código se mantiene bajo un cierto estándar.

Si quieres correr el chequeo con pre-commit para los archivos que acabas de agregar o modificar, primero asegúrate que agregaste todos esos archivos con ```git add (tus-archivos)``` y luego corre:
```
pre-commit
```
Si se modificó algún archivo, tienes que volver a agregar tus archivos con ```git add``` y ya debería estar listo para que le hagas commit.

# Crear el paquete con el ambiente de Gymnasium

Para instalar el paquete de gymnasium primero tenemos que ir al directorio de GameEnvs haciendo
```
cd GameEnvs
```
Una vez ahí, corremos el siguiente commando para instalarlo, lo que nos permitirá llamarlo posteriormente
```
pip install -e .
```

# Recursos RL

# Cursos

- UCL Course on RL - David Silver - https://www.davidsilver.uk/teaching/
- Huggingface DeepRL course - https://huggingface.co/learn/deep-rl-course/unit0/introduction
- Practical_RL - https://github.com/yandexdataschool/Practical_RL

# Mate

- 3Blue1Brown Essence of Linear Algebra - https://www.youtube.com/playlist?list=PLZHQObOWTQDPD3MizzM2xVFitgF8hE_ab

# Libros

- Intro to RL Barto Sutton - http://incompleteideas.net/book/RLbook2020.pdf
    - [Exercise solutions](https://github.com/LyWangPX/Reinforcement-Learning-2nd-Edition-by-Sutton-Exercise-Solutions/tree/master)

[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
