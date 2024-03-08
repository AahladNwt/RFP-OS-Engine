

import openai
import requests 
from PIL import Image 
from langchain.chains import SequentialChain
from utils.util import FallbackLLMChain
from agent_tools.api_credentials import chat_model
from prompt.prompts import (costing_breakdown_intro_prompt,
                            labor_costs_text_prompt,
                            labor_costs_table_prompt,
                            extract_roles_with_rates_prompt,
                            materials_equipment_text_prompt,
                            item_prompt,
                            software_licensing_text_prompt,
                            software_licensing_table_json_prompt,
                            overheads_text_prompt,
                            overheads_json_prompt,
                            overheads_graph_json_prompt
                            
                           )


class FinanceManager():
    def __init__(self, summary_company_profile,
                 objective,
                 problem_statement,
                 summary_requirement,
                 scope,
                 client_company_name,
                 proposed_solution,
                 project_timeline,
                 project_duration_and_key_stages,
                 deliverable
                 ):

        self.summary_company_profile = summary_company_profile
        self.objective = objective
        self.problem_statement = problem_statement
        self.summary_requirement = summary_requirement
        self.scope = scope
        self.client_company_name = client_company_name
        self.proposed_solution = proposed_solution
        self.project_timeline = project_timeline
        self.project_duration_and_key_stages = project_duration_and_key_stages
        self.deliverable = deliverable
        super().__init__()   
    
    def direct_cost(self, domain, project_name):
        chain_one = FallbackLLMChain(llm=chat_model, prompt=costing_breakdown_intro_prompt, output_key="costing_breakdown_intro")
        chain_two = FallbackLLMChain(llm=chat_model, prompt=extract_roles_with_rates_prompt, output_key="roles_hourly_rate")
        
        chain_three = FallbackLLMChain(llm=chat_model, prompt=labor_costs_text_prompt, output_key="labor_costs_text")
        
        chain_four = FallbackLLMChain(llm=chat_model, prompt=labor_costs_table_prompt, output_key="labor_costs_table")
        
        chain_five = FallbackLLMChain(llm=chat_model, prompt=materials_equipment_text_prompt, output_key="materials_equipment_intro") 
        
        chain_six = FallbackLLMChain(llm=chat_model, prompt=item_prompt, output_key="items") 
        
        chain_seven = FallbackLLMChain(llm=chat_model, prompt=software_licensing_text_prompt, output_key="software_licensing_text") 
        
        chain_eight = FallbackLLMChain(llm=chat_model, prompt=software_licensing_table_json_prompt, output_key="software_licensing_table") 


        overall_chain = SequentialChain(
                            chains=[chain_one, chain_two, chain_three, chain_four, chain_five, chain_six, chain_seven, chain_eight], 
                            input_variables=["client_company_name","your_company_name","proposed_solution", "scope", "project_duration_and_key_stages", "problem_statement", "objective", "project_name"],
                            output_variables=["costing_breakdown_intro", "roles_hourly_rate", "labor_costs_text", "labor_costs_table", "materials_equipment_intro", "items", "software_licensing_text",  "software_licensing_table"],
                            verbose=True
                                        ) 
        response = overall_chain({'client_company_name':self.client_company_name, 'your_company_name':domain,
                                  'proposed_solution':self.proposed_solution, "scope":self.scope,"project_duration_and_key_stages":self.project_duration_and_key_stages,
                                  "problem_statement":self.problem_statement, "project_name":project_name, "objective":self.objective, "proposed_solution":self.proposed_solution
                                }) 
        return response
    
    def indirect_cost(self,project_name):
        chain_one = FallbackLLMChain(llm=chat_model, prompt=overheads_text_prompt, output_key="overheads_text")
        chain_two = FallbackLLMChain(llm=chat_model, prompt=overheads_json_prompt, output_key="overheads_table")
        
        chain_three = FallbackLLMChain(llm=chat_model, prompt=overheads_graph_json_prompt, output_key="overheads_graph")
        
        # chain_four = FallbackLLMChain(llm=chat_model, prompt=labor_costs_table_prompt, output_key="labor_costs_table")
        

        overall_chain = SequentialChain(
                            chains=[chain_one, chain_two, chain_three],
                            input_variables=["project_name", "objective", "deliverable", "scope", "summary_requirement","project_timeline"],
                            output_variables=["overheads_text", "overheads_table",],
                            verbose=True
                                        ) 
        response = overall_chain({
                                  'project_name':project_name, "objective":self.objective,"deliverable":self.deliverable,
                                  "scope":self.scope, "summary_requirement":self.summary_requirement, "project_timeline":self.project_timeline
                                }) 
        return response
    
    
    """def pricing_phylosophy(self, proj_understand):
        chain_one = FallbackLLMChain(llm=chat_model, prompt=financial_overview_prompt, output_key="phylosophy")
        chain =  SequentialChain(
                            chains=[chain_one], 
                            input_variables=["client_company_name","your_company_name","objective", "scope", "key_stakeholders"],
                            output_variables=["phylosophy"],
                            verbose=True
                                        ) 
        response = chain({'client_company_name':self.client_company_name,
                                  'objective':self.objective, "scope":self.scope,"kproj_understand":proj_understand,
                                  "objective": self.objective,
                                  "problem_statement": self.problem_statement,
                                  "summary_requirements": self.summary_requirements,
                                  "scope": self.scope
                                }) 
        return response"""

def generate_image(img_desc, size = "1024x1024", openai_key=None):
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

def load_img(img_url, show=False):

    """
    returns image name
    """
    import numpy as np
    data = requests.get(img_url).content 
    
    # Opening a new file named img with extension .jpg 
    # This file would store the data of the image file 
    n = np.random.randint(1,9)
    img_n = f"img{1+n}{n-1}.jpg"
    f = open(img_n,'wb') 
    
    # Storing the image data inside the data variable to the file 
    f.write(data) 
    f.close() 
  
    # Opening the saved image and displaying it 
    if show == True:
        img = Image.open(img_n) 
        img.show()

    return img_n

def make_cost_plots(cost_table):
    import matplotlib.pyplot as plt
    import pandas as pd
    import seaborn as sns
    sns.set(style="whitegrid")
    df = cost_table.copy()
    fig_dict = {}
    
    def mult(row):
        ehr = row['estimated_hours'] 
        hr =  row['hourly_rate']
        if (ehr == 0):
            ehr = 1
        if hr == 0:
            hr = 1
        return ehr * hr
    
    df['estimated_labour_cost'] = df[['estimated_hours','hourly_rate']].apply(mult, axis=1)
    
    # make hourly rates plots
    fig, axs = plt.subplots(2, 1, figsize=(10, 12))
    
    #hour_fig =  plt.figure(figsize=(10, 6))
    hours_fig = sns.barplot(data=df, x=df.index, y='estimated_hours', ax=axs[0], color='skyblue')
    axs[0].set_title('Estimated Hours per Role')
    axs[0].set_xlabel('Role')
    axs[0].set_ylabel('Hours')
    axs[0].tick_params(axis='x', rotation=45, )
    axs[0].spines[['bottom', 'left']].set_visible(False)
    
    #fig_dict['estimated_hours'] = fig
    
    # Plot hourly rates
    rates_fig = sns.barplot(data=df, x=df.index, y='hourly_rate', ax=axs[1], color='orange')
    axs[1].set_title('Hourly Rate per Role')
    axs[1].set_xlabel('Role')
    axs[1].set_ylabel('Rate ($/hr)')
    axs[1].tick_params(axis='x', rotation=45)
    fig_dict['hourly_rate'] = fig

    # Make Piechart
    labels = df.index
    val = df['estimated_labour_cost'].values

    pie_fig = plt.figure(figsize=(12, 12))

    plt.title("Distribution of Labour Costs ($)", 
            {'fontsize': 25,
            'fontweight': 10,
            'color': "black"})
    #print("VAL", val)
    #print("LAB", labels)
    plt.pie(val, labels=labels, autopct='%0.2f%%');

    fig_dict['pie_plot'] = pie_fig
    #plt.savefig('labour.png')

    return fig_dict