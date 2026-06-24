import streamlit as st   # 这是导入做网页的工具箱
from openai import OpenAI

# ---------- 请替换成你的密钥 ----------
SILICONFLOW_KEY = "sk-geymrnipsboxsuwjhmblrjfuetxgupgdmqmofwfkiozoqgax"  # 替换成 sk-xxx
# ------------------------------------

st.set_page_config(page_title="AI导师", page_icon="🤖")
st.title("🐟小鱼的")

client = OpenAI(api_key=SILICONFLOW_KEY, base_url="https://api.siliconflow.cn/v1")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "你是一个风趣的Python导师，用通俗易懂的方式回答问题"}
    ]

for msg in st.session_state.messages:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

if prompt := st.chat_input("想问点什么？"):
    with st.chat_message("user"):
        st.write(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        with st.spinner("思考中..."):
            response = client.chat.completions.create(
                model="deepseek-ai/DeepSeek-V3",  # 用最稳的模型，确保不卡
                messages=st.session_state.messages
            )
            reply = response.choices[0].message.content
            st.write(reply)
            st.session_state.messages.append({"role": "assistant", "content": reply})
