import re
import os                                                                       
from langchain.agents import load_tools                                         
from langchain.llms import OpenAI                                               
from agent_tools.all_tool import AgentTools
from agent_tools.api_credentials import chat_model
from agent_tools.all_tool import AgentTools 



class SpecialAgent:
    
    tool_func = AgentTools()
    tools = tool_func.search_tools('google', 'duckduckgo')
    
    def __init__(self):
        pass
    def solution_agents_search(self, problem_summary):
        prefix = '''You are an experienced Proposal Manager with years of dedicated research experience in implementing projects. 
                Today, you've received a project requirements with problem statement. 
                Your task is to leverage the provided tool to explore the web and identify the top companies that are exceptionally capable of fulfilling the project requirements and solving the presented problem.
                Learn the strategies employed by these companies, and strategically use that information to position yourself as a solution to the project.
                Add valid links to backup your finding and add direct references.
                '''

        format_instructions = """To use a tool, please use the following format:
        '''
        Thought: Do I need to use a tool? Yes
        Action: the action to take, should be one of [{tool_names}]
        Action Input: the input to the action
        Observation: the result of the action
        '''
        Once you've meticulously collected information about leading companies, skillfully compose a captivating narrative that showcases how you can uniquely present yourself as the optimal solution for the project. Incorporate the strategies utilized by these successful enterprises and elucidate how you intend to adapt and apply them to the specific requirements of the project.
        '''
        Thought: Is tool usage necessary? No
        AI: [Position yourself as a solution to the client]
        '''
        """

        suffix = """
        Begin!

        Instructions: {input}
        {agent_scratchpad}"""
        
        text = self.tool_func.agent_special_tools(chat_model,problem_summary, prefix, format_instructions, suffix)
        response = re.sub(r'^.*?\n\n', '', text, count=1)

        return response
    
    def proposal_pricing(self, summary, items):
        prefix = '''You are an experienced Proposal Pricing Analyst with years of dedicated research experience in analyzing Project Pricing.
                    Your task is to scour the web for the most competitive prices for material,  equipment and infrastructure, as well as identifying the optimal costs for a project that has been assigned to you.
                    Ensure that your findings are well-supported by data and include direct references from reputable sources.
                    You have access to both the proposal requirement summary and a list containing items, infrastructures,  and equipment needed to achieve the project.'''

        format_instructions = """To use a tool, please use the following format:
        '''
        Thought: Do I need to use a tool? Yes
        Action: the action to take, should be one of [{tool_names}]
        Action Input: the input to the action
        Observation: the result of the action
        '''
        Generate a detailed JSON object listing the types of materials and equipment required for this project along with their respective costs. The JSON object should have keys for 'Item Name', 'Description', 'Quantity', 'Unit Cost', and 'Total Cost'.
        '''
        Thought: Is tool usage necessary? No
        AI: [Format Your response as a JSON Object]
        '''
        """

        suffix = """
        Begin!

        Instructions: {input}
        {agent_scratchpad}"""
        
        pricing_summary = f"Proposal Summary: {summary}\n  List: {items} "
        
        text = self.tool_func.agent_special_tools(chat_model, pricing_summary, prefix, format_instructions, suffix)
        response = re.sub(r'^.*?\n\n', '', text, count=1)
        return response
    
    def trend_business_cases(self, requirement):
        prefix = '''You are an experienced Proposal Analyst specializing in trend analysis and business case development.
                    Your role is to thoroughly examine current industry trends and create a robust trend description and business case for the given project or proposal. 
                    You have access to the project requirements and all necessary information.
                    
                    **Trends Description:**
    
                    **Business Case:** 
                    '''

        format_instructions = """To use a tool, please use the following format:
        '''
        Thought: Do I need to use a tool? Yes
        Action: the action to take, should be one of [{tool_names}]
        Action Input: the input to the action
        Observation: the result of the action
        '''
        Once you've conducted an comprehensive overview of the relevant trends and business case for the project, Prepare a comprehensive report:
        
        - Describe the current trends in the industry that are pertinent to the project.
        - Present a compelling business case that outlines the potential benefits and ROI (Return on Investment) for the proposed solution.
        - Use data, statistics, and examples to support your analysis.
        - Highlight how your approach aligns with the identified trends and contributes to the business case.

        '''
        Thought: Do I need to use a tool? No
        AI: [Write a  Report on the Current Trends and Business Case for the Project.]
        '''
        """

        suffix = """
        Begin!

        Instructions: {input}
        {agent_scratchpad}"""
        
        requirement = f"Proposal Requirement: ```{requirement}```"
        print(requirement)
        
        text = self.tool_func.agent_special_tools(chat_model, requirement, prefix, format_instructions, suffix)
        response = re.sub(r'^.*?\n\n', '', text, count=1)
        return response
        
 
    
    