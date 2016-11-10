Proyecto final de la matería: Sistemas de Información.

Integrantes:
    -González Ojeda Erick Osvaldo.
    -Septién Hernández José Antonio.

Lenguaje de programación: Python.
Lenguaje para bases de datos: MySQL.
APIs: Flask, SQLAlchemy.

Título: SkyNet.

Descripción:
Se implementará una red social sencilla. Va a poder manejar distintos
usuarios.

Para simular el proyecto, se hará uso de una Virtual Box y de valgrant.

*Nota: Para poder simularlo adecuadamente, se sugiere que se tenga instalado
el paquete cygwin o git bash.

Instalar Virtual Box:
Dirígete a la [página](https://www.virtualbox.org/wiki/Downloads) y
descarga la versión 4.3.0. Instálala siguiendo los pasos.

Instalar Vagrant:
Dirígete a las [página](https://www.vagrantup.com/downloads.html) e
instala la versión para tu sistema operativo.

Ejecutando vagrant:
Una vez que hayas instalado los paquetes anteriores, diríjete la
carpeta de tu proyecto (contiene el archivo Vagrantfile) y ejecuta el
comando vagrant up. Si es la primera vez que ejecutas el comando, va a
instalar todas las dependencias necesarias para poder ejecutar la máquina.
En caso contrario, únicamente va a iniciar la máquina.
*Nota: Si intentas correr el comando, una vez instalada la caja, y te marca
un error (no ha podido iniciar), intenta abrir la interfaz gráfica de
Virtual Box e inicia manualmente la caja correspondiente. Una vez que haya
iniciado por completo, apágala y vuelve a correr el comando.

Cuando se haya iniciado la caja, ejecuta el comando vagrant ssh, esto te va
conectar con la caja, y vas a poder empezar a trabajar dentro de ella.

Carpetas:
Las siguientes carpetas van a estar incluidas en el proyecto:
templates/  ->  contiene los .html correspondientes.
static/  ->  contiene los .css, .js y demás arhivos que se van a enviar desde
el servidor.

Archivos:
templates/inicio.html  -> html de la página de entrada.
templates/home.html  ->  template de la página de inicio de cada usuario.