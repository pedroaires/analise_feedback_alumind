from langchain.output_parsers import PydanticOutputParser, OutputFixingParser
from langchain_openai import ChatOpenAI
from config import get_config

llm = ChatOpenAI(temperature=0, api_key=get_config().OPENAI_API_KEY)