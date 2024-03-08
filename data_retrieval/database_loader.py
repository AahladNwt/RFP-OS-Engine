from llama_index import VectorStoreIndex
from llama_index import Document
import multiprocessing
from dask import delayed, compute



class ChatBotManager:
    def __init__(self, rerank):
        self.rerank = rerank
        
    def get_query_engine(self, document):
        #  load document
        # docs = self.get_docs(document)
        # build index
        index = VectorStoreIndex.from_documents(documents=document)
        query_engine = index.as_query_engine(
            similarity_top_k=10, node_postprocessors=[self.rerank]
        )

        return query_engine
    
    @staticmethod
    def chat_with_data_bot(prompt, query_engine):
        """
        Perform a chat interaction with the bot.
        
        Args:
            prompt: User's input.
            qa: Initialized RetrieverQueryEngine 
            
        Returns:
            Bot's response.
        """
        
        response = query_engine.query(
                        prompt,
                    )
        
        return  response
    
    def parallel_process_inputs(self, input_value, document):
        
        # Initialize query_engine here, if possible
        query_engine = self.get_query_engine(document)
        
        if isinstance(input_value, str):
            results = ChatBotManager.chat_with_data_bot(input_value, query_engine)
        elif type(input_value) == tuple:
            with multiprocessing.Pool(processes=len(input_value)) as pool:
                # results = pool.starmap(self.chat_with_data_bot, [(input1, query_engine) for input1 in input_value])
                delayed_functions = [delayed(ChatBotManager.chat_with_data_bot)(input1, query_engine) for input1 in input_value]
                
                results = compute(*delayed_functions)
            results = {'company_profile': results[0].response, 'company_details': results[1].response}
        else: 
            with multiprocessing.Pool(processes=len(input_value)) as pool:
                # results = pool.starmap(self.chat_with_data_bot, [(input1, query_engine) for input1 in input_value])
                delayed_functions = [delayed(ChatBotManager.chat_with_data_bot)(input1, query_engine) for input1 in input_value]
                results = compute(*delayed_functions)
            results = {'requirement': results[0].response,'financial_requirement':results[1].response, 'scope': results[2].response, 'evaluation_criteria': results[3].response, "expected_rfp_response": results[4].response,
                       'budget_and_financials': results[5].response, 'legal_and_contractual': results[6].response, 'submission_guidelines': results[7].response, "project_timeline": results[8].response,
                       'vendor_responsibilities': results[9].response, 'communication_and_reporting': results[10].response, 'objective': results[11].response, "deliverable": results[12].response,
                       'qualification': results[13].response, "technical_requirement": results[14].response, "project_duration_and_key_stages": results[15].response,
                       'collaboration_methods': results[16].response, "update_frequency": results[17].response, 'problem_statement':results[18].response,"client_company_name":results[19].response,
                       "role":results[20].response} 
        return results