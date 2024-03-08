coc_response = """
        We are the Consultant, [enter name of Consultant]. We have signed a contract with [enter
        name of Client] for [enter description of the Services]. These Services will be carried out at
        [enter the Site and other locations where the Services will be carried out, as appropriate].
        Our contract requires us to implement measures to address environmental and social risks
        related to the Services, including the risks of sexual exploitation, sexual abuse and sexual
        harassment.
        This Code of Conduct is part of our measures to deal with environmental and social risks
        related to the Services. It applies to all Experts in places where the Services are being
        carried out.
        This Code of Conduct identifies the behavior that we require from all Experts.
        Our workplace is an environment where unsafe, offensive, abusive or violent behavior will
        not be tolerated and where all persons should feel comfortable raising issues or concerns
        without fear of retaliation.
       \n\n### **REQUIRED CONDUCT**\n\n
        Experts shall:
        1. Carry out his/her duties competently and diligently;
        2. Comply with this Code of Conduct and all applicable laws, regulations and other
        requirements, including requirements to protect the health, safety and well-being of
        other Experts and any other person;
        3. Maintain a safe working environment including, as applicable, by:
        a. ensuring that workplaces, equipment and processes under each person’s
        control are safe and without risk to health;
        b. wearing required personal protective equipment; and
        c. following applicable emergency operating procedures.
        4. Report work situations that he/she believes are not safe or healthy and remove
        himself/herself from a work situation which he/she reasonably believes presents an
        imminent and serious danger to his/her life or health;
        5. Treat other people with respect, and not discriminate against specific groups such as
        women, people with disabilities, migrant workers or children;
        6. Not engage in Sexual Harassment, which means unwelcome sexual advances,
        requests for sexual favors, and other verbal or physical conduct of a sexual nature
        with other Experts, Contractor’s Personnel (if applicable) or Client’s Personnel;
        7. Not engage in Sexual Exploitation, which means any actual or attempted abuse of
        position of vulnerability, differential power or trust, for sexual purposes, including, but
        Signature: __________________________________________________________33 |
        Page
        Section 4- Technical Proposal – Standard Forms
        not limited to, profiting monetarily, socially or politically from the sexual exploitation of
        another;
        8. Not engage in Sexual Abuse, which means the actual or threatened physical
        intrusion of a sexual nature, whether by force or under unequal or coercive
        conditions;
        9. Not engage in any form of sexual activity with individuals under the age of 18, except
        in case of pre-existing marriage;
        10. Complete relevant training courses that will be provided related to the environmental
        and social aspects of the Contract, including on health and safety matters, Sexual
        Exploitation and Abuse (SEA), and Sexual Harassment (SH);
        11. Report violations of this Code of Conduct; and
        12. Not retaliate against any person who reports violations of this Code of Conduct,
        whether to us or the Client, or who makes use of grievance mechanism for Experts, if
        any, or the project’s Grievance Redress Mechanism.
        \n\n ### **RAISING CONCERNS**\n\n
        If any person observes behavior that he/she believes may represent a violation of this Code
        of Conduct, or that otherwise concerns him/her, he/she should raise the issue promptly. This
        can be done in either of the following ways:
        1. Contact [enter name of the Consultant’s social expert with relevant experience in
        handling sexual exploitation, sexual abuse and sexual harassment cases, or if such
        person is not required under the Contract, another individual designated by the
        Consultant to handle these matters] in writing at this address [ ] or by telephone at [ ]
        or in person at [ ]; or
        2. Call [ ] to reach the Consultant’s hotline (if any) and leave a message.
        The person’s identity will be kept confidential, unless reporting of allegations is mandated by
        the country law. Anonymous complaints or allegations may also be submitted and will be
        given all due and appropriate consideration. We take all reports of possible misconduct
        seriously, and will investigate and take appropriate action. We will provide warm referrals to
        service providers that may help support the person who experienced the alleged incident, as
        appropriate.
        There will be no retaliation against any person who raises a concern in good faith about any
        behavior prohibited by this Code of Conduct. Such retaliation would be a violation of this
        Code of Conduct.
        \n\n  ### **CONSEQUENCES OF VIOLATING THE CODE OF CONDUCT** \n\n
        Any violation of this Code of Conduct by Experts may result in serious consequences, up to
        and including termination and possible referral to legal authorities.
        FOR EXPERT:
        I have received a copy of this Code of Conduct written in a language that I comprehend. I
        understand that if I have any questions about this Code of Conduct, I can contact [enter
        name of Consultant’s contact person(s) with relevant experience] requesting an explanation.
        
        Name of Expert: [insert name]
        Signature: __________________________________________________________34 
        Section 4- Technical Proposal – Standard Forms
        Date: (day month year): _______________________________________________
        Countersignature of authorized representative of the Consultant:
        Signature: ________________________________________________________
        Date: (day month year): ______________________________________________
        
        \n\n ### ATTACHMENT 1 TO THE CODE OF CONDUCT FORM BEHAVIORS CONSTITUTING SEXUAL EXPLOITATION AND ABUSE (SEA) AND
                                   BEHAVIORS CONSTITUTING SEXUAL HARASSMENT (SH)\n\n
                                   
        The following non-exhaustive list is intended to illustrate types of prohibited behaviors:
        \n **(1) Examples of sexual exploitation and abuse** include, but are not limited to\n
            ● An Expert tells a member of the community that he/she can get them jobs related to
            the Services (e.g. cooking and cleaning) in exchange for sex.
            ● An Expert that is connecting electricity input to households says that he can connect
            women headed households to the grid in exchange for sex.
            ● An Expert rapes, or otherwise sexually assaults a member of the community.
            ● An Expert denies a person access to the Site unless he/she performs a sexual favor.
            ● An Expert tells a person applying for employment under the Contract that he/she will
            only hire him/her if he/she has sex with him/her.
        \n **(2) Examples of sexual harassment in a work context**\n
        ● An Expert comment on the appearance of another Expert (either positive or negative)
        and sexual desirability.
        ● When An Expert complains about comments made by another Expert on his/her
        appearance, the other Expert comment that he/she is “asking for it” because of how
        he/she dresses.
        ● Unwelcome touching of an Expert or Client’s Personnel by another Expert.
        ● An Expert tells another Expert that he/she will get him/her a salary raise, or
        promotion if he/she sends him/her naked photographs of himself/herself.

  """
  
coc_qa = 'Based on the provided context, there is a mention of a "Code of Conduct" in the document. The Code of Conduct is mentioned in Section 11 and Section 12 of the document. \n\nSection 11 states that individuals should report any violations of the Code of Conduct and Section 12 emphasizes that there should be no retaliation against anyone who reports violations. \n\nUnfortunately, the specific contents of the Code of Conduct are not provided in the given context.'

from utils.util import create_final_prompt
from agent_tools.api_credentials import chat_model
from prompt.prompts import code_of_conduct_prompt

def create_coc(coc):
    examples = [
        {"input": code_of_conduct_prompt.format(coc_qa), "response": coc_response},
    ]

    final_prompt = create_final_prompt(examples, chat_model)

    response = final_prompt.invoke({"input": code_of_conduct_prompt.format(coc)})

    return response.content
    