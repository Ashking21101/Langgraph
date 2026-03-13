from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
import os

os.environ['LANGCHAIN_PROJECT'] = 'LangSmith_Demo_2' # making it in a new project

load_dotenv()

prompt1 = PromptTemplate(
    template='Generate a detailed report on {topic}',
    input_variables=['topic']
)

prompt2 = PromptTemplate(
    template='Generate a 5 pointer summary from the following text \n {text}',
    input_variables=['text']
)

model = ChatOpenAI(model='gpt-4.1-nano')

parser = StrOutputParser()

chain = prompt1 | model | parser | prompt2 | model | parser

# adding my custom tags and meatdata
config = {
    'run_name':'sequential_chain',# changing from default runnablesequence name to custom
    'tags':['llm_app', 'report generation', 'summarization'],
    'metadata':{'model':'gpt-4.1-nano', 'parser':'stroutputparser'}
}

result = chain.invoke({'topic': 'Unemployment in India'}, config=config)

print(result)
