import streamlit as st
from openai import AzureOpenAI

client = AzureOpenAI()

# openai.api_type = "azure"
# openai.api_version = "2023-07-01-preview"
# openai.api_base = os.environ['OPENAI_URI']
# # openai.api_base = "https://assistantai-dev-01.openai.azure.com/"
# openai.api_key = os.environ['OPENAI_KEY']
# # openai.api_key = "b39a619eb5994cbe898bfe5d74f6b536"

st.title("StreamlitのChatサンプル")

# 定数定義
USER_NAME = "user"
ASSISTANT_NAME = "assistant"
model="gpt-35-turbo"

def response_chatgpt(user_msg: str, chat_history: list = []):

    system_msg = """あなたはアシスタントです。"""
    messages=[
        {"role": "system", "content": system_msg}
    ]

    #チャットログがある場合は、チャットログをmessagesリストに追加
    if len(chat_history) > 0:
        for chat in chat_history:
            messages.append({"role": chat["name"], "content": chat["msg"]})
    #ユーザメッセージをmessagesリストに追加
    messages.append({"role": USER_NAME, "content": user_msg})

    print(" ■システムメッセージ: "  + system_msg)
    print(" ■ユーザメッセージ: " + user_msg)

    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0
    )
    return response


# チャットログを保存したセッション情報を初期化
if "chat_log" not in st.session_state:
    st.session_state.chat_log = []


user_msg = st.chat_input("ここにメッセージを入力")
if user_msg:
    # 以前のチャットログを表示
    for chat in st.session_state.chat_log:
        with st.chat_message(chat["name"]):
            st.write(chat["msg"])

    # 最新のユーザメッセージを表示
    with st.chat_message(USER_NAME):
        st.write(user_msg)

    # アシスタントのメッセージを表示
    response = response_chatgpt(user_msg, chat_history=st.session_state.chat_log)
    with st.chat_message(ASSISTANT_NAME):
        assistant_msg = response.choices[0].message.content
        assistant_response_area = st.empty()
        assistant_response_area.write(assistant_msg)

    # セッションにチャットログを追加
    st.session_state.chat_log.append({"name": USER_NAME, "msg": user_msg})
    st.session_state.chat_log.append({"name": ASSISTANT_NAME, "msg": assistant_msg})
    # チャットログを出力
    print(" ■チャットログ:")
    for chat in st.session_state.chat_log:
        print("  " + chat["name"] + ": " + chat["msg"])