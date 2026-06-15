import streamlit as st
import time
from Admin.View import View as AdminView

class EntregadorInterface:
    @staticmethod
    def main() -> None:
        st.title("🚚 Painel de Distribuição do Entregador")
        st.info(f"Logado como: {st.session_state.nome_cliente_logado}")

        if st.button("Sair", type="primary"):
            st.session_state.usuario_logado = False
            st.session_state.email_logado = None
            st.session_state.tipo_usuario = None
            st.rerun()

        st.header("Minhas Rotas Designadas", divider="orange")
        try:
            todas = AdminView.entrega_listar()
            minhas = [e for e in todas if e.idEntregador == st.session_state.id_entregador_logado]

            if not minhas:
                st.info("Você não possui entregas alocadas no momento.")
                return

            st.dataframe([e.to_dict() for e in minhas], use_container_width=True)

            ativas = [e for e in minhas if e.status != "Entregue"]
            if not ativas:
                st.success("Excelente trabalho! Todas as suas entregas foram concluídas.")
                return

            with st.form("form_status_entrega"):
                st.subheader("Atualizar Progresso de Entrega")
                id_e = st.selectbox("ID da Entrega:", [e.id for e in ativas])
                novo_st = st.selectbox("Mudar Status para:", ["Em trânsito", "Entregue"])
                sub = st.form_submit_button("Salvar Progresso", type="primary")

            if sub:
                if AdminView.entrega_atualizar_status(id_e, novo_st):
                    st.success("Status atualizado com sucesso!")
                    time.sleep(1.5)
                    st.rerun()
        except Exception as e:
            st.error("Erro ao processar painel de entregas.")