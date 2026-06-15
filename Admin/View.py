from Admin.Cliente import Cliente, ClienteDAO
from Admin.Categoria import Categoria, CategoriaDAO
from Admin.Produto import Produto, ProdutoDAO
from Cliente.Carrinho import Carrinho, CarrinhoDAO
from Admin.Promocao import Promocao, PromocaoDAO
from datetime import datetime
from Admin.Entregador import Entregador, EntregadorDAO
from Admin.Entrega import Entrega, EntregaDAO

class View:
    #CLIENTE
    @staticmethod
    def cliente_inserir(nome, email, senha, fone):
        c = Cliente(0, nome, email, senha, fone)
        ClienteDAO.inserir(c)

    @staticmethod
    def cliente_listar():                            
        return ClienteDAO.listar()
    
    @staticmethod
    def cliente_atualizar(id, nome, email, senha, fone):                         
        c = Cliente(id, nome, email, senha, fone)
        ClienteDAO.atualizar(c)

    @staticmethod
    def cliente_excluir(id):                           
        c = Cliente(id, "", "", "", "")
        ClienteDAO.excluir(c)

    #CATEGORIA
    @staticmethod
    def categoria_inserir(desc):                           
        c = Categoria(0, desc)
        CategoriaDAO().inserir(c)

    @staticmethod
    def categoria_listar():                            
        return CategoriaDAO().listar()
    
    @staticmethod
    def categoria_atualizar(id, desc):
        c = Categoria(id, desc)
        CategoriaDAO().atualizar(c)

    @staticmethod
    def categoria_excluir(id):
        c = Categoria(id, "")
        CategoriaDAO().excluir(c)

    #PRODUTO
    @staticmethod
    def produto_inserir(descricao, preco, estoque, idCategoria, imagem):
        p = Produto(0, descricao, preco, estoque, idCategoria, imagem)
        ProdutoDAO().inserir(p)
    
    @staticmethod
    def produto_listar():                            
        return ProdutoDAO().listar()

    @staticmethod
    def produto_atualizar(id, descricao, preco, estoque, idCategoria, imagem):
        # 1. Recupera a instância do produto existente diretamente do arquivo por meio do ID
        p = ProdutoDAO().listar_id(id)
        
        if p is not None:
            # 2. Modifica os atributos do objeto APENAS se novos dados foram enviados pela interface
            if descricao: 
                p.descricao = descricao
            if preco is not None:
                p.preco = preco
            if estoque is not None:
                p.estoque = estoque
            if idCategoria is not None:
                p.idCategoria = idCategoria
            if imagem:
                p.imagem = imagem
            ProdutoDAO().atualizar(p)

    @staticmethod
    def produto_excluir(id):
        p = Produto(id, "", 0.0, 0, 0, "")
        ProdutoDAO().excluir(p)

    @staticmethod
    def produto_alterar_preco_geral(percentual):
        ProdutoDAO().alterar_preco_geral(percentual)

    #VENDA
    @staticmethod
    def listar_vendas(idCliente):
        return CarrinhoDAO.listar_compras(idCliente)
    
    #PROMOÇOES
    @staticmethod
    def promocao_inserir(data_inicio, data_fim, percentual_desconto):
        p = Promocao(0, data_inicio, data_fim, percentual_desconto)
        PromocaoDAO.inserir(p)

    @staticmethod
    def promocao_listar():
        return PromocaoDAO.listar()

    @staticmethod
    def promocao_excluir(id):
        p = Promocao(id, datetime.now(), datetime.now(), 0.0)
        PromocaoDAO.excluir(p)

    @staticmethod
    def obter_promocao_ativa():
        return PromocaoDAO.obter_promocao_ativa()
    
    @staticmethod
    def entregador_inserir(nome, email, senha, fone):
        e = Entregador(0, nome, email, senha, fone)
        EntregadorDAO.inserir(e)

    @staticmethod
    def entregador_listar():
        return EntregadorDAO.listar()

    # ENTREGAS
    @staticmethod
    def entrega_listar():
        return EntregaDAO.listar()

    @staticmethod
    def entrega_alocar(idEntrega, idEntregador):
        EntregaDAO.abrir()
        entrega = EntregaDAO.listar_id(idEntrega)
        if entrega:
            entrega.idEntregador = idEntregador
            entrega.status = "Em trânsito"
            EntregaDAO.atualizar(entrega)
            return True
        return False

    @staticmethod
    def entrega_atualizar_status(idEntrega, novo_status):
        EntregaDAO.abrir()
        entrega = EntregaDAO.listar_id(idEntrega)
        if entrega:
            entrega.status = novo_status
            EntregaDAO.atualizar(entrega)
            return True
        return False