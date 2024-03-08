import os
import json
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import ResponseSchema
from langchain.output_parsers import StructuredOutputParser
from langchain.agents import AgentType
from langchain.agents import initialize_agent
import concurrent.futures
from functools import partial
from typing import Any, Dict, List, Optional, Union, cast
from langchain.callbacks.manager import (
    AsyncCallbackManagerForChainRun,
    CallbackManagerForChainRun,
)
from evaluation.error_handler import SearchLimitError
from utils.util import FallbackLLMChain, clean_response
from agent_tools.all_tool import AgentTools
from agent_tools.api_credentials import chat_model
from prompt.prompts import (
                            company_profile_prompt,
                            summary_prompt
                            )

CBManager = Union[AsyncCallbackManagerForChainRun, CallbackManagerForChainRun]

os.environ["LANGCHAIN_TRACING"] = "true"



        

class TopFiveCompanies:
    """A class to handle tasks related to summarizing and extracting information about top companies."""

    tool_func = AgentTools()
    tools = tool_func.search_tools('google', 'duckduckgo')

    def __init__(self):
        pass
    
    def text_summary(self, summary_prompt: str, sample_problem_requirement:str) -> str:
        """Generate a text summary using the provided prompt and requirement.

        Args:
            summary_prompt (str): The prompt for generating the summary.

        Returns:
            str: The generated summary.
        """
        chain = FallbackLLMChain(llm= chat_model, prompt=summary_prompt)
        summary = chain.run(sample_problem_requirement)

        # Store the summary in the class variable
        self.stored_summary = summary

        return summary
    
    def top_five_web_search_agent(self):
        """Generate a response using the web search agent based on the generated summary.

        Returns:
            str: The response generated by the web search agent.
        """
        summary = self.text_summary(summary_prompt)

        websearch_prompt = f"""
                As a Proposal Vendor Expert, your task is to research the Web and extract the following information: \
                List the top five companies worldwide along with their websites that offer services as described in the following **Text**. \
                You are an expert in this field and your task is to gather this information.
                
                You have the option to refuse to answer if there is insufficient information. If there are ambiguous terms or acronyms, define them before proceeding with your answers.\
                Please provide your answers as a Python List.
                  
                Text:
                ```{summary}```
                
                Note: If you are unable to find sufficient information or if the terms in the text are ambiguous, please provide a message explaining why you are unable to complete the task.
                """

        agent = initialize_agent(self.tools,
                                 chat_model,
                                 agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
                                 verbose=True,
                                 handle_parsing_errors="Check your output and make sure it conforms!")
        
        try:
            response = agent.run(websearch_prompt)
            print(response, 'Agent Response!!!      ')
            if "Your account has run out of searches." in response:
                raise SearchLimitError("Got error from SerpAPI: Your account has run out of searches.")
        except SearchLimitError as e:
            print(e)
    
        return response
    
    def json_parser(self):
        """Create a structured output parser for extracting company details.

        Returns:
            Tuple[StructuredOutputParser, str]: The output parser and format instructions.
        """

        company_name_schema = ResponseSchema(name="company name",
                                             description="What is the company names? **default** if not known or unknown.")
        website_schema = ResponseSchema(name="website",
                                        description="What is the company website? **default** if not known or unknown.")
        response_schemas = [company_name_schema, website_schema]

        output_parser = StructuredOutputParser.from_response_schemas(response_schemas)

        return output_parser, output_parser.get_format_instructions()
    
    def top_five_company_details(self):
        """Extract and format the company details from the web search agent response.

        Returns:
            str: The formatted output containing company details.
        """

        text = self.top_five_web_search_agent()
        _, format_instructions = self.json_parser()

        first_prompt = ChatPromptTemplate.from_template(template=company_profile_prompt)

        messages = first_prompt.format_messages(text=text)
        response = chat_model(messages)
        output = clean_response(response)

        return output
        

class ProjectRunner:
    def __init__(self, company_name, project_execution_prompt, summary):
        self.company_names = company_name
        self.execution_prompt = project_execution_prompt
        self.summary = summary

    def run_chat_for_company(self, company_name):
        messages = self.execution_prompt.format_messages(
                                    name=company_name,
                                    project= self.summary)
        project_response = chat_model(messages)
        return company_name, project_response

    def run_chats_concurrently(self):
        response_data = {}  # Dictionary to store responses

        with concurrent.futures.ThreadPoolExecutor(max_workers=len(self.company_names)) as executor:
            # Use partial to create functions with fixed arguments (company_name in this case)
            tasks = [executor.submit(partial(self.run_chat_for_company, name)) for name in self.company_names]

            # Collect results as they finish
            for future in concurrent.futures.as_completed(tasks):
                company_name, response = future.result()
                response_data[company_name] = response.content
        # Convert dictionary to JSON
        json_data = json.dumps(response_data)
        return json_data
    
    
class SolutionPosition:
    """_summary_
    """
    def __init__(self, prompt_template, company_info, top_companies):
        """_summary_

        Args:
            prompt_template (_type_): _description_
            company_info (_type_): _description_
            top_companies (_type_): _description_
        """
        self.prompt = prompt_template
        self.company_info = company_info
        self.top_companies = top_companies
        
    def position_vendor_as_solution(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        messages = self.prompt.format_messages(
                                        company_info=self.company_info,
                                        top_companies=self.top_companies)
        solution_company  = chat_model(messages)
        
        return  solution_company
    
    













