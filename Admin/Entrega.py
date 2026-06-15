# Admin/Entrega.py
import json
from Admin.Crud import CRUD

class Entrega:
    def __init__(self, id: int, idVenda: int, idEntregador: int, status: str):
        self.id = id
        self.idVenda = idVenda
        self.idEntregador = idEntregador  # 0 significa que ainda não foi alocado
        self.status = status

    def to_dict(self):
        from Admin.Entregador import EntregadorDAO
        EntregadorDAO.abrir()
        entregador = next((e for e in EntregadorDAO.objetos if e.id == self.idEntregador), None)
        nome_entregador = entregador.nome if entregador else "Aguardando Alocação"
        return {
            "ID Entrega": self.id,
            "ID Pedido": self.idVenda,
            "Entregador": nome_entregador,
            "Status": self.status
        }

class EntregaDAO(CRUD):
    objetos = []

    @classmethod
    def salvar(cls):
        with open("Jsons/entregas.json", mode="w") as arquivo:
            json.dump(cls.objetos, arquivo, default=vars)

    @classmethod
    def abrir(cls):
        cls.objetos = []
        try:
            with open("Jsons/entregas.json", mode="r") as arquivo:
                dados = json.load(arquivo)
                for obj in dados:
                    e = Entrega(obj["id"], obj["idVenda"], obj["idEntregador"], obj["status"])
                    cls.objetos.append(e)
        except FileNotFoundError:
            cls.objetos = []