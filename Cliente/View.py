from .Carrinho import Carrinho, CarrinhoDAO
from Admin.Produto import Produto, ProdutoDAO

class View:
    # CARRINHO
    @staticmethod
    def listar_produtos():
        return ProdutoDAO().listar()
    
    @staticmethod
    def inserir_produto_carrinho(idCliente, idProduto, quantidade):
        produto = ProdutoDAO().listar_id(idProduto)

        if produto is None:
            return False
        
        CarrinhoDAO.inserir_produto_carrinho(idCliente, idProduto, produto.descricao, quantidade, produto.preco)
        return True
    
    @staticmethod
    def visualizar_carrinho(idCliente):
        return CarrinhoDAO.visualizar_carrinho(idCliente)
    
    @staticmethod
    def comprar_carrinho(idCliente):
        return CarrinhoDAO.comprar_carrinho(idCliente)
    
    @staticmethod
    def listar_compras(idCliente):
        return CarrinhoDAO.listar_compras(idCliente)
    
    @staticmethod
    def limpar_carrinho(idCliente):
        return CarrinhoDAO.limpar_carrinho(idCliente)

    @staticmethod
    def total_carrinho_com_desconto(idCliente):
        return CarrinhoDAO.total_com_desconto(idCliente)