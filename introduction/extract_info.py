import sys
sys.path.append("..")
from typing import Optional
from langchain.utilities import GoogleSerperAPIWrapper
from langchain.document_loaders import SeleniumURLLoader
# from langchain.document_loaders import WebBaseLoader
from typing import List, Optional
from agent_tools.all_tool import AgentTools
from data_retrieval.database_loader import ChatBotManager
from agent_tools.api_credentials import llm, SERPER_API_KEY, embeddings_model #, hugging_embeddings

class CompanyProfile(ChatBotManager):
    """_summary_
    """
        
    def __init__(self, name:Optional[str]=None, rfp_requirements:str=None, documents:Optional[str]=None):
        """_summary_

        Args:
            name (str): _description_
            website (Optional[str], optional): _description_. Defaults to None.
            documents (Optional[str], optional): _description_. Defaults to None.
        """
        self.name = name
        self.documents = documents
        self.rfp_requirements = rfp_requirements
        super().__init__()   
        
    def get_company_profile(self,domain_name) -> List[str]:
        # other_details = [self.website, self.documents]
        # values = [value for value in other_details if value is not None]
        # Assuming 'search' is an instance of GoogleSerperAPIWrapper class
        search = GoogleSerperAPIWrapper(k=3)
        results = search.results(domain_name)
        links = [items['link'] for items in results['organic']]
        # if self.website:
        #     links.append(self.website)
        return list(set(links))

    def convert_to_loader(self, links:list) -> List[str]:
        try:
            loader = SeleniumURLLoader(urls=links)
            docs = loader.load()
            return docs
        except ValueError as e:
            print("", e)
            
    def company_qa(self, links:list[str]):
        docs = self.convert_to_loader(links)
        qa = self.load_db(embeddings_model, docs)
        return qa
    
    def extract_info(self, qa, query:str):
        response = self.parallel_process_inputs(query, qa)
        return response

class UserProfile():
    
    def __init__(self, name:str, workplace:Optional[str]=None, profession:Optional[str]=None):
        self.name = name
        self.workplace = workplace
        self.profession = profession
    

    def get_user_profile(self) -> List[str]:
        pass








