import json
from datetime import datetime
from Admin.Crud import CRUD

class Promocao:
    def __init__(self, id: int, data_inicio: datetime, data_fim: datetime, percentual_desconto: float):
        self.id = id
        self.data_inicio = data_inicio
        self.data_fim = data_fim
        self.percentual_desconto = percentual_desconto

    def to_dict(self):
        return {
            "Id": self.id,
            "Início": self.data_inicio.strftime("%d/%m/%Y - %H:%M:%S"),
            "Fim": self.data_fim.strftime("%d/%m/%Y - %H:%M:%S"),
            "Desconto (%)": f"{self.percentual_desconto}%"
        }

class PromocaoDAO(CRUD):
    objetos: list[Promocao] = []

    @staticmethod
    def converte_str(o):
        if isinstance(o, datetime):
            return o.isoformat()
        return vars(o)

    @classmethod
    def salvar(cls) -> None:
        with open("Jsons/promocoes.json", mode="w") as arquivo:
            json.dump(cls.objetos, arquivo, default=cls.converte_str)

    @classmethod
    def abrir(cls) -> None:
        cls.objetos = []
        try:
            with open("Jsons/promocoes.json", mode="r") as arquivo:
                dados = json.load(arquivo)
                for obj in dados:
                    p = Promocao(
                        obj["id"],
                        datetime.fromisoformat(obj["data_inicio"]),
                        datetime.fromisoformat(obj["data_fim"]),
                        obj["percentual_desconto"]
                    )
                    cls.objetos.append(p)
        except FileNotFoundError:
            cls.objetos = []

    @classmethod
    def obter_promocao_ativa(cls) -> Promocao or None:
        """Verifica se a data atual está dentro de algum período promocional cadastrado"""
        cls.abrir()
        agora = datetime.now()
        for promo in cls.objetos:
            if promo.data_inicio <= agora <= promo.data_fim:
                return promo
        return None