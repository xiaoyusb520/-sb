import json
import os
import streamlit as st   # 这是导入做网页的工具箱
from openai import OpenAI
# 聊天记录存到这个文件里
HISTORY_FILE = "chat_history.json"
def load_history():
    """如果存在历史记录文件，就读取它；否则返回None"""
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return None

def save_history(messages):
    """把聊天记录保存到文件"""
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(messages, f, ensure_ascii=False, indent=2)
# ---------- 请替换成你的密钥 ----------
api_key=st.secrets["SILICONFLOW_KEY"]  # 替换成 sk-xxx
# ------------------------------------

st.set_page_config(page_title="AI导师", page_icon="🤖")
st.title("🤖 xiaoyu")
# 侧边栏设置
with st.sidebar:
    st.header("⚙️ 设置")
    enable_search = st.checkbox("🔍 开启联网搜索", value=False)
    st.caption("开启后，AI能回答2026年的最新事件")

client = OpenAI(api_key="sk-geymrnipsboxsuwjhmblrjfuetxgupgdmqmofwfkiozoqgax", base_url="https://api.siliconflow.cn/v1")


# 初始化聊天记录：优先从文件加载，如果文件不存在则用默认提示词
if "messages" not in st.session_state:
    loaded = load_history()
    if loaded:
        st.session_state.messages = loaded
    else:
        st.session_state.messages = [
            {"role": "system", "content": "你是DeepSeek-V3，一个知识渊博且风趣的AI助手。"}
        ]

for msg in st.session_state.messages:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

if prompt := st.chat_input("想问点什么？"):
    with st.chat_message("user"):
        st.write(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    save_history(st.session_state.messages)

    with st.chat_message("assistant"):
        with st.spinner("思考中..."):
            response = client.chat.completions.create(
                model="deepseek-ai/DeepSeek-V3",  # 用最稳的模型，确保不卡
                messages=st.session_state.messages
            )
            reply = response.choices[0].message.content
            st.write(reply)
            st.session_state.messages.append({"role": "assistant", "content": reply})
            save_history(st.session_state.messages)
            