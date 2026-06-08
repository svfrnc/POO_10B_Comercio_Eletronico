import json
from Admin.Crud import CRUD

class Cliente:
    def __init__(self, id, nome, email, senha, fone):
        self.id = id
        self.nome = nome
        self.email = email
        self.senha = senha
        self.fone = fone
    def __str__(self):
        return f"Id: {self.id} - Nome: {self.nome} - Email: {self.email} - Senha: {self.senha} - Telefone: {self.fone}"
    
    def to_dict(self):
        return {"Id": self.id, "Nome": self.nome, "Email": self.email, "Telefone": self.fone}
    
class ClienteDAO(CRUD):
    objetos = []
    
    @classmethod
    def salvar(cls):
        with open("Jsons/clientes.json", mode="w") as arquivo:
            json.dump(cls.objetos, arquivo, default = vars)  
                           
    @classmethod
    def abrir(cls):
        cls.objetos = []
        try:
            with open("Jsons/clientes.json", mode="r") as arquivo:
                clientes_json = json.load(arquivo)
                for obj in clientes_json:
                    c = Cliente(obj["id"], obj["nome"], obj["email"], obj["senha"], obj["fone"])
                    cls.objetos.append(c)        
        except FileNotFoundError:
            ClienteDAO.objetos = []