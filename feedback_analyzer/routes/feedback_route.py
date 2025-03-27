from flask import Blueprint, request, jsonify
from pydantic import ValidationError
from feedback_analyzer.dtos.feedback_dto import FeedbackRequestDTO, FeedbackResponseDTO
from feedback_analyzer.services.feedback_service import FeedbackService 
from sqlalchemy.exc import SQLAlchemyError
feedback_bp = Blueprint('feedback', __name__)



@feedback_bp.route('/feedback/classifica', methods=['POST'])
def classify_feedback():
    try: 
        feedback_data = FeedbackRequestDTO.model_validate(request.json)
        feedback = FeedbackService.perform_classification(feedback_data)
        feedback_resp = FeedbackResponseDTO.from_orm(feedback)
        return jsonify(feedback_resp.model_dump()), 200
    except ValidationError as e:
        return jsonify({
            "error": "Validation Error",
            "details": e.errors()
        }), 400
    except SQLAlchemyError as e:
        return jsonify({
            "error": "Database Error",
            "message": str(e)
        }), 500
    except Exception as e:
        # Tratamento de erro genérico
        return jsonify({
            "error": "Internal Server Error",
            "message": str(e)
        }), 500
    

@feedback_bp.route('/feedback/lista', methods=['GET'])
def list_feedbacks():
    feedbacks = FeedbackService.list_feedbacks()
    resp_list = [FeedbackResponseDTO.from_orm(f).model_dump() for f in feedbacks]
    return jsonify(resp_list), 200
    
