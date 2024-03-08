from tabulate import tabulate

def create_cv_section(company_name, text):
    
    htemplate = f"""## {company_name}\n

            #### Team Qualifications and Experience\n

            **Table of Contents**\n

            1. Executive Team
            2. Project Management Team
            3. Technical Team
            4. Subject Matter Experts
            5. Support Staff
            """
    
    # Define the data for the tables
    executive_team = [
        ["Period",  "Name 1", "CEO", "Education 1", "Relevant Experience 1"],
        ["Period", "Name 2", "COO", "Education 2", "Relevant Experience 2"],
        ["Period", "Name 3", "CFO", "Education 3", "Relevant Experience 3"]
    ]

    project_management_team = [
        ["Period", "Name 4", "Project Manager", "Education 4", "Relevant Experience 4"],
        ["Period", "Name 5", "Project Manager", "Education 5", "Relevant Experience 5"],
        ["Period", "Name 6", "Project Manager", "Education 6", "Relevant Experience 6"]
    ]

    technical_team = [
        ["Period", "Name 7", "Lead Developer", "Education 7", "Relevant Experience 7"],
        ["Period", "Name 8", "Systems Analyst", "Education 8", "Relevant Experience 8"],
        ["Period", "Name 9", "Database Expert", "Education 9", "Relevant Experience 9"]
    ]

    subject_matter_experts = [
        ["Period", "Name 10", "Industry Expert", "Education 10", "Relevant Experience 10"],
        ["Period", "Name 11", "Legal Advisor", "Education 11", "Relevant Experience 11"],
        ["Period", "Name 12", "Environmentalist", "Education 12", "Relevant Experience 12"]
    ]

    support_staff = [
        ["Period", "Name 13", "Administrative", "Education 13", "Relevant Experience 13"],
        ["Period", "Name 14", "IT Support", "Education 14", "Relevant Experience 14"],
        ["Period", "Name 15", "Customer Support", "Education 15", "Relevant Experience 15"]
    ]
    
    
    # Define the headers for the tables
    headers = ["Period", "Name", "Title", "Education", "Relevant Experience"]

    # Create and print the tables using tabulate
    tables = {'headers':headers}
    print("1. Executive Team")
    tables["1. Executive Team"] = executive_team
    
    tables["2. Project Management Team"] = project_management_team
    
    tables["3. Technical Team"] = technical_team
    
    tables["4. Subject Matter Experts"] = subject_matter_experts
    
    tables["5. Support Staff"] = support_staff
    
    
    ftemplate = f"""
        ### **Contact Information:**\n
        - E-mail: [Your Email Address]
        - Phone: [Your Phone Number]

        ### **Certification:**\n
        {text}

        **Name of Expert:______________________________________________Signature:_________________________________Date:**__________________________________________

        **[Authorized Signature]______________________________________________Signature:__________________________________________Date:**__________________________________________

        """
    
    return htemplate, tables, ftemplate


# Create Resume Section
from agent_tools.api_credentials import chat_model
from prompt.prompts import  generate_resume_prompt, clean_resume_prompt, convert_to_latex, convert_to_markdown



from utils.util import FallbackLLMChain

def get_staff_resume(roles_with_qualifications_json):
    chain = FallbackLLMChain(llm=chat_model, prompt=generate_resume_prompt)
    response = chain({'roles_with_qualifications_json':roles_with_qualifications_json}) 
    output = response['text']
    return output

def clean_staff_resume(resume_json):
    chain = FallbackLLMChain(llm=chat_model, prompt=clean_resume_prompt)
    response = chain({'resume_json':resume_json}) 
    output = response['text']
    return output

def resume_to_latex(resume_json):
    chain = FallbackLLMChain(llm=chat_model, prompt=convert_to_latex)
    response = chain({'resume_json':resume_json}) 
    output = response['text']
    return output

def resume_to_markdown(resume_json):
    chain = FallbackLLMChain(llm=chat_model, prompt=convert_to_markdown)
    response = chain({'resume_json':resume_json}) 
    output = response['text']
    return output


        

    