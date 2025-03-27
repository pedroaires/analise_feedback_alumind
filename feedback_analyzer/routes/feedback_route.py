from flask import Blueprint, request, jsonify
from pydantic import ValidationError
from feedback_analyzer.dtos.feedback_dto import FeedbackRequestDTO, FeedbackResponseDTO
from feedback_analyzer.services.feedback_service import FeedbackService 
from feedback_analyzer.services.feature_service import FeatureService
from sqlalchemy.exc import SQLAlchemyError
feedback_bp = Blueprint('feedback', __name__)



@feedback_bp.route('/feedbacks', methods=['POST'])
def process_feedback():
    try: 
        feedback_data = FeedbackRequestDTO.model_validate(request.json)
        feedback, features = FeedbackService.process_feedback(feedback_data)
        feedback_resp = FeedbackResponseDTO.from_orm(feedback, features)
        return jsonify(feedback_resp.model_dump()), 200
    except ValidationError as e:
        # TODO: implement error handlers
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
    try:
        # Retrieve feedbacks
        feedbacks = FeedbackService.list_feedbacks()
        
        # Convert to response DTOs
        resp_list = [
            FeedbackResponseDTO.from_orm(
                feedback, 
                FeatureService.get_features_by_feedback_id(str(feedback.id))
            ).model_dump() 
            for feedback in feedbacks
        ]
        
        return jsonify(resp_list), 200
    
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
    
