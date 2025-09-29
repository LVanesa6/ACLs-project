from models.constants import *

class AccessControl:
    """
    Clase que implementa un mecanismo de control de acceso basado en los 
    modelos de seguridad BLP (Bell-LaPadula) y BIBA.
    
    Proporciona métodos para verificar permisos de acceso a recursos
    según el rol del usuario, el nivel del recurso y la acción solicitada.
    """

    def __init__(self):
        """Constructor de la clase AccessControl. Actualmente no inicializa atributos."""
        pass

    def check_permissions(self, model, role, resource_level, action):
        """
        Verifica si un rol tiene permisos para realizar una acción sobre un recurso.

        Parámetros:
            model (str): Modelo de seguridad a aplicar (MODEL_BLP o MODEL_BIBA).
            role (str): Rol del usuario (ADMIN, USER, GUEST).
            resource_level (str): Nivel de clasificación del recurso (SECRET, CONFIDENTIAL, PUBLIC).
            action (str): Acción que se desea realizar (por ejemplo: "read", "write").

        Retorna:
            tuple: 
                - 1 y un mensaje de éxito si el acceso es permitido.
                - 0 y un mensaje de error si el acceso es denegado.
        """
        # Selección del conjunto de permisos según el modelo de seguridad
        if model == MODEL_BLP:
            acl_permissions = BLP_PERMISSIONS
        elif model == MODEL_BIBA:
            acl_permissions = BIBA_PERMISSIONS
        
        # Obtiene los permisos correspondientes al rol y nivel del recurso
        permisses = acl_permissions.get((role, resource_level), set())

        # Si no hay permisos definidos, acceso denegado
        if not permisses:
            return 0, self.get_error_message(model, role, resource_level)

        # Si la acción no está dentro de los permisos, acceso denegado
        if action not in permisses:
            return 0, self.get_error_message(model, role, resource_level)

        # Acceso permitido
        return 1, "Acceso concedido, tienes los permisos necesarios para realizar esta acción."
    
    def get_error_message(self, model, role, resource_level):
        """
        Devuelve un mensaje de error detallado en caso de denegación de acceso,
        dependiendo del modelo, rol y nivel de recurso.

        Parámetros:
            model (str): Modelo de seguridad (MODEL_BLP o MODEL_BIBA).
            role (str): Rol del usuario.
            resource_level (str): Nivel de clasificación del recurso.

        Retorna:
            str: Mensaje explicativo del motivo de la denegación de acceso.
        """
        # Reglas para el modelo Bell-LaPadula (BLP)
        if model == MODEL_BLP:
            if role == USER:
                if resource_level == SECRET:
                    return "Los usuarios no pueden leer ni escribir en recursos clasificados como secretos."
                elif resource_level == CONFIDENTIAL:
                    return "Los usuarios solo pueden leer recursos clasificados como confidenciales."
            elif role == GUEST:
                if resource_level == SECRET:
                    return "Los invitados no pueden leer ni escribir en recursos clasificados como secretos."
                elif resource_level == CONFIDENTIAL:
                    return "Los invitados no pueden leer ni escribir en recursos clasificados como confidenciales."
                elif resource_level == PUBLIC:
                    return "Los invitados solo pueden leer recursos clasificados como públicos."
     
        # Reglas para el modelo BIBA
        elif model == MODEL_BIBA:
            if role == ADMIN:
                if resource_level == CONFIDENTIAL:
                    return "Los administradores no pueden leer recursos clasificados como confidenciales."
                if resource_level == PUBLIC:
                    return "Los administradores no pueden leer recursos clasificados como públicos."
            elif role == USER:
                if resource_level == SECRET:
                    return "Los usuarios solo pueden leer recursos clasificados como secretos."
                if resource_level == PUBLIC:
                    return "Los usuarios no pueden leer recursos clasificados como públicos."
            elif role == GUEST:
                if resource_level == SECRET:
                    return "Los invitados solo pueden leer recursos clasificados como secretos."
                if resource_level == CONFIDENTIAL:
                    return "Los invitados solo pueden leer recursos clasificados como confidenciales."

        # Mensaje por defecto si no aplica ninguna regla específica
        return "Acceso denegado."
