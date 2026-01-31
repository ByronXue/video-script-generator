import streamlit as st
from utils import generate_script

# 标题
st.title("🎬️视频脚本生成器")

# 侧边栏
with st.sidebar:
    # 模型选择下拉框
    model_choice = st.selectbox(
        "请选择API模型",
        options=[
            "deepseek-chat",
            "gpt-3.5-turbo",
            "gpt-4",
        ],
        index=0
    )

    # 根据选择的模型显示相应的获取链接
    if model_choice == "deepseek-chat":
        st.markdown("[获取DeepSeek API秘钥](https://platform.deepseek.com/)")
    elif model_choice == "openai-gpt-3.5" or model_choice == "openai-gpt-4":
        st.markdown("[获取OpenAI API秘钥](https://platform.openai.com/api-keys)")

    # API密钥输入
    api_key = st.text_input("请输入API秘钥", type="password")


# 主体

# 视频主题(文本输入框)
subject = st.text_input("💡请输入视频主题")
# 视频时长(数字输入框+调节按钮)
video_length = st.number_input("⏱️请输入视频的大致时长(单位:分钟)", min_value=0.1, step=0.1)
# 视频创造力(拖动条)
creativity = st.slider("🤔请选择视频的创造力(数字越小越严谨,反之更多样)", min_value=0.1, max_value=1.0, value=.5, step=0.1)

# 提交按钮
submit = st.button("📽️生成视频脚本")

# 校验输入项
if submit and not api_key:
    st.error("请输入deepseek API秘钥")
    st.stop()

if submit and not subject:
    st.error("请输入视频主题")
    st.stop()

# 生成脚本
if submit:
    with st.spinner("视频脚本生成中..."):
        search_result, title, script = generate_script(subject, video_length, creativity, api_key, model_choice)
    st.success("视频脚本已生成!")
    st.subheader("🔥标题: ")
    st.write(title)
    st.subheader("📝视频脚本: ")
    st.write(script)
    with st.expander("维基百科搜索结果 👀"):
        st.write(search_result)