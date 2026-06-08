import json
from datetime import datetime
from Admin.Cliente import Cliente, ClienteDAO
from Admin.Crud import CRUD

class Venda:
    def __init__(self, id: int, data: datetime, carrinho: bool, total: float, idCliente: int):
        self.id = id
        self.data = data
        self.carrinho = carrinho
        self.total = total
        self.idCliente = idCliente
    
    def __str__(self) -> str:
        data_formatada = self.data.strftime("%d/%m/%Y - Horário: %H:%M:%S")
        cliente = ClienteDAO.listar_id(self.idCliente)
        nome = cliente.nome if cliente else "Desconhecido"
        return f"ID Compra: #{self.id} - Data: {data_formatada} - Total: R$ {self.total} - Cliente: {nome}"
    
    def to_dict(self):
        data_formatada = self.data.strftime("%d/%m/%Y - Horário: %H:%M:%S")
        cliente = ClienteDAO.listar_id(self.idCliente)
        nome = cliente.nome if cliente else "Desconhecido"
        return {"ID Compra": self.id, "Data": data_formatada,"Total": self.total, "Cliente": nome}
    
class VendaDAO(CRUD):
    objetos: list[Venda] = []
            
    @staticmethod
    def converte_str(o):
        if isinstance(o, datetime):
            return o.isoformat()
        return vars(o)

    @classmethod
    def salvar(cls) -> None:
        with open("Jsons/vendas.json", mode = "w") as arquivo:
            json.dump(cls.objetos, arquivo, default = cls.converte_str)

    @classmethod
    def abrir(cls) -> None:
        cls.objetos = []
        try:
            with open("Jsons/vendas.json", mode = "r") as arquivo:
                vendas_json = json.load(arquivo)
                for obj in vendas_json:
                    v = Venda(obj["id"], datetime.fromisoformat(obj["data"]), obj["carrinho"], obj["total"], obj["idCliente"])
                    cls.objetos.append(v)
        except FileNotFoundError:
            cls.objetos = []