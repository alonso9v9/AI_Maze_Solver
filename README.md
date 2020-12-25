# Entorno básico de laberito #

Este código sirve de base para el proyecto final del curso 
EL5852 Introducción al Reconocimiento de Patrones.

Este semestre dicho proyecto deben controlar agentes robóticos móviles
virtuales, que pueden ejecutar tres acciones:

  * Rotar a la derecha
  * Rotar a la izquierda
  * Avanzar
  
Dichos agentes viven en un laberinto, que puede ser cargado de un
archivo o generado por el código entregado.

El objetivo del proyecto es lograr que dichos agentes resuelvan el
laberinto, utilizando técnicas del aprendizaje reforzado.

El proyecto tiene dos etapas:

  * En la primera etapa, el agente se usa en un modo "simple", en el
    cual él puede rotar en pasos de 90° en sentido horario o
    anti-horario (aunque reaccionará con cierta imprecisión), y podrá 
    avanzar en celdas discretas.
  * En la segunda etapa, el agente tiene un estado más libre, y su
    posición y ángulos de rotación son continuos.

El agente debe descubrir su entorno.  Para ello, en su estado actual
es posible acceder a "sensores virtuales" que producen distancias a
las paredes.

Como parte del proyecto debe lograrse que el agente explore el entorno
y con ello pueda determinar las probabilidades de transición entre
estados.


# Entorno simulado  #

El entorno de simulación se actualiza paso a paso, en tiempo discreto.
Es posible hacer la simulación "ciega", en donde se realiza el ciclo
de actualización de estado de agente y ejecución de acciones, pero en
ese ciclo, cada iteración o cada cierto número de iteraciones puede
visualizarse el universo.

# ¿Cómo hago un "fork" del proyecto original?

El proceso para hacer un "fork" puede depender del sitio que usted elija para hacer su git.

Si va a hacerlo desde gitlab, puede seguir los pasos en

  https://docs.gitlab.com/ee/user/project/repository/forking_workflow.html#creating-a-fork
  
  
# ¿Cómo puedo clonar el proyecto derivado?

La guía para que cada quien clone el proyecto del grupo en gitlab está en:

  https://docs.gitlab.com/ee/gitlab-basics/start-using-git.html

# ¿Cómo pudo sincronizar cambios en el proyecto original?

De esta respuesta:

  https://forum.gitlab.com/t/refreshing-a-fork/32469/2


Es necesario primero crear una referencia al repositorio original con

    git remote add upstream https://https://gitlab.com/palvaradomoya/maze-rl.git
  
Esa línea anterior solo es necesario ejecutarla una única vez, y crea
una referencia remota denominada "upstream", que puede usarse posteriormente.

    git checkout master
    git fetch upstream
    git pull upstream master
  
