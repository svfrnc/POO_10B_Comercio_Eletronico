import json
from Admin.Crud import CRUD
# vou utilizar tipado esse arquivo por fins de estudo
class Produto:
    def __init__(self, id: int, descricao: str, preco: float, estoque: int, idCategoria: int, imagem: str ):
        self.id = id
        self.descricao = descricao
        self.preco = preco
        self.estoque = estoque
        self.idCategoria = idCategoria
        self.imagem = imagem

    def __str__(self) -> str:
        return f" #{self.id} - Nome: {self.descricao} - Preço: R$ {self.preco} - Estoque: {self.estoque} - id da Categoria: #{self.idCategoria} - imagem: {self.imagem}"
    
    def to_dict(self):
        return {"Id":self.id,"Nome": self.descricao, "Preço": self.preco, "Estoque": self.estoque, "idCategoria": self.idCategoria, "Imagem": f"data:image/png;base64,{self.imagem}" if self.imagem else None}
    
class ProdutoDAO(CRUD):
    objetos: list[Produto] = []

    @classmethod
    def alterar_preco_geral(cls, percentual: float) -> None:

        cls.abrir()
        for produto in cls.objetos:
            produto.preco = round(produto.preco * (1 + percentual / 100), 2)
        cls.salvar()

    @classmethod
    def aplicar_desconto(cls, percentual: float) -> None:

        cls.abrir()
        for produto in cls.objetos:
            produto.preco = round(produto.preco - (produto.preco * percentual / 100), 2)
        cls.salvar()

    @classmethod
    def salvar(cls) -> None:
        with open("Jsons/produtos.json", mode = "w") as arquivo:
            json.dump(cls.objetos, arquivo, default = vars)

    @classmethod
    def abrir(cls) -> None:
        cls.objetos = []
        try:
            with open("Jsons/produtos.json", mode = "r") as arquivo:
                objetos_json = json.load(arquivo)
                for obj in objetos_json:
                    p = Produto(obj["id"], obj["descricao"], obj["preco"], obj["estoque"], obj["idCategoria"], obj["imagem"])
                    cls.objetos.append(p)
        except FileNotFoundError:
            cls.objetos = []