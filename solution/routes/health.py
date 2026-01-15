from flask import Blueprint, jsonify
import logging

health_bp = Blueprint("health", __name__)
logger = logging.getLogger(__name__)


@health_bp.route("/health")
def health():
    logger.info("Health check requested")
    return jsonify({"status": "ok"})
