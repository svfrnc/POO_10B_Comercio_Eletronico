from .Carrinho import Carrinho, CarrinhoDAO
from Admin.Produto import Produto, ProdutoDAO

class View:
    # CARRINHO
    @staticmethod
    def listar_produtos():
        return ProdutoDAO().listar()
    
    @staticmethod
    def inserir_produto_carrinho(idCliente, idProduto, quantidade):
        from Admin.View import View as AdminView
        produto = ProdutoDAO().listar_id(idProduto)

        if produto is None:
            return False
        
        # Se houver promoção ativa, o preço inserido no carrinho já computa o desconto geral
        promo = AdminView.obter_promocao_ativa()
        preco_final = produto.preco
        if promo:
            preco_final = round(produto.preco * (1 - promo.percentual_desconto / 100), 2)
            
        CarrinhoDAO.inserir_produto_carrinho(idCliente, idProduto, produto.descricao, quantidade, preco_final)
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