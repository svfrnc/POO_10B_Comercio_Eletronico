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
                icons = ["box-seam", "cart" , "currency-dollar" , "file-earmark-text"],
                default_index = 0,
                key = "cliente_menu"
            )
            button_sair: bool = st.button("Sair", type="primary")
            if button_sair:
                ClienteInterface.sair()

        if aba_selecionada == "Produtos":
            ClienteInterface.produto_listar()

        elif aba_selecionada == "Meu Carrinho":
            ClienteInterface.meu_carrinho()

        elif aba_selecionada == "Meus Pedidos":
            ClienteInterface.ver_pedidos()
        
 # VER PRODUTOS EM FORMATO DE CARDS COM RECORTE DE PROMOÇÃO GERAL
    @staticmethod
    def produto_listar() -> None:
        import base64
        from Admin.View import View as AdminView

        st.header("Produtos", divider="blue")
        
        # 1. Verifica se há uma promoção geral ativa neste momento
        promo_ativa = AdminView.obter_promocao_ativa()
        if promo_ativa:
            st.warning(f"🔥 PROMOÇÃO DISCOOL: Tudo com {promo_ativa.percentual_desconto}% de desconto direto na vitrine!")
        else:
            st.caption("A partir de 5 unidades do mesmo produto, você ganha 25% de desconto.")

        try:
            produtos = ClienteView.listar_produtos()
            if not produtos:
                st.info("Nenhum produto cadastrado no catálogo.")
                return

            colunas_por_linha = 3
            for i in range(0, len(produtos), colunas_por_linha):
                grupo_produtos = produtos[i : i + colunas_por_linha]
                colunas = st.columns(colunas_por_linha)

                for col, produto in zip(colunas, grupo_produtos):
                    with col:
                        with st.container(border=True):
                            # Renderização da imagem em bytes salvos no JSON
                            if produto.imagem:
                                try:
                                    img_bytes = base64.b64decode(produto.imagem)
                                    st.image(img_bytes, use_container_width=True)
                                except Exception:
                                    st.image("https://via.placeholder.com/150", use_container_width=True)
                            else:
                                st.image("https://via.placeholder.com/150", use_container_width=True)

                            st.subheader(produto.descricao)
                            
                            # 2. Lógica Visual de Preço: Normal vs Promocional
                            if promo_ativa:
                                preco_desconto = produto.preco * (1 - promo_ativa.percentual_desconto / 100)
                                st.write(f"❌ De: ~~R$ {produto.preco:.2f}~~")
                                st.write(f"✅ **Por: R$ {preco_desconto:.2f}**")
                            else:
                                st.write(f"💰 **Preço:** R$ {produto.preco:.2f}")
                            
                            if produto.estoque > 0:
                                st.write(f"📦 *Estoque:* {produto.estoque} un.")
                                quantidade = st.number_input(
                                    "Quantidade:", min_value=1, max_value=produto.estoque, value=1, key=f"qtd_{produto.id}"
                                )

                                if st.button("Adicionar ao Carrinho", key=f"btn_{produto.id}", use_container_width=True, type="primary"):
                                    if ClienteView.inserir_produto_carrinho(st.session_state.id_cliente_logado, produto.id, quantidade):
                                        st.success("Adicionado!")
                                        time.sleep(1)
                                        st.rerun()
                                    else:
                                        st.error("Erro ao adicionar.")
                            else:
                                st.error("Produto Esgotado")
        except Exception as erro:
            st.error("Erro ao renderizar catálogo.")

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