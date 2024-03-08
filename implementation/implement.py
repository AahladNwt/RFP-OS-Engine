from langchain.chains import SequentialChain
from utils.util import FallbackLLMChain
from agent_tools.api_credentials import chat_model
from prompt.prompts import (
                            implementation_plan_prompt,
                            key_stages_and_phases_prompt,
                            resource_allocation_and_dependencies_prompt,
                            contingency_measures_prompt
                        )


class ImplementationManager():
    def __init__(self, proposed_solution, timeline_milestones, summary_requirements,objective, deliverable):
        self.proposed_solution = proposed_solution
        self.timeline_milestones = timeline_milestones
        self.summary_requirements = summary_requirements
        self.objective = objective
        self.deliverable = deliverable
        super().__init__()   
    
    def implementation_chain(self, key_stakeholders):
        
        chain_one = FallbackLLMChain(llm=chat_model, prompt=implementation_plan_prompt, output_key="implementation_plan")
        
        chain_two = FallbackLLMChain(llm=chat_model, prompt=key_stages_and_phases_prompt, output_key="key_stages_and_phases")
        
        chain_three = FallbackLLMChain(llm=chat_model, prompt=resource_allocation_and_dependencies_prompt, output_key="resource_allocation_and_dependencies")
        
        chain_four = FallbackLLMChain(llm=chat_model, prompt=contingency_measures_prompt, output_key="contingency_measures") 
        
        overall_chain = SequentialChain(
                            chains=[chain_one, chain_two, chain_three, chain_four],#, chain_two, chain_three, chain_four], 
                            input_variables=["proposed_solution","summary_requirements", "objective", "timeline_milestones", "deliverable", "key_stakeholders"],
                            output_variables=["implementation_plan", "key_stages_and_phases", "resource_allocation_and_dependencies", "contingency_measures"],
                            verbose=True
                                        ) 
        response = overall_chain({'proposed_solution':self.proposed_solution,'summary_requirements':self.summary_requirements,
                                   "objective":self.objective,"timeline_milestones":self.timeline_milestones,"deliverable":self.deliverable,
                                   "key_stakeholders":key_stakeholders
                                }) 
        return response
