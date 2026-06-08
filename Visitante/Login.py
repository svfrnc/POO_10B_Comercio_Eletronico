from Admin.Cliente import Cliente, ClienteDAO 



class Login:
    def __init__(self, email: str, senha: str):
        self.email = email
        self.senha = senha

    def __str__(self):
        return f"{self.email} - {self.senha}"
    
class LoginDAO:
    usuario_logado = False
    idCliente_logado = None
    nome_logado = None

    @classmethod
    def logado(cls, email, senha) -> bool:
        
        ClienteDAO.abrir()

        for cliente in ClienteDAO.objetos:
            if (cliente.email == email) and (cliente.senha == senha):
                cls.usuario_logado = True
                cls.idCliente_logado = cliente.id
                cls.nome_logado = cliente.nome
                return True
             
        cls.usuario_logado = False
        cls.idCliente_logado = None
        return False