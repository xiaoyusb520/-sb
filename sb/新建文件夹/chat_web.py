import json
import os
import streamlit as st
from openai import OpenAI

# ---------- 密钥配置 ----------
# 如果在云端运行，从 st.secrets 读取；本地运行时请确保有 .streamlit/secrets.toml
try:
    SILICONFLOW_KEY = st.secrets["SILICONFLOW_KEY"]
except:
    SILICONFLOW_KEY = "sk-wylxodzacvexkvoidpbqjsegqxguwsslemffcjiyuoltkdlb"  # 本地测试时可临时写死
# -----------------------------

# 聊天记录存储文件
HISTORY_FILE = "chat_history.json"

def load_history():
    """从文件加载聊天记录，如果文件不存在则返回 None"""
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return None

def save_history(messages):
    """将聊天记录保存到文件"""
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(messages, f, ensure_ascii=False, indent=2)

# ---------- 页面设置 ----------
st.set_page_config(page_title="极速AI导师", page_icon="⚡")
st.title("🐟小鱼sb的ai)")

# ---------- 侧边栏 ----------
with st.sidebar:
    st.header("⚙️ 设置")
    enable_search = st.checkbox("🔍 开启联网搜索", value=False)
    st.caption("开启后，AI能回答2026年的最新事件")
    
    # 清空对话按钮
    if st.button("🗑️ 清空对话"):
        st.session_state.messages = [{"role": "system", "content": "你是DeepSeek-V3，一个知识渊博且风趣的AI助手。"}]
        save_history(st.session_state.messages)
        st.rerun()

# ---------- 初始化聊天记录（优先从文件加载） ----------
if "messages" not in st.session_state:
    loaded = load_history()
    if loaded:
        st.session_state.messages = loaded
    else:
        st.session_state.messages = [
            {"role": "system", "content": "你是DeepSeek-V3，一个知识渊博且风趣的AI助手。"}
        ]

# ---------- 显示历史消息 ----------
for msg in st.session_state.messages:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

# ---------- 输入框与回复 ----------
if prompt := st.chat_input("试试问我点有深度的问题..."):
    # 显示用户消息
    with st.chat_message("user"):
        st.write(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    save_history(st.session_state.messages)   # 立即保存

    # 调用 AI（流式）
    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_response = ""
        client = OpenAI(
    api_key="sk-wylxodzacvexkvoidpbqjsegqxguwsslemffcjiyuoltkdlb",  # 把这里换成你刚才测试成功的那个密钥
    base_url="https://api.siliconflow.cn/v1"
)
        
        stream = client.chat.completions.create(
            model="deepseek-ai/DeepSeek-V3",
            messages=st.session_state.messages,
            stream=True,
            temperature=0.7
        )
        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                full_response += chunk.choices[0].delta.content
                placeholder.markdown(full_response + "▌")
        placeholder.markdown(full_response)
    
    # 保存 AI 回复
    st.session_state.messages.append({"role": "assistant", "content": full_response})
    save_history(st.session_state.messages)
