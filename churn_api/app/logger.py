import hashlib
import json
import logging

from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format="%(message)s"
)

logger = logging.getLogger(__name__)


def create_hash(data):
    """
    Create a SHA256 hash of the request.
    """

    json_string = json.dumps(
        data,
        sort_keys=True
    )

    return hashlib.sha256(
        json_string.encode()
    ).hexdigest()
    
    
def log_prediction(
    input_data,
    prediction,
    latency
):
    logger.info(
        json.dumps(
            {
                "timestamp": datetime.now().isoformat(),
                "input_hash": create_hash(input_data),
                "prediction": prediction,
                "latency_ms": round(latency, 2)
            }
        )
    )    