# import torch
from langchain.llms import OpenAI
from dotenv import load_dotenv, find_dotenv
from langchain.tools import DuckDuckGoSearchRun
from langchain.utilities import SerpAPIWrapper
from langchain.embeddings import OpenAIEmbeddings
#from langchain.embeddings import HuggingFaceEmbeddings
from langchain.chat_models import ChatOpenAI
import streamlit as st
# DEVICE = "cuda:0" if torch.cuda.is_available() else "cpu"
import os



_ = load_dotenv(find_dotenv()) # read local .env file
#serapi set up
SERPAPI_API_KEY = os.environ.get("SERPAPI_API_KEY")
SERPER_API_KEY = os.environ.get("SERPAPI_API_KEY")
serpapi_search  = SerpAPIWrapper(serpapi_api_key=SERPAPI_API_KEY)

def select_llm():
    """
    Read user selection of parameters in Streamlit sidebar.
    """
    model_name = st.sidebar.radio("Choose LLM:",
                                  (
                                   "gpt-3.5-turbo-16k-0613",
                                   "gpt-4",
                                   
                                   ))
    
    temperature = st.sidebar.slider("Temperature:", min_value=0.0,
                                    max_value=1.0, value=0.0, step=0.01)
    return model_name, temperature
model_name, temperature = select_llm()
#if model_name.startswith("gpt-"):
#llm =  ChatOpenAI(temperature=temperature, model_name=model_name)
#def choose_llm(model_name, te)
#OpenAI setup



chat_model = ChatOpenAI(temperature=temperature, model=model_name, streaming=True, max_retries=10)
#chat_model.openai_api_key = os.environ['OPENAI_API_KEY'] 

chat_model = ChatOpenAI(temperature=temperature, model=model_name, streaming=True, max_retries=10)
#chat_model_16k.openai_api_key = os.environ['OPENAI_API_KEY'] 
llm = OpenAI(temperature=temperature)

agent_llm = OpenAI(model_name=model_name, temperature = 0.7, model="gpt-3.5-turbo-0613")


#llm.openai_api_key = os.environ['OPENAI_API_KEY'] 
##Hugginface
#huggingface_api_token = os.environ.get("HUGGINGFACEHUB_API_TOKEN")

#duckduckgo
duckduck_search = DuckDuckGoSearchRun()

###Embedding
embeddings_model = OpenAIEmbeddings(request_timeout=20.0)
#hugging_embeddings = HuggingFaceEmbeddings(model_name="all-mpnet-base-v2")

####### Llama Index API Models
from llama_index import ServiceContext, set_global_service_context
from llama_index.llms import OpenAI
from llama_index.embeddings import resolve_embed_model
from llama_index.indices.postprocessor import SentenceTransformerRerank


embed_model = resolve_embed_model("local:BAAI/bge-large-en-v1.5")

llama_llm = OpenAI(model=model_name)
service_context = ServiceContext.from_defaults(
    llm=llama_llm, embed_model=embed_model
)
set_global_service_context(service_context)

rerank = SentenceTransformerRerank(
            model="cross-encoder/ms-marco-MiniLM-L-2-v2", top_n=3
        )