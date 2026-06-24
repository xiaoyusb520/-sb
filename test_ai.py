import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="测试", page_icon="🧪")
st.title("🧪 API 连接测试")

# 替换成你的密钥
client = OpenAI(
    api_key="你的硅基流动密钥",  # ⚠️ 这里填你的 sk-xxx
    base_url="https://api.siliconflow.cn/v1"
)

# 一个简单的输入框
user_input = st.text_input("随便说句话，测试连接：")

if user_input:
    with st.spinner("连接中..."):
        try:
            response = client.chat.completions.create(
                model="Qwen/Qwen2.5-7B-Instruct",  # 用最稳的模型
                messages=[{"role": "user", "content": user_input}]
            )
            st.success("✅ 连接成功！AI 回复：")
            st.write(response.choices[0].message.content)
        except Exception as e:
            st.error(f"❌ 报错：{e}")