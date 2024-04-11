# Experiment Module

Author: Zhong, Yinjie.  
Email: yinjie.zhong@vanderbilt.edu

[TOC]

## 1. Introduction

This component records and manages the information related to experiment performed by EnzyHTP Web Application.

This component provides following methods:

- `index`: A list of experiments belonging to current user.
- `detail`: The detailed information of a specified experiment. Only the owner of the experiment has the access.

## 2. Database

The table in the database for `experiment` is named `experiments`, which is defined as follows in the `models.py` file located in the current directory.

```python
class Experiment(db.Model):
    """Experiment Model: Experiment information."""

    __tablename__ = 'experiments'
    id = db.Column(db.String(36), primary_key=True, unique=True)
    type = db.Column(db.Integer, nullable=False, default=0)
    name = db.Column(db.String(128), nullable=False, default=0)
    status = db.Column(db.Integer, nullable=False, default=0)
    metrics = db.Column(db.String(64), nullable=True)
    description = db.Column(db.String(128), nullable=True)
    created_time = db.Column(db.DateTime, nullable=False)
    updated_time = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=True)
    user = db.relationship('User', backref=db.backref('experiments'))
```

The sqlite database will be generated as `/flask-server/instance/enzyhtp-gpt.db` the first time we run the `server.py` if no existing database file in the folder.

Shut down the server, change the directory to the `/flask-server` directory, and run `python instance/init_db.py`. Then, some example fake data will be added to the `users` table of the sqlite database.

## 3. Basic Features

### 3.1 Index

- Path: `/api/experiment/` or `/api/experiment/`.
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
    - Response Body: None.

### 3.2 Detail

- Path: `/api/experiment/<experiment_id>`.
- Request Method: `GET`.
- Returns:
  - If succeeded,
    - Status Code: `200 OK`.
    - Response Body (URI: `/api/experiment/1bcb7760-c94e-4bcb-85f5-221169df8089`)
    ```json
    {
        "type": 0,
        "id": "1bcb7760-c94e-4bcb-85f5-221169df8089",
        "status": 0,
        "description": "Let's start a test.",
        "updated_time": "2024-02-21 04:53:43.210687",
        "name": "exp-test-02",
        "metrics": "[]",
        "created_time": "2024-02-21 04:53:43.210686",
        "user_id": "78a5f120-63ac-4ce1-aa84-8cce1826a415"
    }
    ```
  - If failed (due to no match result),
    - Status Code: `404 NOT FOUND`.
    - Response Body: None.
  - If failed (due to anonymous user),
    - Status Code: `401 UNAUTHORIZED`.
    - Response Body: None.

### 3.3 Create Experiment

(See Postman for now, will be here later.)

### 3.4 Update Information

(See Postman for now, will be here later.)

### 3.5 Validate PDB File.

(See Postman for now, will be here later.)

### 3.6 Generate Pattern

(See Postman for now, will be here later.)