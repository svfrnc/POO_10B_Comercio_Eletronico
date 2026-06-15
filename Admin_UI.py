from Admin.View import View as AdminView
import streamlit as st
from streamlit_option_menu import option_menu
import time
import base64

class AdminUI:
    #TELA DE ACESSO DO ADMIN
    @staticmethod
    def main() -> None:

        st.session_state.email_logado
        st.session_state.nome_cliente_logado

        with st.sidebar:
            st.info(f"Bem vindo, Admin")


            aba_selecionada = option_menu(
                menu_title = "Painel Admin",
                options = ["Clientes", "Categorias", "Produtos", "Promoções", "Entregas"],
                icons = ["people", "tags", "box-seam", "percent", "truck"],
                default_index = 0,
                key = "admin_menu"
            )
            button_sair: bool = st.button("Sair", type="primary")
            if button_sair:
                AdminUI.sair()

        if aba_selecionada == "Clientes":
            st.header("Gerenciamento de Clientes", divider="red")
            aba1, aba2, aba3 = st.tabs(["Inserir Cliente", "Atualizar Cliente","Excluir Cliente"])

            with aba1:
                AdminUI.cliente_inserir()
            with aba2:
                AdminUI.cliente_atualizar()
            with aba3:
                AdminUI.cliente_excluir()

        if aba_selecionada == "Categorias":
            st.header("Gerenciamento de Categorias", divider="red")
            aba1, aba2, aba3 = st.tabs(["Inserir Categoria", "Atualizar Categoiria", "Excluir Categoria"])

            with aba1:
                AdminUI.categoria_inserir()
            with aba2:
                AdminUI.categoria_atualizar()
            with aba3:
                AdminUI.categoria_excluir()

        if aba_selecionada == "Produtos":
            st.header("Gerenciamento de Produtos", divider="red")
            aba1, aba2, aba3, aba4 = st.tabs(["Inserir Produto", "Atualizar Produto", "Excluir Produto", "Reajuste Geral de Preços"])

            with aba1:
                AdminUI.produto_inserir()
            with aba2:
                AdminUI.produto_atualizar()
            with aba3:
                AdminUI.produto_excluir()
            with aba4:
                AdminUI.produto_alterar_preco_geral()

        if aba_selecionada == "Promoções":
            st.header("Gerenciamento de Promoções Gerais", divider="red")
            aba1, aba2 = st.tabs(["Criar Período Promocional", "Listar / Excluir Promoções"])
            with aba1:
                AdminUI.promocao_inserir()
            with aba2:
                AdminUI.promocao_gerenciar()
        
        if aba_selecionada == "Entregas":
            AdminUI.alocar_entregas()

    @staticmethod
    def sair() -> None:
        st.session_state.usuario_logado = False
        st.session_state.email_logado = None
        st.rerun()

#CLIENTE POR ADMIN
    @staticmethod
    def cliente_inserir() -> None:
        try:   
            with st.form("form_inserir_cliente"):
                st.subheader("Cadastro de Clientes")
                nome: str = st.text_input("Informe o nome: ")
                email: str = st.text_input("Informe o e-mail: ")
                senha: str = st.text_input("Informe a senha: ")
                fone: str = st.text_input("Informe o fone: ")

                submit: bool = st.form_submit_button("Inserir Cliente", type="secondary")
        
            if submit:
                AdminView.cliente_inserir(nome, email, senha, fone)
                st.success("Cliente inserido com sucesso!")
                time.sleep(2)
                st.rerun()
        except ValueError as erro:
            print(" ---- Erro ---->", erro)

    @staticmethod
    def cliente_listar() -> None:
        with st.container(border=True):
            st.subheader("Listagem de Clientes")
            for c in AdminView.cliente_listar():
                st.text(c)

    @staticmethod
    def cliente_atualizar() -> None:
        try:
            with st.form("form_atualizar_cliente"):
                lista_clientes = [p.to_dict() for p in AdminView.cliente_listar()]
                st.dataframe(
                    lista_clientes,
                    column_config={
                        "Id": st.column_config.Column(alignment="left"),
                        "Nome": st.column_config.Column(alignment="left"),
                        "Email": st.column_config.Column(alignment="left"),
                        "Telefone": st.column_config.Column(alignment="left"),
                    })
                    
                st.subheader("Atualização de Cliente")
                id_str: str = st.text_input("Qual o id do cliente a ser atualizado: ", value=1) or ''
                id: int = int(id_str) if id_str.isdigit() else 0
                nome: str = st.text_input("Informe o novo nome: ")
                email: str = st.text_input("Informe o novo e-mail: ")
                senha: str = st.text_input("Informe a nova senha: ")
                fone: str = st.text_input("Informe o novo fone: ")
                submit: bool = st.form_submit_button("Atualizar Cliente", type="secondary")

            if submit:
                AdminView.cliente_atualizar(id, nome, email, senha, fone)
                st.success("Cliente atualizado com sucesso!")
                time.sleep(2)
                st.rerun()
        except ValueError as erro:
            print(" ---- Erro ---->", erro)

    @staticmethod
    def cliente_excluir() -> None:
        try:
            with st.form("form_excluir_cliente"):
                lista_clientes = [p.to_dict() for p in AdminView.cliente_listar()]
                st.dataframe(
                    lista_clientes,
                    column_config={
                        "Id": st.column_config.Column(alignment="left"),
                        "Nome": st.column_config.Column(alignment="left"),
                        "Email": st.column_config.Column(alignment="left"),
                        "Telefone": st.column_config.Column(alignment="left"),
                    })
                st.subheader("Exclusão de Cliente")
                id_str: str = st.text_input("Qual o id do cliente a ser excluído: ", value=1) or ''
                id: int = int(id_str) if id_str.isdigit() else 0
                submit: bool = st.form_submit_button("Excluir cliente", type="secondary")         

            if submit:
                AdminView.cliente_excluir(id)
                st.success("Cliente excluído com sucesso!")
                time.sleep(2)
                st.rerun()
        except ValueError as erro:
            print(" ---- Erro ---->", erro)

#CATEGORIA POR ADMIN
    @staticmethod
    def categoria_inserir() -> None:
        try:
            with st.form("form_inserir_categoria"):
                st.subheader("Cadastro de Categorias")
                desc: str = st.text_input("Informe o nome da nova descrição: ")

                submit: bool = st.form_submit_button("Inserir Categoria", type="secondary")

            if submit:
                AdminView.categoria_inserir(desc)
                st.success("Categoria inserida com sucesso!")
                time.sleep(2)
                st.rerun()
        except ValueError as erro:
            print(" ---- Erro ---->", erro)

    @staticmethod
    def categoria_listar() -> None:
        try:
            with st.container(border=True):
                st.subheader("Listagem de Categorias")
                for c in AdminView.categoria_listar():
                    st.text(c)
        except ValueError as erro:
            print(" ---- Erro ---->", erro)

    @staticmethod
    def categoria_atualizar() -> None:
        try:
            with st.form("form_atualizar_categoria"):
                listr_categorias = [p.to_dict() for p in AdminView.categoria_listar()]
                st.dataframe(
                    listr_categorias,
                    column_config={
                        "Id": st.column_config.Column(alignment="left")
                    })

                st.subheader("Atualização de Cliente")

                id_str: str = st.text_input("Qual o id da categoria a ser atualizado: ", value=1) or ''
                id: int = int(id_str) if id_str.isdigit() else 0

                desc: str = st.text_input("Informe a nova descrição: ")
                submit: bool = st.form_submit_button("Atualizar categoria", type="secondary")

            if submit:
                AdminView.categoria_atualizar(id, desc)
                st.success("Categoria atualizada com sucesso!")
                time.sleep(2)
                st.rerun()
        except ValueError as erro:
            print(" ---- Erro ---->", erro)        

    @staticmethod
    def categoria_excluir() -> None:
        try:
            with st.form("form_excluir_categoria"):
                listr_categorias = [p.to_dict() for p in AdminView.categoria_listar()]
                st.dataframe(
                    listr_categorias,
                    column_config={
                        "Id": st.column_config.Column(alignment="left")
                    })
                st.subheader("Exclusão de Categoria")

                id_str = st.text_input("Qual o id da categoria a ser excluído: ", value=1) or ''
                id = int(id_str) if id_str.isdigit() else 0

                submit: bool = st.form_submit_button("Excluir categoria", type="secondary")

            if submit:
                AdminView.categoria_excluir(id)
                st.success("Categoria excluída com sucesso!")
                time.sleep(2)
                st.rerun()
        except ValueError as erro:
            print(" ---- Erro ---->", erro)

# PRODUTO POR ADMIN
    @staticmethod
    def produto_inserir() -> None:
        try:
            with st.form("form_inserir_produto"):
                st.subheader("Cadastro de Produtos")
                descricao: str = st.text_input("Informe a descrição: ")

                preco_str: str = st.text_input("Informe o preço: ", value=1.0) or ''
                try:
                    preco: float = float(preco_str.replace(",", "."))
                except ValueError:
                    preco = 0.0

                estoque_str: str = st.text_input("Informe a quantidade em estoque: ", value=1) or ''
                estoque = int(estoque_str) if estoque_str.isdigit() else 0

                idCategoria_str: str = st.text_input("Insira a categoria do produto: ", value=1) or ''
                idCategoria = int(idCategoria_str) if idCategoria_str.isdigit() else 0

                imagem_arquivo = st.file_uploader("Selecione a imagem do produto", type=['png', 'jpg', 'jpeg'])
            
                submit: bool = st.form_submit_button("Inserir produto", type="secondary")
                
            if submit:
                imagem_base64: str = ''

                if imagem_arquivo is not None:
                    bytes_data = imagem_arquivo.getvalue()
                    imagem_base64 = base64.b64encode(bytes_data).decode("utf-8")

                AdminView.produto_inserir(descricao, preco, estoque, idCategoria, imagem_base64)
                st.success("Produto inserido com sucesso!")
                time.sleep(2)
                st.rerun()
        except ValueError as erro:
            print(" ---- Erro ---->", erro)
            
    @staticmethod
    def produto_listar() -> None:
        try:

            with st.container(border=True):
                st.subheader("Listagem de Produtos")
                for p in AdminView.produto_listar():
                    st.text(p)
        except ValueError as erro:
            print(" ---- Erro ---->", erro)
            
    @staticmethod
    def produto_atualizar() -> None:
        try:
            with st.form("form_atualizar_produto"):
                listar_produtos = [p.to_dict() for p in AdminView.produto_listar()] 
                st.dataframe(
                        listar_produtos,
                        column_config={
                            "Id": st.column_config.Column(alignment="left"),
                            "Nome": st.column_config.Column(alignment="left"),
                            "Preço": st.column_config.Column(alignment="left"),
                            "Estoque": st.column_config.Column(alignment="left"),
                            "idCategoria": st.column_config.Column(alignment="left"),
                            "Imagem": st.column_config.ImageColumn("Imagem", help="Prévia do produto", width="small")
                    })
                st.subheader("Atualização de Produto")

                id_str: str = st.text_input("Insira o id do produto a ser atualizado: ", value="") or ''
                id: int = int(id_str) if id_str.isdigit() else 0

                # Removemos os placeholders numéricos para que fiquem vazios por padrão se não modificados
                descricao: str = st.text_input("Insira a nova descrição (deixe em branco para manter a atual): ")

                preco_str: str = st.text_input("Insira o novo preço (deixe em branco para manter o atual): ") or ''
                preco = float(preco_str.replace(",", ".")) if preco_str else None

                estoque_str: str = st.text_input("Insira a nova quantidade em estoque (deixe em branco para manter a atual): ") or ''   
                estoque = int(estoque_str) if estoque_str.isdigit() else None

                idCategoria_str: str = st.text_input("Insira o id da nova categoria (deixe em branco para manter a atual): ") or ''
                idCategoria = int(idCategoria_str) if idCategoria_str.isdigit() else None

                image_arquivo = st.file_uploader("Selecione a nova imagem do produto (deixe em branco para manter a atual)", type=['png', 'jpg', 'jpeg'])

                submit: bool = st.form_submit_button("Atualizar produto", type="secondary")

            if submit:
                image_base64 = ''
                if image_arquivo is not None:
                    bytes_data = image_arquivo.getvalue()
                    image_base64 = base64.b64encode(bytes_data).decode("utf-8")

                # Passa as variáveis (que agora podem ser None se não preenchidas) para a View
                AdminView.produto_atualizar(id, descricao, preco, estoque, idCategoria, image_base64)
                st.success("Produto atualizado com sucesso!")
                time.sleep(2)
                st.rerun()
        except ValueError as erro:
            print(" ---- Erro ---->", erro)


    @staticmethod
    def produto_excluir() -> None:
        try:

            with st.form("form_excluir_produto"):
                listar_produtos = [p.to_dict() for p in AdminView.produto_listar()] 
                st.dataframe(
                        listar_produtos,
                        use_container_width=True,
                        column_config={
                            "Id": st.column_config.Column(alignment="left"),
                            "Nome": st.column_config.Column(alignment="left"),
                            "Preço": st.column_config.Column(alignment="left"),
                            "Estoque": st.column_config.Column(alignment="left"),
                            "idCategoria": st.column_config.Column(alignment="left"),
                            "Imagem": st.column_config.ImageColumn("Imagem", help="Prévia do produto", width="small")
                    })
                st.subheader("Exclusão de Produto")

                id_str: str = st.text_input("Insira o id do produto a ser excluído: ", value=1) or ''
                id = int(id_str) if id_str.isdigit else 0
            
                submit: bool = st.form_submit_button("Excluir produto", type="secondary")

            if submit:
                AdminView.produto_excluir(id)
                st.success("Produto excluído com sucesso!")
                time.sleep(2)
                st.rerun()
        except ValueError as erro:
            print(" ---- Erro ---->", erro)

    @staticmethod
    def produto_alterar_preco_geral() -> None:
        try:

            with st.form("form_alterar_preco_produtos"):
                listar_produtos = [p.to_dict() for p in AdminView.produto_listar()] 
                st.dataframe(
                        listar_produtos,
                        column_config={
                            "Id": st.column_config.Column(alignment="left"),
                            "Nome": st.column_config.Column(alignment="left"),
                            "Preço": st.column_config.Column(alignment="left"),
                            "Estoque": st.column_config.Column(alignment="left"),
                            "idCategoria": st.column_config.Column(alignment="left"),
                            "Imagem": st.column_config.ImageColumn("Imagem", help="Prévia do produto", width="small")

                    })
                st.subheader("Alteração permanente de Preços")

                st.info("⚠️ Atenção: Esta operação modifica o preço base dos produtos de forma definitiva no banco de dados.")

                percentual_str: str = st.text_input("Insira o percentual de alteracao (ex: 10 para +10%, -5 para -5%): ", value=1.0) or ''
                try:
                    percentual = float(percentual_str.replace(",", "."))
                except ValueError:
                    percentual = 0.0

                submit: bool = st.form_submit_button("Alterar preços", type="secondary")

            if submit:
                AdminView.produto_alterar_preco_geral(percentual)
                st.success("Precos alterados com sucesso!")
                time.sleep(2)
                st.rerun()
        except ValueError as erro:
            print(" ---- Erro ---->", erro)

    @staticmethod
    def promocao_inserir() -> None:
        from datetime import datetime, time
        try:
            with st.form("form_inserir_promocao"):
                st.subheader("Configurar Novo Período")
                
                col1, col2 = st.columns(2)
                with col1:
                    d_inicio = st.date_input("Data de Início")
                    t_inicio = st.time_input("Horário de Início", time(0, 0))
                with col2:
                    d_fim = st.date_input("Data de Fim")
                    t_fim = st.time_input("Horário de Fim", time(23, 59))
                    
                percentual = st.number_input("Percentual de Desconto (%)", min_value=0.0, max_value=100.0, value=10.0, step=1.0)
                submit = st.form_submit_button("Ativar Período Promocional", type="primary")
                
            if submit:
                dt_inicio = datetime.combine(d_inicio, t_inicio)
                dt_fim = datetime.combine(d_fim, t_fim)
                
                if dt_fim <= dt_inicio:
                    st.error("A data de término deve ser estritamente posterior à data de início!")
                else:
                    AdminView.promocao_inserir(dt_inicio, dt_fim, percentual)
                    st.success("Período promocional registrado com sucesso!")
                    time.sleep(1.5)
                    st.rerun()
        except Exception as erro:
            st.error(f"Erro ao inserir período promocional.")

    @staticmethod
    def promocao_gerenciar() -> None:
        try:
            promocoes = AdminView.promocao_listar()
            if not promocoes:
                st.info("Nenhum período promocional cadastrado até o momento.")
                return
                
            lista_promos = [p.to_dict() for p in promocoes]
            st.dataframe(lista_promos, use_container_width=True)
            
            with st.form("form_excluir_promocao"):
                st.subheader("Remover Período Promocional")
                id_promo = st.number_input("Informe o ID da promoção a ser excluída:", min_value=1, step=1)
                submit = st.form_submit_button("Excluir Promoção", type="secondary")
                
            if submit:
                AdminView.promocao_excluir(id_promo)
                st.success("Promoção removida com sucesso!")
                time.sleep(1.5)
                st.rerun()
        except Exception as erro:
            st.error(f"Erro ao gerenciar promoções.")
    
    @staticmethod
    def alocar_entregas() -> None:
        st.header("Gerenciamento Logístico", divider="red")
        try:
            entregas = AdminView.entrega_listar()
            entregadores = AdminView.entregador_listar()

            if not entregas:
                st.info("Nenhuma entrega registrada.")
                return

            st.subheader("Status Geral das Entregas")
            st.dataframe([e.to_dict() for e in entregas], use_container_width=True)

            entregas_pendentes = [e for e in entregas if e.status == "Aguardando Entregador"]
            if not entregas_pendentes:
                st.success("Todas as entregas já foram distribuídas!")
                return

            if not entregadores:
                st.warning("Cadastre entregadores no sistema para realizar a alocação.")
                return

            with st.form("form_alocacao"):
                st.subheader("Vincular Entregador ao Pedido")
                id_ent = st.selectbox("Selecione a Entrega (ID):", [e.id for e in entregas_pendentes])
                dict_motocas = {e.nome: e.id for e in entregadores}
                nome_motoca = st.selectbox("Selecione o Entregador:", list(dict_motocas.keys()))
                sub = st.form_submit_button("Confirmar Envio", type="primary")

            if sub:
                id_moto = dict_motocas[nome_motoca]
                if AdminView.entrega_alocar(id_ent, id_moto):
                    st.success("Entregador alocado e pedido atualizado para 'Em trânsito'!")
                    time.sleep(1.5)
                    st.rerun()
        except Exception as e:
            st.error("Erro no controle de entregas.")