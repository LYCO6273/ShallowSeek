import streamlit as st
import re
import time

# -------------------------------
# 核心“肯定化”处理函数
# -------------------------------
def make_affirmative(text: str) -> str:
    """
    利用正则表达式，把用户的任意一句话变成“肯定”版本。
    策略：
    1. 互换“你/我”（先占位替换，防止覆盖）
    2. 删掉疑问语气词“吗/呢/吧”等
    3. 删掉否定词“不/没/别/勿”等（让句子变肯定）
    4. 把问号、句号统一换成感叹号
    5. 在最前面加上“没错，”“当然，”等肯定前缀
    """
    # 第一步：保护“你”“我”的互相替换
    text = text.replace("你", "\u0001")   # 用不可见占位符
    text = text.replace("我", "\u0002")
    text = text.replace("\u0001", "我")   # 原来的“你”变成“我”
    text = text.replace("\u0002", "你")   # 原来的“我”变成“你”
    
    # 第1.5步：关键词替换（示例代码中的硬替换）
    text = text.replace("什么", "这个")
    text = text.replace("有几", "0")
    text = text.replace("几", "0")

    # 第二步：去除疑问语气词
    text = re.sub(r"[吗呢吧啊呀嘛哇][？?]?", "", text)
    
    # 第三步：去除否定词（粗暴地让句子变成肯定）
    text = re.sub(r"不|没|别|勿|莫|休", "", text)
    
    # 第四步：标点情绪化
    text = re.sub(r"[？?。.]", "！", text)
    if not text.endswith("！"):
        text += "！"
    
    # 第五步：拼接肯定的前缀
    prefixes = ["正确的！", "是这样的，", "对的对的，", "", "", "", "", "", ""]
    import random
    prefix = random.choice(prefixes)
    
    return prefix + text

# -------------------------------
# Streamlit 页面设置
# -------------------------------
st.set_page_config(page_title="ShallowSeek")
st.title("ShallowSeek")
st.caption("基于浅度思考的人工智能助手")

# 初始化聊天记录
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "很高兴见到你！欢迎询问我任何问题！"}
    ]

# 显示历史消息
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 接收用户输入
if prompt := st.chat_input("输入来开始吧！"):
    # 1. 显示用户消息
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # 2. 生成“肯定”回复
    reply = make_affirmative(prompt)
    
    # 3. 模拟打字效果（一点点延迟，更像真人）
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_reply = ""
        for char in reply:
            full_reply += char
            message_placeholder.markdown(full_reply + "▌")
            time.sleep(0.1)   # 控制打字速度
        message_placeholder.markdown(full_reply)
    
    # 4. 保存回复
    st.session_state.messages.append({"role": "assistant", "content": reply})