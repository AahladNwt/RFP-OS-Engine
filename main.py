import sys
sys.path.append("..")
import os
import streamlit as st
from agent_tools.api_credentials import embeddings_model, rerank#, hugging_embeddings
from data_retrieval.database_loader import ChatBotManager
from loaders.reader import parse_docs
from introduction.background_intro import load_vendor_contractors_info
from introduction.intro_summary import ProposalIntoduction
from introduction.extract_info import CompanyProfile
from introduction.get_company_info import get_links
from approach_methodology.technical import app_method
from cv.cv_section import create_cv_section
from code_of_conduct.conduct import create_coc
from anti_bribery_policy.abp_coc import create_anti_bribery_undertaking
from toc.table_of_content import content
from prompt.prompts import (
                            code_of_conduct_query,
                            terms_and_conditions_prompt,
                            anti_bribery_coc_prompt,
                            )
from prompt.prompts import (requirements_qa,financial_requirements_qa, scope_qa, evaluation_criteria_qa, expected_rfp_response_qa,
                            budget_and_financials_qa, legal_and_contractual_qa,submission_guidelines_qa,
                            project_timeline_qa, vendor_responsibilities_qa, communication_and_reporting_qa,
                            objective_qa, deliverable_qa, qualification_qa,technical_requirement_qa,
                            project_duration_and_key_stages_qa, company_profile_qa, company_details_qa,
                            collaboration_and_preferences_qa,update_frequency_qa,problem_statement_or_opportunity_qa,
                            issuer_name_qa,roles_extraction_qa
                            )
from utils.util import SolutionEngine, VisulaizeRFP, paraphrase_text, company_parser
from project_management.management import ProjectManager
from agent_tools.special_agents import SpecialAgent
from implementation.implement import ImplementationManager
from financial_proposal.utils.finance_util import FinanceManager
from financial_proposal.executive_summary.exec_summary import financial_intro

os.environ["LANGCHAIN_TRACING"] = "true"

agent = SpecialAgent()

@st.cache_data
def load_files(rfpfile:str, orgfiles:str):
    if rfpfile is None or orgfiles is None:
        raise ValueError("Both file_path and company_path must be provided")
    print('Loading Files')
    company_docs = load_vendor_contractors_info(orgfiles)
    rfp_docs = parse_docs(rfpfile)
    # chatbot = ChatBotManager(rerank)
    # qa = chatbot.get_query_engine(document)
    # print('Successfully Done!!!')
    return company_docs, rfp_docs

@st.cache_data()
def get_intro(_company_docs, _rfp_docs, business_year:int=18):
    
    chatbot = ChatBotManager(rerank)

    information_list  = [requirements_qa, financial_requirements_qa,  scope_qa, evaluation_criteria_qa, expected_rfp_response_qa,
                    budget_and_financials_qa, legal_and_contractual_qa,submission_guidelines_qa,
                    project_timeline_qa, vendor_responsibilities_qa, communication_and_reporting_qa,
                    objective_qa, deliverable_qa, qualification_qa, technical_requirement_qa, 
                    project_duration_and_key_stages_qa, collaboration_and_preferences_qa,update_frequency_qa,
                    problem_statement_or_opportunity_qa,issuer_name_qa, roles_extraction_qa ]
    
    print("Comprehensive Inquiry for Extracting RFP Details: Requirements, Scope, Objectives, Evaluation Criteria and Expected RFP response.")
    result_dict = chatbot.parallel_process_inputs(information_list, _rfp_docs)
    print(result_dict)
    print(result_dict.keys())
    print("Extracting Company Information")
    # company_qa = _chatbot.get_query_engine(_company_docs)
    # print('Done loading company QA')
    company_info = chatbot.parallel_process_inputs((company_profile_qa,company_details_qa), _company_docs)
    
    company_profile, company_details = company_info.values()
    print('Successfully Extracted Company Info!!!')
    print('--------------------------------------------------------------------------------------------')
    print('Extracting Introduction section')
    proposal_intro = ProposalIntoduction(result_dict['requirement'],result_dict['scope'],
                                     result_dict['expected_rfp_response'],result_dict['objective'],
                                     result_dict['vendor_responsibilities'],result_dict['deliverable'],
                                     result_dict["evaluation_criteria"],
                                     company_profile)
    intro = proposal_intro.summary_intro()
    # full_response = intro["expected_response"]
    proposal_strings = [string for string in intro['expected_response'] if "Proposal" in string]
    if len(proposal_strings) != 0:
        intro['expected_response'] = proposal_strings
    print('Successfully Extracted  Inroduction!!!')
    print(company_details)
    print('--------------------------------------------------------------------------------------------')
    company_dict = company_parser(company_details)
    company_dict['Number of Years in Business'] = business_year
    
    print('Writting Introduction section')
    write_intoduction = proposal_intro.write_intro(intro['expected_response'], intro['requirement'], intro['scope'],'newwave')
    
    print("Extracting Organization Background and Experience")
    organization = proposal_intro.organization_background_experience_chain(*company_dict.values())
    
    print("Understanding of Project Section")
    project_understanding = proposal_intro.project_understanding_section()
    
    print("Display Table of Content!!!")
    toc = content(result_dict['requirement'], 
                        result_dict['expected_rfp_response'], 
                        result_dict['legal_and_contractual'],  )
    executive_summary = proposal_intro.cv_executive_summary()

    return proposal_intro, intro, result_dict, company_profile, company_details, write_intoduction, organization, project_understanding, toc, executive_summary


@st.cache_data
def get_partners(website):
    print('Extracting partners')
    urls,domain =  get_links(website)
    company = CompanyProfile()
    selenium_qa = company.company_qa(urls)
    query =  f"Extract  all the partners of {domain} and return your output as a Python list, and nothing more."
    partners = company.extract_info(selenium_qa, query)
    return partners, domain


# def get_comment_suggestion(**kwargs):
#     proposal_intro = kwargs['proposal_intro']
#     requirement = kwargs['requirement']
#     company_profile = kwargs['company_profile']
#     qa = kwargs['qa']
#     scope = kwargs['scope']
#     solution_engine = SolutionEngine(proposal_intro.summary_requirement, requirement, company_profile, scope)
#     sections = solution_engine.extraction_qa(comment_suggestion_qa, qa)
#     comment_suggestion = solution_engine.generate_rfp_feedback(sections )
#     return comment_suggestion, solution_engine

@st.cache_data
def get_biz_trends(_proposal_intro):
    trend_business = agent.trend_business_cases(_proposal_intro.summary_requirement) 
    
    return trend_business

@st.cache_data
def get_overview_of_our_approach(_proposal_intro, result_dict, _trend_business, company_profile):
    
   overview = app_method(_proposal_intro.summary_requirement,result_dict['objective'] ,result_dict['expected_rfp_response'], _trend_business,company_profile )

   solution_engine = SolutionEngine(_proposal_intro.summary_requirement, result_dict['requirement'],
                                 company_profile, result_dict['scope'], result_dict['objective'])
   proposal_expert = agent.solution_agents_search(_proposal_intro.summary_requirement) 
   
   break_sol = solution_engine.solution_chain(proposal_expert, result_dict['project_duration_and_key_stages'])
   
   return overview, solution_engine, proposal_expert, break_sol

@st.cache_data
def get_project_management(break_sol,_proposal_intro,result_dict,team_experience:str=''):
    management = ProjectManager(break_sol['proposed_solution'],
                            _proposal_intro.summary_requirement, 
                            result_dict['project_duration_and_key_stages'],
                            result_dict['objective'],
                            )
    # print('--------------------------------------------------------------------------------------------')
    # print(result_dict['objective'])
    # print('--------------------------------------------------------------------------------------------')
    # print(result_dict['project_duration_and_key_stages'])
    # print('--------------------------------------------------------------------------------------------')
    # print(result_dict['requirement'])
    
    
    project_management =  management.management_chain(team_experience=team_experience)
    return project_management

@st.cache_data
def get_project_implementation(break_sol,_proposal_intro,result_dict, key_stakeholders:str='' ):
    implementation = ImplementationManager(break_sol['proposed_solution'],
                                           break_sol['timeline_milestones'], 
                                           _proposal_intro.summary_requirement, 
                                           result_dict['objective'],
                                           result_dict['deliverable']
                            
                            )    
    implementation =  implementation.implementation_chain(key_stakeholders=key_stakeholders)
    
    return implementation

@st.cache_data
def get_financial_section(break_sol, _proposal_intro,result_dict, project_name, domain='newwave' ):

    financial_intoduction = financial_intro(_proposal_intro.summary_company_profile,
                                    result_dict['objective'],
                                    result_dict['budget_and_financials'],
                                    result_dict['scope'])
    
    manager = FinanceManager(_proposal_intro.summary_company_profile, 
                         result_dict['objective'],
                         result_dict['problem_statement'],
                         _proposal_intro.summary_requirement,
                         result_dict['scope'],
                         result_dict['client_company_name'],
                         break_sol["proposed_solution"],
                         result_dict['project_timeline'],
                         result_dict['project_duration_and_key_stages'],
                         result_dict['deliverable'],
                         )
    costing_breakdown_dict = manager.direct_cost(domain, project_name)
    
    item_cost_summary = agent.proposal_pricing(_proposal_intro.summary_requirement, costing_breakdown_dict['items'])

    indirect_costing = manager.indirect_cost(project_name)
    
    return financial_intoduction, costing_breakdown_dict, item_cost_summary, indirect_costing

#def get_pricing_model(proj_understand, result):


def get_soln_break(solution_engine, 
                    proposal_expert, approach_methodology, proposed_work):
    break_sol = solution_engine.make_chain(proposal_expert, approach_methodology, proposed_work)

    Proposed_solution = break_sol['Proposed_solution']
    Solution_breakdown = break_sol['Solution_breakdown']
    Benefits_outcome = break_sol['Benefits_outcome']
    Differentiators = break_sol['Differentiators']
    implementation_plan = break_sol['implementation_plan']
    items = break_sol['items']

    return (Proposed_solution, Solution_breakdown, Benefits_outcome,
                            Differentiators, implementation_plan, items)


def get_cv_n_coc(solution_engine, company_profile, qa):
    cv_text = paraphrase_text()
    cv = create_cv_section('NewWave', cv_text)
    print("Comprehensive Code of Conduct")
    coc = solution_engine.extraction_qa(code_of_conduct_query, qa)
    coc_response = create_coc(coc)
    terms_anti_bribery_coc = solution_engine.extraction_qa(anti_bribery_coc_prompt, qa)
    anti_bribery_undertaking = create_anti_bribery_undertaking(company_profile, terms_anti_bribery_coc)
    
    
    return cv, coc_response, anti_bribery_undertaking


def get_terms_n_cond(solution_engine, proposed_work, proposal_intro, qa):
    
    terms_and_conditions = solution_engine.extraction_qa(terms_and_conditions_prompt, qa)
    proposal_securing_declaration = solution_engine.psdf_spoa(terms_and_conditions)
    special_power_attorney = proposal_securing_declaration['special_power_attorney']
    proposal_securing_declaration = proposal_securing_declaration['proposal_securing_declaration']
    #items = solution_engine.items(proposed_work)  
    
    return proposal_securing_declaration, special_power_attorney



def get_cost_fin_analyis(solution_engine,special_agent,
                            proposal_intro, items,
                            domain):

    financial_proposal = proposal_intro.finacial_info(domain)
    
    item_cost_summary = special_agent.proposal_pricing(proposal_intro.summary_requirement, items)
    #cost = solution_engine.pricing(item_cost_summary)
    
    pricing = solution_engine.pricing(item_cost_summary)
    cost = pricing['text']
    #print('BREAKDOWN OF REMUNERATION')
    
    return financial_proposal, cost


def get_exec_summanry_n_action(solution_engine,
                        Proposed_solution, implementation_plan, items):
    #display(Markdown("### Call to Action"))
    exe_summary = solution_engine.executive_summary(Proposed_solution, implementation_plan, items)
    action_call = solution_engine.call_to_action(exe_summary['text'])

    return exe_summary['text'], action_call