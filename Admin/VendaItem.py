import json
from Admin.Crud import CRUD

class VendaItem:
	def __init__(self, id: int, qtd: int, preco: float, idVenda: int, idProduto: int):
		self.id = id
		self.qtd = qtd
		self.preco = preco
		self.idVenda = idVenda
		self.idProduto = idProduto

	def __str__(self) -> str:
		return f"{self.id} - {self.qtd} - {self.preco} - {self.idVenda} - {self.idProduto}"

class VendaItemDAO(CRUD):
	objetos: list[VendaItem] = []


	@classmethod
	def salvar(cls) -> None:
		with open("Jsons/vendaitens.json", mode = "w") as arquivo:
			json.dump(cls.objetos, arquivo, default = vars)

	@classmethod
	def abrir(cls) -> None:
		cls.objetos = []
		try:
			with open("Jsons/vendaitens.json", mode = "r") as arquivo:
				objetos_json = json.load(arquivo)
				for obj in objetos_json:
					vi = VendaItem(obj["id"], obj["qtd"], obj["preco"], obj["idVenda"], obj["idProduto"])
					cls.objetos.append(vi)
		except FileNotFoundError:
			cls.objetos = []