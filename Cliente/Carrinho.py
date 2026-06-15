import json
from datetime import datetime
from Admin.Venda import Venda, VendaDAO
from Admin.VendaItem import VendaItem, VendaItemDAO
from Admin.Produto import ProdutoDAO
from Admin.Entrega import Entrega, EntregaDAO

class CarrinhoItem:
    def __init__(self, idProduto: int, descricao: str, quantidade: int, preco: float):
        self.idProduto = idProduto
        self.descricao = descricao
        self.quantidade = quantidade
        self.preco = preco
    
    def __str__(self) -> str:
        return f"Produto #{self.idProduto} - {self.descricao} - Quantidade: {self.quantidade} - Preço: {self.preco}"

    def to_dict(self):
        return {"Produto": self.descricao, "Quantidade": self.quantidade, "Preço": self.preco}
    
class Carrinho:
    def __init__(self, id: int, idCliente: int):
        self.id = id
        self.idCliente = idCliente
        self.itens = []
    
    def __str__(self) -> str:
        return f"Carrinho #{self.id} - Cliente #{self.idCliente} - {len(self.itens)} itens"
    
class CarrinhoDAO:
    carrinhos = {}
    proximoIdCarrinho = 1

    @staticmethod
    def obter_ou_criar_carrinho(idCliente):
        """Obtém o carrinho do cliente ou cria um novo se não existir"""
        idCliente_str = str(idCliente)
        if idCliente_str not in CarrinhoDAO.carrinhos:
            # Cria novo carrinho para o cliente
            CarrinhoDAO.carrinhos[idCliente_str] = Carrinho(CarrinhoDAO.proximoIdCarrinho, idCliente)
            CarrinhoDAO.proximoIdCarrinho += 1
        return CarrinhoDAO.carrinhos[idCliente_str]

    @staticmethod
    def inserir_produto_carrinho(idCliente, idProduto, descricao, quantidade, preco):
        CarrinhoDAO.abrir()
        carrinho = CarrinhoDAO.obter_ou_criar_carrinho(idCliente)
        
        item = CarrinhoItem(idProduto, descricao, quantidade, preco)
        carrinho.itens.append(item)
        CarrinhoDAO.salvar()

    @staticmethod
    def comprar_carrinho(idCliente):
        CarrinhoDAO.abrir()
        
        idCliente_str = str(idCliente)
        if idCliente_str not in CarrinhoDAO.carrinhos:
            return False
        
        carrinho = CarrinhoDAO.carrinhos[idCliente_str]
        if len(carrinho.itens) == 0:
            return False

        total = 0.0
        for item in carrinho.itens:
            subtotal = item.preco * item.quantidade
            if item.quantidade >= 5:
                subtotal = subtotal * 0.75
            total += subtotal

        venda = Venda(0, datetime.now(), False, total, idCliente)
        VendaDAO.inserir(venda)
        
        if venda.id == 0:
            return False
        
        venda_id = venda.id
        
        # Cria automaticamente o controle de entrega em estado pendente
        nova_entrega = Entrega(0, venda_id, 0, "Aguardando Entregador")
        EntregaDAO.inserir(nova_entrega)

        for item in carrinho.itens:
            # 1. Registra o item da venda
            venda_item = VendaItem(0, item.quantidade, item.preco, venda_id, item.idProduto)
            VendaItemDAO.inserir(venda_item)
            
            # 2. Recupera a instância do produto vendido
            produto = ProdutoDAO.listar_id(item.idProduto)
            if produto:
                # 3. Deduz a quantidade do estoque do objeto
                produto.estoque -= item.quantidade
                # 4. Atualiza o produto modificado de volta no arquivo JSON
                ProdutoDAO.atualizar(produto)
        
        # Limpa carrinho
        carrinho.itens = []
        CarrinhoDAO.salvar()
        return True
    
    @staticmethod
    def limpar_carrinho(idCliente):
        CarrinhoDAO.abrir()
        idCliente_str = str(idCliente)
        if idCliente_str in CarrinhoDAO.carrinhos:
            CarrinhoDAO.carrinhos[idCliente_str].itens = []
            CarrinhoDAO.salvar()

    @staticmethod
    def visualizar_carrinho(idCliente):
        CarrinhoDAO.abrir()
        idCliente_str = str(idCliente)
        if idCliente_str not in CarrinhoDAO.carrinhos:
            return []
        return CarrinhoDAO.carrinhos[idCliente_str].itens
    
    @staticmethod
    def listar_compras(idCliente):
        """Lista apenas as compras do cliente específico (segurança de dados)"""
        VendaDAO.abrir()
        compras_cliente = [venda for venda in VendaDAO.objetos if venda.idCliente == idCliente]
        return compras_cliente

    @staticmethod
    def total_com_desconto(idCliente):
        CarrinhoDAO.abrir()
        total = 0.0

        for item in CarrinhoDAO.visualizar_carrinho(idCliente):
            subtotal = item.preco * item.quantidade
            if item.quantidade >= 5:
                subtotal = subtotal * 0.75
            total += subtotal

        return total

    @staticmethod
    def salvar():
        carrinhos_dict = {}
        for chave, carrinho in CarrinhoDAO.carrinhos.items():
            carrinhos_dict[chave] = {
                "id": carrinho.id,
                "idCliente": carrinho.idCliente,
                "itens": [vars(item) for item in carrinho.itens]
            }
        
        with open("Jsons/carrinhos.json", mode="w") as arquivo:
            json.dump(carrinhos_dict, arquivo, indent=4)
                           
    @staticmethod
    def abrir():
        CarrinhoDAO.carrinhos = {}
        try:
            with open("Jsons/carrinhos.json", mode="r") as arquivo:
                dados = json.load(arquivo)
                
                # Suporta estrutura antiga e nova
                if "carrinhos" in dados:
                    carrinhos_data = dados.get("carrinhos", {})
                else:
                    carrinhos_data = dados
                
                # Carrega carrinhos
                for chave, carrinho_data in carrinhos_data.items():
                    carrinho = Carrinho(carrinho_data["id"], carrinho_data["idCliente"])
                    for item_data in carrinho_data.get("itens", []):
                        item = CarrinhoItem(
                            item_data["idProduto"],
                            item_data["descricao"],
                            item_data["quantidade"],
                            item_data["preco"]
                        )
                        carrinho.itens.append(item)
                    CarrinhoDAO.carrinhos[chave] = carrinho
                    
                    # Atualiza proximoIdCarrinho para não gerar IDs duplicados
                    if carrinho.id >= CarrinhoDAO.proximoIdCarrinho:
                        CarrinhoDAO.proximoIdCarrinho = carrinho.id + 1
        except FileNotFoundError:
            pass