  SISTEMA DE GESTIÓN DE TORNEOS DE TAEKWONDO
  Versión 1.0.0

DESCRIPCIÓN
-----------
Sistema completo para la gestión de torneos de taekwondo que incluye:
- Registro y gestión de administradores
- Creación y gestión de torneos
- Creación y gestión de combates
- Tablero central en tiempo real con WebSocket
- Tablero de visualización de combates
- Sistema de puntajes y faltas (GAM-JEOM) en tiempo real
- Gestión de jueces y competidores


REQUISITOS DEL SISTEMA
-----------------------
1. Python 3.8 o superior instalado
2. Backend corriendo en http://localhost:8080
3. Conexión a internet (para descargar dependencias la primera vez)
4. Windows, Linux o macOS


ESTRUCTURA DE ARCHIVOS
-----------------------
├── main.py                      # Archivo principal de la aplicación
├── config.py                    # Configuración del sistema
├── api_client.py                # Cliente para comunicación con backend
├── session_manager.py           # Gestor de sesiones de usuario
├── registro.py                  # Pantalla de registro
├── inicio_sesion.py             # Pantalla de inicio de sesión
├── cuenta.py                    # Pantalla de perfil de usuario
├── actualizar.py                # Pantalla de actualización de datos
├── crear_torneo.py              # Pantalla de creación de torneos
├── crear_combate.py             # Pantalla de creación de combates
├── torneos_anteriores.py        # Gestión de torneos existentes
├── actualizar_torneos.py        # Edición de torneos
├── combates_anteriore.py        # Gestión de combates
├── actualizar_combate.py        # Edición de combates
├── tablero.py                   # Tablero de visualización (solo lectura)
├── tablero_central.py           # Tablero central con controles
├── Imagen5-Photoroom.png        # Logo de la aplicación
├── requirements.txt             # Dependencias de Python
├── run.bat                      # Script de ejecución para Windows
└── README.txt                   # Este archivo


INSTALACIÓN
-----------

OPCIÓN 1: Instalación Automática (Windows)
1. Haz doble clic en "run.bat"
2. El script instalará automáticamente todas las dependencias
3. La aplicación se iniciará automáticamente

OPCIÓN 2: Instalación Manual
1. Abre una terminal/CMD en la carpeta del proyecto
2. Ejecuta: pip install -r requirements.txt
3. Ejecuta: python main.py


DEPENDENCIAS PRINCIPALES
-------------------------
- kivy==2.3.0                    # Framework de interfaz gráfica
- requests==2.31.0               # Cliente HTTP
- websocket-client==1.7.0        # Cliente WebSocket para tiempo real


CONFIGURACIÓN
-------------

1. API Backend:
   - El sistema espera el backend en: http://localhost:8080
   - Para cambiar la URL, edita el archivo config.py:
     API_BASE_URL = "http://tu-servidor:puerto"

2. Timeouts:
   - DEFAULT_TIMEOUT = 15 segundos
   - SHORT_TIMEOUT = 5 segundos
   - LONG_TIMEOUT = 30 segundos
   - Ajusta estos valores en config.py si tu red es lenta


USO DEL SISTEMA
---------------

1. PRIMER USO:
   - Crear una cuenta de administrador en "Registro"
   - Iniciar sesión con las credenciales creadas

2. GESTIÓN DE TORNEOS:
   - Crear Torneo: Define nombre, fecha, sede y horarios
   - Ver Torneos: Lista todos los torneos con opciones de editar/eliminar
   - Editar Torneo: Modifica datos del torneo existente

3. GESTIÓN DE COMBATES:
   - Crear Combate: Define competidores, jueces, configuración
   - Ver Combates: Lista combates por torneo
   - Contraseña: Cada combate tiene una contraseña para acceso
   
4. TABLEROS:
   
   A. TABLERO CENTRAL (Operadores):
      - Requiere contraseña del combate
      - Control total del cronómetro
      - Agregar/restar puntos en tiempo real
      - Agregar/restar faltas GAM-JEOM
      - Descalificación automática con 3 faltas
      - Gestión de rounds y descansos
   
   B. TABLERO DE VISUALIZACIÓN:
      - Solo lectura (público/jueces)
      - Actualización automática en tiempo real vía WebSocket
      - Muestra puntajes y faltas
      - Sin controles de modificación

5. SISTEMA DE PUNTOS:
   - Los puntajes se guardan en la base de datos
   - Actualización en tiempo real para todos los tableros
   - El timer debe estar activo para registrar puntos

6. SISTEMA GAM-JEOM (Faltas):
   - Cada competidor puede acumular hasta 3 faltas
   - 3 faltas = Descalificación automática
   - Las faltas se sincronizan en tiempo real
   - El timer debe estar activo para registrar faltas


CARACTERÍSTICAS PRINCIPALES
----------------------------

Interfaz responsive (se adapta a diferentes tamaños de ventana)
Comunicación en tiempo real vía WebSocket
Sistema de autenticación seguro
Validación de datos en formularios
Gestión completa de CRUD para todas las entidades
Sistema de rounds con cronómetro
Descalificación automática por faltas
Contraseñas de combate para seguridad
Actualización automática de puntajes y faltas


FLUJO DE TRABAJO TÍPICO
------------------------

1. PREPARACIÓN:
   - Administrador crea torneo
   - Administrador crea combates dentro del torneo
   - Sistema genera contraseña para cada combate

2. DÍA DEL TORNEO:
   - Operador ingresa al "Tablero Central" con contraseña
   - Público/Jueces ven "Tablero" (solo visualización)
   - Operador controla: timer, puntajes, faltas

3. DURANTE EL COMBATE:
   - Operador inicia el cronómetro
   - Registra puntos y faltas en tiempo real
   - Sistema actualiza todos los tableros automáticamente
   - Sistema descalifica automáticamente con 3 faltas

4. FIN DEL COMBATE:
   - Todos los puntajes quedan registrados en BD
   - Historial disponible en "Ver Combates"


SOLUCIÓN DE PROBLEMAS
----------------------

PROBLEMA: "No se pudo conectar con el servidor"
SOLUCIÓN: 
- Verifica que el backend esté corriendo en http://localhost:8080
- Verifica tu firewall
- Revisa la configuración en config.py

PROBLEMA: "Error al instalar dependencias"
SOLUCIÓN:
- Asegúrate de tener Python 3.8+: python --version
- Actualiza pip: python -m pip install --upgrade pip
- Instala Visual C++ Redistributable (Windows)

PROBLEMA: "WebSocket no disponible"
SOLUCIÓN:
- Ejecuta: pip install websocket-client
- Verifica que el backend tenga WebSocket habilitado

PROBLEMA: "No se registran puntos o faltas"
SOLUCIÓN:
- Verifica que el cronómetro esté ACTIVO
- Los puntos/faltas solo se registran con timer activo
- Verifica conexión con el backend

PROBLEMA: "La ventana se ve mal o cortada"
SOLUCIÓN:
- El sistema es responsive, ajusta el tamaño de ventana
- Prueba en pantalla completa (F11 en la mayoría de sistemas)
- Ajusta la resolución de tu pantalla

PROBLEMA: "Error de permisos al ejecutar"
SOLUCIÓN:
- Windows: Ejecuta como administrador
- Linux/Mac: Verifica permisos: chmod +x run.bat


ARQUITECTURA DEL SISTEMA
-------------------------

FRONTEND (Esta aplicación - Kivy):
- Interfaz gráfica de usuario
- Cliente HTTP para operaciones CRUD
- Cliente WebSocket para tiempo real
- Gestión de sesiones local

BACKEND (Servidor Spring Boot - separado):
- API REST en http://localhost:8080
- WebSocket server para actualizaciones en tiempo real
- Base de datos (MySQL/PostgreSQL)
- Gestión de combates, puntajes y faltas


ENDPOINTS PRINCIPALES
---------------------

ADMINISTRADORES:
- POST   /api/auth/admin/login
- POST   /api/auth/admin/logout
- GET    /apiAdministradores/administrador/{id}
- PUT    /apiAdministradores/administrador/{id}

TORNEOS:
- GET    /apiTorneos/torneo
- POST   /apiTorneos/torneo
- PUT    /apiTorneos/torneo/{id}
- DELETE /apiTorneos/torneo/{id}

COMBATES:
- GET    /apiCombates/combates
- POST   /apiCombates/combate
- PUT    /apiCombates/combate/{id}
- DELETE /apiCombates/combate/{id}
- GET    /apiCombates/combates/torneo/{id}

PUNTAJES:
- GET    /apiPuntajes/puntaje/alumno/{id}/count
- POST   /apiPuntajes/puntaje/simple
- DELETE /apiPuntajes/puntaje/alumno/{id}/last

GAM-JEOM (FALTAS):
- GET    /apiGamJeom/falta/alumno/{id}/combate/{id}/count
- POST   /apiGamJeom/falta/simple
- DELETE /apiGamJeom/falta/alumno/{id}/combate/{id}/last

WEBSOCKET:
- ws://localhost:8080/ws/tablero/{combateId}


SEGURIDAD
---------

1. AUTENTICACIÓN:
   - Sistema de login con usuario y contraseña
   - Tokens de sesión
   - Contraseñas hasheadas en backend

2. CONTRASEÑAS DE COMBATE:
   - Cada combate tiene contraseña única
   - Solo operadores con contraseña pueden modificar
   - Público puede ver sin contraseña

3. VALIDACIONES:
   - Validación de todos los campos obligatorios
   - Verificación de formatos (email, fechas, etc.)
   - Protección contra inyección SQL (backend)


NOTAS IMPORTANTES
-----------------

TIMER Y REGISTRO DE EVENTOS:
   El cronómetro DEBE estar activo (corriendo) para registrar:
   - Puntos
   - Faltas GAM-JEOM
   Esto previene registros accidentales antes/después del combate

WEBSOCKET PARA TIEMPO REAL:
   Si websocket-client no está instalado:
   - Los tableros NO se actualizarán automáticamente
   - Deberás refrescar manualmente
   - Instala con: pip install websocket-client

DESCALIFICACIÓN:
   La descalificación por 3 faltas es AUTOMÁTICA e INMEDIATA
   - No se puede revertir
   - El combate se marca como finalizado
   - Se muestra popup de descalificación

PERSISTENCIA:
   Todos los datos se guardan en el backend:
   - No hay almacenamiento local
   - Requiere conexión constante
   - Los puntajes persisten entre sesiones


ACTUALIZACIONES FUTURAS
------------------------

Posibles mejoras planificadas:
- [ ] Modo offline con sincronización posterior
- [ ] Estadísticas avanzadas por competidor
- [ ] Exportación de resultados a PDF
- [ ] Sistema de brackets/llaves
- [ ] Transmisión en vivo
- [ ] Aplicación móvil nativa
- [ ] Múltiples idiomas


SOPORTE Y CONTACTO
------------------

Para reportar problemas o sugerencias:
1. Verifica este README primero
2. Revisa los logs de la consola
3. Documenta los pasos para reproducir el error
4. Incluye la versión de Python y sistema operativo


LICENCIA
--------

Sistema desarrollado para gestión de torneos de taekwondo.
Todos los derechos reservados.


CHANGELOG
---------

Versión 1.0.0 (Actual):
- Release inicial
- Sistema completo de gestión de torneos
- Tableros en tiempo real
- Sistema de puntajes y faltas
- WebSocket para actualizaciones automáticas

  ¡Gracias por usar el Sistema de Gestión de Torneos de Taekwondo!
