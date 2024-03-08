import langchain
from prompt.prompts import retrieval_ga
from data_retrieval.database_loader import load_db, chat_with_data_bot
from loaders.reader import parse_docs
import openai
from dotenv import load_dotenv, find_dotenv
import os


###Load API Keys
_ = load_dotenv(find_dotenv()) # read local .env file
openai.api_key = os.environ['OPENAI_API_KEY']  
huggingface_api_token = os.environ.get("HUGGINGFACEHUB_API_TOKEN")
os.environ["LANGCHAIN_TRACING"] = "true"
langchain.debug = False
default_dict = dict()

question_answers = [
    {'question' : "Which company sold the microcomputer kit that his friend built himself?", 'answer' : 'Healthkit'},
    {'question' : "What was the small city he talked about in the city that is the financial capital of USA?", 'answer' : 'Yorkville, NY'},
]

# if __name__ == '__main__':
path = r"C:\Users\Glodaris\Downloads\RFP Doc\RFP DATA CENTER.doc-1.pdf"
document = parse_docs(path)
qa = load_db(document)
response = chat_with_data_bot(retrieval_ga, qa)
default_dict['query'], default_dict['answer'] = retrieval_ga, response
predictions = qa.apply(question_answers)




