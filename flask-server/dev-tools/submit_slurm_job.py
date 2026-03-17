"""Dev tool to submit a Slurm job with a local entry script and optional files.
Used only for development and testing purposes.
To use:
1. change content of the dev-tools/entry_script.sh to run different commands on ACCRE.
2. obtain the job uuid in stdout after submission.
3. check under /data/yang_lab/yanglab_enzyhtp_app/web_slurm_jobs/<job_uuid> on ACCRE for job status and outputs.
"""
import os
import sys
from json import loads
from typing import Tuple

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, BASE_DIR)

from config import MONGO_URI, SLURM_API_URL  # noqa: E402
from services.accre_slurm_service import SlurmJobRequest, SlurmJobData  # noqa: E402
from requests import get as req_get, post as req_post, delete as req_delete  # noqa: E402
from pymongo import MongoClient  # noqa: E402

# Edit these variables directly for dev testing.
ENTRY_SCRIPT_PATH = "dev-tools/entry_script.sh"
JOB_NAME = "mutexa_manual_test"
FILE_LIST = []
SLURM_TOKEN = ""
QOS = "mutant_int"


def submit_slurm_job(
    entry_script_content: str,
    slurm_token: str,
    file_list: list,
    job_name: str,
    qos: str = "",
    account: str = "yang_lab_int",
    partition: str = "interactive",
) -> Tuple[int, str, str]:
    if not slurm_token:
        return 403, "Empty slurm token.", ""

    slurm_request = SlurmJobRequest(
        job_name=job_name,
        account=account,
        partition=partition,
        qos=qos,
    )
    payload = {
        "slurm_request": slurm_request.serialize(),
        "entry_script": entry_script_content,
    }
    file_data = SlurmJobData.post_files_pack(file_list=file_list)
    headers = {"Authorization": f"Bearer {slurm_token}"}
    response = req_post(SLURM_API_URL, headers=headers, data=payload, files=file_data)

    if response.ok:
        response_dict = loads(response.text)
        message = response_dict.get("message", "")
        if response_dict.get("success", False):
            job_uuid = response_dict.get("data", {}).get("job_uuid", "")
            return response.status_code, message, job_uuid
        return response.status_code, message, ""

    message = "The Slurm Job submission is failed."
    try:
        response_dict = loads(response.text)
        message = response_dict.get("message", message)
    except Exception:
        pass
    return response.status_code, message, ""


def get_slurm_token_from_mongo(mongo_uri: str = MONGO_URI) -> Tuple[str, str]:
    client = MongoClient(mongo_uri)
    try:
        db = client.get_default_database()
        token_doc = db.tokens.find_one({"name": "slurm_token"}) if db else None
        if not token_doc:
            return "", ""
        return token_doc.get("token", ""), token_doc.get("refresh_token", "")
    finally:
        client.close()


def fetch_slurm_job_info(job_uuid: str, slurm_token: str) -> Tuple[int, dict]:
    if not slurm_token:
        return 403, {}
    headers = {"Authorization": f"Bearer {slurm_token}"}
    response = req_get(f"{SLURM_API_URL}/{job_uuid}", headers=headers)
    if response.ok:
        response_dict = loads(response.text)
        return response.status_code, response_dict.get("data", {})
    return response.status_code, {}


def delete_slurm_job(job_uuid: str, slurm_token: str) -> Tuple[int, str]:
    if not slurm_token:
        return 403, "Empty slurm token."
    headers = {"Authorization": f"Bearer {slurm_token}"}
    cancel_response = req_post(f"{SLURM_API_URL}/{job_uuid}/cancel", headers=headers)
    delete_response = req_delete(f"{SLURM_API_URL}/{job_uuid}", headers=headers)
    if delete_response.status_code == 200:
        return 200, "The Slurm Job has successfully been deleted."
    return delete_response.status_code, f"Unable to delete the Slurm Job. cancel_status={cancel_response.status_code}"

def submit_slurm_job_main():
    entry_script_path = os.path.abspath(ENTRY_SCRIPT_PATH)
    if not os.path.isfile(entry_script_path):
        print(f"Entry script not found: {entry_script_path}")
        return 2

    with open(entry_script_path, "r", encoding="utf-8") as fobj:
        entry_script_content = fobj.read()

    slurm_token = SLURM_TOKEN
    if not slurm_token:
        slurm_token, _ = get_slurm_token_from_mongo()

    status, message, job_uuid = submit_slurm_job(
        entry_script_content=entry_script_content,
        slurm_token=slurm_token,
        file_list=FILE_LIST,
        job_name=JOB_NAME,
        qos=QOS,
    )
    return status, message, job_uuid

def main() -> int:
    status, message, job_uuid = submit_slurm_job_main()
    print(f"status={status} job_uuid={job_uuid} message={message}")
    print(f"Check ACCRE /data/yang_lab/yanglab_enzyhtp_app/web_slurm_jobs/{job_uuid} for job status and outputs.")
    # if job_uuid:
    #     info_status, job_info = fetch_slurm_job_info(job_uuid, slurm_token)
    #     remote_job_id = job_info.get("remote_job_id") or job_info.get("job_id", "")
    #     if remote_job_id:
    #         print(f"slurm_job_id={remote_job_id} (status={info_status})")
    #     else:
    #         print(f"slurm_job_info_status={info_status} job_info={job_info}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
