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
            st.info(f"Bem Vindo, {st.session_state.nome_cliente_logado}!")

            aba_selecionada = option_menu(
                menu_title = "Painel do usuário",
                options = ["Produtos", "Meu Carrinho", "Meus Pedidos"],
                icons = ["box-seam", "carshopping_cart", "dollar", "receipt"],
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
 # VER PRODUTOS E ADICIONAR AO CARRINHO (MODELO EM CARDS)
    @staticmethod
    def produto_listar() -> None:
        import base64  # Necessário para decodificar a string da imagem salvada no JSON

        st.header("💽 Produtos", divider="blue")
        st.caption("Veja aqui os ultimos lançamentos e produtos adicionados a loja.")

        try:
            # Obtém a lista de instâncias de objetos diretamente da View
            produtos = ClienteView.listar_produtos()

            if not produtos:
                st.info("Nenhum produto disponível no momento.")
                return

            # Configuração do número de colunas por linha na vitrine
            colunas_por_linha = 3
            
            # Loop que divide os produtos em grupos do tamanho estipulado
            for i in range(0, len(produtos), colunas_por_linha):
                grupo_produtos = produtos[i : i + colunas_por_linha]
                colunas = st.columns(colunas_por_linha)

                for col, produto in zip(colunas, grupo_produtos):
                    with col:
                        # O container com borda cria o efeito visual de 'Card'
                        with st.container(border=True):
                            
                            # 1. Renderização da Imagem do Produto
                            if produto.imagem:
                                try:
                                    img_bytes = base64.b64decode(produto.imagem)
                                    st.image(img_bytes, use_container_width=True)
                                except Exception:
                                    # Caso haja falha na string base64, exibe um placeholder
                                    st.image("https://via.placeholder.com/150", caption="Erro ao carregar imagem", use_container_width=True)
                            else:
                                st.image("https://via.placeholder.com/150", caption="Sem imagem", use_container_width=True)

                            # 2. Informações do Produto (Acessadas diretamente por POO)
                            st.subheader(produto.descricao)
                            st.write(f"**Preço:** R$ {produto.preco:.2f}")
                            
                            if produto.estoque > 0:
                                st.write(f"📦 *Estoque:* {produto.estoque} un.")
                                
                                # 3. Seletor de Quantidade interno ao Card
                                quantidade = st.number_input(
                                    "Quantidade:",
                                    min_value=1,
                                    max_value=produto.estoque,
                                    value=1,
                                    key=f"qtd_{produto.id}"  # Chave única obrigatória
                                )

                                # 4. Botão de Compra Dedicado
                                if st.button("🛒 Adicionar ao Carrinho", key=f"btn_{produto.id}", use_container_width=True, type="primary"):
                                    if ClienteView.inserir_produto_carrinho(st.session_state.id_cliente_logado, produto.id, quantidade):
                                        st.success(f"Adicionado!")
                                        time.sleep(1)
                                        st.rerun()
                                    else:
                                        st.error("Erro ao adicionar produto.")
                            else:
                                st.error("Produto Esgotado")

        except Exception as erro:
            st.error(f"Erro ao carregar a vitrine de produtos.")
            print(" ---- Erro Interno ---->", erro)

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
                if st.button("🛒 Limpar Carrinho", use_container_width=True, type="secondary"):
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