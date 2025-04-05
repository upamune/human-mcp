import streamlit as st
import human_mcp.db_utils as db_utils

# データベースの初期化
db_utils.initialize_db()

def main():
    st.set_page_config(
        page_title="Human-MCP Operator Interface",
        page_icon="🧠",
        layout="wide"
    )

    st.title("🧠 Human-MCP Operator Interface")
    st.markdown("""
    このインターフェースは、AIアシスタントからの要求に対して人間が応答するためのものです。
    下に表示されるタスクに対して応答を入力し、「Submit Response」ボタンをクリックしてください。
    """)

    # リロードボタン
    if st.button("🔄 タスクを更新", type="primary"):
        st.rerun()

    # 保留中のタスクを取得
    pending_tasks = db_utils.get_pending_tasks()

    if not pending_tasks:
        st.info("📭 保留中のタスクはありません。")
    else:
        st.header(f"📋 保留中のタスク: {len(pending_tasks)}件")

        # 各タスクを処理
        for task_id, instruction in pending_tasks:
            st.markdown("---")
            st.subheader(f"タスクID: {task_id}")
            st.info(f"指示: {instruction}")

            # 応答入力フォーム
            response = st.text_area(
                "あなたの応答:",
                key=f"response_{task_id}",
                height=100
            )

            # 送信ボタン
            submit_button = st.button(
                "応答を送信",
                key=f"btn_{task_id}"
            )

            # ボタンが押され、かつ入力がある場合
            if submit_button and response:
                db_utils.update_task_result(task_id, response)
                st.success(f"タスク {task_id} の応答を送信しました！")
                st.rerun()

if __name__ == "__main__":
    main()
