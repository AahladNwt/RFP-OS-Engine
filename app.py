import sys
sys.path.append("..")
import utils
import ast
import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import tabulate as tb
import markdown as md
import os
#os.environ["OPENAI_API_KEY"] = "False"
def start():

    st.set_page_config(
        )
    icon, title = st.columns([3, 20])
    with icon:
        st.image('image.png')
    with title:
        st.title('RFP AI System')
start()

def open_ai_key():
    
    cont = st.container()
    pl = st.sidebar.empty()
    submitted = False
    with cont:
        with pl.form("APIKey"):
            
            openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password").strip()
            "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"
            st.info("Please add your OpenAI API key to continue.")
            submitted =  st.form_submit_button('Submit')
            if submitted:
                with st.spinner('Processing...'):
                    os.environ["OPENAI_API_KEY"] = openai_api_key
                    st.success("System Acitive")

try:
    key = os.environ["OPENAI_API_KEY"]
    print("OpenAI API KEY Found")
    
except KeyError:
    open_ai_key()
    st.stop()

from utils import util as ut


from langchain.chat_models import ChatOpenAI
#from IPython.display import display, Markdown
from agent_tools.api_credentials import embeddings_model#, hugging_embeddings
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
from top_companies.top_5_companies import TopFiveCompanies

from utils.util import SolutionEngine, VisulaizeRFP, paraphrase_text, clean_response
from agent_tools.special_agents import SpecialAgent
os.environ["LANGCHAIN_TRACING"] = "true "
from main import (get_intro, get_partners, get_biz_trends, get_overview_of_our_approach,
                    get_cost_fin_analyis, get_exec_summanry_n_action, get_cv_n_coc,
                    get_soln_break, get_terms_n_cond, load_files,get_project_management,
                    get_project_implementation
                    )
from timeline_schedule.timeline_milestone import project_timeline
import dotenv
dotenv.load_dotenv()


st.session_state['outputs'] = " "

def start_page():
    st.session_state['outputs'] += "\n" + """<div class="page-break"></div>"""

from utils.html_util import table_css, page_style

def tab_to_html(tab):
    css = table_css
    css = table_css
    tab_html = tab.to_html(classes='my-table-class', index=False)
    
    html_with_css = f"<style>{css}</style>{tab_html}"
    
    return html_with_css

def extend_ouput(text, raw=False):
    if raw == True:
        st.session_state['outputs'] += "\n\n" + text + "\n "
    else:
        st.session_state['outputs'] += "\n\n" + md.markdown(text) + "\n "
def mark_page():
    st.session_state['outputs'] += md.markdown('---------------------------------------------------------------------------------------------------------')

import openai
import asyncio
if __name__ == '__main__':

    @ut.on_files    
    #@st.cache(suppress_st_warning=True)
    def request_comp_details():
        import time
        import regex as re
        def validate(waddress):
            if re.match(r"^https?:\/\/[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\/?$", waddress):
                return True
            return False
        
        container =  st.container()
        with container:
            pholder = st.empty()
            with pholder.form("CompDetails"):
                st.write("Company Details")
                compname = st.text_input('Company Name', placeholder='google').strip()
                website = st.text_input("Website", placeholder="https://google.com/").strip()
                
                submitted = st.form_submit_button('Submit')
                if submitted:
                    if not validate(website):
                        st.sidebar.warning("Invalid URL: URL must be in the form with 'https://url.com' ot 'http://url.com'")
                        st.stop()
                    st.session_state['compurl'] = website
                    st.session_state['compname'] = compname
                    if not compname:
                        st.stop()
                    print("Submitted")
                    with st.spinner():
                        time.sleep(1)
                        st.success("Accepted")
                    #pholder.empty()
        

        st.sidebar.title(compname)
        st.sidebar.write(website)
        
  
        
    async def get_rfp():
        rfp_docs = st.file_uploader(
            label="##### Here, upload your RFP document",
            key="rfp_docs_uploader"  # Unique key for this file uploader

        )
        return rfp_docs
    
    async def get_vendr():
        rfp_docs = await get_rfp()
        org_docs = st.file_uploader(
            label="##### Here, upload your Organisational documents",
            type='pdf',
            accept_multiple_files=True,

        )
        return rfp_docs, org_docs

    def request_files(rfp_docs, org_docs) -> None:
        import tempfile
        rfp_docs_uploaded = False
        org_docs_uploaded = False

        if rfp_docs:
            rfp_docs_uploaded = True
            with tempfile.NamedTemporaryFile(delete=False) as tpfile:
                tpfile.write(rfp_docs.getvalue())
                st.session_state['rfpfile'] = tpfile.name
        if org_docs:
            org_docs_uploaded = True
            orgfile_names = []
            for doc in org_docs:
                with tempfile.NamedTemporaryFile(delete=False) as tpfile:
                    tpfile.write(doc.getvalue())
                    orgfile_names.append(tpfile.name)
            st.session_state['orgfiles'] = orgfile_names
            # Get the directory of the first org document.
            
        if rfp_docs_uploaded and org_docs_uploaded:
            with st.spinner("Loading Files"):
                rfpfile = st.session_state.get('rfpfile')
                orgfiles = st.session_state.get('orgfiles')
        else:
            if not rfp_docs_uploaded:
                st.warning("Please upload your RFP document.")
            if not org_docs_uploaded:
                st.warning("Please upload your Organisational documents.")
            st.stop()
        company_docs, rfp_docs = load_files(rfpfile, orgfiles)
        st.session_state['company_docs'] = company_docs
        st.session_state['rfp_docs'] = rfp_docs
        # st.session_state['qa'] = qa
        
        return company_docs, rfp_docs #qa # True
    
    request_comp_details()
    rfp_docs, org_docs = asyncio.run(get_vendr())
    with st.spinner("Wait while we put your files in place"):
        company_docs, rfp_docs = request_files(rfp_docs, org_docs)
        st.success("There you go, you can now generate your RFP response")
    
    try:
        state = st.button("Generate Proposal")
        
        #Initialize Generate Proposal state
        if "Generate Proposal" not in st.session_state:
            st.session_state['Generate Proposal'] = False
                        
        if state or st.session_state['Generate Proposal']:
            with st.spinner("Generating Responses"):
                print("Got Files")   
                proposal_intro, intro, result_dict, company_profile, company_details, write_intoduction, organization, project_understanding, toc, executive_summary = get_intro(company_docs, rfp_docs) 
                print('TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT')
                print(result_dict)
                print('-------------------------------------------------------------------')
                st.markdown(toc)
                extend_ouput(toc)
                st.markdown('----------------------------------------------------------------------------------------------')
                mark_page()

                
                # partners, domain = get_partners(st.session_state.get('compurl'))
                domain = 'newwave'
                print('-------------------------------------------------------------------')
                print('Write Application Form')
                intro_table = proposal_intro.intro_table(domain) 
                sign_table = proposal_intro.sign_table()
                
                @ut.on_intro
                def display_intro(partners=None, intro_text=None, intro_table=None, sign_table=None):
                    
                    """
                    displays proposal intro data as table on UI

                    text: [str] : intro writeup
                    table: [pd.dataframe| list[list] | ] : eg. introtable = [['No.', 'Consulting Firms', 'Address', 'Country of \nRegistration'], 
                                                                    [1, 'NewWave Zanzibar', 'Please Provide', 'Zanzibar'],
                                                                    [2, 'Proxima Consultancy', 'Please Provide', 'Tanzania']]

                            if list[list] first row will be treated as header
                    signtable: [pd.dataframe| list[list] | ] : e.g signtable = [['Authorised Signature', ' '], 
                                                                    ['Name and title\n of Signatory', '  '],
                                                                    ['Name and Firm', '  '],
                                                                    ['Address', ' ']]

                    """

                    start_page()
                    text = intro_text
                    
                    if text != None:
                        st.markdown(text)
                        st.session_state['outputs'] += md.markdown(text) + "\n "

                    if intro_table != None:
                        table = intro_table
                        if type(table) == list:
                            table = pd.DataFrame(intro_table)
                            table.columns = table.iloc[0]
                            table = table.iloc[1:]
                        st.table(table)
                        st.session_state['outputs'] += '\n\n' + tab_to_html(table)

                    if sign_table != None:
                        table = sign_table
                        if type(sign_table) == list:
                            table = pd.DataFrame(sign_table)
                            table.columns = ['    ', ' ']
                            
                        st.table(table)
                        st.session_state['outputs'] += '\n\n' + tab_to_html(table)

                    if partners != None:
                        
                        st.markdown(partners)
                        st.session_state['outputs'] += "\n\n" + md.markdown(partners)
                    st.markdown('----------------------------------------------------------------------------------------------')
                    
                    mark_page()

                st.markdown("### 2. Cover Letter & Executive Summary")
                display_intro(text=write_intoduction, intro_table=intro_table, sign_table=sign_table)
                
                
                @ut.on_prelima
                def display_cv_exec_sum(exec_sum):
                    start_page()
                    st.session_state['outputs'] += md.markdown("### 2. Cover Letter & Executive Summary")
                    intro = exec_sum["introduction"]
                    # overview_tech_prop = exec_sum['overview_technical_proposal']
                    business_context = exec_sum['business_context']

                    st.markdown(intro)
                    extend_ouput(intro)

                    # st.markdown(overview_tech_prop)
                    # extend_ouput(overview_tech_prop)
                    start_page()

                    st.markdown(business_context)
                    extend_ouput(business_context)

                    mark_page()

                display_cv_exec_sum(executive_summary)
                
                st.markdown("### 3. Company Overview")
                org_backgd = organization['organization_background']
                
                org_exp = organization['organization_experience']
                print('UUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUU')
                #print(clean_response(org_exp))

                org_arch = organization['achievements_recognitions']
                
                
                @ut.on_background
                def display_cbg(org_bg=None, org_exp=None, lang_prof=None, org_arch=None):
                    """ 
                    Displays the organisation background from the model

                    pg_output: [str] Organisation Background
                    pt_out: [str] partners

                    returns None
                    """
                    start_page()
                    import ast
                    import pandas as pd

                    def dedict(d):
                        return ' || '.join([f"{k}: {v}" for k, v in d.items()])

                    def delist(l):
                        return ' | '.join(l)
                    st.session_state['outputs'] += md.markdown("### 3. Company Overview")
                    if org_bg != None:
                        
                        st.markdown(org_bg)
                        extend_ouput(org_bg)
                        
                    start_page()
                    
                    if org_exp != None:
                        st.markdown("### 3.2 Organization Experience")
                        extend_ouput("### 3.2 Organization Experience")
                    
                        
                        # Your JSON data
                        # st.write(org_exp)
                        org_exp = ast.literal_eval(org_exp) 
                        org_exp = org_exp['Organization Experience']
                        import numpy as np

                        # Extracting the 'Analogous Ventures' data
                        def bold(s):
                            return "**" + s + "**"
                        
                        def tab_to_output(tab):
                            st.session_state['outputs'] += "\n\n" + tab_to_html(tab)


                        for org in org_exp.keys():
                            val = org_exp[org]
                            if ut.islistofdict(val):
                                st.markdown(bold(org))
                                extend_ouput(bold(org))

                                vals = ut.normalize(val)
                                df = pd.DataFrame(vals)
                                st.table(df)
                                tab_to_output(df)
                                
                                
                            elif ut.islistoflist(val):
                                st.markdown(bold(org))
                                extend_ouput(bold(org))
                                vals = ut.normalize(val)
                                cols = list(range(len(vals)))
                                df = pd.DataFrame(vals, columns=cols)
                                st.table(df)
                                tab_to_output(df)
                                
                                
                            elif isinstance(val, dict):
                                st.markdown(bold(org))
                                extend_ouput(bold(org))
                                v = list(val.values())
                                df = pd.Series(v).to_frame()
                                df.index = list(val.keys())
                                df = df.to_frame()
                                st.table(df)
                                tab_to_output(df)
                                    
                            elif isinstance(val, list):
                                
                                st.markdown(bold(org))
                                extend_ouput(bold(org))

                                df = pd.Series(val)
                                df.name = org
                                df = df.to_frame()
                                st.table(df)
                                tab_to_output(df)
                                
                            elif isinstance(val, str):
                                st.markdown(bold(org))
                                extend_ouput(bold(org))

                                st.markdown(val)
                                extend_ouput(val)
                        
                    start_page()
                        
                    if lang_prof != None:
                    
                        st.markdown(lang_prof)
                        st.session_state['outputs'] += "\n\n" + md.markdown(lang_prof)

                    if org_arch != None:
                    
                        st.markdown(org_arch)
                        st.session_state['outputs'] +=  "\n\n" + md.markdown(org_arch)

                    
                    mark_page()
                display_cbg(org_bg=org_backgd, org_exp=org_exp, org_arch=org_arch)


                @ut.on_prelima
                def display_project_und(proj_und):
                    
                    start_page()
                    #st.markdown("### 4. Understanding of the Project")
                    st.session_state['outputs'] += md.markdown("### 4. Understanding of the Project")
                    st.markdown(proj_und['project_understanding'])
                    extend_ouput(proj_und['project_understanding'])
                    
                    start_page()
                    st.markdown(proj_und['client_insight'])
                    extend_ouput(proj_und['client_insight'])
                    
                    start_page()
                    st.markdown(proj_und['objective_and_goal'])
                    extend_ouput(proj_und['objective_and_goal'])
                    
                    start_page()
                    st.markdown(proj_und['comment_suggestion'])
                    extend_ouput(proj_und['comment_suggestion'])

                    mark_page()

                display_project_und(project_understanding)

                def display_biz_trend(texts=None):
                    """
                    displays the business trend
                    texts: [str] text output from models

                    return None
                    """
                    start_page()
                    if texts != None:
                        extend_ouput("#### 4.4 Trend and Business Cases")

                        st.markdown(texts)
                        extend_ouput(texts)
                        
                    mark_page()

                trend_business = get_biz_trends(proposal_intro)
                
                st.markdown("### 4.4 Trend and Business Cases")
                display_biz_trend(trend_business)
                print('NNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNN')
                print(trend_business)
                
                start_page()
                overview, solution_engine, proposal_expert, break_sol = get_overview_of_our_approach(proposal_intro, result_dict, trend_business, company_profile)
                st.markdown('### 5. Approach & Methodology')
                st.session_state['outputs'] += md.markdown("### 5. Approach & Methodology")
                st.markdown(overview)
                extend_ouput(overview)
                start_page()
                
                st.markdown('-----------------------------------------------------------------------------------------------------------------')


                def display_soln(sln_break):
                    start_page()

                    prop_sol = sln_break['proposed_solution']
                    st.markdown(prop_sol)
                    extend_ouput(prop_sol)
                    
                    start_page()
                
                    #st.markdown('#### Solution Components and Breakdown')
                    sol_com = sln_break['solution_components']
                    st.markdown(sol_com)
                    extend_ouput(sol_com)
                    
                    start_page()

                    #st.markdown('#### Tools and Technologies Utilized (if applicable)')
                    tool_tech = sln_break['tool_technology']
                    st.markdown(tool_tech)
                    extend_ouput(tool_tech)
                    
                    start_page()

                    print('-------------------------------------------------------------------')
                    #st.markdown('#### Benefits and Outcomes of Our Approach and Methodology')
                    benefit = sln_break['benefits_outcome']
                    st.markdown(benefit)
                    extend_ouput(benefit)
                    
                    start_page()

                    print('-------------------------------------------------------------------')
                    #st.markdown("#### What Differentiates Us From The Rest")
                    diff = sln_break['differentiators']
                    st.markdown(diff)
                    extend_ouput(diff)

                display_soln(break_sol)
                
                project_implementation = get_project_implementation(break_sol,proposal_intro,result_dict )

                def display_project_imp(project_implementation):
                    over_tab, del_tab, timeline, resource = ut.process_implementation(project_implementation)
                    
                    mark_page()
                    start_page()
                    st.markdown(project_implementation['implementation_plan'])
                    extend_ouput(project_implementation['implementation_plan'])

                    start_page()
                    mark_page()

                    #st.markdown(project_implementation['key_stages_and_phases'])
                    
                    extend_ouput('#### Key Stages and Phases')
                    """**Overview**"""
                    extend_ouput("""**Overview**""") 
                    
                    st.table(over_tab)
                    st.session_state['outputs'] += tab_to_html(over_tab)


                    """**Deliverables**"""
                    extend_ouput("""**Deliverables**""")


                    st.table(del_tab)
                    st.session_state['outputs'] += tab_to_html(del_tab)

                    """**Timeline**"""
                    extend_ouput("""**Timeline**""")
                    st.table(timeline)
                    #values = timeline[['Key', 'Value']].values
                    #tme_html = ut.build_timeline(values)
                    #extend_ouput(tme_html, raw=True)
                    st.session_state['outputs'] += tab_to_html(timeline)
                    
                    start_page()
                    mark_page()
                    st.markdown('#### Resource Allocation and Dependencies')
                    extend_ouput('Resource Allocation and Dependencies')

                    allocation = resource['Resource_Allocation']

                    """**Resource Allocation**"""
                    extend_ouput("""**Resource Allocation**""")
                    allocate_tab = pd.DataFrame(allocation)
                    st.table(allocate_tab)
                    st.session_state['outputs'] += tab_to_html(allocate_tab)

                    dependencies = resource['Dependencies']

                    """**Dependencies**"""
                    extend_ouput("""**Dependencies**""")
                    depend_tab = pd.DataFrame(dependencies)
                    st.table(depend_tab)
                    st.session_state['outputs'] += tab_to_html(depend_tab)

                    mark_page()
                display_project_imp(project_implementation)

                def display_contigenc():

                    start_page()
                    print('Contingency Measures and Pre-requisites')
                    extend_ouput('Contingency Measures and Pre-requisites')
                    st.markdown('Contingency Measures and Pre-requisites')
                    st.markdown(project_implementation['contingency_measures'])
                    extend_ouput(project_implementation['contingency_measures'])
                    mark_page()

                display_contigenc()
                management = get_project_management(break_sol,proposal_intro,result_dict)

                def display_strategy():
                    start_page()
                    st.markdown("#### 7.2 Our Communication Strategy")
                    extend_ouput("#### Our Communication Strategy")

                    communication_strategy = management['communication_strategy']
                    st.markdown(communication_strategy)
                    extend_ouput(communication_strategy)
                    mark_page()
                
                def display_risk():
                    start_page()
                    st.markdown("#### 7.3  Our Risk Management Approach")
                    extend_ouput("#### Our Risk Management Approach")
                    risk_management = management['risk_management']
                    st.markdown(risk_management)
                    extend_ouput(risk_management)

                    mark_page()
                    
                display_strategy()
                display_risk()

                def display_work():
                    start_page()
                    st.markdown("#### 7.4 Anticipated Work Schedule and Plan")
                    extend_ouput("#### Anticipated Work Schedule and Plan")

                    work_schedule = management['work_schedule']
                    print('---------------------------------------------------')
                    print(work_schedule)
                    print('---------------------------------------------------')

                    # workplan = ast.literal_eval(work_schedule)
                    workplan = clean_response(work_schedule)

                    name = workplan['Project_Name']
                    duration = workplan['Total_Duration']
                    tasks = workplan['Tasks']
                    sum = pd.DataFrame({'Project Name': name, "Total Duration": duration}, index=[' '])
                    # st.markdown(work_schedule)

                    st.table(sum)
                    st.session_state['outputs'] += "\n" + sum.to_html()
                    
                    task_tab = pd.DataFrame(tasks)
                    st.table(task_tab)
                    st.session_state['outputs'] += "\n\n" + tab_to_html(task_tab)

                    mark_page()
                    return name
                
                project_name = display_work()

                def display_time_n_delive():
                    start_page()

                    # import ast
                    main_deliverables = project_timeline(result_dict)
                    st.session_state['outputs'] += md.markdown("### 8. Timeline and Schedule")
                    st.markdown("### 8. Timeline and Milestones")

                    timeline = break_sol['timeline_milestones'] 
                    st.markdown(timeline)
                    extend_ouput(timeline)

                    start_page()
                    st.markdown("#### 8.2 Main Deliverables and Deadlines")
                    extend_ouput("#### Main Deliverables and Deadlines")

                    #st.markdown(main_deliverables)     
                    
                    deliverables =  clean_response(main_deliverables)
                    name = deliverables['Project_Name']
                    duration = deliverables['Total_Duration']
                    delvs = deliverables['Main_Deliverables']

                    sum = pd.DataFrame({'Project Name': name, "Total Duration": duration}, index=[' '])  
                    st.table(sum)
                    st.session_state['outputs'] += "\n" + sum.to_html()
                    
                    del_tab = pd.DataFrame(delvs)
                    st.table(del_tab)
                    st.session_state['outputs'] += "\n" + tab_to_html(del_tab)

                    mark_page()

                display_time_n_delive()
            
            
# #############################################################  Financial Proposal ###########################################################
                from main import get_financial_section
                from prompt.prompts import finance_toc
                from utils import html_util as hu
                from financial_proposal.utils import finance_util as fut

                start_page()
                fin_section = hu.section_title.format('Financial Proposal')
                extend_ouput(fin_section, raw=True)

                print('Financial Proposal Table of Content')
                st.markdown('## Financial Proposal Table of Content')
                extend_ouput('## Financial Proposal Table of Content')
                
                st.markdown(finance_toc)
                extend_ouput(finance_toc)
                
                #get project_name from #Anticipated Work Schedule and Plan section
                financial_intoduction, costing_breakdown_dict, item_cost_summary, indirect_costing = get_financial_section(break_sol,proposal_intro,result_dict, project_name, domain='newwave')
                
                print("#### 1. Executive Summary")
                print('- 1.1 Introduction')
                #print(financial_intoduction)

                def fin_prop(financial_intoduction, overview=None):
                    start_page()
                    st.markdown('### 1. Executive Summary')
                    extend_ouput('### 1. Executive Summary')

                    st.markdown("## 1.1 Introduction")
                    extend_ouput("## 1.1 Introduction")

                    st.markdown(financial_intoduction)
                    extend_ouput(financial_intoduction)

                    mark_page()
                
                    if overview != None:
                            start_page()
                            st.markdown('### 2. Understanding of the Project Scope')
                            extend_ouput('### 2. Understanding of the Project Scope')

                            st.markdown(overview['overview'])
                            extend_ouput(overview['overview'])

                            mark_page()
                        
                fin_prop(financial_intoduction)
            
                def display_cost_break():
                    start_page()
                    
                    st.markdown('# 2. Costing Breakdown')
                    extend_ouput('# 2. Costing Breakdown')

                    cost_intro = costing_breakdown_dict['costing_breakdown_intro']
                    st.markdown(cost_intro)
                    extend_ouput(cost_intro)

                    st.markdown('## 2.1 Direct Costs')
                    extend_ouput('## 2.1 Direct Costs')

                    # text,table and graph
                    # Display Labor cost table
                    # plot dist of Labor costs, cost per hourly rate
                    st.markdown('### 2.1.1 Labor Costs')
                    extend_ouput('### 2.1.1 Labor Costs')
                    labout_costs = costing_breakdown_dict['labor_costs_text']
                    st.markdown(labout_costs)
                    extend_ouput(labout_costs)
                    # text
                    cost_data = costing_breakdown_dict['labor_costs_table']
                    # process it

                    if isinstance(item_cost_summary, str):
                        cost_data = ast.literal_eval(cost_data)
                    try:
                        df = pd.DataFrame(cost_data['labor_costs'])
                    except:
                        
                        df = pd.DataFrame(cost_data['roles'])
                    
                    st.write(df.T)
                    #df = df.rename({'index':'role'}, axis=1)
                    try:
                        figures = fut.make_cost_plots(df)
                    except KeyError:
                        figures = fut.make_cost_plots(df.T)
                    for name, fig in figures.items():
                        print(name+":")
                        figpath = ut.display_viz(fig)
                        fightml = ut.wrap_img_html(figpath)
                        extend_ouput(fightml, raw=True)

                    #print(costing_breakdown_dict['roles_hourly_rate'])  # bar chat hourly rate vs labor
                display_cost_break()

                def make_item_mat_plots(item_cost_summary):
                    print('### 2.1.2 Materials and Equipment') # text,table and Visual
                    st.markdown('### 2.1.2 Materials and Equipment')
                    extend_ouput('### 2.1.2 Materials and Equipment')

                    cost_break = costing_breakdown_dict['materials_equipment_intro']  # text
                    st.markdown(cost_break)
                    extend_ouput(cost_break)
                    

                    
                    if ut.islistofdict(item_cost_summary):# tab
                        items_cost_summary_tab  = pd.DataFrame(item_cost_summary)
                        
                    elif isinstance(item_cost_summary, str):
                        item_cost_summary_temp = f'[{item_cost_summary}]'
                        item_cost_summary = ast.literal_eval(item_cost_summary_temp)
                        items_cost_summary_tab  = pd.DataFrame(item_cost_summary)
                    
                    
                    st.table(items_cost_summary_tab)
                    st.session_state['outputs']  += '\n\n' + tab_to_html(items_cost_summary_tab)
                    
                    # Generate Item Images
                    n = np.random.randint(1, items_cost_summary_tab.shape[1])
                    item1 =items_cost_summary_tab['Item Name'].iloc[n]
                    #item1 = "QuickBooks Online order processing software" 
                    
                    i = n
                    while i == n:
                        i = np.random.randint(1, items_cost_summary_tab.shape[1])
                        item2 = items_cost_summary_tab['Item Name'].iloc[i]
                    #item2 = "TEKLYNX barcode labeling software for GS1 DataBar barcodes" #items_cost_summary_tab['Item Name'].iloc[i]

                    with st.spinner(f'Generate image of {item1}'):
                        img_1url = ut.generate_image(item1)  # visual like two items, generate with image_generator function in util.py. remember to replace pick any item with actual item
                        
                        from PIL import Image
                        import requests
                        data = requests.get(img_1url).content 
                        cwd = os.getcwd()
                        img1_path = cwd + "//first_image.png"
                        fp = open(img1_path,'wb')
                        # Storing the image data inside the data variable to the file 
                        fp.write(data) 
                        fp.close()
                        img1 = Image.open(img1_path)
                        
                        st.image(img1, caption=item1, use_column_width=False)

                        extend_ouput(item1)
                        extend_ouput(ut.wrap_img_html(img1_path), raw=True)

                    with st.spinner(f'Generate image of {item2}'):
                        img_2url = ut.generate_image(item2)  # visual like two items, generate with image_generator function in util.py. remember to replace pick any item with actual item
                        data = requests.get(img_2url).content 
                        cwd = os.getcwd()
                        img2_path = cwd + "//second_image.png"
                        fp = open(img2_path,'wb')
                        # Storing the image data inside the data variable to the file 
                        fp.write(data) 
                        fp.close()
                        img2 = Image.open(img2_path)
                        st.image(img2, caption=item2, use_column_width=False)

                        extend_ouput(item2)
                        extend_ouput(ut.wrap_img_html(img2_path), raw=True)

                ### USING A SAMPLE WELL FORMATTED COST SUMMARY
                #item_sample = ut.sample_items_cost_summary ### REMEMBER TO DELETE AFTER TESTING
                try:

                    make_item_mat_plots(item_cost_summary)
                except Exception as e:
                    err =  str(e)
                    print(e)

                    from PIL import Image
                    cwd = os.getcwd()
                    #st.write(item_cost_summary)
                    # item 1
                    img1_path = cwd + "//first_image.png"
                    img1 = Image.open(img1_path)
                    st.image(img1, use_column_width=False)
                    #extend_ouput(item1)
                    extend_ouput(ut.wrap_img_html(img1_path), raw=True)

                    # item 2
                    
                    img2_path = cwd + "//second_image.png"
                    img2 = Image.open(img2_path)
                    st.image(img2, use_column_width=False)
                    #extend_ouput(item2)
                    extend_ouput(ut.wrap_img_html(img2_path), raw=True)
                    st.warning(err)

                def display_softawre_license():
                    start_page()
                    st.markdown('### 2.1.3 Software and Licensing Fees')
                    extend_ouput('### 2.1.3 Software and Licensing Fees') # text,table

                    license_text = costing_breakdown_dict['software_licensing_text']  # text
                    st.markdown(license_text)
                    extend_ouput(license_text)

                    license_data = costing_breakdown_dict['software_licensing_table']  # table
                    if ut.islistofdict(license_data):
                        license_tab = pd.DataFrame(license_data)
                    elif isinstance(license_data, dict):
                        license_tab = pd.DataFrame(license_data)
                    elif isinstance(license_data, str):
                        try:
                            license_data = ast.literal_eval(license_data)
                            license_tab = pd.DataFrame(license_data)
                        except Exception as e:
                            err =  str(e)
                            st.warning(err)
                            st.write(license_data)
                    try:

                        st.table(license_tab)
                        st.session_state['outputs'] += '\n\n' + tab_to_html(license_tab)
                    except NameError:
                        pass
                    
    
                display_softawre_license()

                def display_indirect():

                    st.markdown('## 2.2 Indirect Costs')
                    st.markdown('## 2.2.1 Overheads') # text,table and graph
                    st.markdown('## 2.1.3 Software and Licensing Fees') # text,table
                    extend_ouput('## 2.2 Indirect Costs')
                    extend_ouput('## 2.2.1 Overheads') # text,table and graph
                    extend_ouput('## 2.1.3 Software and Licensing Fees') #
                    overhead_text = indirect_costing['overheads_text']

                    st.markdown(overhead_text)  # text
                    extend_ouput(overhead_text)
                    overhead_data = indirect_costing['overheads_table']
                    
                    if isinstance(overhead_data, str):
                        overhead_data = ast.literal_eval(overhead_data)

                    overhead_tab = pd.DataFrame(overhead_data["overhead_costs"])
                    st.table(overhead_tab)
                display_indirect()

            
#     ####################################################################################################################
            
                if st.session_state.get('exec_summary_md'):
                    outputs = st.session_state.get('exec_summary_md') + st.session_state.get('outputs')
                else:
                    outputs = st.session_state.get('outputs')

                all_outputs = page_style(outputs) 
                
                if all_outputs !=None:
                    st.download_button(
                        "Download as HTML",
                        all_outputs,
                        "rfp.html"
                    )
                    n = np.random.randint(0,50)
                    
                    import pdfkit
                    config = pdfkit.configuration(wkhtmltopdf='C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe')
                    pdfkit.from_string(all_outputs, 
                                        output_path=f'rfp_output{n}.pdf',
                                        options = {
                                                    'page-size': 'A4',
                                                    'margin-top': '0.75in',
                                                    'margin-right': '0.75in',
                                                    'margin-bottom': '0.75in',
                                                    'margin-left': '0.75in',
                                                    'encoding': "UTF-8",
                                                    "enable-local-file-access": ""},
                                        configuration=config)
                    st.success("Saved as PDF")

        
    except openai.error.APIError as oe:
        st.warning("OpenAI Error! \nFull detail logged into record")
        with open("log.txt", 'a+') as fp:
            err = str(oe)
            fp.write(err)