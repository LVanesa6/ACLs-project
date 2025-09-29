"""
Define las constantes utilizadas en el sistema de control de acceso.

Incluye:
- Niveles de clasificación de los recursos (seguridad).
- Roles de los usuarios dentro del sistema.
- Acciones que pueden realizarse sobre los recursos.
- Modelos de seguridad implementados (Bell-LaPadula y Biba).
- Tablas de permisos (ACLs) específicas para cada modelo.
"""

# -----------------------------------
# Niveles de clasificación de recursos
# -----------------------------------
PUBLIC = 1          # Nivel más bajo, información pública
CONFIDENTIAL = 2    # Nivel intermedio, información sensible/confidencial
SECRET = 3          # Nivel más alto, información secreta/estricta

# -------------------
# Definición de roles
# -------------------
ADMIN = "admin"     # Rol de administrador, con mayores privilegios
USER = "user"       # Rol de usuario estándar
GUEST = "guest"     # Rol de invitado, acceso muy limitado

# ---------------------------
# Conjunto de acciones posibles
# ---------------------------
READ = "read"       # Acción de lectura
WRITE = "write"     # Acción de escritura

# -------------------------------
# Modelos de seguridad soportados
# -------------------------------
MODEL_BLP = "Bell-LaPadula"  # Modelo Bell-LaPadula: protege la confidencialidad
MODEL_BIBA = "Biba"          # Modelo Biba: protege la integridad

# ----------------------------------------
# Permisos para el modelo Bell-LaPadula (BLP)
# ----------------------------------------
# Estructura:
#   clave: (ROL, NIVEL)
#   valor: conjunto de acciones permitidas
BLP_PERMISSIONS = {

    # Permisos para Administrador
    (ADMIN, SECRET): {READ, WRITE},        # Puede leer y escribir en recursos secretos
    (ADMIN, CONFIDENTIAL): {READ, WRITE},  # Puede leer y escribir en confidenciales
    (ADMIN, PUBLIC): {READ, WRITE},        # Puede leer y escribir en públicos


    # Permisos para Usuario
    (USER, SECRET): set(),                 # No tiene acceso a recursos secretos
    (USER, CONFIDENTIAL): {READ},          # Puede leer confidenciales
    (USER, PUBLIC): {READ, WRITE},         # Puede leer y escribir en públicos

    # Permisos para Invitado
    (GUEST, SECRET): set(),                # No tiene acceso a secretos
    (GUEST, CONFIDENTIAL): set(),          # No tiene acceso a confidenciales
    (GUEST, PUBLIC): {READ},               # Solo puede leer públicos
}

# ----------------------------------------
# Permisos para el modelo BIBA (Biba)
# ----------------------------------------
# Estructura:
#   clave: (ROL, NIVEL)
#   valor: conjunto de acciones permitidas
BIBA_PERMISSIONS = {

    # Permisos para Administrador
    (ADMIN, SECRET): {READ, WRITE},        # Puede leer y escribir en secretos
    (ADMIN, CONFIDENTIAL): {WRITE},        # Solo puede escribir en confidenciales
    (ADMIN, PUBLIC): {WRITE},              # Solo puede escribir en públicos

    # Permisos para Usuario
    (USER, SECRET): {READ},                # Puede leer secretos
    (USER, CONFIDENTIAL): {READ, WRITE},   # Puede leer y escribir en confidenciales
    (USER, PUBLIC): {WRITE},               # Solo puede escribir en públicos

  
    # Permisos para Invitado
    (GUEST, SECRET): {READ},               # Puede leer secretos
    (GUEST, CONFIDENTIAL): {READ},         # Puede leer confidenciales
    (GUEST, PUBLIC): {READ, WRITE},        # Puede leer y escribir en públicos
}
