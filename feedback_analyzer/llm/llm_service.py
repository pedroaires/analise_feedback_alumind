from typing import Dict
from langchain.schema.runnable import RunnableLambda
from feedback_analyzer.llm.llm_config import llm
from langchain.prompts import PromptTemplate
from feedback_analyzer.llm.models import FeedbackAnalysisModel, SPAMdetection
from langchain.output_parsers import PydanticOutputParser, OutputFixingParser

class LLMService:
    feedback_analysis_parser = PydanticOutputParser(pydantic_object=FeedbackAnalysisModel)
    feedback_analysis_fixing_parser = OutputFixingParser.from_llm(llm=llm, parser=feedback_analysis_parser)
    spam_detection_parser = PydanticOutputParser(pydantic_object=SPAMdetection)
    spam_fixing_parser = OutputFixingParser.from_llm(llm=llm, parser=spam_detection_parser)
    @classmethod
    def process_feedback_analysis_response(cls, response):
        parsed = cls.feedback_analysis_fixing_parser.parse(response.content)
        return parsed.dict()
    
    
    @classmethod
    def analyze_feedback(cls, feedback: str) -> Dict:
        prompt = PromptTemplate(
            template="""Analise o seguinte feedback e identifique o sentimento e as funcionalidades solicitadas:
            {format_instructions}
            Feedback: {feedback}
            """,
            input_variables=["feedback"],
            partial_variables={
                "format_instructions": cls.feedback_analysis_parser.get_format_instructions()
            },
        )

        flow = ( prompt | llm | RunnableLambda(cls.process_feedback_analysis_response))
        return flow.invoke({"feedback": feedback})
    
    @classmethod
    def generate_email(cls, metrics: Dict) -> str:
        prompt = PromptTemplate(
            template="""
            Você faz parte de um serviço de análise de feedbacks da Alumind, sua tarefa é escrever um e-mail que será enviado para stakeholders do AluMind. Faça um breve resumo sobre as métricas de feedbacks e features sugeridas, além disso, explique por que seria interessante ter cada uma. 
            \n{metrics}\n
            Sua mensagem será enviada diretamente para os stakeholders entitulada de Serviço de Análise de Feedback, por isso não deixe informações com place holders.
            """,
            input_variables=["metrics"]
        )
        flow = ( prompt | llm )
        return flow.invoke({"metrics": metrics}).content
        
    
    @classmethod
    def process_spam_detection_response(cls, response):
        parsed = cls.spam_fixing_parser.parse(response.content)
        return parsed.dict()

    @classmethod
    def is_spam(cls, feedback:str):
        prompt = PromptTemplate(
            template="""
            Você é um sistema de detecção de SPAM, análise o feedback e classifique o feedback como SIM ou NAO para spam.
            {format_instructions}
            {feedback}
            """,
            input_variables=["feedbacks"],
            partial_variables={
                  "format_instructions": cls.spam_detection_parser.get_format_instructions()
            }
        )
        
        flow = ( prompt | llm | RunnableLambda(cls.process_spam_detection_response))
        return flow.invoke({"feedback": feedback})