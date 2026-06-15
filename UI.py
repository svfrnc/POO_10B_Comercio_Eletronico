import streamlit as st
from Visitante.View import View as LoginView
from Visitante.Login import LoginDAO
from Admin_UI import AdminUI
from Admin.View import View as AdminView
from Cliente_UI import ClienteInterface
import time


class UI:
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
        if "tela" not in st.session_state:
            st.session_state.tela = "login"

        if st.session_state.usuario_logado:
            if st.session_state.email_logado == "admin@gmail.com":
                AdminUI.main()
            else:
                ClienteInterface.main()
        else:
            st.header("DISCOOL VINIS E CDS", divider="orange")

            if not st.session_state.usuario_logado:
                        
                        # Verifica qual tela deve ser exibida baseada no nosso estado
                        if st.session_state.tela == "login":
                            UI.validacao() # Mostra o formulário de login
                            
                            # Botão para ir para o cadastro
                            if st.button("Não tem conta? Cadastre-se"):
                                st.session_state.tela = "cadastro" # Muda o destino
                                st.rerun() # Recarrega a página imediatamente
                        
                        else:
                            UI.criar_usuario() # Mostra o formulário de cadastro
                            
                            # Botão para voltar para o login
                            if st.button("Já tem uma conta? Faça Login"):
                                st.session_state.tela = "login" # Muda o destino de volta
                                st.rerun() # Recarrega a página imediatamente

        if st.session_state.usuario_logado:
            if st.session_state.email_logado == "admin@gmail.com":
                AdminUI.main()
            elif st.session_state.tipo_usuario == "Entregador":
                from Entregador_UI import EntregadorInterface
                EntregadorInterface.main()
            else:
                ClienteInterface.main()            
            


    
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
        with st.form("form_criar_conta"):
            tipo_perfil = st.radio("Cadastrar como:", ["Cliente", "Entregador"])
            nome: str = st.text_input("Informe o nome: ")
            # ... resto dos inputs ...
            submit: bool = st.form_submit_button("Criar Conta")
        
        if submit:
            if tipo_perfil == "Cliente":
                AdminView.cliente_inserir(nome, email, senha, fone)
            else:
                AdminView.entregador_inserir(nome, email, senha, fone)
            st.success("Conta criada com sucesso! Faça login agora.")
            time.sleep(2)
            st.session_state.tela = "login"
            st.rerun()

    #VALIDAÇÃO DE USUÁRIO
    @staticmethod
    def validacao() -> None:
        st.subheader("Forneça seu email e senha para logar no sistema: ")
        with st.form("form_logar"):
            tipo_login = st.radio("Entrar como:", ["Cliente / Admin", "Entregador"])
            email: str = st.text_input("Email: ")
            senha: str = st.text_input("Senha: ", type="password")
            button: bool = st.form_submit_button("Confirmar")

        if button:
            if tipo_login == "Cliente / Admin":
                if (email == "admin@gmail.com") and (senha == "1234"):
                    st.success("Admin logado com sucesso!")
                    st.session_state.usuario_logado = True
                    st.session_state.email_logado = email
                    st.session_state.tipo_usuario = "Admin"
                    st.session_state.nome_cliente_logado = "Admin"
                    st.rerun()
                elif LoginView.login(email, senha):
                    st.success("Login realizado com sucesso!")
                    st.session_state.usuario_logado = True
                    st.session_state.email_logado = email
                    st.session_state.tipo_usuario = "Cliente"
                    st.session_state.id_cliente_logado = LoginDAO.idCliente_logado
                    st.session_state.nome_cliente_logado = LoginDAO.nome_logado
                    st.rerun()
                else:
                    st.error("Email e/ou senha incorretos!")
            else:
                if LoginDAO.logado_entregador(email, senha):
                    st.success("Entregador logado!")
                    st.session_state.usuario_logado = True
                    st.session_state.email_logado = email
                    st.session_state.tipo_usuario = "Entregador"
                    st.session_state.id_entregador_logado = LoginDAO.idEntregador_logado
                    st.session_state.nome_cliente_logado = LoginDAO.nome_logado
                    st.rerun()
                else:
                    st.error("Credenciais de entregador inválidas!")
UI.home()