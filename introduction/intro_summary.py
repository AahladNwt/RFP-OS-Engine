import json

from tabulate import tabulate
from utils.util import FallbackLLMChain
from langchain.chains import SequentialChain
from agent_tools.api_credentials import chat_model
from prompt.prompts import (
                    summary_prompt,
                    application_form_prompt,
                    introduction_prompt,
                    # overview_prompt,
                    business_context_prompt,
                    project_understanding_prompt,
                    client_insight_prompt,
                    objective_and_goal_prompt,
                    comment_suggestion_prompt,
                    organization_background_prompt,
                    organization_experience_prompt,
                    achievements_recognitions_prompt,
                    language_proficiency_prompt,
                    financial_proposal_prompt
                )
                      
class ProposalIntoduction:
    def __init__(self, requirement, scope, expected_rfp_response, objective,vendor_responsibilities,deliverables,evaluation_criteria, company_profile):
        self.requirement = requirement
        self.scope = scope
        self.expected_rfp_response = expected_rfp_response
        self.objective = objective
        self.company_profile = company_profile
        self.vendor_responsibilities=vendor_responsibilities
        self.deliverables = deliverables
        self.evaluation_criteria = evaluation_criteria
        self.summary_company_profile = ''
        self.summary_requirement = ''

    def summary_intro(self):
        chain = FallbackLLMChain(llm=chat_model, prompt=summary_prompt)
        response = chain({'expected_rfp_response':self.expected_rfp_response,
                        'requirement': self.requirement, 
                        'scope':self.scope,
                        'company_profile':self.company_profile,
                        }) 
        json_output = response['text']
        data_dictionary = json.loads(json_output)
        self.summary_company_profile += data_dictionary['company_profile']
        self.summary_requirement += data_dictionary['requirement']
        return data_dictionary
    
    def write_intro(self, expected_rfp_response, requirement, scope, name):
        chain = FallbackLLMChain(llm=chat_model, prompt=application_form_prompt)
        response = chain({'expected_rfp_response':expected_rfp_response,
                        'requirement': requirement, 
                        'scope':scope,
                        'company_name':name,
                        }) 
        output = response['text']
        return output
    
    # def write_intro(self, expected_rfp_response, requirement, scope, domain):
    #     examples = [
    #     {"input": intro_input.format(expected_rfp_response, requirement, scope, domain), "response": technical_form},
    #            ]

    #     final_prompt = create_final_prompt(examples, chat_model_16k)

    #     response = final_prompt.invoke({"input": intro_prompt.format(expected_rfp_response, requirement, scope, domain)})

    #     return response.content
    
    def intro_table(self, domain):
        table = [['No.', ' Firms', 'Address', 'Country of \nRegistration'], 
                 [1, domain, 'Please Provide', 'Please Provide'],
                 [2, '____', 'Please Provide', 'Please Provide'],
                 [3, '____', 'Please Provide', 'Please Provide'],
                 [4, '____', 'Please Provide', 'Please Provide']]
        
        return table
    
    def sign_table(self):
        table = [['Authorised Signature', '_______________________'], 
                 ['Name and title of Signatory', '_______________________'],
                 ['Name and Firm', '_______________________'],
                 ['Address', '_______________________']]
        return  table
    
    def organization_background_experience_chain(self, business_years,specialization_areas, certifications,past_projects,technology_stack):
        
        chain_one = FallbackLLMChain(llm=chat_model, prompt=organization_background_prompt, output_key="organization_background")
        
        chain_two = FallbackLLMChain(llm=chat_model, prompt=organization_experience_prompt, output_key="organization_experience")
        
        chain_three = FallbackLLMChain(llm=chat_model, prompt=achievements_recognitions_prompt, output_key="achievements_recognitions")

        overall_chain = SequentialChain(
                            chains=[chain_one, chain_two, chain_three], 
                            input_variables=["company_profile","summary_requirement", "objective", "business_years","specialization_areas", "certifications", "past_projects", "technology_stack"],
                            output_variables=["organization_background", "organization_experience","achievements_recognitions"],
                            verbose=True
                                        ) 
        response = overall_chain({'company_profile':self.company_profile,'summary_requirement':self.summary_requirement, 
                                  "objective":self.objective,"business_years":business_years, "specialization_areas":specialization_areas,
                                  "certifications":certifications,"past_projects":past_projects,"technology_stack":technology_stack}) 
        return response
    
    def language_proficiency(self):
        chain = FallbackLLMChain(llm=chat_model, prompt=language_proficiency_prompt)
        response = chain({'company_profile':self.company_profile, 'expected_rfp_response':self.expected_rfp_response}) 
        return response['text']    
    
    def intro_template(self, company_name):
        # Split the text into words
        words = self.summary_company_profile.split()

        # Group the words into groups of 5
        word_groups = [words[i:i+5] for i in range(0, len(words), 5)]

        # Create new lines for each group of words
        lines = [' '.join(group) for group in word_groups]

        # Combine the lines into the final formatted text
        formatted_text = '\n'.join(lines)
        header = f"{company_name}".center(len(formatted_text.split('\n')[0]))
        return  tabulate([[formatted_text]], headers=[header],  tablefmt="heavy_grid")
    
    def finacial_info(self, company_name):
        chain = FallbackLLMChain(llm=chat_model, prompt=financial_proposal_prompt)
        response = chain({
                         'company_name':company_name,
                        'scope':self.scope,
                        'requirement': self.requirement, 
                        }) 
        output = response['text']
        return output
    
    
    def cv_executive_summary(self):
        chain_one = FallbackLLMChain(llm=chat_model, prompt=introduction_prompt, output_key="introduction")
        # chain_two = FallbackLLMChain(llm=chat_model, prompt=overview_prompt, output_key="overview_technical_proposal")
        chain_two = FallbackLLMChain(llm=chat_model, prompt=business_context_prompt, output_key="business_context")

        
        overall_chain = SequentialChain(
                    chains=[chain_one, chain_two], 
                    input_variables=["summary_requirement", "objective", "summary_company_profile", "scope"],
                    output_variables=["introduction", "business_context"],
                    verbose=True
                                ) 
        response = overall_chain({'summary_requirement':self.summary_requirement,"objective":self.objective, 'summary_company_profile':self.summary_company_profile,
                                  "scope":self.scope}) 

        return response
    
    def project_understanding_section(self):
        chain_one = FallbackLLMChain(llm=chat_model, prompt=project_understanding_prompt, output_key="project_understanding")
        chain_two = FallbackLLMChain(llm=chat_model, prompt=client_insight_prompt, output_key="client_insight")
        chain_three = FallbackLLMChain(llm=chat_model, prompt=objective_and_goal_prompt, output_key="objective_and_goal")
        chain_four = FallbackLLMChain(llm=chat_model, prompt=comment_suggestion_prompt, output_key="comment_suggestion")

        
        overall_chain = SequentialChain(
                    chains=[chain_one, chain_two, chain_three, chain_four], 
                    input_variables=["summary_requirement", "objective", "scope", "expected_rfp_response", "summary_company_profile"],
                    output_variables=["project_understanding", "client_insight", "objective_and_goal", "comment_suggestion"],
                    verbose=True
                                ) 
        response = overall_chain({"summary_requirement":self.summary_requirement, "objective":self.objective, "scope":self.scope,
                                  'expected_rfp_response':self.expected_rfp_response,"summary_company_profile":self.summary_company_profile,
                                  }) 

        return response



        
        
        