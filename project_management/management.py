from langchain.chains import SequentialChain
from utils.util import FallbackLLMChain
from agent_tools.api_credentials import chat_model
from prompt.prompts import (team_composition_prompt,
                            communication_strategy_prompt, 
                            risk_management_prompt,
                            work_schedule_prompt)


class ProjectManager():
    def __init__(self, proposed_solution,summary_requirement, project_duration_and_key_stages,objective):
        self.proposed_solution = proposed_solution
        self.summary_requirement = summary_requirement
        self.project_duration_and_key_stages = project_duration_and_key_stages
        self.objective = objective
        super().__init__()   
    
    def management_chain(self, team_experience):
        chain_one = FallbackLLMChain(llm=chat_model, prompt=team_composition_prompt, output_key="team_composition")
        
        chain_two = FallbackLLMChain(llm=chat_model, prompt=communication_strategy_prompt, output_key="communication_strategy")
        
        chain_three = FallbackLLMChain(llm=chat_model, prompt=risk_management_prompt, output_key="risk_management")
        
        chain_four = FallbackLLMChain(llm=chat_model, prompt=work_schedule_prompt, output_key="work_schedule") 
        
        overall_chain = SequentialChain(
                            chains=[chain_one, chain_two, chain_three, chain_four], 
                            input_variables=["proposed_solution","summary_requirement", "team_experience", "project_duration_and_key_stages", "objective"],
                            output_variables=["team_composition", "communication_strategy","risk_management", "work_schedule"],
                            verbose=True
                                        ) 
        response = overall_chain({'proposed_solution':self.proposed_solution,'summary_requirement':self.summary_requirement, "team_experience":team_experience,
                                  "project_duration_and_key_stages":self.project_duration_and_key_stages, "objective":self.objective
                                }) 
        return response


