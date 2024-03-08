from langchain.agents import Tool
from agent_tools.api_credentials import duckduck_search, serpapi_search
from langchain.agents import Tool, AgentType, initialize_agent
import re                                 

class AgentTools:
    
    def __init__(self):
        pass
        
    def search_tools(self, *args):
        tools = []
        
        for search_func in args:
            if search_func == 'google':  # Corrected the spelling to 'goggle'
                serpapi_tool = Tool(
                    name="Google Search",
                    func=serpapi_search.run,
                    description="Useful for when you need to answer questions about current events or the current state of the world"
                )
                tools.append(serpapi_tool)
            if search_func == 'duckduckgo':
                duckduck_tool = Tool(
                    name="Search",
                    func=duckduck_search.run,
                    description="Useful for when you need to answer questions about current events or the current state of the world"
                )
                tools.append(duckduck_tool)
        
        return tools
    
    def agent_special_tools(self, llm,problem_summary, *args):
        prefix, format_instructions, suffix = args[0], args[1], args[2]
        agent = initialize_agent(
            tools=self.search_tools('google', 'duckduckgo'),
            llm=llm,
            agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            verbose=True,
            early_stopping_method="generate",
            # handle_parsing_errors="Check your output and make sure it conforms!",
            handle_parsing_errors=True,
            agent_kwargs={
                'prefix': prefix, 
                'format_instructions': format_instructions,
                'suffix': suffix
            },  
        )
        try:
            response = agent.run(input=problem_summary)
            print(response)
        except ValueError as e:
            response = str(e)
            if not response.startswith("Could not parse LLM output: `"):
                raise e
            response = response.removeprefix("Could not parse LLM output: `").removesuffix("`")
        # Use regex to remove text starting from 'AI:' and backward
        filtered_text = re.sub(r'.*AI:', '', response, flags=re.DOTALL)

        return filtered_text
