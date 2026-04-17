#! python3
# -*- coding: utf-8 -*-
"""Backfill conversation fields for experiment documents."""

from __future__ import annotations

import argparse
import os
from urllib.parse import urlparse

from pymongo import MongoClient


def _default_db_name_from_uri(mongo_uri: str) -> str:
    parsed = urlparse(mongo_uri)
    db_name = parsed.path.strip("/")
    return db_name or "enzyhtp_gpt"


def _build_update_payload(experiment_doc: dict) -> dict:
    payload = {}
    if ("current_conversation_id" not in experiment_doc):
        payload["current_conversation_id"] = None
    if ("conversation_id_list" not in experiment_doc):
        payload["conversation_id_list"] = list()
    if ("openai_runtime" not in experiment_doc):
        has_thread_data = bool(experiment_doc.get("current_thread_id") or experiment_doc.get("thread_id_list"))
        payload["openai_runtime"] = "assistants_legacy" if has_thread_data else "responses"
    return payload


def main():
    parser = argparse.ArgumentParser(description="Migrate experiment records from thread fields to conversation-compatible fields.")
    parser.add_argument("--mongo-uri", default=os.environ.get("MONGO_URI", "mongodb://localhost:27017/enzyhtp_gpt"))
    parser.add_argument("--db-name", default=None)
    parser.add_argument("--apply", action="store_true", help="Persist updates to database.")
    parser.add_argument("--sample-size", type=int, default=10)
    args = parser.parse_args()

    db_name = args.db_name or _default_db_name_from_uri(args.mongo_uri)
    client = MongoClient(args.mongo_uri)
    db = client[db_name]
    collection = db.experiments

    cursor = collection.find(
        {},
        {
            "_id": 1,
            "id": 1,
            "current_thread_id": 1,
            "thread_id_list": 1,
            "current_conversation_id": 1,
            "conversation_id_list": 1,
            "openai_runtime": 1,
        },
    )

    total_count = 0
    pending_count = 0
    applied_count = 0
    sample_updates = list()

    for experiment_doc in cursor:
        total_count += 1
        update_payload = _build_update_payload(experiment_doc)
        if (not update_payload):
            continue

        pending_count += 1
        if (len(sample_updates) < args.sample_size):
            sample_updates.append({
                "id": experiment_doc.get("id", str(experiment_doc.get("_id"))),
                "update": update_payload,
            })

        if (args.apply):
            result = collection.update_one({"_id": experiment_doc["_id"]}, {"$set": update_payload})
            if (result.modified_count > 0):
                applied_count += 1

    print(f"database={db_name}")
    print(f"total_experiments={total_count}")
    print(f"pending_updates={pending_count}")
    print(f"applied_updates={applied_count if args.apply else 0}")
    print(f"mode={'apply' if args.apply else 'dry-run'}")
    print("sample_updates:")
    for sample in sample_updates:
        print(sample)


if __name__ == "__main__":
    main()
