
from flask import Blueprint, jsonify, request
from feedback_analyzer.services.feature_service import FeatureService
from feedback_analyzer.dtos.feature_dto import FeatureDTO


feature_bp = Blueprint('feature', __name__)

@feature_bp.route('/features', methods=['GET'])
def list_features():
    feedback_id = request.json.get('feedback_id')
    try:
        features = FeatureService.list_features(feedback_id=feedback_id)
        resp_list = [FeatureDTO.from_orm(feat).model_dump() for feat in features]
        return jsonify(resp_list)
    except Exception as e:
        return jsonify({
            "error": "Internal Server Error",
            "message": str(e)
        }), 500
         

    
