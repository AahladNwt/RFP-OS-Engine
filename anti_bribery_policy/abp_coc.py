tabc_response = """

    ### UNDERTAKING BY CONSULTANT ON ANTI – BRIBERY POLICY / CODE OF CONDUCT AND COMPLIANCE PROGRAMME\n\n
      
    Example 1:

    I, [Name of Consultant], place importance on competitive tendering taking place on a basis that is free, fair, competitive, and not open to abuse. I am pleased to confirm that I will not offer or facilitate, directly or indirectly, any improper inducement or reward to any public officer, their relations, or business associates in connection with my proposal or in the subsequent performance of the contract if I am successful.

    I have an Anti-Bribery Policy/Code of Conduct and a Compliance Program, which includes all reasonable steps necessary to ensure that I comply with the No-bribery commitment given in this statement, as well as by all third parties working with me on the public sector projects or contract, including agents, consultants, consortium partners, sub-contractors, and suppliers. Copies of the Anti-Bribery Policy/Code of Conduct and Compliance Program are attached.

    Authorized Signature: ____________________________________________
    Name and Title of Signatory: _______________________________________
    Name of Consultant: ______________________________________________
    Signature: _____________________________________________________
    Page Section 4 - Technical Proposal - Standard Forms
    Address: _______________________________________________________

    Example 2:
    
    ### UNDERTAKING BY CONSULTANT ON ANTI – BRIBERY POLICY / CODE OF CONDUCT AND COMPLIANCE PROGRAMME\n\n

    I, [Name of Consultant], have issued, for the purposes of this proposal, a Compliance Program copy attached - which includes all reasonable steps necessary to assure that I will comply with the No-bribery commitment given in this statement, as well as by all third parties working with me on the public sector projects or contract, including agents, consultants, consortium partners, subcontractors, and suppliers.

    Authorized Signature: ____________________________________________
    Name and Title of Signatory: _______________________________________
    Name of Consultant: ______________________________________________
    Address: _______________________________________________________

    Note: Please fill in the blanks with the appropriate information for each example.

  """
  

from utils.util import create_final_prompt
from agent_tools.api_credentials import chat_model
from prompt.prompts import anti_bribery_undertaking_prompt

def create_anti_bribery_undertaking(company_profile,tabc):
    examples = [
        {"input": anti_bribery_undertaking_prompt.format(company_profile,tabc), "response": tabc_response},
    ]

    final_prompt = create_final_prompt(examples, chat_model)

    response = final_prompt.invoke({"input": anti_bribery_undertaking_prompt.format(company_profile,tabc)})

    return response.content
    