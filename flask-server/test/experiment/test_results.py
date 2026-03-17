import math
import os

from pymongo import MongoClient

import experiment.models as models
from experiment.analysis import METRICS_MAPPER
from experiment.models import Result


EXPERIMENT_ID = "9968f203-629b-4422-8698-fec04a5da35d"


def _get_db():
    uri = os.environ.get("MONGO_URI", "mongodb://localhost:27017/enzyhtp_gpt")
    client = MongoClient(uri)
    db = client.get_default_database() or client.get_database("enzyhtp_gpt")
    return client, db


def test_get_experiment_results_real_db():
    client, db = _get_db()
    original_db = models.db
    try:
        models.db = db
        aggregated = Result.get_experiment_results(EXPERIMENT_ID)
        assert aggregated, "No aggregated results returned from db.results."

        metric_key = "cavity"
        for row in aggregated:
            value = row.get(metric_key)
            assert isinstance(value, (int, float)) and not math.isnan(value)
    finally:
        models.db = original_db
        client.close()
