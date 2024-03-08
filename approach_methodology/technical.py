from agent_tools.api_credentials import chat_model
from prompt.prompts import  approach_methodology_prompt



from utils.util import FallbackLLMChain

def app_method(summary_requirements,objective, expected_rfp_response, trends,company_strengths ):
    chain = FallbackLLMChain(llm=chat_model, prompt=approach_methodology_prompt)
    response = chain({'summary_requirement':summary_requirements,"objective":objective,
                      "expected_rfp_response":expected_rfp_response,
                      'trends':trends,"company_strengths":company_strengths }) 
    app_meth = response['text']
    return app_meth


    