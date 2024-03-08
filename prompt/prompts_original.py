from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)

template="As a specialized AI assistant in the domain of Request For Proposals (RFPs), I am tasked with crafting a compelling and highly competitive RFP response on behalf of my organization. The objective of my meticulously prepared proposal is to emulate the nuances and tone of human-generated content, while aiming for the highest standard of excellence to secure us the coveted project or assignment."
system_message_prompt = SystemMessagePromptTemplate.from_template(template)
########################################  QA Retrieval Prompts  ##################################################

problem_statement_or_opportunity_qa = "Identify the core problem or opportunity that the issuer aims to address with this project. Extract any specific challenges, pain points, or goals outlined in the RFP. This will serve as the foundation upon which to build your solution in the proposal. Note any quantitative or qualitative metrics that the issuer uses to describe the problem or opportunity."

requirements_qa = """
        Please use the information provided in the RFP document to comprehend the problem and extract **all** the 
        mentioned requirements. Your response should include a clear explanation of the problem presented in the 
        RFP and a detailed list of all the specified requirements.Identify the problem and object stated in
        the RFP. You may assume that the RFP document contains the necessary information to understand the problem 
        and its requirements thoroughly.  When listing the requirements, make sure to clearly indicate each 
        requirement and provide relevant context or clarifications if needed." 
      """
      
financial_requirements_qa = "Extract key financial terms from the RFP, including pricing models, budget limits, payment terms, and any performance-related penalties or incentives. Note any financial documentation or compliance needs."

scope_qa = "Identify the specific tasks, deliverables, and outcomes the issuer expects. What are the main components of the project as described in the RFP?"

evaluation_criteria_qa = "Extract the criteria on which the proposal will be evaluated. Does the RFP highlight any particular parameters or metrics for assessment?"

expected_rfp_response_qa = "As a proposal bidder, you've got an RFP from a potential client outlining project needs and expectations. Your goal is to extract the expected responses they seek. Identify and detail these response types:"

budget_and_financials_qa = "In the RFP document, identify and extract all information related to budget and financial considerations. Provide a detailed summary of the financial constraints, budget limits, and any financial guidelines or expectations that have been outlined for the project. Ensure that any specified cost parameters, financial scopes, or monetary limits are clearly presented."

legal_and_contractual_qa = "Identify and summarize all legal and contractual information, terms, and conditions specified in the RFP. Provide clear insights into the legal considerations, obligatory terms, expected contractual commitments, and any other regulations or compliances that the bidder needs to be aware of while crafting the proposal."
      
submission_guidelines_qa = "Extract all pertinent information regarding proposal submission guidelines from the RFP. Detail the format, length, structure, and any specific inclusion criteria for the proposal. Ensure to highlight any deadlines, submission platforms or addresses, and any other relevant instructions that pertain to the proposal submission process."

project_timeline_qa = "Analyze the RFP and provide a detailed summary of the project timeline and any critical milestones. Ensure to encapsulate the project’s start and end date, and any intermediate dates or phases that are crucial for project execution. Your extraction should clearly denote the expected progression and any key timeline-related expectations from the bidder."
         
vendor_responsibilities_qa = "Please understand and extract the roles and responsibilities that are expected from the vendor, as per the RFP. Your extraction should illustrate what the client expects from the vendor in terms of deliverables, management, collaboration, and other relevant areas throughout the project duration. Ensure to capture any specific roles or tasks that the vendor is mandated to perform."

communication_and_reporting_qa = "Identify and detail the communication and reporting requirements specified in the RFP. This includes expected reporting frequencies, formats, and any specific content to be reported. Also, provide insights into the preferred communication channels, any designated points of contact, and expectations regarding availability or response times."
                    
objective_qa = "Identify and summarize the key objectives of the project stated in the  document."

deliverable_qa = "Analyze the RFP document to extract all key deliverables that is expected from the proposal bidder or vendor. Provide the expected deliverables in a JSON format. "

qualification_qa = "Please extract the qualifications or requirements that a prospective vendor, bidder, or consultant should have in order to bid for the project."
technical_requirement_qa = "Extract technical specifications or requirements. Are there specific systems, technologies, or standards that the proposal needs to adhere to?"

project_duration_and_key_stages_qa = "extract the expected timeline or duration for the project, outline the key stages involved in the project."

company_profile_qa = "Gather essential company information: name, history, achievements. Explain guiding principles and partnership approach. Explore past projects and expertise. Define mission for objectives and value. Outline visionary goals and industry impact."

company_details_qa = "Extract the Number of Years in Business, Areas of Specialization, Certifications and Recognitions, Past Client Projects, and Technology Proficiencies for the company. Format your output as JSON"

company_strength_capabilities_qa = "extract the companies strength and capabilities"

collaboration_and_preferences_qa = "Analyze the RFP to identify preferred collaboration tools, platforms, methods, and any specific client preferences regarding project involvement or communication channels. Summarize the findings."

update_frequency_qa = "From the RFP, extract details on the expected frequency and format of updates (e.g., email, video calls). Summarize the information."

issuer_name_qa = "Extract the name of the entity issuing the RFP. If the name is not specified, note that as well."

roles_extraction_qa = "Review the RFP to identify and list all the roles required to successfully execute the project. Include titles and any specified qualifications, experience or skills necessary for each role. Format your output as JSON."

########################################  Summarize QA responses  ##################################################

summary_prompt  = ChatPromptTemplate.from_template("""
        You have been provided with different text delimited by triple 
        backticks, you are to perform the below actions.
        
        - From the provided expected Response, extract the terms that contain the word "proposal" and organize them into a python list.
        
        - Summarize the **Requirement** in at most 50 words, and focusing on any aspects  that are relevant, add relevant timeline. 
        
        - Summarize the **Scope** in at most 40 words, add relevant timeline and dates.
        
        - Summarize the **Company Profile** in at most 50 words, and focusing on any aspects that are relevant.
        
        
        expected proposal: ```{expected_rfp_response}```
        
        requirement: ```{requirement}```
        
        scope: ```{scope}```
        
        company profile: ```{company_profile}```
                
        Format the output as JSON with the following keys:
        
        expected response
        requirement
        scope
        company_profile
        
        """)
######################################## Table of Content Prompt  ##################################################

toc_rfp_response_prompt = ChatPromptTemplate.from_template("""
     Generate a concise and technically-focused Table of Contents (TOC) for an RFP Technical Proposal, incorporating both standard and RFP-specific sections. Ensure a unified and seamless TOC for optimal clarity and relevance.

        **GENERIC SECTIONS**:
        ### Table Of Contents
        1. Application Form
        2. Cover Letter and Executive Summary
                - Introduction
                - Business Context and Relevance
        3. Company Overview
                - Organization's Background
                - Expertise and Experience
                - Past Achievements and Recognitions
        4. Understanding of the Project
                - Insights into the Client's Needs
                - Established Objectives and Goals
                - Comments and Suggestions
                - Trend and Business Cases 
        5. Approach/Methodology
                - Overview of the Approach
                        - Project Context
                        - Our Approach in a Nutshell
                        - Aligning Strengths to Needs
                        - Future Outlook
                - Proposed Solution
                        - Solution Components and Breakdown
                        - Tools and Technologies Utilized (if applicable)
                - Benefits and Outcomes of Our Approach and Methodology
                - What Differentiates Us From The Rest
                - Client Collaboration & Feedback
        6. Project Implementation Plan
                - Implementation Strategy
                - Key Stages and Phases
                - Resource Allocation and Dependencies
                - Contingency Measures and Pre-requisites
        7. Project Management
                - Team Composition and Roles
                - Communication Strategy
                - Management of Risks
                - Anticipated Work Schedule and Plan
        8. Timeline and Schedule
                - Timeline and Milestones
                - Main Deliverables and Deadlines

        **RFP-SPECIFIC INPUTS**:
        - Requirements: ```{requirement}```
        - Expected Technical Response: ```{expected_response}```
        - Legal and Contractual: ```{legal_and_contractual}```

        **DERIVE AND INTEGRATE THE TOC BASED ON THE RFP INPUTS**:
        (Based on the above RFP inputs, develop specific sections and integrate them seamlessly into the TOC. These should be directly tied to the information provided and not be influenced by any external examples.)

        The completed TOC should appear as a unified list, arranged logically. Ensure sections like the Conclusion are placed appropriately and avoid including or repeating contents not based on the **RFP-SPECIFIC INPUTS**.
""")

########################################Application Form ################################################################################################33
application_form_prompt = ChatPromptTemplate.from_template("""
    - You are tasked to respond to a client's RFP using the provided details. Your objective is to ensure your response stands out and immediately draws attention. Remember, first impressions are essential!
    Task:
    Craft a detailed, clear, and compelling proposal submission form. Incorporate the proposal response, company name, timeline, and address the recipient as "Sir" or "Ma'am". Personalize where necessary.

    Company name: ```{company_name}```
    Expected Proposal: ```{expected_rfp_response}```
    Project Requirement: ```{requirement}```
    Project Scope: ```{scope}```

    - Ensure your response is professional yet captivating.
    - Do not simply restate the information; infuse it with a persuasive narrative.
    - Conclude with a strong call to action.
    - Sign and date the form.
    
    Note: Use the example below as a foundation but go beyond it. Think creatively and strategically.

    **Sample TECHNICAL PROPOSAL SUBMISSION FORM**:

    ### 1. TECHNICAL PROPOSAL SUBMISSION FORM

    To: [Client name]
                                                           
    From: [Your company name]

    Dear Sir/Ma'am,

    It gives us immense pleasure at ```{company_name}``` to present our proposal to you. Given the transformative era we live in, we understand the importance of [specific project requirement]. Our proposal encapsulates [expected RFP response], meticulously tailored to meet and exceed your requirements.

    Our commitment to excellence is second to none, and with our rich history in [relevant industry/sector], we are excited to bring our expertise to the fore and contribute to the successful execution of the project which encompasses [scope].

    Partnering with renowned firms such as:
                                                           

    +-----+---------------------+-------------------+-----------------------+
    | No. |            Firms    | Address           | Country of Residence  |
    | --- | --------------------| ------------------| ----------------------|
    | 1.  | [Partner1]          | [Address1]        | [Country1]            |
    | 2.  | [Partner2]          | [Address2]        | [Country2]            |
    +-----+---------------------+-------------------+-----------------------+
                                                           
                                                           
    We are confident in delivering value-driven results. Our proposal remains valid till [validity date], and we are eager to discuss any modifications or specifics during this period.

    As partners in progress, we're eager to kick-start this journey together on [proposed start date]. We uphold the highest standards of integrity, and as a testament to our credibility, we have always distanced ourselves from any unethical practices.

    We cherish the opportunity to collaborate and bring this vision to life. We're only a call away to discuss the next steps.

    In anticipation,
                                                           
    [Your Signature],
                                                           
    [Your Name],
                                                           
    [Your Position],
                                                           
    ```{company_name}```
                                                           
    [Date]
    
    Format the header using markdown (### 1. TECHNICAL PROPOSAL SUBMISSION FORM)

    """)

######################################## Cover Letter/Executive Summary Section Prompts ##################################################


introduction_prompt = ChatPromptTemplate.from_template("""
     Using the details provided, craft a compelling introduction for the RFP response. This introduction should weave the provided details into a narrative, striking a balance between providing necessary information and not sounding repetitive. Position your company as an ideal fit for the project, bringing out its unique strengths, past achievements, and how it aligns with the client's needs.

      ### 2.1 Introduction
      
      **Your Company details**: ```{summary_company_profile}```
      **RFP Requirements**: ```{summary_requirement}```
      **Project Objective**: ```{objective}```

      As you shape the introduction, be guided by these points:
      - Begin by expressing genuine excitement about the opportunity presented by the RFP.
      - Delve into the challenges emphasized in the RFP. Illustrate briefly how your proposed solution addresses these issues.
      - Provide a concise preview of the forthcoming proposal sections, hinting at the comprehensive solution you intend to present.
      - Highlight your company's distinctive attributes, and if possible, provide a specific example or number that showcases your expertise and past success.
      - Convey commitment to the project's success, emphasizing the tangible value you aim to deliver.
      - Incorporate your company name naturally, making the narrative feel personalized and authentic.

      Format the header using markdown (### 2.1 Introduction).
      
      """)



# - Finish with a brief overview of major deliverables and your pledge to drive project fruition.

# overview_prompt = ChatPromptTemplate.from_template("""
#     Craft a **Technical Proposal Summary** using the information supplied. The aim is to create a compelling narrative that highlights the strength of your proposal and aligns it with the client's project vision.

#       ### 2.2 Brief Overview of the Technical Proposal
      
#       **RFP Requirements**: ```{summary_requirement}```
#       **Project Scope**: ```{scope}```
#       **Project Objective**: ```{objective}```
#       **Your Company's Responsibilities**: ```{vendor_responsibilities}```
#       **Deliverables**: ```{deliverable}```
#       **Company Profile**: ```{summary_company_profile}```

#        Follow these guidelines to structure the summary:
#         - Begin by acknowledging the specific project objectives as defined in the RFP.
#         - Showcase how your approach and expertise align seamlessly with the project's technical requirements.
#         - Highlight key technical aspects that set your company apart and reinforce your capabilities.
#         - Clearly outline the expected deliverables, providing clarity on what the client can expect.
#         - Emphasize the strength and accountability of your team.

#       Utilize markdown for the heading (### 2.2 Brief Overview of the Technical Proposal).
      
#       """)




business_context_prompt = ChatPromptTemplate.from_template("""
      Craft a **Business Context and Relevance** section for our RFP proposal. This section should elucidate the background, underscore the importance of the project to the client, and demonstrate how our company's expertise aligns with the client's needs. Please utilize the subsequent details:
     
      ### 2.2 Business Context and Relevance
      
      **RFP Requirements**: ```{summary_requirement}```
      **Project Scope**: ```{scope}```
      **Project Objective**: ```{objective}```
      **Company Profile**: ```{summary_company_profile}```
      format the header using markdown(### 2.2 Business Context and Relevance)
      """)

######################################## Company Overview Section Prompts ##################################################


organization_background_prompt = ChatPromptTemplate.from_template("""
     Provide a brief yet comprehensive background of your company in relation to the project requirements.

      **Your company Profile:** ```{company_profile}```
      
      **Project Requirements:** ```{summary_requirement}```
      
      ### 3.1 Organization Background
        - Introduce your company and its background.
        - Discuss how your company aligns with the project's needs.
        - Mention any industry certifications, affiliations, or recognitions that enhance your credibility.
        - Share your company's history, mission, and core values.
        - Use simple language and support your points with relevant examples.
        
        format only the header using  markdown(### 3.1 Organization Background)
      
      """)


organization_experience_prompt = ChatPromptTemplate.from_template("""
    Create a detailed **Organization Experience** section for our RFP proposal. This segment needs to underscore our company's track record and successes, especially those that are pertinent to the project's prerequisites. Present the experiences in a clear JSON format for versatility. Incorporate the provided data:

    **Project Requirements**: ```{summary_requirement}```
    **Project Goal**: ```{objective}```
    **Years of Operation**: ```{business_years}```
    **Expertise Domains**: ```{specialization_areas}```
    **Prior Client Engagements**: ```{past_projects}```

    ### 3.2 Experts and  Experience

    1. Emphasize the firm's operational duration and its pertinence to the RFP.
    2. Elaborate on expertise domains and elucidate their alignment with the project's imperatives.
    3. Chronicle past analogous ventures, stipulating:
      * Client Identity
      * Assignment Venue
      * Tenure of assignment (in months)
      * Professionals Deployed by our Firm: Count and Duration (Person-Months)
      * Initiation Date of Assignment (Month/Year) and Termination Date (Month/Year)
      * Key Personnel (e.g., Project Overseer/Coordinator, Chief Expert) and their contributions
      * Synopsis of services discharged by our crew

    Culminate with a persuasive assertion underscoring why our firm's antecedents make it the quintessential contender for the project.
    
    Do remember to encompass only analogous ventures that were culminated triumphantly in the recent past.
    Render the entire Organization Experience section as a single JSON object, with each of the above points being key-value pairs.
    Note: Do not make up answers that are not part of the provided details, if information is not available use unknown as the key-value.

    """)

achievements_recognitions_prompt = ChatPromptTemplate.from_template("""
    Based on our company details, craft the **Past Achievements and Recognitions** section for our RFP proposal. Ensure the content aligns with the specific RFP project/assignment at hand.

    **Company details** ```{company_profile}```
    **Project Requirements**: ```{summary_requirement}```
    
    ### 3.3 Past Achievements And Recognition

    1. Enumerate the significant awards and honors our company has received over the years, especially those that relate to the project's domain.
    2. Detail the industry recognitions that highlight our expertise and credibility in the relevant field.
    3. Extract and incorporate standout testimonials from our esteemed clients that emphasize our excellence and reliability.
    4. Spotlight key milestones that demonstrate our company's growth, innovation, and commitment to quality.

    Wrap up the section by emphasizing how our past achievements and recognitions make us a top contender for the project. 
    Use markdown for headers(### 3.3 Past Achievements And Recognition)

    """)

######################################## Understanding of the Project Section Prompts ##################################################


project_understanding_prompt = ChatPromptTemplate.from_template("""
      Please provide a succinct **overview and understanding** of the project based on:

      **RFP Requirements**: ```{summary_requirement}```
      **Project Scope**: ```{scope}```
      **Project Objective**: ```{objective}```

      ### 4. Understanding of the Project
      
      Craft a clear and concise response, demonstrating a deep understanding of the project's essence. Ensure the overview connects the requirements, scope, and objectives into a cohesive narrative.
      
      Format your header using markdown.(### 4. Understanding of the Project)

      """)

client_insight_prompt = ChatPromptTemplate.from_template("""
      Summarize your understanding of the client's project expectations based on:

      **RFP Requirements**: ```{summary_requirement}```
      **Expected RFP Response Types**: ```{expected_rfp_response}```
      
      ### 4.1 Insights into the Client's Needs
      
      Elaborate on how your solution aligns with the client's needs and goals. Ensure clarity and coherence.
      Use markdown for headers(### 4.1 Insights into the Client's Needs)

      
      """)

objective_and_goal_prompt = ChatPromptTemplate.from_template("""
      Elaborate on the project's core objectives and goals for an impactful RFP response. Please refer to:

      **Project Objective**: ```{objective}```
      
      ###  4.2 Established Objectives and Goals
      
      Strive for perfection in your response, making it both persuasive and organized.
      Use markdown for headers(### 4.2 Established Objectives and Goals)

      """)


comment_suggestion_prompt = ChatPromptTemplate.from_template("""
                                                                 
        Draft a vibrant **Comments and Suggestions** section for an RFP project, focusing on innovative enhancements for the Terms of Reference (TOR). Dive deep into areas like talent development, data security, training, and deliverables. Leverage details the following  details.

        Your Company Info: ```{summary_company_profile}```
        Project requirements: ```{summary_requirement}```
        Project Objectives: ```{objective}```
        
        ### 4.3  Comments and Suggestions

        💡 **Inspiration Corner**:

        - **Talent Development**:
          Forge partnerships with top universities, curating a robust talent pipeline for the project.
          
        - **Deliverables**:
          Craft a meticulous continuity plan. Evaluate talent readiness, skill gaps, and draft bridging strategies.
          
        - **Staff & Facilities**:
          Enlist cloud tech gurus, setting aside resources for their global insights during the feasibility phase.

        - **Technical Aspects**:
          Design a state-of-the-art Data Center blueprint, aligned with premier international standards.
          
        - **Security**:
          Embark on a dual-phase risk assessment, both pre and post security measures.

        Let the above inspirations guide, but not limit, your creative flair. Think big, think fresh!
        Use markdown for headers(### 4.3  Comments and Suggestions)
        
        """)

trends_and_business_case_prompt = ChatPromptTemplate.from_template("""
    You have been provided with RFP project requirements  delimited by triple backticks.

    Provide a comprehensive overview of the relevant trends and business case for the project or proposal.

    - Describe the current trends in the industry that are pertinent to the project.
    - Present a compelling business case that outlines the potential benefits and ROI (Return on Investment) for the proposed solution.
    - Use data, statistics, and examples to support your analysis.
    - Highlight how your approach aligns with the identified trends and contributes to the business case.

    ### 4.4 Trend and Business Cases
    
    **Business Case:** 
    
    Project Requirements:
         ```{requirement}```
         
      Use markdown for headers(### 4.4 Trend and Business Cases)
    """)



######################################## Approach/Methodology Section Prompts ##################################################
approach_methodology_prompt = ChatPromptTemplate.from_template("""
    Generate a compelling **Overview of the Approach** for our RFP response using the provided information:

    **Project Requirements**: ```{summary_requirement}```
    **Project Objectives**: ```{objective}```
    **Expected project response**: ```{expected_rfp_response}```
    **Client's Industry Trends (if available)**: ```{trends}```
    **Our Company's Strengths and Capabilities**: ```{company_strengths}```

    #### 5.1 Overview of the Approach

    Begin with an executive summary that reflects our deep understanding of the client's needs, challenges, and aspirations. This summary should serve as a captivating introduction to our approach.

    - 5.1.1 **Project Context**: Acknowledge the current industry landscape and any relevant trends, demonstrating awareness of the client's environment. If data or statistics are available, consider presenting them visually for impact.

    - 5.1.2 **Our Approach in a Nutshell**: Provide a concise yet comprehensive overview of our strategy to address the client's needs. Highlight the key elements of our approach that resonate with the client's objectives and showcase the synergy between their aspirations and our capabilities.

    - 5.1.3 **Aligning Strengths to Needs**: Utilize a well-structured table to align our company's core strengths and capabilities with the specific requirements outlined in the RFP. This table should be a visual representation of our suitability for the project, demonstrating a clear connection between what the client needs and what we excel at.
        +-------------------------------+--------------------------------------------+
        | Client's Needs                | Our Strengths & Solutions                  |
        |-------------------------------|--------------------------------------------|
        | (Extract from requirement)    | (Relevant strength from company_strengths) |
        | ...                           | ...                                        |
        +-------------------------------+--------------------------------------------+
    - 5.1.4 **Future Outlook**: Conclude this section with a forward-looking statement that envisions a successful partnership. Paint a picture of how our approach, backed by our proven track record, can lead to transformative results for the client. This statement should inspire confidence and excitement about what we can achieve together.

    Ensure that this overview is not only coherent and persuasive but also meticulously aligned with the client's requirements. Employ markdown for headers (#### 5.1 Overview of the Approach) and structured presentation to enhance readability and professionalism.

        """)


proposed_solution_prompt = ChatPromptTemplate.from_template(
    """
    You are tasked with crafting a detailed response to an RFP project based on the following information:
    - Client's problem or project summary.
    - Your expertise and positioning as the solution, based on your research.
    - The project's objectives and any known constraints or prerequisites.

    Using this information, provide a comprehensive description of your proposed solution, addressing the client's specific issues and how you plan to navigate challenges. 

    ### 5.2 Our Proposed Solution
    **PROBLEM SUMMARY**:
    {summary_requirement}

    **OUR EXPERTISE**:
    {proposal_expert}

    **PROJECT OBJECTIVES**:
    {objective}

    **GUIDELINES**:
    - Highlight the direct benefits and advantages the client will receive from your proposed solution.
    - Address potential challenges and how you plan to mitigate them.
    - Instead of naming specific tools or systems, discuss approaches, methodologies, and strategies you recommend, citing any industry trends or evidence.
    - Include mentions of post-implementation support, upgrades, or maintenance if relevant.
    - Use clear, concise language to ensure the proposal is easily understood, avoiding unnecessary jargon.
    - Consider embedding pertinent references or case studies to bolster credibility, making sure the proposal feels tailored and not generic.

    
    Use markdown for headers(### 5.1 Our Proposed Solution)
    """
)


solution_components_prompt = ChatPromptTemplate.from_template(
    """
    Given the overarching proposed solution for the RFP project, it's essential to delve deeper and provide a granular breakdown of the components that constitute this solution. This breakdown will help the client understand the intricacies of your approach and foster confidence in the feasibility and thoroughness of your proposal.
    
    **PROPOSED SOLUTION**:
    {proposed_solution}


    **INSTRUCTIONS**:
    1. Clearly list and define each primary component of your proposed solution.
    2. For each component, provide a brief description detailing its purpose, functionality, and how it integrates with other components.
    3. If relevant, mention any technologies, tools, or methodologies that will be employed for each component.
    4. Highlight any dependencies or prerequisites associated with the components.
    5. Ensure the explanation is succinct, clear, and free from jargon, unless it's industry-specific and vital to the description.

    ##### 5.2.1 Solution Components and Breakdown:

    1. **Component Name**:
       - **Purpose**: Why this component is vital to the solution.
       - **Description**: A brief overview of the component's functionality.
       - **Integration**: How this component interacts or complements other components.
       - **Technologies/Tools**: Any specific technologies or tools associated with this component.
       - **Dependencies**: Any prerequisites or dependencies related to this component.

    [Repeat the structure for each additional component]

    Conclude with an overarching summary that ties together the significance of each component in achieving the desired outcome for the client's project.
    
    Use markdown for headers(##### 5.2.1  Solution Components and Breakdown:)
    """
    
)


tools_and_technology_prompt = ChatPromptTemplate.from_template(
    """
        Given the details of the:
        - PROPOSED SOLUTION:
        {proposed_solution}

        - SOLUTION COMPONENTS AND BREAKDOWN:
        {solution_components}
        
        ##### 5.2.2 Tools and Technologies Utilized:

        Please detail the essential tools and technologies incorporated in your proposed solution. Address the following:

        1. Relevance: Why were these specific tools and technologies chosen? How do they align with the requirements or challenges presented?
        2. Advantages: What benefits do these tools and technologies offer over other potential alternatives?
        3. Implementation: How will these tools and technologies be seamlessly integrated into the client's existing ecosystem? 
        4. Scalability & Future Proofing: How do these tools and technologies ensure that the solution can evolve with future needs?

        If no specific tools or technologies are employed, provide reasoning behind the decision to avoid or exclude them.

        Your response should be precise and should highlight the strategic value each tool or technology brings to the solution.

        Use markdown for headers(##### 5.2.2 Tools and Technologies Utilized:)
    """
)



benefits_prompt = ChatPromptTemplate.from_template("""
        Given the following details:

        - PROPOSED SOLUTION:
        {proposed_solution}

        - PROBLEM SUMMARY:
        {summary_requirement}
        
        ### 5.3 Benefits and Outcomes of Our Approach and Methodology:

        Please outline the significant benefits the client can expect from implementing your proposed solution. Specifically, address the following:

        1. Increased Efficiency: How will your solution streamline operations or processes?
        2. Cost Savings: Can the client expect reduced expenses, and if so, in what areas?
        3. Improved Performance: What aspects of their operations will see noticeable improvement?
        4. Other Positive Outcomes: Are there other benefits not covered in the above?

        Additionally, highlight clear Key Performance Indicators (KPIs) that are expected to improve post-implementation.

        Your response should be concise, impactful, and tailored to emphasize the tangible advantages to the client's organization.

        Use markdown for headers(### 5.3 Benefits and Outcomes of Our Approach and Methodology)

        """)

differentiators_prompt = ChatPromptTemplate.from_template("""
        Given the details:

        - PROPOSED SOLUTION:
        {proposed_solution}

        - PROBLEM SUMMARY:
        {summary_requirement}
        
        Your Company Profile: ```{company_profile}```
        
        ### 5.4 What Differentiates Us From The Rest

        Please articulate the unique differentiating factors of our solution. Specifically, address the following:

        1. Innovative Technology: What cutting-edge tools or technologies are you using that others aren't?
        2. Unique Methodology: How does your approach differ from standard practices?
        3. Exclusive Expertise: What knowledge or experience does your team possess that sets you apart?

        These differentiators should showcase why our solution stands out and is the preferred choice over competitors.

        Your response should be both concise and impactful, emphasizing the tangible advantages these unique factors bring to the client's organization.

        Use markdown for headers(### 5.4 What Differentiates Us From The Rest)
     """)


client_collaboration_prompt = ChatPromptTemplate.from_template(
    """
    Based on the provided information:

    - PROJECT OBJECTIVE:
    {objective}

    - CLIENT'S COLLABORATION METHODS AND PREFERRED MEANS OF COMMUNICATION:
    {collaboration_methods}

    - FREQUENCY & FORMAT:
    {update_frequency}
    
    ### 5.5 Client Collaboration & Feedback

    Detail your approach to fostering close collaboration with the client and ensuring their feedback drives the project's success. Specifically, delve into:

    1. Collaboration Tools: Specify the platforms, tools, or software that will be utilized to facilitate direct collaboration with the client.
    2. Feedback Loops: Describe the structured intervals and methods through which client feedback will be sought, such as regular check-ins, status updates, and review meetings.
    3. Integration of Feedback: Discuss the measures in place to promptly address and implement client feedback into the ongoing work.
    4. Addressing Client Concerns: Highlight the processes for attending to client queries, concerns, or suggestions, ensuring their active involvement and satisfaction.
    5. Contingencies for Collaboration: Address any backup plans or strategies to handle potential collaboration challenges, ensuring the project remains on track.

    Your response should underscore the significance of open communication, the value placed on the client's input, and the strategies to ensure their active participation aligns with the project's objectives.

    Use markdown for headers(### 5.5 Client Collaboration & Feedback)
    """
)

###################################################################################################################3


##########################################################  Project Management ################################################################

team_composition_prompt = ChatPromptTemplate.from_template("""
        Drawing from the specific details provided in the Request for Proposal (RFP):

        - PROPOSED SOLUTION:
        {proposed_solution}

        - RFP PROJECT PROBLEM SUMMARY:
        {summary_requirement}

        Create a structured JSON representation of your project team tailored to the given RFP. Ensure you adhere strictly to the provided details and resist the urge to add extra roles or members not explicitly mentioned. 

        Your JSON should encapsulate:

        1. Team Structure: Limit your description to the core team relevant to the given solution.
        2. Key Roles: Only highlight the critical roles essential to the problem summary and proposed solution.
        3. Individual Expertise: Be concise in providing details on the member's expertise, experience, and relevance to this project. Do not invent team members or roles.
        
        ```json
        {{
            "Team_Structure": "Only describe based on the information provided",
            "Key_Roles": [
                {{
                    "Role": "Role Name – based on the proposed solution and problem summary",
                    "Responsibilities": "Specific duties relevant to the RFP",
                    "Member_Name": "If a name is provided, include; otherwise, label as 'To be Assigned'",
                    "Expertise": "Brief on expertise relevant to the RFP",
                    "Relevance_to_Project": "Tailor the relevance to the specific RFP details"
                }},
                // Only add roles explicitly relevant to the RFP.
            ]
        }}
        ```

        This is a response for a specific RFP, and any information beyond what has been provided or directly inferred should be avoided.

        ### Team Composition and Roles:

""")


communication_strategy_prompt = ChatPromptTemplate.from_template("""
        Based on the following information:

        - PROPOSED SOLUTION:
        {proposed_solution}

        - PROBLEM SUMMARY:
        {summary_requirement}

        - PROJECT TIMELINE:
        {project_duration_and_key_stages}

        Please describe the communication approach your team will employ internally and with the client at a high level. Specifically, touch upon the following:

        1. Tools and Platforms: Which communication tools, platforms, or software will the team use for internal discussions and decision-making processes?
        2. Communication Hierarchy: How is information cascaded within the team? Who are the primary decision-makers, and how is information relayed to them?
        3. High-Level Client Communication: While detailed collaboration will be covered separately, briefly discuss how you intend to maintain transparency with the client regarding significant milestones, changes, or decisions.
        4. Points of Contact: Identify the primary and secondary contacts for the client for high-level project discussions or concerns.
        5. Contingencies: Outline any measures in place to handle communication breakdowns or barriers, ensuring that communication flows remain consistent and efficient.

        Your response should be structured and clear, emphasizing the team's dedication to transparency, effective communication, and collaboration at both the team and client levels.

        ### Our Communication Strategy:

""")

risk_management_prompt = ChatPromptTemplate.from_template("""
        Drawing from the following Request for Proposal (RFP) details:

        - PROPOSED SOLUTION:
        {proposed_solution}

        - PROBLEM SUMMARY:
        {summary_requirement}

        - KNOWN PROJECT CHALLENGES:
        (Consider any potential challenges or obstacles explicitly related to the given problem summary and proposed solution.)

        Construct a robust risk management approach tailored to the specific nature of this project. Ensure your description touches upon:

        1. Risk Identification: Specify how your team, given the context of this RFP, would identify potential risks. Highlight methodologies that are particularly relevant to the problem statement and proposed solution.
        2. Risk Assessment: Delve into how you would evaluate risks based on their impact and likelihood, and mention if you'd leverage any models or matrices specifically suited to the project's nature.
        3. Risk Mitigation Strategies: Detail strategies that are pertinent to the known challenges and potential risks of this project. How do these strategies ensure the project's success?
        4. Stakeholder Engagement: Describe how stakeholder input will be integrated into the risk management process, ensuring alignment with their expectations and concerns.
        5. Contingency Plans: Discuss contingency plans tailored to the project's potential challenges, ensuring the project stays on course even if risks materialize.
        6. Continuous Monitoring and Feedback Loop: Elaborate on how risks will be continuously monitored and reassessed throughout the project, and how learnings from any materialized risks will be integrated back for future reference.
        7. Risk Reporting: Briefly touch upon how and when risks (and their statuses) will be communicated to stakeholders, ensuring transparency.

        Your response should not only be comprehensive but also tailored to the specific requirements and challenges presented in this RFP, highlighting your team's expertise and proactive approach.

        If you don't have information on any of the requested details, simply input **unknown** as the value.

        ### Our Risk Management Approach:

""")


work_schedule_prompt = ChatPromptTemplate.from_template("""
        Drawing from the specific details provided in the Request for Proposal (RFP):

        - PROJECT OBJECTIVES:
        {objective}
        
        - RFP PROJECT DURATION AND KEY MILESTONES:
        {project_duration_and_key_stages}
        
        - RFP PROJECT Requirements:
        {summary_requirement}

        Create a structured JSON representation of the anticipated work schedule and plan for the project. Your structure should encompass:

        1. Individual tasks or activities strictly based on the provided milestones.
        2. Start and end dates for each task aligned with the RFP's project duration.
        3. Dependencies between tasks, but only if they have been explicitly mentioned.
        4. Responsible team members or roles for each task, without adding additional roles not mentioned.
        5. Status or progress indicators, ensuring it's relevant to the project's start stage.

        Remember to resist the urge to extrapolate or add information not explicitly present or directly inferred from the RFP details.

        ```json
        {{
            "Project_Name": "Provide the project name or title based on **objectives**",
            "Total_Duration": "Provide the duration based on **RFP PROJECT DURATION AND KEY MILESTONES",
            "Tasks": [
                {{
                    "Task_Name": "Directly derive from the provided key milestones",
                    "Start_Date": "Begin date within the RFP's project duration",
                    "End_Date": "End date within the RFP's project duration",
                    "Dependencies": ["List ONLY the dependent tasks explicitly mentioned in the RFP"],
                    "Responsible_Role": "Mention the role ONLY if specified for the task in the RFP"
                }},
                // Add ONLY the tasks explicitly mentioned or directly inferred from the RFP.
               Add more tasks based on the provided key milestones, objective.

            ]
        }}     
        ```

        ### Anticipated Work Schedule and Plan:

""")

####################################################################################################################################3333


######################################## Timeline/Schedule ##################################################
timeline_milestones_prompt = ChatPromptTemplate.from_template(
    """
    You are tasked with detailing a project timeline that clearly defines the major milestones, expected durations, and key deliverables based on the following information:
    - Overall project scope and objectives.
    - Expected project duration or deadline.
    - Key stages of the project.
    
    Using this information, develop a structured timeline that assures the client of your ability to manage time efficiently and ensures timely delivery of each phase of the project.
    
    **PROJECT Requirements**:
    {summary_requirement}
    
    **PROJECT Objectives**:
    {objective}

    **PROJECT SCOPE**:
    {scope}

    **EXPECTED DURATION AND KEY STAGES**:
    {project_duration_and_key_stages}
    
    **GUIDELINES**:
    - Start with an overview of the entire timeline, providing a clear picture of the project's lifecycle.
    - Break down the timeline into phases or stages, detailing the major milestones within each.
    - Clearly define the expected outcomes or deliverables at the end of each milestone.
    - Highlight any dependencies or prerequisites that could influence the timeline.
    - Address any contingencies in place for potential delays or risks, assuring the client of the robustness of your planning.
    - Use graphical elements, like Gantt charts or flow diagrams, if possible, to visually represent the timeline.

    ### 8.1 Timeline and Milestones
    
    Just provide the **Timeline and Milestones** and nothing more.
    
    Use markdown for headers(### 8.1 Timeline and Milestones)
    """
)

deliverables_deadlines_prompt = ChatPromptTemplate.from_template("""
        Drawing from the specific details provided in the Request for Proposal (RFP):

        - PROJECT OBJECTIVES:
        {objective}

        - RFP PROJECT DURATION AND KEY MILESTONES:
        {project_duration_and_key_stages}

        Craft a structured JSON representation of the main deliverables and their associated deadlines. Ensure that each deliverable is directly tied to the project's objectives and milestones provided in the RFP. Do not add any deliverables or deadlines not explicitly mentioned or directly inferred from the RFP details.

        ```json
        {{
            "Project_Name": "Provide the project name or title based on **objectives**",
            "Total_Duration": "Provide the duration based on **RFP PROJECT DURATION AND KEY MILESTONES",
            "Main_Deliverables": [
                {{
                    "Deliverable_Name": "Name of the deliverable derived from RFP objectives/milestones",
                    "Description": "A concise description based on the RFP's context",
                    "Deadline": "Specific date within the RFP's project duration"
                }},
                // Repeat for all deliverables mentioned or inferred from the RFP.
            ]
        }}
        ```

        This response should be tailored to the specific RFP, ensuring that all deliverables and deadlines align with the provided details.

""")




####################################################################################################################################3333

################################################################ Project Implementation Plan ####################################################################


implementation_plan_prompt = ChatPromptTemplate.from_template("""
        You are an expert Proposal Manager with years of experience working on RFP projects.\n\n
        You have been provided with the following information:\n
        \n- A proposed solution from you.
        \n- A summary of the problem statement and requirements from you.
        \n- Project timeline.
        
        ### 6. Project Implementation Plan
        #### 6.1 Implementation Plan
        
        Lay out a step-by-step plan that you will adopt to implement the solution. Include timelines, milestones, and key deliverables. 
        Describe how you will continuously monitor the progress and make adjustments if necessary during the implementation.

        PROPOSED SOLUTION:
        ```{proposed_solution}```

        PROBLEM SUMMARY:
        ```{summary_requirements}```
        
        PROJECT TIMELINE:
        ```{timeline_milestones}```

        Implementation Plan:
        
        Ensure that your implementation plans clearly demonstrates the strategic differentiators of your proposed solution and highlights the concrete benefits it offers to the client's organization.

        Use markdown for headers(### 6. Project Implementation Plan\n
                                        #### 6.1 Implementation Plan)
""")


key_stages_and_phases_prompt = ChatPromptTemplate.from_template("""
    Based on the provided details in the RFP:
    
    - PROPOSED SOLUTION:
    ```{proposed_solution}```
    
    - PROJECT REQUIREMENTS:
    ```{summary_requirements}```
    
    - PROJECT OBJECTIVE:
     ```{objective}```
     
    - PROJECT TIMELINE:
    ```{timeline_milestones}```
    
    - PROJECT DELIVERABLES:
    ```{deliverable}```

    AI Assistant: Your task is to Create a structured breakdown of the key stages and phases of the project tailored to the given RFP. Ensure that the stages and phases align closely with the proposed solution, problem summary, and project timeline.

    {{
        "Key_Stages": [
            {{
                "Stage": "Stage name based on **PROPOSED SOLUTION**/**PROJECT REQUIREMENTS**",
                "Requirements": "Requirements based on **PROPOSED SOLUTION**/**PROJECT REQUIREMENTS**",
                "Objectives": "Objectives aligned with **PROJECT OBJECTIVE**",
                "Deliverables": "Deliverables based on **PROJECT DELIVERABLES**/**PROPOSED SOLUTION**/**PROJECT TIMELINE**",
                "Timeline": "Timeline within **PROJECT TIMELINE**"
            }},
            // Repeat for all key stages.
        ]
    }}
      Format the output as JSON, including the relevant keys and values you can find.
      Do not make up answers that are not part of the provided details, if information is not available use unknown as the key-value.
""")


resource_allocation_and_dependencies_prompt = ChatPromptTemplate.from_template("""
    Informed by the following RFP details:

    - PROPOSED SOLUTION:
    {proposed_solution}

    - PROBLEM SUMMARY:
    {summary_requirements}

    - PROJECT TIMELINE:
    {timeline_milestones}

    - KEY STAKEHOLDERS:
    {key_stakeholders}

    AI Assistant: Your task is to create a structured JSON representation detailing the resource allocation and dependencies for this project. Make sure it aligns closely with the RFP information provided.
    
    {{
        "Resource_Allocation": [
            {{
                "Resource_Type": "Type based on **PROPOSED SOLUTION**",
                "Skill_Set": "Specific skills and/or certifications required",
                "Quantity_Primary": "Primary quantity needed per **PROJECT TIMELINE**",
                "Quantity_Backup": "Backup quantity needed",
                "Responsibility": "Individual/Team responsible for managing this resource",
                "Hierarchy": "Position in team hierarchy (e.g., Team Lead, Member)",
                "Timeline": "Resource availability within **PROJECT TIMELINE**",
                "Scalability_Options": "Options for scaling up or down based on project needs"
            }},
            // Repeat for each type of resource.
        ],
        "Dependencies": [
            {{
                "Dependency_Name": "Name based on **PROPOSED SOLUTION**/**PROJECT REQUIREMENTS**",
                "Owner": "Who within your team or the client's team is responsible",
                "Impact": "Detailed impact on project stages based on **PROJECT TIMELINE**",
                "Severity": "Critical/Medium/Low impact",
                "Mitigation_Plan": "Primary steps to mitigate delays or issues",
                "Alternative_Plan": "Secondary steps if primary mitigation fails",
                "Mitigation_KPIs": "Metrics for success of the mitigation plan",
                "Timeline_for_Mitigation": "Timeline for implementing/reviewing the mitigation plan"
            }},
            // Repeat for each identified dependency.
        ]
    }}
    
    Format the output as JSON, including the relevant keys and values you can find.
    Do not make up answers that are not part of the provided details, if information is not available use unknown as the key-value.
    
""")

contingency_measures_prompt = ChatPromptTemplate.from_template("""
    AI Assistant: Your task is to generate the 'Contingency Measures' section of our RFP response. The information provided in the RFP is essential, and your output needs to be thorough yet concise, demonstrating our expertise and preparedness for the project. Make sure your output closely mirrors a human-generated response in tone and complexity.

    RFP Details for Reference:

    - PROPOSED SOLUTION:
    {proposed_solution}

    - PROBLEM SUMMARY:
    {summary_requirements}

    - PROJECT TIMELINE:
    {timeline_milestones}

    - KEY STAKEHOLDERS:
    {key_stakeholders}
    
    #### 6.4 Contingency Measures

    Guidelines for Crafting the Contingency Measures:

    ### Contingency Measures:
    
    - Risk Identification: Use insights from the **PROPOSED SOLUTION**, **PROBLEM SUMMARY**, and **PROJECT TIMELINE** to identify potential risks.
    - Risk Assessment: For each identified risk, provide a 'Likelihood' rating. Support your assessment with data points or analogous project experiences if possible.
    - Mitigation Strategies: Discuss immediate, short-term, and long-term steps. Be specific about the tools, techniques, or best practices that will be employed.
    - Stakeholder Communication: Detail how key stakeholders will be informed and engaged throughout the process.
    - Adaptive Measures: Outline alternative strategies ('Plan B' options) should primary mitigation steps prove ineffective.

    Note: Your narrative should be rooted in the complexities as delineated in the RFP, spotlighting our team's resourcefulness and readiness to navigate through potential challenges.
    Use markdown for headers(#### 6.4 Contingency Measures)
""")

####################################################################################################################################3333

##########################################################  Financial TOC ################################################################

finance_toc = """
### Table of Contents

##### 1. Executive Summary
  - 1.1 Introduction
  - 1.2 Key Financial Highlights

##### 2. Costing Breakdown
  - 2.1 Direct Costs
    - 2.1.1 Labor Costs
    - 2.1.2 Materials and Equipment
    - 2.1.3 Software and Licensing Fees
  - 2.2 Indirect Costs
    - 2.2.1 Overheads
    - 2.2.2 Administration and Operational Costs
  - 2.3 Contingency Funds
  - 2.4 Taxes and Duties

##### 3. Pricing Model
  - 3.1 Pricing Philosophy
  - 3.2 Pricing Structure
    - 3.2.1 Fixed Pricing
    - 3.2.2 Variable Pricing
  - 3.3 Discounts and Incentives

##### 4. Payment Terms and Conditions
  - 4.1 Payment Milestones
  - 4.2 Accepted Payment Methods
  - 4.3 Late Payment Penalties

##### 5. Financial Risk Analysis
  - 5.1 Risk Identification
  - 5.2 Risk Quantification
  - 5.3 Risk Mitigation Strategies

##### 6. Supporting Documents
  - 6.1 Tax Returns and Audited Financial Statements
  - 6.2 Banking References
  - 6.3 Proof of Insurance

##### 7. Conclusion and Final Remarks

##### 8. Appendices

"""

####################################################################################################################################3333


##########################################################  Financial Executive Summary ################################################################
finance_introduction_prompt = """
     Given the following details:
     
      **Company's Background**: ```{0}```
      **Client's Objectives**: ```{1}```
      **RFP Financial Requirements**: ```{2}```
      **Scope of Work**: ```{3}```

    #### 1.1 Introduction:

    Please create an introductory section for our Financial Proposal that accomplishes the following goals:

    1. **Engagement**: Quickly capture the client's attention with a compelling opening statement.
    2. **Contextualization**: Briefly outline the current challenges or opportunities the client is facing.
    3. **Relevance**: Explain why our proposal is timely and how it aligns with the client's objectives.
    4. **Scope of Work**: Provide a high-level overview of the proposed financial solution, including key elements such as the project duration and estimated budget.
    5. **Objective**: State the primary objectives of our proposal in a clear and concise manner.

    Your response should serve as an engaging and informative preamble that sets the stage for the detailed solution that follows. Make sure your language is client-centric and tailored to the financial sector. Use specific financial jargon where appropriate but keep the language accessible.

    Use markdown for headers (#### 1.1 Introduction:)
    
    """


# finance_introduction_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_finance_introduction_prompt])

# finance_introduction_prompt_2 = ChatPromptTemplate.from_template("""
#     Craft an impactful and concise introduction using the details below. Your primary goals are to engage the reader immediately, position your company as the unparalleled choice, and create anticipation for the rest of the proposal.

#     **Your Company Background**: ```{summary_company_profile}```
#     **Client's Objectives**: ```{objective}```
#     **RFP Financial Requirements**: ```{rfp_financial_requirements}```
#     **Scope of Work**: ```{scope}```

#     Guidelines:
#     - Start with a crisp opening line that blends professionalism with excitement about the RFP opportunity.
#     - Tackle the RFP's financial aspects with precision. Use one or two sentences to show how your company’s capabilities directly address these requirements.
#     - Provide a sneak-peek of upcoming sections in one sentence to pique interest without giving too much away.
#     - Showcase your company's unique strengths with concrete data—think percentages, dollar amounts, or case study outcomes—to add credibility.
#     - Articulate your dedication to the client's objectives using concise and specific language; remove any fluff.
#     - Include your company's name naturally, but just once or twice for optimum impact. Overuse can be off-putting.

#     Format the header using markdown (### 2.1 Introduction).
# """)

####################################################################################################################################3333

##########################################################  Costing Breakdown ################################################################


costing_breakdown_intro_prompt = ChatPromptTemplate.from_template("""
    Given the following details:

    - CLIENT'S COMPANY NAME:
    {client_company_name}

    - YOUR COMPANY NAME:
    {your_company_name}

    - PROPOSED SOLUTION:
    {proposed_solution}

    - SCOPE OF WORK:
    {scope}

    - PROJECT DURATION:
    {project_duration_and_key_stages}

    #### 2. Costing Breakdown: Introduction

    Please provide a concise yet thorough introduction for the Costing Breakdown section of our financial proposal. The introduction should:

    1. State the purpose of the Costing Breakdown section.
    2. Briefly outline the components that will be discussed (Direct Costs, Indirect Costs, Contingency Funds, Taxes and Duties).
    3. Indicate the importance of this section to the {client_company_name} in understanding the financial implications of the project.
    
    Your response should establish a context for the reader, preparing them to delve into the detailed financial aspects of the proposed solution.

    Use markdown for headers (#### 2. Costing Breakdown: Introduction).
""")



labor_costs_text_prompt = ChatPromptTemplate.from_template("""
    Given the following details:

    - CLIENT'S COMPANY NAME:
    {client_company_name}

    - YOUR COMPANY NAME:
    {your_company_name}

    - LIST OF ROLES INVOLVED:
    {roles_hourly_rate}

    - PROJECT DURATION:
    {project_duration_and_key_stages}

    ###### Text Description for 2.1.1 Labor Costs

    Please provide a comprehensive textual description that outlines the types of labor required for this project. Your text should detail the roles, skill levels, and duration for each role involved. 

    Your description should help the {client_company_name} understand the human resource aspects involved in the proposed solution.
""")

labor_costs_table_prompt = ChatPromptTemplate.from_template("""
    Given the following details:

    - CLIENT'S COMPANY NAME:
    {client_company_name}

    - YOUR COMPANY NAME:
    {your_company_name}

    - LIST OF ROLES INVOLVED AND HOURLY RATE FOR EACH ROLE:
    {roles_hourly_rate}
    
    - PROJECT OBJECTIVE:
    {objective}

    - ESTIMATED HOURS FOR EACH ROLE:
    figure this out from your domain knowledge onProject execution

    ###### JSON Output for 2.1.1 Labor Costs

    Please create a JSON output that itemizes labor costs. The JSON should include keys for roles, estimated hours, and hourly rates. Each role involved in the project should have its corresponding estimated hours and hourly rates listed.
    Format the output as JSON, including the relevant keys and values you can find.

""")

extract_roles_with_rates_prompt = ChatPromptTemplate.from_template("""
    Given the following details:

    - PROJECT NAME:
    {project_name}

    - PROJECT OBJECTIVE:
    {objective}

    - PROBLEM STATEMENT:
    {problem_statement}

    - PROJECT DURATION:
    {project_duration_and_key_stages}

    ##### Extract List of Roles and Hourly Rates

    Based on the project name, project objective, problem statement, and duration provided, please generate a JSON-formatted list of roles and their estimated hourly rates that are likely to be involved in executing this project. Your list should be comprehensive yet concise, including roles across various expertise and departments as needed.

    Specifically, the output should be in JSON format with roles as keys and their estimated hourly rates as values. For example: {{"Project Manager": 60, "Developer": 50, "QA Tester": 40}}

""")

#---------------------------------------------------------------------------------------------------------------------------------#

materials_equipment_text_prompt = ChatPromptTemplate.from_template("""
    Given the following details:

    - PROJECT NAME:
    {project_name}
    
    - PROJECT OBJECTIVE:
    {objective}

    - PROJECT DURATION:
    {project_duration_and_key_stages}

    ###### 2.1.2 Materials and Equipment: Text Introduction

    Please provide an introductory text that describes the types of materials and equipment required for this project. Include what they will be used for and why they are essential to meet the project objectives. Your introduction should be concise and informative.
""")

item_prompt = ChatPromptTemplate.from_template("""
        An RFP problem statement summary and a Proposed Work Schedule are provided to you, delimited by triple backticks.

        Your task is to clearly outline all the materials, items, equipments, and infrastructures needed to achieve this project in a Python list.

        Proposed Solution:
        ```{proposed_solution}```

        PROBLEM SUMMARY:
        ```{problem_statement}```
        
        ```{objective}```

        Please provide a Python list containing all the required materials, items, equipment, and infrastructure needed for the project.
""")


software_licensing_text_prompt = ChatPromptTemplate.from_template("""
    Given the following details extracted from the RFP:

    - PROJECT NAME:
    {project_name}
    
    - PROJECT OBJECTIVE:
    {objective}

    - PROJECT DURATION:
    {project_duration_and_key_stages}

    - SOFTWARE AND LICENSING REQUIREMENTS:
      ```Figure this out based on your domain knowledge.```

    ###### 2.1.3 Software and Licensing Fees: Text Explanation

    Please provide a detailed explanation for any software tools and licenses that will be utilized in this project. Explain why these specific software tools and licenses are needed and how they align with the project objectives and requirements outlined in the RFP.
""")


software_licensing_table_json_prompt = ChatPromptTemplate.from_template("""
    Given the following details extracted from the RFP:

    - PROJECT NAME:
    {project_name}
    
    - PROJECT OBJECTIVE:
    {objective}

    - PROJECT DURATION:
    {project_duration_and_key_stages}

    - SOFTWARE AND LICENSING REQUIREMENTS:
    ```Figure this out based on your domain knowledge.```

    ###### 2.1.3 Software and Licensing Fees: Table

    Generate a detailed JSON object listing the types of software and licenses required for this project along with their respective costs. The JSON object should have keys for 'Software/License Name', 'Description', 'Quantity', 'Unit Cost', and 'Total Cost'.

    Example JSON structure:
    {{
        "Software_1": {{
            "Description": "string",
            "Quantity": "number",
            "Unit Cost": "currency",
            "Total Cost": "currency"
        }},
        "License_1": {{
            "Description": "string",
            "Quantity": "number",
            "Unit Cost": "currency",
            "Total Cost": "currency"
        }},
        ...
    }}
""")


####################################################################################################################################

######################################################### INDIRECT COST ##################################################################

overheads_text_prompt = ChatPromptTemplate.from_template("""
    Given the details:

    - PROJECT NAME:
    {project_name}
    
    - PROJECT OBJECTIVES:
     {objective}
    
    - PROJECT  DELIVERABLES:
     {deliverable}

    - PROJECT SUMMARY REQUIREMENTS
    {summary_requirement}
    
    ###### 2.2.1 Overheads: Text

    Describe the various possible overhead costs such as utilities, rent, and insurance that will be incurred for the project. Provide justification for each type of overhead.

  """)

overheads_json_prompt = ChatPromptTemplate.from_template("""
    Given the details:

    - PROJECT NAME:
    {project_name}

    - PROJECT OBJECTIVES:
    {objective}
    
    - PROJECT SUMMARY REQUIREMENTS
    {summary_requirement}

    ###### 2.2.1 Overheads: JSON

    Generate a detailed JSON object that lists the types of overhead costs for this project along with their respective amounts in the currency of the country. The JSON should have keys for 'Overhead Type', 'Description', and 'Estimated Amount'.

""")

overheads_graph_json_prompt = ChatPromptTemplate.from_template("""
    Given the details:

    - PROJECT NAME:
    {project_name}
    
    - OVERHEAD COST:
    {overheads_table}

    - TIMEFRAME:
    {project_timeline}

    ###### 2.2.1 Overheads: Graph Data in JSON

    Generate a JSON object containing data that can be used to produce a bar chart comparing different overhead costs. The JSON should contain keys such as 'Overhead Type' and 'Amount', which will enable the manual creation of a bar plot to display the proportion of each overhead cost in relation to the total.

""")



####################################################################################################################################
language_proficiency_prompt = ChatPromptTemplate.from_template("""
    Check if Language Skills are part of the Expected  Responses in the RFP project. 
    If "Language Skills" is mentioned, provide information about your company's language proficiency.
    
    The  primary language of your company **English**.
    
    Company Profile: ```{company_profile}```
    
    Expected proposal Response: ```{expected_rfp_response}```
    
    Use the section you find the Langauge skill in the **Expected proposal Response** as the title header for this section.    
    Provide a detailed response about the language proficiency and proficiency level in each language.
    """)


     
cv_prompt = "I, the undersigned, certify that to the best of my knowledge and belief, this CV correctly describes myself, my qualifications, and my experience, and I am available, as and when necessary,\
             to undertake the assignment in case of an award. I understand that any misstatement or misrepresentation described herein may lead to my disqualification or dismissal by the Client."
     
code_of_conduct_query = """Extract and summarize the "Code of Conduct" from the RFP document, noting their location. Report if no Code of Conduct are found."""

code_of_conduct_prompt = """

        Your have a Code of Conduct from a Request for Proposal document  delimited by triple backticks.
        You also have a human-generated Code of Conduct **response:**.

        Your task:

        - Write a Code of Conduct section of the RFP proposal that is better than a Human response.
        - Apply Markdown formatting to the headers and subheaders in your text.
        
        Code of Conduct:
        ```{}```
      """
      
terms_and_conditions_prompt = """Extract and summarize the "Terms and Conditions" from the RFP document, noting their location. Report if no Terms and Conditions are found."""
      
proposal_securing_declaration_prompt = ChatPromptTemplate.from_template("""
        Please create the "Proposal Securing Declaration Form" section for our RFP response. You have the following information:

        Your Company Information:
        ```{company_profile}```
        
        Project Requirement:
        ```{summary_requirement}

        Terms and Conditions in the RFP:
        ```{term_and_conditions}```

        Your task:

        1. Create a "Proposal Securing Declaration Form" section using Markdown formatting.
        2. Include the Vendor Information, acknowledging the Authorized Representative's intent to submit the proposal.
        3. Reference and summarize the key Terms and Conditions from the RFP.
        4. Express your commitment to complying with these terms.
        5. Mention your understanding of and agreement with the Project Requirements.
        6. Sign and date the Declaration Form.

        Ensure the content is clear, professional, and adheres to standard formatting practices. Thank you.
      """)

special_power_attorney_prompt = ChatPromptTemplate.from_template("""
        Please create the "Special Power of Attorney" section for our RFP response. You have the following information:

        Your Company Information:
        ```{company_profile}```
        
        Project Requirement:
        ```{summary_requirement}

        Your task:

        1. Clearly state that your company, [Your Company Name], hereby appoints [Authorized Representative's Name] as its authorized representative to act on its behalf for the purpose of preparing and submitting the proposal in response to RFP [RFP Number].
        2. Mention the authority granted to the authorized representative, including the ability to sign documents and make commitments on behalf of the company.
        3. Provide contact information for the authorized representative.
        4. Express your company's commitment to abide by all the terms and conditions of the RFP.
        5. Include any additional relevant information.

        Please ensure the content is clear, professional, and adheres to standard formatting practices. Thank you.
      """)

anti_bribery_coc_prompt = """Extract and summarize the "Anti-Bribery" or related term  from the RFP document. Report if no Anti- Bribery are found."""
      


        
anti_bribery_undertaking_prompt = """
    If the RFP includes an "Anti-Bribery Policy and Code of Conduct" section, proceed as follows. If not, take no action.

    Create the "UNDERTAKING ON ANTI-BRIBERY POLICY / CODE OF CONDUCT AND COMPLIANCE PROGRAM" section for our RFP response using the provided information:

    Your Company Information:
    ```{0}```

    RFP Anti-Bribery Policy and Code of Conduct:
    ```{1}```

    Your task:

    1. Start with a heading, "Undertaking on Anti-Bribery Policy and Code of Conduct."
    2. Clearly state your commitment to ethical business practices and anti-bribery policy compliance.
    3. Mention your Anti-Bribery Policy/Code of Conduct and Compliance Program.
    4. Express your commitment to not engage in improper inducements or rewards.
    5. Sign and date the Undertaking.

    Your goal is to convey your commitment to ethical conduct and anti-bribery compliance briefly and clearly, adhering to standard formatting practices.
   """
   

financial_proposal_prompt = ChatPromptTemplate.from_template("""
        - You've been given your company name, expected proposal response, project requirement, and project scope.
        Task:
        Write a financial proposal submission form. Mention the proposal response you're submitting, your company name (if applicable), timeline, and address the recipient as "Sir" or "Ma'am".

        Company name: ```{company_name}```
        Project Scope: ```{scope}```
        Project Requirement: ```{requirement}```
         
        - Ensure to mention your company name where applicable.
        - Sign and date the form.
        
         Note: The example below is for reference only. Please be creative and innovative.
         
        **Example FINANCIAL PROPOSAL SUBMISSION FORM**:
        
        ### FINANCIAL PROPOSAL SUBMISSION FORM
       
        To: [Name and address of Client]

        Dear Sirs:
        
        We, the undersigned, offer to provide the consulting services for [Insert title of
        assignment] in accordance with your Request for Proposal dated [Insert Date] and our
        Technical Proposal. Our attached Financial Proposal is for the sum of [Insert amount in
        words and figures]. This amount is exclusive of local taxes, which we have estimated at
        [insert amount in words and figures].
        Our Financial Proposal shall be binding upon us subject to the modifications resulting
        from Contract negotiations, up to expiration of the validity period of the Proposal, i.e. before
        (insert day, month and year in accordance with Proposal Data Sheet ITC 25.1).
        Commissions and gratuities, if any, paid or to be paid by us to agents relating to this
        Proposal and Contract execution, if we are awarded the Contract, are listed as follows:

        | No. | Name and Address of Agents    | Amount           | Purpose of commission or gratuity |
        | --- | ------------------------------| -----------------| --------------------------------- |
        | 1.  |                               |                  |                                   |
        | 2.  |                               |                  |                                   |

        We also declare that the Government of the United Republic of Tanzania has not
        declared us or any sub-Consultants for any part of the Contract, ineligible on charges of
        engaging in corrupt, fraudulent or coercive practices. We furthermore, pledge not to indulge
        in such practices in competing for or in executing the Contract, and are aware of the relevant
        provisions of Proposal Data Sheet ITC 3 [Corrupt, Fraudulent or Coercive Practices]
        We understand you are not bound to accept any Proposal you receive.
        Signed:
        In the capacity of:
        Duly authorized to sign the proposal on behalf of the Applicant.
        Date:____________________________________________________________
        Signature:_____________________________________________________________________________
        

        """)

princing_phylosophy_prompt = """

"""




price_prompt = ChatPromptTemplate.from_template("""
        As experienced Proposal Pricing Analyst in analyzing Project Pricing\n
        You have been provided with the following information:\n
        \n- A summary of the problem statement and requirements from you.
        \n- Cost of that items, infrastructure and equipments in a text format.
        
        Perform the following actions: 
        
        1 - Extract the items and cost from the **ITEM COST SUMMARY**
        
        2 - Output a json object that contains the following \
            keys: items, cost.

        PROBLEM SUMMARY:
        {summary_requirement}
        
        ITEM COST SUMMARY:
        {item_cost_summary}
""")


# executive_summary_prompt = ChatPromptTemplate.from_template("""
                                                            
#         Please provide an executive summary that effectively conveys the project's purpose, goals, target audience, milestones, budget, and timeline.
#         You have been tasked with creating an executive summary for the following project:\n
#         Note: Note you are writting a request for proposal exectuve summary with all the information provided to you.
#         \n- Project Description: {problem_summary}
#         \n- Project Goals: {Proposed_solution}
#         \n- Target Audience: Highlight who the target audience are.
#         \n- Key Milestones: {implementation_plan}
#         \n- Budget Allocation: {budget_allocation}
#         \n- Timeline: Highlight the Timeline for the project.
#         \n- Scope: {scope}
        
#         Your executive summary should provide a concise yet informative overview of the project's key aspects. Focus on presenting the project's significance, goals, target audience, and major milestones.

#         PROJECT EXECUTIVE SUMMARY:

#         """)


call_to_action_prompt = ChatPromptTemplate.from_template("""
        Your task is to create a persuasive call to action statement that will entice potential investors to support our project financially.
        Craft a compelling call to action that emphasizes the potential for mutual success and encourages investors to take action.
        
        You have been provided with the following information:\n
        \n- A project Overview.
        \n- A summary of the problem statement and requirements from you.
       executive summary
        {exe_summary}

    
        PROJECT SUMMARY:
        {problem_summary}
        """)


company_profile_prompt = """\
        Given the following text, your task is to:

        1. Extract the company **NAME** and **WEBSITE** if they exist.
        2. If either the company name or website is missing, generate placeholder values for them.
        3. Create a JSON object with the keys 'company name' and 'website', populated with the extracted or generated values.

        Text: "{text}"
        """