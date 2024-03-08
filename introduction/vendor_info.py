
from agent_tools.all_tool import AgentTools
from agent_tools.api_credentials import llm
from evaluation.error_handler import SearchLimitError
from langchain.agents import initialize_agent
from langchain.agents import AgentType
tool = AgentTools()
tools = tool.search_tools('google', 'duckduckgo')

def company_agent(company_name):
    """_summary_

    Args:
        prompt (_type_): _description_

    Returns:
        _type_: _description_
    """
    
    prompt = f"Tell me about {company_name} company, what they do, mission and vision"

    agent = initialize_agent(
        tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, #verbose=True,
        handle_parsing_errors="Check your output and make sure it conforms!"
    )
    try:
        response = agent.run(prompt)
        if "Your account has run out of searches." in response:
            raise SearchLimitError("Got error from SerpAPI: Your account has run out of searches.")
    except SearchLimitError as e:
        print(e)
    
    return response