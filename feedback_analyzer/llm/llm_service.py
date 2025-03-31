from typing import Dict
from langchain.schema.runnable import RunnableLambda
from feedback_analyzer.llm.llm_config import llm
from langchain.prompts import PromptTemplate
from feedback_analyzer.llm.models import FeedbackAnalysisModel
from langchain.output_parsers import PydanticOutputParser, OutputFixingParser

class LLMService:
    parser = PydanticOutputParser(pydantic_object=FeedbackAnalysisModel)
    fixing_parser = OutputFixingParser.from_llm(llm=llm, parser=parser)
    
    @classmethod
    def process_llm_response(cls, response: str):
        parsed = cls.fixing_parser.parse(response.content)
        return parsed.dict()
    
    
    @classmethod
    def analyze_feedback(cls, feedback: str) -> Dict:
        prompt = PromptTemplate(
            template="""Analise o seguinte feedback e identifique o sentimento e as funcionalidades solicitadas:\n{format_instructions}\nFeedback: {feedback}""",
            input_variables=["feedback"],
            partial_variables={
                "format_instructions": cls.parser.get_format_instructions()
            },
        )

        flow = ( prompt | llm | RunnableLambda(cls.process_llm_response))
        return flow.invoke({"feedback": feedback})