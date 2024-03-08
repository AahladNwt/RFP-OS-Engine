# from langchain.utilities import GoogleSerperAPIWrapper
# from langchain.llms.openai import OpenAI
# from langchain.agents import initialize_agent, Tool
# from langchain.agents import AgentType
# from langchain.prompts import MessagesPlaceholder
# from langchain.memory import ConversationBufferMemory


# llm = OpenAI(temperature=0, model_name='gpt-3.5-turbo')
# search = GoogleSerperAPIWrapper()

# name = "Okolie Chukwuka Albert"
# profession = "Machine Learning Engineer"
# location = "Nigeria"
# chat_history = MessagesPlaceholder(variable_name="chat_history")
# memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
# tools = [
#     Tool(
#         name="Intermediate Answer",
#         func=search.run,
#         description= f"""Useful for when you want to find information about {name}. 
#                         This includes details like his {location}, personal website, and {profession}. 
#                         Input should be a fully formed question about {name}.""",
#     )
# ]

# self_ask_with_search = initialize_agent(
#     tools, 
#     llm, 
#     agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
#     verbose=True,
#     verboseverbose=True, 
#     memory=memory, 
    
# )
# self_ask_with_search.run(
#     "Give important information about him"
# )



#     def proposal_pricing(self, problem_summary, implementation_plan):
#         prefix = '''You are an experienced Proposal Pricing Analyst with 20 years of dedicated research experience in analyzing Project Pricing.\n
#             Your task is to scour the web for the most competitive prices for equipment and infrastructure, as well as identifying the optimal costs for a project that has been assigned to you.
#             Ensure that your findings are well-supported by data and include direct references from reputable sources.\n
#             You have access to both the proposal summary and the implementation plans, allowing you to align your pricing analysis with the project's objectives and scope.
#             '''

#         format_instructions = """To utilize the tool effectively, adhere to the following format:
#         '''
#         Thought: Is tool usage necessary? Yes
#         Action: Specify the action to undertake, selecting from [{tool_names}]
#         Action Input: Provide the required input for the action
#         Observation: Record the outcome of the action
#         '''
#         When you have gathered all the information Pricing for the RFP project, just write it to the user in the form of a json file.
#         '''
#         Thought: Is tool usage necessary? No
#         AI: [your response here]
#         '''
#         """
#         suffix = """Begin!

#         Question: {input}
#         {agent_scratchpad}"""
        
#         proplem_with_plan  = "RFP Requirements Summary:\n\n {}\n\n Implementation Plan:\n\n {}".format(problem_summary, implementation_plan)
        
#         text = self.tool_func.agent_special_tools(chat_model, proplem_with_plan, prefix, format_instructions, suffix)
#         response = re.sub(r'^.*?\n\n', '', text, count=1)
#         return response
