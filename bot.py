from llama_index import StorageContext, ServiceContext, GPTVectorStoreIndex, LLMPredictor, PromptHelper, SimpleDirectoryReader, load_index_from_storage
from langchain.chat_models import ChatOpenAI
import gradio as gr
from config import (OPENAI_API_KEY)
import sys
import os

os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY


def create_service_context():
    # 参数配置
    max_input_size = 4096
    num_outputs = 512
    max_chunk_overlap = 20
    chunk_size_limit = 600

    # 允许用户显式设置某些参数配置
    prompt_helper = PromptHelper(
        max_input_size, num_outputs, max_chunk_overlap, chunk_size_limit=chunk_size_limit)

    # LLMPredictor 是 LangChain 的 LLMChain 的包装类，可以轻松集成到 LlamaIndex 中
    llm_predictor = LLMPredictor(llm=ChatOpenAI(
        temperature=0.5, model_name="gpt-3.5-turbo", max_tokens=num_outputs))

    # 构造 service_context
    service_context = ServiceContext.from_defaults(
        llm_predictor=llm_predictor, prompt_helper=prompt_helper)
    return service_context


def data_ingestion_indexing(directory_path):
    # 从指定目录路径加载数据
    documents = SimpleDirectoryReader(directory_path).load_data()

    # 第一次建立索引时
    index = GPTVectorStoreIndex.from_documents(
        documents, service_context=create_service_context()
    )

    # 持久化索引到磁盘，默认 storage 文件夹
    index.storage_context.persist()

    return index


def data_querying(input_text):
    # 重建存储上下文
    storage_context = StorageContext.from_defaults(persist_dir="./storage")

    # 从存储加载索引
    index = load_index_from_storage(
        storage_context, service_context=create_service_context())

    # 用输入文本查询索引
    response = index.as_query_engine().query(input_text)

    return response.response


iface = gr.Interface(fn=data_querying,
                     inputs=gr.components.Textbox(
                         lines=7, label="Enter your text"),
                     outputs="text",
                     title="DevPoint's Knowledge Base")

# passes in data directory
index = data_ingestion_indexing("data")

iface.launch(share=False)
