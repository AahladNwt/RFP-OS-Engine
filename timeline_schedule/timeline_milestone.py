
import streamlit as st
from utils.util import FallbackLLMChain
from agent_tools.api_credentials import chat_model
from prompt.prompts import deliverables_deadlines_prompt

@st.cache_data
def project_timeline(result_dict):
    chain = FallbackLLMChain(llm=chat_model, prompt=deliverables_deadlines_prompt)
    response = chain({'objective':result_dict['objective'], 'project_duration_and_key_stages':result_dict['project_duration_and_key_stages']}) 
    return response['text']