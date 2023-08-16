import databutton as db
import streamlit as st
from embedchain import App
import os
import time
from config import (OPENAI_API_KEY)

custom_style = """
    <style>
        .block-container{
            max-width:780px
        }
        body{
            font-size:12px
        }
        .stButton button  {
            border-radius:0px;
            padding:5px 20px;
            font-size:12px
        }
        .stButton button p{
            font-size:12px
        }
        .stTextInput input {
            border-radius:0px;
            padding:5px;
            line-height:1.6
            font-size:12px
        }
        .stTextInput input:focus{
            border-radius:0px;
        }
        .stTextInput .st-br{
            border-radius:0px;
        }
        .stTextInput>label p{
            line-height:2
        }
        .stAlert p{
            font-size:12px
        }
    </style>
"""
st.markdown(custom_style, unsafe_allow_html=True)
st.subheader("Embedchain AI Knowledge 🤖 ")
st.markdown(
    "Repo : [AI-DevSecOps](https://github.com/QuintionTang/AI-DevSecOps)")

os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY


@st.cache_resource
def initBot(URL):
    # 创建一个机器人实例
    devsec_bot = App()
    devsec_bot.add("web_page", URL)
    # 这里支持嵌入多个在线资源
    # devsec_bot.add("youtube_video", "")
    # devsec_bot.add("pdf_file", "")
    # devsec_bot.add("web_page", "https://www.devpoint.cn/index.shtml")
    return devsec_bot


if "btn_state" not in st.session_state:
    st.session_state.btn_state = False

prompt = st.text_input(
    "请输入内容URL",
    placeholder="请输入内容URL",
    value="https://www.devpoint.cn/index.shtml"
)

btn = st.button("初始化机器人")

if prompt:
    if btn or st.session_state.btn_state:
        st.session_state.btn_state = True
        devsec_bot = initBot(prompt)
        st.success("机器人已就绪🤖")

        # 初始化聊天记录
        if "messages" not in st.session_state:
            st.session_state.messages = []

        # 在应用程序重新运行时显示历史记录中的聊天消息
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # 接收聊天内容
        if prompt := st.chat_input("有什么可以帮忙？"):
            # 增加聊天历史记录
            st.session_state.messages.append(
                {"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                full_response = ""
                assistant_response = devsec_bot.query(prompt)
            # 模拟具有毫秒延迟的响应流
            for chunk in assistant_response.split():
                full_response += chunk + " "
                time.sleep(0.05)
                # 模拟闪烁的光标来模拟打字
                message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)
            # Add assistant response to chat history
            st.session_state.messages.append(
                {"role": "assistant", "content": full_response}
            )
    else:
        st.info("首先启动一个机器人！")
else:
    st.info('您需要输入一个内容URL来启动 DevSecOps 机器人', icon="⚠️")
