from flask import Blueprint, request, jsonify
from pydantic import ValidationError
from feedback_analyzer.dtos.feedback_dto import FeedbackRequestDTO, FeedbackResponseDTO
from feedback_analyzer.services.feedback_service import FeedbackService 
from sqlalchemy.exc import SQLAlchemyError




feedback_bp = Blueprint('feedback', __name__)



@feedback_bp.route('/feedbacks', methods=['POST'])
def process_feedback():
    try: 
        feedback_data = FeedbackRequestDTO.model_validate(request.json)
        feedback = FeedbackService.process_feedback(feedback_data)
        feedback_resp = FeedbackResponseDTO.from_orm(feedback)
        return jsonify(feedback_resp.model_dump()), 200
    except ValidationError as e:
        # TODO: implement error handlers
        return jsonify({
            "error": "Validation Error",
            "details": e.errors()
        }), 400
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    except SQLAlchemyError as e:
        return jsonify({
            "error": "Database Error",
            "message": str(e)
        }), 500
    except Exception as e:
        return jsonify({
            "error": "Internal Server Error",
            "message": str(e)
        }), 500
    

@feedback_bp.route('/feedbacks', methods=['GET'])
def list_feedbacks():
    try:
        feedbacks = FeedbackService.list_feedbacks_with_features()
        resp_list = [FeedbackResponseDTO.from_orm(f).model_dump() for f in feedbacks]
        
        return jsonify(resp_list), 200
    
    except SQLAlchemyError as e:
        return jsonify({
            "error": "Database Error",
            "message": str(e)
        }), 500
    except Exception as e:
        return jsonify({
            "error": "Internal Server Error",
            "message": str(e)
        }), 500
    
@feedback_bp.route('/feedbacks/<uuid:feedback_id>', methods=['GET'])
def get_feedback(feedback_id):
    try:
        feedback = FeedbackService.get_feedback_by_id(feedback_id)
        if not feedback:
            return jsonify({"error": "Feedback not found"}), 404

        feedback_resp = FeedbackResponseDTO.from_orm(feedback)
        return jsonify(feedback_resp.model_dump()), 200

    except SQLAlchemyError as e:
        return jsonify({"error": "Database Error", "message": str(e)}), 500
    except Exception as e:
        return jsonify({"error": "Internal Server Error", "message": str(e)}), 500

    
@feedback_bp.route('/feedbacks/metrics', methods=['GET'])
def generate_metrics():
    try:
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')

        metrics = FeedbackService.generate_metrics(start_date, end_date)
        return jsonify(metrics), 200

    except SQLAlchemyError as e:
        return jsonify({"error": "Database Error", "message": str(e)}), 500
    except Exception as e:
        return jsonify({"error": "Internal Server Error", "message": str(e)}), 500
    
# Apenas para testes
@feedback_bp.route('/feedbacks/send-email-report', methods=['POST'])
def send_email_report():
    try:

        email_content = FeedbackService.send_weekly_feedback_email()
        return jsonify({"conteudo_email": email_content}), 200

    except SQLAlchemyError as e:
        return jsonify({"error": "Database Error", "message": str(e)}), 500
    except Exception as e:
        return jsonify({"error": "Internal Server Error", "message": str(e)}), 500