from Cliente.View import View as ClienteView
from Visitante.Login import LoginDAO
import streamlit as st
from streamlit_option_menu import option_menu
import time


class ClienteInterface:
    @staticmethod
    def main() -> None:

        st.session_state.email_logado
        st.session_state.nome_cliente_logado

        with st.sidebar:
            st.info(f"Bem Vindo, {st.session_state.nome_cliente_logado}")

            aba_selecionada = option_menu(
                menu_title = "Painel Cliente",
                options = ["Ver Produtos", "Carrinho", "Meus Pedidos"],
                icons = ["box-seam", "cart", "cash-coin", "receipt"],
                default_index = 0,
                key = "cliente_menu"
            )
            button_sair: bool = st.button("Sair", type="primary")
            if button_sair:
                ClienteInterface.sair()

        if aba_selecionada == "Ver Produtos":
            ClienteInterface.produto_listar()

        elif aba_selecionada == "Carrinho":
            ClienteInterface.meu_carrinho()

        elif aba_selecionada == "Meus Pedidos":
            ClienteInterface.ver_pedidos()
        
    #VER PRODUTOS E ADICIONAR AO CARRINHO
    @staticmethod
    def produto_listar()-> None:
        st.header("Produtos", divider="blue")
        try:
            with st.container(border=True):
                st.subheader("Produtos Disponiveis")
                listar_produtos = [p.to_dict() for p in ClienteView.listar_produtos()]
                st.caption("A partir de 5 unidades, voce ganha um desconto de 25%.")
                st.dataframe(
                        listar_produtos, 
                        column_config={
                            "Id": st.column_config.Column(alignment="left"),
                            "Nome": st.column_config.Column(alignment="left"),
                            "Preço": st.column_config.Column(alignment="left"),
                            "Estoque": st.column_config.Column(alignment="left"),
                            "idCategoria": st.column_config.Column(alignment="left"),
                            "Imagem": st.column_config.ImageColumn("Imagem", help="Prévia do produto"),
                    })

        except ValueError as erro:
            print(" ---- Erro ---->", erro)

        try:
            with st.container(border=True):
                    st.subheader("Adicionar produtos ao carrinho")
                    idProduto = st.number_input("Informe o ID do produto: ", min_value=1)
                    quantidade = st.number_input("Informe a quantidade: ", min_value=1)
                    if st.button("Adicionar ao Carrinho"):
                        try:
                            if ClienteView.inserir_produto_carrinho(st.session_state.id_cliente_logado, idProduto, quantidade):
                                st.success("Produto adicionado ao carrinho!")
                                time.sleep(2)
                                st.rerun()
                            else:
                                st.error("Produto não encontrado!")
                        except ValueError as erro:
                            print(" ---- Erro ---->", erro)
        except ValueError as erro:
            print(" ---- Erro ---->", erro)

    #VER CARRINHO E FINALIZAR COMPRA
    @staticmethod
    def meu_carrinho()-> None:
        st.header("Carrinho", divider="red")
        
        if ClienteView.visualizar_carrinho(st.session_state.id_cliente_logado): 
            with st.container(border=True):
                listar_carrinho = [c.to_dict() for c in ClienteView.visualizar_carrinho(st.session_state.id_cliente_logado)]
                st.dataframe(
                        listar_carrinho,
                        column_config={
                                "Quantidade": st.column_config.Column(alignment="left"),
                                "Preço": st.column_config.Column(alignment="left")
                            })
                total = ClienteView.total_carrinho_com_desconto(st.session_state.id_cliente_logado)
                st.success(f"Total a pagar: R$ {total:.2f}")

            col1, col2 = st.columns(2)

            with col1:
                if st.button("Limpar Carrinho", use_container_width=True, type="secondary"):
                    ClienteView.limpar_carrinho(st.session_state.id_cliente_logado)
                    st.success("Carrinho limpo!")
                    time.sleep(2)
                    st.rerun()
            with col2:
                if st.button("Confirmar Compra", use_container_width=True, type="primary"):
                        if ClienteView.comprar_carrinho(st.session_state.id_cliente_logado):
                            st.success("Compra realizada com sucesso!")
                            time.sleep(2)
                            st.rerun()
                        else:
                            st.error("Carrinho vazio!")
            

        else:
            st.info("Seu Carrinho esta vazio no momento!")
    
    @staticmethod
    def ver_pedidos()-> None:
        st.header("Historico de Compras", divider="green")
        try:   
            with st.container(border=True):
                listar_compras = [p.to_dict() for p in ClienteView.listar_compras(st.session_state.id_cliente_logado)]
                st.dataframe(
                        listar_compras,
                        column_config={
                                "ID Compra": st.column_config.Column(alignment="left"),
                                "Total": st.column_config.Column(alignment="left")
                            })

        except ValueError as erro:
            print(" ---- Erro ---->", erro)

    @staticmethod
    def sair() -> None:
        st.session_state.usuario_logado = False
        st.session_state.email_logado = None
        st.rerun()