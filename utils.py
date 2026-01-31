import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.utilities import WikipediaAPIWrapper

def generate_script(subject, video_length, creativity, api_key, model_type="deepseek-chat"):
    # 获取标题模板
    title_template = ChatPromptTemplate.from_messages(
        [
            ("human", "请为'{subject}'这个主题的视频想一个吸引人的标题"),
        ]
    )

    # 获取内容模板
    script_template = ChatPromptTemplate.from_messages(
        [
            ("human", """你是一位短视频频道的博主。根据以下标题和相关信息，为短视频频道写一个视频脚本。
             视频标题：{title}，视频时长：{duration}分钟，生成的脚本的长度尽量遵循视频时长的要求。
             要求开头抓住限球，中间提供干货内容，结尾有惊喜，脚本格式也请按照【开头、中间，结尾】分隔。
             整体内容的表达方式要尽量轻松有趣，吸引年轻人。
             脚本内容可以结合以下维基百科搜索出的信息，但仅作为参考，只结合相关的即可，对不相关的进行忽略：
             ```{wikipedia_search}```""")
        ]
    )
    # 构建AI模型
    if model_type == "deepseek-chat":
        # model = ChatOpenAI(api_key=os.environ.get('OPENAI_API_KEY'),base_url="https://aigc789.top/v1",model="gpt-3.5-turbo", temperature=creativity)
        model = ChatOpenAI(api_key=api_key,base_url="https://api.deepseek.com",model="deepseek-chat", temperature=creativity)
    elif model_type == "gpt-3.5-turbo":
        model = ChatOpenAI(api_key=api_key,model="gpt-3.5-turbo", temperature=creativity)
    elif model_type == "gpt-4":
        model = ChatOpenAI(api_key=api_key,model="gpt-4", temperature=creativity)
    else:
        model = ChatOpenAI(api_key=api_key, base_url="https://api.deepseek.com", model="deepseek-chat", temperature=creativity)

    # 构建链
    title_chain = title_template | model
    script_chain =  script_template | model

    # 生成标题
    title = title_chain.invoke({"subject": subject}).content
    print(title)

    # 维基百科搜索
    search = WikipediaAPIWrapper(lang="zh")
    search_result = search.run(subject)

    # 生成脚本
    script = script_chain.invoke({"title": title, "duration": video_length, "wikipedia_search": search_result}).content
    return search_result, title, script

if __name__ == '__main__':
    search_result, title, script = generate_script("中华田园猫", 1, 0.5, os.environ.get('DEEPSEEK_API_KEY'))
    print(f"{title}\n{script}")