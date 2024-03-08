
from agent_tools.api_credentials import chat_model
from prompt.prompts import toc_rfp_response_prompt
from utils.util import FallbackLLMChain

def content(requirement, 
            expected_response,
            legal_and_contractual,
            ):
    chain = FallbackLLMChain(llm=chat_model, prompt=toc_rfp_response_prompt)
    response = chain({'requirement':requirement, 'expected_response':expected_response, "legal_and_contractual":legal_and_contractual
                     }) 
    return response['text']