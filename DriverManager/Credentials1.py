class Credentials1:
    """
    Clase que almacena las credenciales de un usuario.
    """
    def __init__(self, username, pwd):
        """
        Inicializa las credenciales con el nombre de usuario y la contraseña.

        :param username: El nombre de usuario.
        :param pwd: La contraseña.

        :type username: str
        :type pwd: str
        """
        self.username = username
        self.pwd = pwd