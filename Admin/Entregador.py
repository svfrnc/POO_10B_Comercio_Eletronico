import json
from Admin.Crud import CRUD

class Entregador:
    def __init__(self, id: int, nome: str, email: str, senha: str, fone: str):
        self.id = id
        self.nome = nome
        self.email = email
        self.senha = senha
        self.fone = fone

    def __str__(self):
        return f"Id: {self.id} - Nome: {self.nome} - Email: {self.email} - Telefone: {self.fone}"

    def to_dict(self):
        return {"Id": self.id, "Nome": self.nome, "Email": self.email, "Telefone": self.fone}

class EntregadorDAO(CRUD):
    objetos = []

    @classmethod
    def salvar(cls):
        with open("Jsons/entregadores.json", mode="w") as arquivo:
            json.dump(cls.objetos, arquivo, default=vars)

    @classmethod
    def abrir(cls):
        cls.objetos = []
        try:
            with open("Jsons/entregadores.json", mode="r") as arquivo:
                dados = json.load(arquivo)
                for obj in dados:
                    e = Entregador(obj["id"], obj["nome"], obj["email"], obj["senha"], obj["fone"])
                    cls.objetos.append(e)
        except FileNotFoundError:
            cls.objetos = []