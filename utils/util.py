import sys
sys.path.append("..")
from tabulate import tabulate
import json
import requests 
from PIL import Image 
import openai

from langchain.chains import SequentialChain
from langchain.chains import LLMChain
from langchain.schema import LLMResult
from typing import Any, Dict, List, Optional, Union, cast
from marshmallow import ValidationError
from langchain.callbacks.manager import (
    AsyncCallbackManagerForChainRun,
    CallbackManagerForChainRun,
)
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI

import streamlit as st

import os


#@st.cache_data


#if not os.environ["OPENAI_API_KEY"] == "False":
 #   st.stop()

from langchain.agents import initialize_agent
from data_retrieval.database_loader import ChatBotManager
from agent_tools.api_credentials import chat_model, llm



from prompt.prompts import (
                            price_prompt,
                            item_prompt,
                            call_to_action_prompt,
                            cv_prompt,
                            proposal_securing_declaration_prompt,
                            special_power_attorney_prompt,
                            proposed_solution_prompt,
                            solution_components_prompt,
                            tools_and_technology_prompt,
                            benefits_prompt,
                            differentiators_prompt,
                            timeline_milestones_prompt,
                            implementation_plan_prompt,
                            # executive_summary_prompt
                            )



CBManager = Union[AsyncCallbackManagerForChainRun, CallbackManagerForChainRun]

class FallbackLLMChain(LLMChain):
    """Chain that falls back to synchronous generation if the async generation fails."""

    async def agenerate(
        self,
        input_list: List[Dict[str, Any]],
        run_manager: Optional[CBManager] = None,
    ) -> LLMResult:
        """Generate LLM result from inputs."""
        try:
            run_manager = cast(AsyncCallbackManagerForChainRun, run_manager)
            return await super().agenerate(input_list, run_manager=run_manager)
        except NotImplementedError:
            run_manager = cast(CallbackManagerForChainRun, run_manager)
            return self.generate(input_list)


class SolutionEngine(ChatBotManager):
    def __init__(self, summary_requirements, requirement, company_profile, scope, objective,rerank=None):
        self.summary_requirements = summary_requirements
        self.requirement = requirement
        self.company_profile = company_profile
        self.scope = scope
        self.objective = objective
        super().__init__(rerank)   
    
    # def introduction(self):
    #     chain = FallbackLLMChain(llm=chat_model_16k, prompt=first_sol_prompt)
    #     response = chain({'summary_requirements':self.summary_requirements, 'problem_requirement':self.requirement}) 
    #     return response
    
    def solution_chain(self, proposal_expert, project_duration_and_key_stages):
        chain_one = FallbackLLMChain(llm=chat_model, prompt=proposed_solution_prompt, output_key="proposed_solution")
        
        chain_two = FallbackLLMChain(llm=chat_model, prompt=solution_components_prompt, output_key="solution_components")
        
        chain_three = FallbackLLMChain(llm=chat_model, prompt=tools_and_technology_prompt, output_key="tool_technology")
        
        chain_four = FallbackLLMChain(llm=chat_model, prompt=benefits_prompt, output_key="benefits_outcome")
        
        chain_five = FallbackLLMChain(llm=chat_model, prompt=differentiators_prompt, output_key="differentiators")
        
        chain_six = FallbackLLMChain(llm=chat_model, prompt=timeline_milestones_prompt, output_key="timeline_milestones")

        
        # chain_six = FallbackLLMChain(llm=chat_model_16k, prompt=implementation_plan_prompt, output_key="implementation_plan")
        
        # chain_seven = FallbackLLMChain(llm=chat_model_16k, prompt=item_prompt, output_key="items")
        
        
        overall_chain = SequentialChain(
                            chains=[chain_one, chain_two, chain_three, chain_four, chain_five, chain_six], 
                            input_variables=["summary_requirement", "proposal_expert", "objective", "company_profile", "scope", "project_duration_and_key_stages"],
                            output_variables=["proposed_solution", "solution_components", "tool_technology", "benefits_outcome", "differentiators", "timeline_milestones"],
                            verbose=True
                                        ) 
        response = overall_chain({'summary_requirement':self.summary_requirements, 'proposal_expert':proposal_expert, "objective":self.objective,
                                  "scope":self.scope, "company_profile":self.company_profile, "project_duration_and_key_stages":project_duration_and_key_stages}) 
        return response

    def pricing(self, item_cost_summary):
        chain = FallbackLLMChain(llm=chat_model, prompt=price_prompt)
        response = chain({'summary_requirements':self.summary_requirements, 'item_cost_summary':item_cost_summary}) 
        self.cost_for_items = response['text']
        return response
    
    def call_to_action(self, exe_summary):
        chain = FallbackLLMChain(llm=chat_model, prompt=call_to_action_prompt)

        response = chain({'exe_summary':exe_summary, 'problem_summary':self.summary_requirements}) 
        return response['text']
    
    # def executive_summary(self, Proposed_solution, implementation_plan, budget_allocation):
    #     chain = FallbackLLMChain(llm=chat_model, prompt=executive_summary_prompt)

    #     response = chain({'problem_summary':self.summary_requirements, 
    #                       'Proposed_solution':Proposed_solution, 
    #                       'implementation_plan':implementation_plan,
    #                       'budget_allocation':budget_allocation,
    #                       'scope':self.scope}) 
    #     return response
    
    def extraction_qa(self, query:str, document):
        # Analyze the "COMMENTS AND SUGGESTIONS" section of the RFP
        response = self.parallel_process_inputs(query, document)
        return response
    
    # def generate_rfp_feedback(self, sections):
    #     chain = FallbackLLMChain(llm=chat_model, prompt=improvement_suggestion_prompt)
    #     response = chain({'company_profile':self.company_profile, 'requirement':self.requirement, "sections":sections}) 
    #     return response['text']
    
    def psdf_spoa(self, term_and_conditions):
        """proposal securing declaration form section and SpecialPower of Attorney section"""
        try:
            chain_one = FallbackLLMChain(llm=chat_model, prompt=proposal_securing_declaration_prompt, output_key="proposal_securing_declaration")
            chain_two = FallbackLLMChain(llm=chat_model, prompt=special_power_attorney_prompt, output_key="special_power_attorney")        
            overall_chain = SequentialChain(
                            chains=[chain_one, chain_two], 
                            input_variables=["company_profile","summary_requirements", "term_and_conditions"],
                            output_variables=["proposal_securing_declaration", "special_power_attorney"],
                            verbose=True
                                        ) 
            response = overall_chain({'company_profile':self.company_profile,'summary_requirements':self.summary_requirements, 'term_and_conditions':term_and_conditions}) 
        except ValidationError as e:
            print("You are not using ChatPromptTemplate: ValidationError: 1 validation error for FallbackLLMChain")
            
        return response

    

class VisulaizeRFP:
    
    def __init__(self) -> None:
        pass

    def visualize(self):
        import matplotlib.pyplot as plt
        from matplotlib_venn import venn2
        import random

        # Create two sets
        set1 = {'Talent development\n\n\n',  '\n\n\nPreformance Mangement', 'Sustainability'}
        set2 = {'Community engagement\n\n\n', '\n\n\nDiversity & Inclusion', 'Sustainability'}

        # Generate random colors for the diagram
        color1 = "#{:02x}{:02x}{:02x}".format(random.randint(0, 255), random.randint(0, 200), random.randint(0, 200))
        color2 = "#{:02x}{:02x}{:02x}".format(random.randint(0, 255), random.randint(0, 200), random.randint(0, 200))

        # Set the figure size
        fig = plt.figure(figsize=(10, 10))

        # Create a Venn diagram for two sets with random colors
        venn = venn2([set1, set2], set_colors=(color1, color2))

        # Customize the Venn diagram
        venn.get_label_by_id('10').set_text('\n'.join(map(str, set1 - set2)))
        venn.get_label_by_id('01').set_text('\n'.join(map(str, set2 - set1)))
        venn.get_label_by_id('11').set_text('\n'.join(map(str, set1 & set2)))

        # Display the plot
        return fig
        
    def work_plan_table(self, data):
        # Convert the nested dictionary into a list of lists for tabulation
        
        parsed_data = json.loads(data)

        table_data = []

        def flatten_dict(d, parent_key=''):
            for k, v in d.items():
                new_key = parent_key + '.' + k if parent_key else k
                if isinstance(v, dict):
                    flatten_dict(v, new_key)
                else:
                    table_data.append([new_key, v])

        flatten_dict(parsed_data)
        
        # Title for your table
        table_title = "Proposed Work Schedule"

        # Create a table with tabulate
        table = tabulate(table_data, headers=["Deliverables", "Value"], tablefmt="fancy_grid")
        
        # Add the title to the table
        table_with_title = f"{table_title}\n\n{table}"
        
        return table_with_title
    
def paraphrase_text():
    from langchain.prompts import PromptTemplate
    template = """Paraphrase the below text delimited by triple backticks and return only the Paraphrase text as a response.: ```{text}```"""
    prompt = PromptTemplate(template=template, input_variables=["text"])
    llm_chain = LLMChain(prompt=prompt, llm=llm)
    response = llm_chain.run(cv_prompt) 
    return response
        


import re
import ast
def clean_response(reponse):
    # Removing markdown signs and white spaces
    cleaned_text = reponse.strip().replace("```json", "").replace("```", "").strip()
    dict_string = ast.literal_eval(cleaned_text)
    # Converting the cleaned string to a JSON object
    # json_obj = json.loads(cleaned_text)
    return dict_string

def flatten_dict(d, parent_key='', sep='_'):
    items = {}
    if isinstance(d, dict):
        for k, v in d.items():
            new_key = parent_key + sep + k if parent_key else k
            if isinstance(v, (dict, list)):
                items.update(flatten_dict(v, new_key, sep=sep))
            else:
                items[new_key] = v
    else:
        items[parent_key] = d
    return items


from tabula import read_pdf
from langchain.schema.document import Document
from typing import List

def read_tables(path, document:List[Document])-> List[Document]:
    #reads table from pdf file
    df = read_pdf(path,pages="all") #address of pdf file

    if len(df) != 0:
        for table in df:
            document.append(Document(page_content = table.to_json(),metadata=''))
    return document
    
from langchain.output_parsers import ResponseSchema
from langchain.output_parsers import StructuredOutputParser

def company_parser(company_details):
    business_years = ResponseSchema(name="Number of Years in Business",
                             description="Extract the years the company has been in existence")
    
    certifications = ResponseSchema(name="Areas of Specialization",
                                        description="extract company areas of specialization.")
    certifications = ResponseSchema(name="Certifications and Recognitions",
                                        description="extract key certification that the business has.")
    past_projects = ResponseSchema(name="Past Client Projects",
                                        description="Extract the past project the company has worked on")
    technology_stack = ResponseSchema(name="Technology Proficiencies",
                                        description="extract technology stack and proficiencies of the company")

    response_schemas = [business_years, 
                        certifications,
                        past_projects,
                        technology_stack]
    output_parser = StructuredOutputParser.from_response_schemas(response_schemas)
    output_dict = output_parser.parse(company_details)
    return output_dict

from langchain.prompts import (
    FewShotChatMessagePromptTemplate,
    ChatPromptTemplate
    )

def create_final_prompt(examples, chat_model):
    example_prompt = ChatPromptTemplate.from_messages(
        [('human', '{input}'), ('ai', '{response}')]
    )

    few_shot_prompt = FewShotChatMessagePromptTemplate(
        examples=examples,
        example_prompt=example_prompt,
    )

    final_prompt = ChatPromptTemplate.from_messages(
        [
            ('system', 'You are a helpful AI Assistant'),
            few_shot_prompt,
            ('human', '{input}'),
        ]
    )
    
    print(final_prompt)

    return final_prompt | chat_model


import openai

def image_generator(prompt):
    # example prompt: "Structural materials (e.g. steel beams, concrete), Decription:Materials for the construction of the data center building",
    response = openai.Image.create(
    prompt = prompt,
    n=1,
    size="512x512"
    )
    image_url = response['data'][0]['url']
    
    return image_url

#######################################################
import streamlit as st
import os

def on_files(*funcs):
    def start():
        for func in funcs:
            func()
    return start

def on_background(func):
    container = st.container()
    def back(**kwargs):
        with container:
            st.write('\n\n')
            func(**kwargs)
    #st.sidebar.subheader('Company Bacground')
    return back


def on_intro(func):
    container = st.container()
    def intro(text=None, intro_table=None, sign_table=None):
        with container:
            st.write('\n\n')
            func(intro_text = text, intro_table=intro_table, sign_table=sign_table)
    return intro

def on_comment(func):
    container = st.container()
    def comment(texts=None):
        with container:
            st.write('\n\n')
            st.markdown("#### COMMENT AND SUGGESTION")
            func(texts)

    return comment

def on_methodology(*funcs):
    container = st.container()

    def write_methods(texts=None):
        with container:
            st.write('\n\n')
            #st.markdown("")
            for func in funcs:
                func(texts)
    return write_methods

def on_cv(func):
    container = st.container()

    def write_cv(htemp=None, tables=None, ftemp=None):
        with container:
            st.write('\n\n')
            st.markdown("#### CURRICULUM VITAE (CV)")
            st.write('---------------------------------------------------------------------------------------------------------')
            func(htemp, tables, ftemp)
    return write_cv

def on_solution(*funcs):
    container = st.container()
    
    def write_solutions(text):

        with container:
            for func in funcs:
                func(text)

    return write_solutions
def on_term_cond(*funcs):
    container = st.container()

    def write_terms(texts=None):
        with container:
            st.write('\n\n')
            for func in funcs:
                func(texts)
    return write_terms

def on_fin_report(func):
    container = st.container()

    def give_report(texts=None):
        with container:
            # st.markdown("### FINANCIAL PROPOSAL SUBMISSION FORM")
            func(texts)

    return give_report

def on_cost(func):
    container =  st.container()

    def give_cost(data):
        with container:
            st.markdown("#### COSTING")
            func(data)

    return give_cost

def on_action(func):
    container = st.container()
    def call_to_action(texts):
        with container:
            st.markdown("CALL TO ACTION")
            func(texts)
    return call_to_action

def on_exec_summary(func):
    container =  st.container()

    def write_abstract(texts):
        with container:
            st.markdown('### EXECUTIVE SUMMARY')
            func(texts)
    return write_abstract

def on_prelima(func):
    container =  st.container()

    def write_sec(texts):
        with container:
            # st.markdown("## 2. Cover Letter & Executive Summary")
            func(texts)
    return write_sec
def process_implementation(project_implementation):
    import pandas as pd
    import numpy as np

    imp_plan = clean_response(project_implementation['key_stages_and_phases'])
    key_stages = imp_plan["Key_Stages"]
    overview = ['Stage_ID', 'Stage', 'Requirements', 'Objectives']
    rows = []
    stage_map = {}
    for i, stage in enumerate(key_stages):
        stage_id = stage['Stage'].split(' ')
        stage_id = stage_id[0][0] + stage_id[-1][0] + f"0{i}"
        stage_map [stage['Stage']] = stage_id
        rows.append([stage_id, stage['Stage'], stage['Requirements'], stage['Objectives']])

    over_tab = pd.DataFrame(rows, columns=overview)
    
    
    def check_timeline(d):
        if "Timeline" in d.keys():
            return True
    rows =[]
    timeline_rows = []
    cols = ['Stage_ID', "Section", 'Key', "Value"]
    for stage in (key_stages):
        stage_id = stage_map[stage['Stage']]
        if check_timeline(stage):
            tl = stage['Timeline']
            print("This is TL!!!!!!!!", tl)
            if isinstance(tl, dict):
                for k,v in tl.items():
                    timeline_rows.append((stage_id, k, v))
            elif isinstance(tl, str):
                for t in tl.split('\n'):
                    vals = t.split(':')
                    k = vals[0]
                    v = ': '.join(vals[1:]) 
                    timeline_rows.append((stage_id, k, v))
        deliverables = stage['Deliverables']
        if isinstance(deliverables, dict):
            for name in deliverables:
                deliv = stage['Deliverables'][name]
                        
                if isinstance(deliv, dict):
                    for v in deliv.keys():
                        val = deliv[v]
                        if val is np.nan:
                            val = "-"
                        key = v
                        row = (stage_id, name, key, val)
                        
                        if name == "Timeline":
                            timeline_rows.append((stage_id, key, val))
                            continue
                        rows.append(row) 

                elif isinstance(deliv, (list, tuple)):
                    for v in deliv:
                        val = deliv[v]
                        if val is np.nan:
                            val = "-"
                        key = "-"
                        row = (stage_id, name, key, val)
                        rows.append(row)
                else:
                    val = deliv
                    key = "-"
                    row = (stage_id, name, key, val)
                    rows.append(row)
        elif isinstance(deliverables, str):
            val = deliverables
            key = "-"
            name = "-"
            row = (stage_id, name, key, val)
            rows.append(row)

        elif isinstance(deliverables, list):
            for i, deliv in enumerate(deliverables):
                val = deliv
                key = f"{i}"
                name = "-"
                row = (stage_id, name, key, val)
                rows.append(row)
        

    del_tab = pd.DataFrame(rows, columns=cols)

    timeline = pd.DataFrame(timeline_rows, columns=['Stage_ID','Key', "Value"])

    resource = clean_response(project_implementation['resource_allocation_and_dependencies'])

    return over_tab, del_tab, timeline, resource

def dedict(d):
    return ' || '.join([f"{k}: {v}" for k, v in d.items()])

def delist(l):
    return ' | '.join(l)

def islistoflist(l, strict=True):
    
    """
    l: list object to be checked if it's a list of list
    strict: if True all elements in the list must be lists.
            if False at least one element in the list is a list
    """
    
    if not isinstance(l, list):
        return False
    
    
    else:
        if len(l) == 0:
            return False
        
        if strict == True:
            for i in l:
                if not isinstance(i, list):
                    return False 
            return True
        
        for i in l:
            if isinstance(i, list):
                return True 
            
        return False
            
            
def islistofdict(l, strict=True):
    if not isinstance(l, list):
        return False
    
    else:
        if len(l) == 0:
            return False
        
        if strict == True:
            for i in l:
                if not isinstance(i, dict):
                    return False 
            return True
        
        for i in l:
            if isinstance(i, dict):
                return True 
            
        return False
    
def normalize(vals):
    seq = []
    for element in vals:
        items = {}
        for k, ele in element.items():
            if isinstance(ele, dict):
                ele = dedict(ele)
            elif isinstance(ele, list):
                ele = delist(ele)
            items[k] = ele
        seq.append(items) 
        
    return seq


   # def implement(imp_plan)
    #    key_stages = imp_plan["Key_Stages"]
     #   overview = ['Stage_ID', 'Stage', 'Requirements', 'Objectives']
      #  rows = []
       # stage_map = {}
        #for i, stage in enumerate(key_stages):
         #   stage_id = stage['Stage'].split(' ')
          #  stage_id = stage_id[0][0] + stage_id[-1][0] + f"0{i}"
           # stage_map [stage['Stage']] = stage_id
            #rows.append([stage_id, stage['Stage'], stage['Requirements'], stage['Objectives']])
        

def generate_image(img_desc, size = "512x512", openai_key=None):
    """
    img_desc: Description of image you want to generate
    size:str
    """

    
    if openai_key:
        openai.api_key = openai_key

    response = openai.Image.create(
    prompt=img_desc,
    n=1,
    size=size,
    
    )
    image_url = response['data'][0]['url']
    
    return image_url


def load_img(img_url, return_fig=True, show=False):

    """
    returns image name
    """
    import numpy as np
    import matplotlib.image as mpimg
    import matplotlib.pyplot as plt
    import io
    data = requests.get(img_url).content 
    
    # Opening a new file named img with extension .jpg 
    # This file would store the data of the image file 
    n = []
    n.append(str(np.random.randint(1,9)))                                 
    n.append(str(np.random.randint(1,9)))   
    n.append(np.random.choice(['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']))         
    n.append(np.random.choice(['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']).upper())         

    name = ''.join(n)
    cwd = os.getcwd()

    img_path = cwd + f"//{name}plot.png"

    import io
    from PIL import Image
    cwd = os.getcwd()
    fp = open(img_path,'wb')
    # Storing the image data inside the data variable to the file 
    data = requests.get(img_url).content 
    fp.write(data) 
    fp.close()

    image = Image.open(img_path)
    #image.save(img_path)
    st.image(image)
    
    

  
    return image, img_path


def build_timeline(timeline, include_top_bottom=False):
        """ timeline: A list of tuple or a dictionary containing milestones and time to be reached
                if list of tuples: each tuple is a pair of time and milestone
                if dict: The key is the time and the value is milestone
        """

        
        tmln = dict(timeline)

        repeating_pattern = """
                        <div class="card">
                                <div class="info">
                                <h3 class="title">{}</h3>
                                <p>{}</p>
                                </div>
                        </div>
                        """
        bottom = """
                        </div>
                </div>
                </body>
                </html>
                """
        patterns = []
        for title, mile in tmln.items():
                pat = repeating_pattern.format(title, mile)

                patterns.append(pat)
        mile_cards = '\n'.join(patterns)
        
        template_path = r"C:\Users\User-pc\Documents\Library\Projects\project_document\experiment\sample_1.html"
        with open(template_path, "r") as fp:
                html_string = fp.read()
        
        html_timeline = html_string + mile_cards + bottom

        if include_top_bottom == True:
                top = """<!DOCTYPE html>
                        <html lang="en" >
                        <head>
                        <meta charset="UTF-8">
                        <title>Project Timeline</title>"""
                
                html_timeline = top + html_string + mile_cards + bottom

        return html_timeline
       
def display_viz(viz):
    import matplotlib.pyplot as plt
    import numpy as np
    n = []
    n.append(str(np.random.randint(1,9)))                                 
    n.append(str(np.random.randint(1,9)))   
    n.append(np.random.choice(['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']))         
    n.append(np.random.choice(['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']).upper())         

    name = ''.join(n)
    st.pyplot(viz)
    cwd = os.getcwd()
    path = cwd + f"\\{name}plot.png"
    viz.savefig(path)
    return path

def wrap_img_html(img_path):
    img_src = f"""
    <div>
    <img src='{img_path}'/>
    </div>"""
    print("THIS IS THE IMAGE SOURCE",img_src)
    return img_src
    

def select_llm():
    """
    Read user selection of parameters in Streamlit sidebar.
    """
    model_name = st.sidebar.radio("Choose LLM:",
                                  ("gpt-3.5-turbo-0613",
                                   "gpt-3.5-turbo-16k-0613",
                                   "gpt-4",
                                   "text-davinci-003",
                                   ))
    temperature = st.sidebar.slider("Temperature:", min_value=0.0,
                                    max_value=1.0, value=0.0, step=0.01)
    return model_name, temperature

    
    
sample_items_cost_summary = [{
  "Item Name": "Architectural plans and blueprints",
  "Description": "Detailed plans and drawings for the construction of the data center",
  "Quantity": "1",
  "Unit Cost": "$10,000",
  "Total Cost": "$10,000"
},
{
  "Item Name": "Mechanical equipment (e.g. HVAC systems)",
  "Description": "Equipment for heating, ventilation, and air conditioning systems",
  "Quantity": "1",
  "Unit Cost": "$50,000",
  "Total Cost": "$50,000"
},
{
  "Item Name": "Electrical equipment (e.g. generators, UPS)",
  "Description": "Equipment for power supply and backup systems",
  "Quantity": "1",
  "Unit Cost": "$100,000",
  "Total Cost": "$100,000"
},
{
  "Item Name": "Structural materials (e.g. steel beams, concrete)",
  "Description": "Materials for the construction of the data center's structure",
  "Quantity": "1",
  "Unit Cost": "$200,000",
  "Total Cost": "$200,000"
},
{
  "Item Name": "Environmental monitoring systems",
  "Description": "Systems for monitoring and controlling the data center's environment",
  "Quantity": "1",
  "Unit Cost": "$20,000",
  "Total Cost": "$20,000"
},
{
  "Item Name": "Data collection tools (e.g. sensors, meters)",
  "Description": "Tools for collecting data and monitoring the data center's performance",
  "Quantity": "1",
  "Unit Cost": "$5,000",
  "Total Cost": "$5,000"
},
{
  "Item Name": "Primary research resources (e.g. interviews, site visits)",
  "Description": "Resources for conducting primary research on the data center's requirements",
  "Quantity": "1",
  "Unit Cost": "$2,000",
  "Total Cost": "$2,000"
},
{
  "Item Name": "Secondary research resources (e.g. market research reports)",
  "Description": "Resources for conducting secondary research on the data center's market",
  "Quantity": "1",
  "Unit Cost": "$1,000",
  "Total Cost": "$1,000"
},
{
  "Item Name": "Multidisciplinary team of experts",
  "Description": "A team of experts with diverse skills and knowledge for the data center project",
  "Quantity": "1",
  "Unit Cost": "$500,000",
  "Total Cost": "$500,000"
},
{
  "Item Name": "Communication tools (e.g. meetings, workshops)",
  "Description": "Tools for facilitating communication and collaboration among project stakeholders",
  "Quantity": "1",
  "Unit Cost": "$10,000",
  "Total Cost": "$10,000"
},
{
  "Item Name": "Post-implementation support services",
  "Description": "Services for providing support and maintenance after the data center is implemented",
  "Quantity": "1",
  "Unit Cost": "$50,000",
  "Total Cost": "$50,000"
},
{
  "Item Name": "References to top companies in feasibility studies",
  "Description": "References to successful companies in similar projects for feasibility studies",
  "Quantity": "1",
  "Unit Cost": "$1,000",
  "Total Cost": "$1,000"
},
{
  "Item Name": "Guidance and consultation services",
  "Description": "Services for providing guidance and consultation throughout the project",
  "Quantity": "1",
  "Unit Cost": "$100,000",
  "Total Cost": "$100,000"
},
{
  "Item Name": "Maintenance and upgrade services",
  "Description": "Services for maintaining and upgrading the data center's equipment and systems",
  "Quantity": "1",
  "Unit Cost": "$50,000",
  "Total Cost": "$50,000"
}
]


data = {
    'roles': {
        'Project Manager': {'estimated_hours': 40, 'hourly_rate': 70},
        'Data Center Architect': {'estimated_hours': 80, 'hourly_rate': 100},
        'Data Center Engineer': {'estimated_hours': 60, 'hourly_rate': 90},
        'IT Consultant': {'estimated_hours': 40, 'hourly_rate': 80},
        'Business Analyst': {'estimated_hours': 40, 'hourly_rate': 70},
        'Financial Analyst': {'estimated_hours': 40, 'hourly_rate': 60},
        'Procurement Specialist': {'estimated_hours': 40, 'hourly_rate': 60},
        'Project Coordinator': {'estimated_hours': 40, 'hourly_rate': 50},
        'Technical Writer': {'estimated_hours': 40, 'hourly_rate': 50},
        'Research Analyst': {'estimated_hours': 40, 'hourly_rate': 50}
    }
}


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def make_cost_plots(cost_table):
    sns.set(style="whitegrid")
    df = cost_table.copy()
    fig_dict = {}

    # Create figure for two separate bar charts
    fig, axs = plt.subplots(2, 1, figsize=(10, 12))

    # Plot estimated hours
    hours_fig = sns.barplot(data=df, x=df.index, y='estimated_hours', ax=axs[0], color='skyblue')
    axs[0].set_title('Estimated Hours per Role')
    axs[0].set_xlabel('Role')
    axs[0].set_ylabel('Hours')
    axs[0].tick_params(axis='x', rotation=45)
    fig_dict['estimated_hours'] = fig

    # Plot hourly rates
    rates_fig = sns.barplot(data=df, x=df.index, y='hourly_rate', ax=axs[1], color='orange')
    axs[1].set_title('Hourly Rate per Role')
    axs[1].set_xlabel('Role')
    axs[1].set_ylabel('Rate ($/hr)')
    axs[1].tick_params(axis='x', rotation=45)
    fig_dict['hourly_rate'] = fig

    plt.tight_layout()

    return fig_dict


# Convert the nested dictionary to a list of records

# Create DataFrame

#df.set_index('Role', inplace=True)

# Call the function and get the figures dictionary


# Now figs['estimated_hours'] and figs['hourly_rate'] hold the respective figures.
