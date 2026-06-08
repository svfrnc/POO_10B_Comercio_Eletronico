import json
from Admin.Crud import CRUD

class Categoria:
    def __init__(self, id, descricao):
        self.id = id
        self.descricao = descricao
    def __str__(self):
        return f"{self.id} - {self.descricao}"
    
    def to_dict(self):
        return {"Id": self.id, "Descrição": self.descricao}
    
class CategoriaDAO(CRUD):
    objetos = []

    @classmethod
    def salvar(cls):
        with open("Jsons/categorias.json", mode="w") as arquivo:
            json.dump(cls.objetos, arquivo, default = vars)
                         
    @classmethod
    def abrir(cls):
        cls.objetos = []
        try:
            with open("Jsons/categorias.json", mode="r") as arquivo:
                objetos_json = json.load(arquivo)
                for obj in objetos_json:
                    c = Categoria(obj["id"], obj["descricao"])
                    cls.objetos.append(c)        
        except FileNotFoundError:
            cls.objetos = []