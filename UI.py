import streamlit as st
from Visitante.View import View as LoginView
from Visitante.Login import LoginDAO
from Admin_UI import AdminUI
from Admin.View import View as AdminView
from Cliente_UI import ClienteInterface
import time


class UI:
    #CRIAÇÃO DE CONTA OU LOGIN
    @staticmethod
    def home() -> None:

        if "usuario_logado" not in st.session_state:
            st.session_state.usuario_logado = False
        if "email_logado" not in st.session_state:
            st.session_state.email_logado = None
        if "tipo_usuario" not in st.session_state:
            st.session_state.tipo_usuario = None
        if "id_cliente_logado" not in st.session_state:
            st.session_state.id_cliente_logado = None
        if "nome_cliente_logado" not in st.session_state:
            st.session_state.nome_cliente_logado = None

        if st.session_state.usuario_logado:
            if st.session_state.email_logado == "admin@gmail.com":
                AdminUI.main()
            else:
                ClienteInterface.main()
        else:
            st.header("Sistema ECommerce - Cantina Santa Clara", divider="red")

            if not st.session_state.usuario_logado:
                aba1, aba2 = st.tabs(["Criar Conta", "Fazer Login"])
                with aba1:
                    UI.criar_usuario()
                with aba2:
                    UI.validacao()
            


    
    #CRIANDO USUARIO
    @staticmethod
    def criar_usuario() -> None:                           
        st.subheader("Cadastro de Clientes")
        with st.form("form_criar_conta"):
            nome: str = st.text_input("Informe o nome: ")
            email: str = st.text_input("Informe o e-mail: ")
            senha: str = st.text_input("Informe a senha: ", type="password")
            fone: str = st.text_input("Informe o fone: ")

            submit: bool = st.form_submit_button("Criar Conta")
        
        if submit:
            AdminView.cliente_inserir(nome, email, senha, fone)
            st.success("Conta criada com sucesso! Faça login agora.")
            time.sleep(2)
            st.rerun()

    #VALIDAÇÃO DE USUÁRIO
    @staticmethod
    def validacao() -> None:
        st.subheader("Forneça seu email e senha para logar no sistema: ")
        with st.form("form_logar"):
            email: str = st.text_input("Email: ")
            senha: str = st.text_input("Senha: ", type="password")

            button: bool = st.form_submit_button("Confirmar", type="secondary")


        if button:
            if (email == "admin@gmail.com") and (senha == "9999"):
                st.success("Admin logado com sucesso!")
                st.session_state.usuario_logado = True #estado atualizado
                st.session_state.email_logado = email
                st.session_state.nome_cliente_logado = LoginDAO.nome_logado
                st.rerun()

            elif LoginView.login(email, senha): #retorna o bool da função para cliente
                st.success("Login realizado com sucesso!")
                st.session_state.usuario_logado = True
                st.session_state.email_logado = email
                st.session_state.id_cliente_logado = LoginDAO.idCliente_logado
                st.session_state.nome_cliente_logado = LoginDAO.nome_logado
                st.rerun()

            else:
                st.error("Email e/ou senha incorretos!")

UI.home()