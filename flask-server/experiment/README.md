# Experiment Module

Author: Zhong, Yinjie.  
Email: yinjie.zhong@vanderbilt.edu

[TOC]

## 1. Introduction

This component records and manages the information related to experiment performed by EnzyHTP Web Application.

## 2. Database

The table in the database for `experiment` is named `experiments`, which is defined as follows in the `models.py` file located in the current directory.

The sqlite database will be generated as `/flask-server/instance/enzyhtp-gpt.db` the first time we run the `server.py` if no existing database file in the folder.

## 3. Basic Operations

### 3.1 Index

Fetch the list of user's experiments.

- Path: `/api/experiment/`.
- Request Method: `GET`.
- Returns:
  - If succeeded,
    - Status Code: `200 OK`.
    - Response Body (example)
    ```json
    {
        "user_id": "78a5f120-63ac-4ce1-aa84-8cce1826a415",
        "email": "san.zhang@example.com",
        "username": "san.zhang",
        "timestamp": "2024-02-21 20:45:06.460931",
        "experiments": [
            {
                "type": 0,
                "status": 0,
                "description": "Let's start a test.",
                "updated_time": "2024-02-21 04:53:43.210652",
                "id": "ae394fd8-4a59-4d0b-a1a2-eaaa04ba6768",
                "name": "exp-test-01",
                "metrics": "[]",
                "created_time": "2024-02-21 04:53:43.210650"
            },
            {
                "type": 0,
                "status": 0,
                "description": "Let's start a test.",
                "updated_time": "2024-02-21 04:53:43.210687",
                "id": "1bcb7760-c94e-4bcb-85f5-221169df8089",
                "name": "exp-test-02",
                "metrics": "[]",
                "created_time": "2024-02-21 04:53:43.210686"
            }
        ]
    }
    ```
  - If failed (due to anonymous user),
    - Status Code: `401 UNAUTHORIZED`.
    - Response Body (example):
    ```json
    {
        "id": null,
        "email": null,
        "username": "",
        "is_successful": false,
        "message": "Unauthorized request, please login first.",
        "timestamp": "2024-06-27 16:54:51.526445",
        "is_authenticated": false
    }
    ```

### 3.2 Detail

Fetch the detail of

- Path: `/api/experiment/<experiment_id>`.
- Request Method: `GET`.
- Returns:
  - If succeeded when the experiment is running,
    - Status Code: `200 OK`.
    - Response Body (URI: `/api/experiment/c6b2d6ea-554b-4356-b8d5-4433414d68f7`)
    ```json
    {
        "type": -1,
        "name": "Zhong's experiment with 7DVP",
        "description": "3CL-Protein with Peptide",
        "user_id": "8dceb918-12f3-42f4-a4d9-d19266c16ac0",
        "metrics": [
            {
                "name": "cavity",
                "arguments": {}
            }
        ],
        "constraints": [
            {
                "type": "distance",
                "arguments": [
                    "C.1",
                    "C.10"
                ]
            }
        ],
        "id": "c6b2d6ea-554b-4356-b8d5-4433414d68f7",
        "created_time": "2024-07-13 01:58:38.750000",
        "updated_time": "2024-07-13 01:58:38.750000",
        "pdb_filepath": "/var/www/files/experiments/c6b2d6ea-554b-4356-b8d5-4433414d68f7/7dvp.pdb",
        "results": [],
        "slurm_job_uuid": null,
        "mutation_pattern": "WT",
        "current_assistant_type": 2,
        "current_thread_id": "thread_EBBrjLMmzHQPlb0lifv2iYtG",
        "status": "-9",
        "progress": "0.0",
        "status_text": "Created"
    }
    ```
  - If succeeded when the experiment is running,
    - Status Code: `200 OK`.
    - Response Body (URI: `/api/experiment/1bcb7760-c94e-4bcb-85f5-221169df8089`, Out of date)
    ```json
    {
        "type": -1,
        "id": "4f018960-c954-4afc-9d6e-00ec5bf2e00e",
        "slurm_job_uuid": "22ac5fbf-5407-48ac-8d91-a3e6f54be9fc",
        "description": null,
        "updated_time": "2024-06-28 15:14:22.535611",
        "user_id": "953e09b6-a2a5-453f-adf9-bc95233f9e56",
        "name": "Zhong's experiment valid PDB",
        "mutation_pattern": "{WT},{H41M},{M165C},{H41S,E166L}",
        "metrics": "[]",
        "created_time": "2024-06-24 17:01:18.773598",
        "pdb_filename": "7dvp.pdb",
        "status": "-8",
        "progress": "0.0",
        "status_text": "Pending"
    }
    ```
  - If succeeded when the experiment is completed,
    - Status Code: `200 OK`.
    - Response Body (URI: `/api/experiment/16e8045c-a45c-4fef-b0a2-2fd8e340e277`, Out of date)
    ```json
    {
        "type": 0,
        "name": "Zhong's experiment #01",
        "mutation_pattern": "{WT},{H41M},{M165C},{H41S,E166L}",
        "metrics": "[]",
        "created_time": "2024-04-10 15:14:31.220061",
        "pdb_filename": "8gws.pdb",
        "id": "16e8045c-a45c-4fef-b0a2-2fd8e340e277",
        "slurm_job_uuid": "6be9bead-bd46-4bf0-ad88-91a3b9e299c5",
        "description": "This is a magic experiment.",
        "updated_time": "2024-07-01 14:27:02.828043",
        "user_id": "953e09b6-a2a5-453f-adf9-bc95233f9e56",
        "status": "0",
        "progress": "1.0",
        "status_text": "Completed",
        "results": [
            {
                "mutant": "WT",
                "spi_metrics": XXX,
                "rmsd": YYY
            },
            {
                "mutant": "H41M",
                "spi_metrics": XXX,
                "rmsd": YYY
            },
            {
                "mutant": "M165C",
                "spi_metrics": XXX,
                "rmsd": YYY
            },
            {
                "mutant": "H41S E166L",
                "spi_metrics": XXX,
                "rmsd": YYY
            }
        ]
    }
    ```
  - If failed (due to no match result),
    - Status Code: `404 NOT FOUND`.
    - Response Body (example):
    ```json
    {
        "id": null,
        "name": null,
        "email": "yinjie.zhong.cn@gmail.com",
        "user_id": "953e09b6-a2a5-453f-adf9-bc95233f9e56",
        "is_successful": false,
        "message": "Unable to find the experiment with id '1bcb7760-c94e-4bcb-85f5-221169df8089'.",
        "is_authenticated": true,
        "timestamp": "2024-06-27 16:57:08.786338"
    }
    ```
  - If failed (due to anonymous user),
    - Status Code: `401 UNAUTHORIZED`.
    - Response Body (example):
    ```json
    {
        "id": null,
        "email": null,
        "username": "",
        "is_successful": false,
        "message": "Unauthorized request, please login first.",
        "timestamp": "2024-06-27 16:54:51.526445",
        "is_authenticated": false
    }
    ```
  - If failed (because the user is not the owner of the experiment),
    - Status Code: `403 FORBIDDEN`.
    - Response Body (example):
    ```json
    {
        "id": "0d065616-f65a-4706-9b54-fd84140b98d9",
        "name": "ThomasWhite's experiment",
        "email": "yinjie.zhong.cn@gmail.com",
        "user_id": "953e09b6-a2a5-453f-adf9-bc95233f9e56",
        "is_successful": false,
        "message": "The current user doesn't have the permission to the experiment.",
        "is_authenticated": true,
        "timestamp": "2024-06-26 18:06:19.386670"
    }
    ```

### 3.3 Create Experiment

Create a new experiment.

(See Postman for now, will be here later.)

### 3.4 Delete Experiment

Delete an experiment.

(See Postman for now, will be here later.)

### 3.5 Update Profile

This endpoint allows updating the editable information field(s) of the specified Experiment.

(See Postman for now, will be here later.)

### 3.6 Update Progress

This endpoint is to update the status and progress of a specific experiment from the Computational Cluster.

This endpoint is not to be called from the frontend, and JWT is required.

(See Postman for now, will be here later.)

## 4. PDB File(s)

### 4.1 Validate PDB File.

Verify the PDB file. The PDB file transmitted to this controller will not be stored anywhere.

(See Postman for now, will be here later.)

### 4.2 Upload PDB File.

Upload the PDB file to a certain experiment, which will be the wildtype structure of this experiment.

(See Postman for now, will be here later.)

### 4.3 Download PDB File

Download the WT PDB file from the experiment if exists.

(See Postman for now, will be here later.)

## 5. Mutations

### 5.1 Get Mutation Pattern

(See Postman for now, will be here later.)

### 5.2 Update Mutation Pattern

This endpoint allows the user to update mutations for a specific experiment.

(See Postman for now, will be here later.)

### 5.3 Generate Mutation Pattern

Generate the mutation pattern via GPT-4 from the natural language input so as to create a mutation space.

(See Postman for now, will be here later.)

### 5.4 Get Mutant PDBs

This API provides PDB file strings for each mutant in key-value pairs.

(See Postman for now, will be here later.)

## 6. Slurm Jobs

### 6.1 Slurm GET

This endpoint retrieves detailed information about the Slurm Job related to a specific experiment.

(See Postman for now, will be here later.)

### 6.2 Slurm POST

This endpoint makes an HTTP POST request to submit a new job to the Slurm API for a specific experiment.

(See Postman for now, will be here later.)

### 6.3 Slurm DELETE

Deletes a Slurm job for a specific experiment if it is Completed, Failed or Cancelled.

(See Postman for now, will be here later.)

### 6.4 Slurm Deploy Download

Download the EnzyHTP Deploy Pack to run simulations on your own Slurm Cluster.

(See Postman for now, will be here later.)

