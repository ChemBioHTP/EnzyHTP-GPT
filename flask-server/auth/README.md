# Authentication Module

Author: Zhong, Yinjie.  
Email: yinjie.zhong@vanderbilt.edu

[TOC]

## 1. Introduction

This component serves as the authentication module for EnzyHTP Webapp.

This component provides following methods.

- `register`: New User Registration.
- `unregister`: Unregister the current User. Only the user him/herself is permitted to do so.
- `login`: User Login and create a cookie.
- `logout`: User Logout and delete the cookie.
- `profile`: Get or Update the profile of the user.
- `password/change`: Change the password of the user him/herself.
- `password/reset`: Reset the password of the user him/herself.
- `oauth/unsafe/login`: Test if the application works properly after passing the social login.
- `oauth/<oauth_vendor>/login`: Perform Social Login with OAuth vendors (e.g. Google, Microsoft, etc.)

The `url_prefix` of this component is `'/api/auth'`.

### 1.1 Functions under construction

Some functions should be treated cautiously since they has different behaviours in `development` and `production` environments.

| Function                        | Router                                                                        | Detail                                        |
| ------------------------------- | ----------------------------------------------------------------------------- | --------------------------------------------- |
| `oauth_login_unsafe()`          | `@auth.route('oauth/unsafe/login', methods=['POST'])`.                        | [OAuth Unsafe Login](#41-oauth-unsafe-login) |
| `oauth_vendor_login_callback()` | `@auth.route('oauth/<oauth_vendor>/login/callback', methods=['GET', 'POST'])` | [OAuth Vendor Login](#422-what-to-do)        |

## 2. Database

The table in the database for `auth` is named `users` and `oauth_users`, which is defined as follows in the `models.py` file located in the current directory.

The sqlite database will be generated as `/flask-server/instance/enzyhtp-gpt.db` the first time we run the `server.py` if no existing database file in the folder.

Shut down the server, change the directory to the `/flask-server` directory, and run `python instance/init_db.py`. Then, some example fake data will be added to the `users` table of the sqlite database.

## 3. Email Authentication

Here, we use the account `maura.attaway@example.com` for instance to show its function, which is an account generated randomly.

### 3.1 Register and Unregister

#### 3.1.1 Register

- Path: `/api/auth/register`.
- Request Method: `POST`.
- Request Body: `form-data`.
  - `email`: Your email address.
  - `username`: The username you want to have.
  - `password`: Password set.
- Returns:
  - If succeeded,
    - Status Code: `201 CREATED`.
    - Response Body:
    ```json
    {
      "id": "b701ff89-84db-44e3-8ed6-bb973efbebcf",
      "email": "maura.attaway@example.com",
      "username": "maura.attaway",
      "is_successful": true,
      "message": "New user `maura.attaway@example.com` is created.",
      "timestamp": "2023-10-30 13:21:55.286660",
      "is_authenticated": false
    }
    ```
  - If username is set to `Maura Attaway`,
    - Status Code: `201 CREATED`.
    - Response Body:
    ```json
    {
      "id": "c2431af8-faa9-4759-9bb5-550ec51ecf04",
      "email": "maura.attaway@example.com",
      "username": "Maura Attaway",
      "is_successful": true,
      "message": "New user `maura.attaway@example.com` is created.",
      "timestamp": "2023-12-07 08:50:22.090936",
      "is_authenticated": false
    }
    ```
  - If failed (due to conflict),
    - Status Code: `400 BAD REQUEST`.
    - Response Body:
    ```json
    {
      "id": null,
      "email": "maura.attaway@example.com",
      "username": "maura.attaway",
      "is_successful": false,
      "message": "New user `maura.attaway@example.com` conflicted with an existing account.",
      "timestamp": "2023-10-30 20:08:36.306698",
      "is_authenticated": false
    }
    ```

#### 3.1.2 Unregister

- Path: `/api/auth/unregister`.
- Request Method: `POST` | `DELETE`.
- Request Body:
  - `email`: The email address of the user to unregister.
- Returns:
  - If succeeded,
    - Status: `200 OK`.
    - Response Body:
    ```json
    {
      "id": "b701ff89-84db-44e3-8ed6-bb973efbebcf",
      "email": "maura.attaway@example.com",
      "is_successful": true,
      "message": "User `maura.attaway@example.com` is unregistered.",
      "timestamp": "2023-10-30 21:44:47.618434",
      "is_authenticated": false
    }
    ```
    - P.s. Cookie is deleted upon this response.
  - If failed (because user didn't log in).
    - Status: `401 UNAUTHORIZED`.
    - Response Body:
    ```json
    {
      "id": null,
      "email": null,
      "is_successful": false,
      "message": "Unauthorized request, please login first.",
      "timestamp": "2023-10-30 21:09:22.485493",
      "is_authenticated": false
    }
    ```
  - If failed (because user does not exist).
    - Status: `404 NOT FOUND`.
    - Response Body:
    ```json
    {
      "id": "1bce4b77-9c60-4144-a907-c46aa1258722",
      "email": "maura.attaway@example.com",
      "is_successful": false,
      "message": "Target user `maua.attaway@example.com` does not exist.",
      "timestamp": "2023-10-30 22:15:18.917277",
      "is_authenticated": true
    }
    ```
  - If failed (because user is not permitted to delete other user).
    - Status: `403 FORBIDDEN`.
    - Response Body:
    ```json
    {
      "id": "017663b8-0bde-4032-84f0-66f7284afeaf",
      "email": "maura.attaway@example.com",
      "is_successful": false,
      "message": "You cannot unregister `tom.white@example.com`.",
      "timestamp": "2023-10-30 21:58:30.902273",
      "is_authenticated": true
    }
    ```

### 3.2 Login and Logout

#### 3.2.1 Login

- Path: `/api/auth/login`.
- Request Method: `POST`.
- Request Body: `form-data`.
  - `email`: Your email address.
  - `password`: Password set.
  - `remember`: Whether to remember the user(s) after the browser(s) is closed. Defaults to `False`.
- Returns:
  - If succeeded,
    - Status Code: `200 OK`.
    - Response Body (example)
    ```json
    {
      "id": "9cbd55b3-cd94-4623-9153-36fd3dcc579d",
      "email": "maura.attaway@example.com",
      "username": "Maura A.",
      "is_successful": true,
      "message": "The user `Maura A.` logged in.",
      "timestamp": "2024-02-18 00:03:20.342158",
      "is_authenticated": true,
      "has_openai_secret_key": true,
      "is_openai_secret_key_valid": false,
      "openai_status_code": 401,
      "openai_response_description": "Invalid OpenAI Secret Key."
    }
    ```
    - Note: The validity of `openai_secret_key` is checked after each successful login.
  - If failed (due to password mismatch).
    - Status Code: `401 UNAUTHORIZED`.
    - Response Body:
    ```json
    {
      "id": null,
      "email": "maura.attaway@example.com",
      "username": "",
      "is_successful": true,
      "message": "The user `maura.attaway@example.com` failed to log in because of a password mismatch.",
      "timestamp": "2024-02-04 23:17:42.922157",
      "is_authenticated": false
    }
    ```
  - If failed (due to user not exist).
    - Status Code: `404 NOT FOUND`.
    - Response Body:
    ```json
    {
      "id": null,
      "email": "mara.attaway@example.com",
      "username": "",
      "is_successful": true,
      "message": "The user `mara.attaway@example.com` failed to log in because user does not exist.",
      "timestamp": "2024-02-04 23:17:42.922157",
      "is_authenticated": false
    }
    ```

#### 3.2.2 Logout

- Path: `/api/auth/logout`.
- Request Method: `GET` | `POST`.
- Request body: Not required.
- Returns:
  - If succeeded,
    - Status Code: `200 OK`.
    - Response Body (example)
    ```json
    {
      "id": "9cbd55b3-cd94-4623-9153-36fd3dcc579d",
      "email": "maura.attaway@example.com",
      "username": "",
      "is_successful": true,
      "message": "The user `maura.attaway@example.com` logged out.",
      "timestamp": "2024-02-04 23:34:13.491143",
      "is_authenticated": false
    }
    ```
  - If failed (because user didn't log in).
    - Status Code: `401 UNAUTHORIZED`.
    - Response Body:
    ```json
    {
      "id": null,
      "email": null,
      "username": "",
      "is_successful": false,
      "message": "Unauthorized request, please login first.",
      "timestamp": "2024-02-04 23:34:13.491143",
      "is_authenticated": false
    }
    ```

### 3.3 Profile

#### 3.3.1 Profile GET

- Path: `/api/auth/profile`.
- Request Method: `GET` | `POST`.
- Request Body: Not required.
- Returns:
  - If succeeded
    - Status: `200 OK`.
    - Response Body:
    ```json
    {
      "id": "9cbd55b3-cd94-4623-9153-36fd3dcc579d",
      "email": "maura.attaway@example.com",
      "username": "maura.attaway",
      "is_successful": true,
      "message": "",
      "timestamp": "2024-02-04 23:34:13.491143",
      "is_authenticated": true,
      "has_openai_secret_key": false
    }
    ```
    - Note: To save costs, the validity of `openai_secret_key` is not checked when getting profile.
  - If failed (happen when the user is not authenticated.)
    - Status Code: `401 UNAUTHORIZED`.
    - Response Body:
    ```json
    {
      "id": null,
      "email": null,
      "username": "",
      "is_successful": false,
      "message": "Unauthorized request, please login first.",
      "timestamp": "2024-02-04 23:34:13.491143",
      "is_authenticated": false
    }
    ```

#### 3.3.2 Profile UPDATE

- Path: `/api/auth/profile`.
- Request Method: `POST` | `PUT`.
- Request Body: `form-data`
  - `username`: The new username you want to have.
  - `openai_secret_key`: Your OpenAI API Key.
  - Any other fields are not editable or not existent.
- Returns:
  - If succeeded,
    - Status: `200 OK`.
    - Response Body:
    ```json
    {
        "id": "b3b26be3-3ef0-42f2-9beb-ab61b4b3e3cf",
        "email": "tom.white@example.com",
        "username": "Thomas White",
        "is_successful": true,
        "message": "Updated field(s): username, openai_secret_key. ",
        "timestamp": "2024-06-18 17:54:39.819247",
        "is_authenticated": true,
        "has_openai_secret_key": true,
        "is_openai_secret_key_valid": false,
        "openai_status_code": 401,
        "openai_response_description": "Invalid OpenAI Secret Key."
    }
    ```
    - Note: Any update to `openai_secret_key` will trigger a check to it.
  - If nothing to update.
    - Status: `200 OK`.
    - Response Body:
    ```json
    {
        "id": "b3b26be3-3ef0-42f2-9beb-ab61b4b3e3cf",
        "email": "tom.white@example.com",
        "username": "ThomasWhite",
        "is_successful": true,
        "message": "Nothing to be updated.",
        "timestamp": "2024-06-18 17:54:01.633238",
        "is_authenticated": true,
        "has_openai_secret_key": false
    }
    ```
  - If failed (happen when the `field` is not existent or not editable.)
    - Status Code: `400 BAD REQUEST`.
    - Response Body 1:
    ```json
    {
        "id": "b3b26be3-3ef0-42f2-9beb-ab61b4b3e3cf",
        "email": "tom.white@example.com",
        "username": "Thomas White",
        "is_successful": false,
        "message": "Nonexistent field(s): field_1, field_2. ",
        "timestamp": "2024-06-18 17:56:08.565655",
        "is_authenticated": true,
        "has_openai_secret_key": true
    }
    ```
    - Response Body 2:
    ```json
    {
        "id": "b3b26be3-3ef0-42f2-9beb-ab61b4b3e3cf",
        "email": "tom.white@example.com",
        "username": "Thomas White",
        "is_successful": false,
        "message": "Uneditable field(s): id. Nonexistent field(s): field_1. ",
        "timestamp": "2024-06-18 17:57:47.230422",
        "is_authenticated": true,
        "has_openai_secret_key": true
    }
    ```
    - Currently only `username` and `openai_secret_key` fields are editable.
    - Note: The validity of `openai_secret_key` is checked after updating `openai_secret_key`.
  - If there's a mixture of success and failure (happen when some fields are updated while some inputs are not.)
    - Status Code: `200 OK`.
    - Response Body:
    ```json
    {
        "id": "b3b26be3-3ef0-42f2-9beb-ab61b4b3e3cf",
        "email": "tom.white@example.com",
        "username": "Thomas White",
        "is_successful": true,
        "message": "Updated field(s): username, openai_secret_key. Uneditable field(s): id. Nonexistent field(s): field_1. ",
        "timestamp": "2024-06-18 17:57:01.291142",
        "is_authenticated": true,
        "has_openai_secret_key": true,
        "is_openai_secret_key_valid": false,
        "openai_status_code": 401,
        "openai_response_description": "Invalid OpenAI Secret Key."
    }
    ```

### 3.4 Password

#### 3.4.1 Change Password

- Path: `/api/auth/password/change`.
- Request Method: `POST` | `PUT`.
- Request Body: `form-data`.
  - `old_password`: Your old password.
  - `new_password`: Your new password.
- Returns:
  - If succeeded,
    - Status: `200 OK`.
    - Response Body:
    ```json
    {
      "id": "9cbd55b3-cd94-4623-9153-36fd3dcc579d",
      "email": "maura.attaway@example.com",
      "username": "maura.attaway",
      "is_successful": true,
      "message": "User `maura.attaway` succeeded to change the password.",
      "timestamp": "2024-02-05 00:01:04.861464",
      "is_authenticated": true,
      "has_openai_secret_key": false
    }
    ```
  - If failed (because the old password does not match.)
    - Status Code: `400 BAD REQUEST`.
    - Response Body:
    ```json
    {
      "id": "9cbd55b3-cd94-4623-9153-36fd3dcc579d",
      "email": "maura.attaway@example.com",
      "username": "maura.attaway",
      "is_successful": false,
      "message": "User `maura.attaway` failed to change the password due to unmatched old password.",
      "timestamp": "2024-02-05 00:01:04.861464",
      "is_authenticated": true,
      "has_openai_secret_key": false
    }
    ```
  - If failed (happen when the user is not authenticated.)
    - Status Code: `401 UNAUTHORIZED`.
    - Response Body:
    ```json
    {
      "id": null,
      "email": null,
      "username": "",
      "is_successful": false,
      "message": "Unauthorized request, please login first.",
      "timestamp": "2023-10-30 20:08:17.820156",
      "is_authenticated": false
    }
    ```

#### 3.4.2 Reset Password

Function when people forget their password, or a new user logs in using Social Login.

Reset password consists of 2 functions: `password_reset_generate()` and `password_reset()`.

| Function                      | Path                              | Method     | Description                          |
| ----------------------------- | --------------------------------- | ---------- | ------------------------------------ |
| password_reset_generate()     | /api/auth/password/reset/generate | POST       | Generate and send verification code. |
| password_reset() | /api/auth/password/reset          | POST / PUT | Reset password.                      |

##### 3.4.2.1 Generate

If the email address exists in our database, an email entitled **Password Reset** will be sent from [EnzyHTP Web Application Mailbox](website.enzyhtp@gmail.com) to the users registered mailbox.

- Path: `/api/auth/password/reset/generate`.
- Request Method: `POST`.
- Request Body: `form-data`.
  - `email`: The email address of the account to have password reset.
- Returns:
  - If succeeded,
    - Status: `200 OK`.
    - Response Body:
    ```json
    {
        "id": "78a5f120-63ac-4ce1-aa84-8cce1826a415",
        "email": "san.zhang@example.com",
        "username": "",
        "is_successful": true,
        "message": "Verification code has been successfully sent to `san.zhang@example.com`.",
        "timestamp": "2024-03-29 01:44:08.861044",
        "is_authenticated": false
    }
    ```
  - If failed (due to account doesn't exist.)
    - Status Code: `404 NOT FOUND`.
    - Response Body:
    ```json
    {
        "id": null,
        "email": "si.li@example.com",
        "username": "",
        "is_successful": false,
        "message": "Target user `si.li@example.com` does not exist.",
        "timestamp": "2024-03-29 01:53:01.061447",
        "is_authenticated": false
    }
    ```
  - If failed (due to general error.)
    - Status Code: `500 Internal Server Error`.
    - Response Body:
    ```json
    {
        "id": "78a5f120-63ac-4ce1-aa84-8cce1826a415",
        "email": "san.zhang@example.com",
        "username": "",
        "is_successful": true,
        "message": "Error raised when sending verification code to `san.zhang@example.com`.",
        "timestamp": "2024-03-29 01:44:08.861044",
        "is_authenticated": false
    }
    ```

##### 3.4.2.2 Reset

- Path: `/api/auth/password/reset`.
- Request Method: `POST`.
- Request Body: `form-data`.
  - `email`: The email address of the account to have password reset.
  - `verification_code`: The verification code sent to mailbox.
  - `new_password`: The new password.
- Returns:
  - If succeeded,
    - Status: `200 OK`.
    - Response Body:
    ```json
    {
        "id": "22ae094c-4725-4d61-8b3d-6c1aada44acb",
        "email": "yinjie.zhong.cn@gmail.com",
        "username": "",
        "is_successful": true,
        "message": "User `Yinjie Zhong` succeeded to change the password.",
        "timestamp": "2024-03-29 03:31:54.793617",
        "is_authenticated": false
    }
    ```
  - If failed (due to account not exist.)
    - Status Code: `404 NOT FOUND`.
    - Response Body:
    ```json
    {
        "id": null,
        "email": "yinjie.zhong.cn@gmail.co",
        "username": "",
        "is_successful": false,
        "message": "Target user `yinjie.zhong.cn@gmail.co` does not exist.",
        "timestamp": "2024-03-29 03:31:54.793617",
        "is_authenticated": false
    }
    ```
  - If failed (due to unmatch verification code.)
    - Status Code: `403 FORBIDDEN`.
    - Response Body:
    ```json
    {
        "id": "22ae094c-4725-4d61-8b3d-6c1aada44acb",
        "email": "yinjie.zhong.cn@gmail.com",
        "username": "",
        "is_successful": false,
        "message": "User `Yinjie Zhong` failed to reset the password due to unmatched verification code.",
        "timestamp": "2024-03-29 03:31:54.793617",
        "is_authenticated": false
    }
    ```
  - If failed (due to expired verification code.)
    - Status Code: `403 FORBIDDEN`.
    - Response Body:
    ```json
    {
        "id": "22ae094c-4725-4d61-8b3d-6c1aada44acb",
        "email": "yinjie.zhong.cn@gmail.com",
        "username": "",
        "is_successful": false,
        "message": "User `Yinjie Zhong` failed to reset the password. Verification code has expired!",
        "timestamp": "2024-03-29 03:31:54.793617",
        "is_authenticated": false
    }
    ```
  - If failed (due to used verification code.)
    - Status Code: `403 FORBIDDEN`.
    - Response Body:
    ```json
    {
        "id": "22ae094c-4725-4d61-8b3d-6c1aada44acb",
        "email": "yinjie.zhong.cn@gmail.com",
        "username": "",
        "is_successful": false,
        "message": "User `Yinjie Zhong` failed to reset the password. Verification code is used!",
        "timestamp": "2024-03-29 03:37:34.397148",
        "is_authenticated": false
    }
    ```

## 4 OAuth

### 4.1 OAuth Unsafe Login

This method is only to test if the application works properly after passing the social login.  
This method is for development mode only.  
This method responds with `405 METHOD NOT ALLOWED` in production mode, otherwise, this method always responds with `200 OK` (with right input).  

- Path: `/api/auth/oauth/unsafe/login`.
- Request Method: `POST`.
- Request Body: `form-data`.
  - `email`: Email address of the oauth user.
  - `oauth_vendor`: OAuth Vendor, e.g. Google, Microsoft, etc. (In this function, whatever `oauth_vendor` fields will eventually be recorded as `Unsafe` in the database.)
  - `username`: The username of the account from OAuth Vendor.
  - `remember`: Whether to remember the user(s) after the browser(s) is closed. Defaults to `False`.
- Returns:
  - If account exists, match.
    - Status Code: `200 OK`.
    - Response Body
    ```json
    {
      "id": "0859579b-234d-4b03-8b56-552552c37230",
      "email": "lisa.green@example.com",
      "username": "lisa.green",
      "is_successful": true,
      "message": "User `lisa.green` logged in using `Unsafe` account.",
      "timestamp": "2023-12-12 21:48:22.255380",
      "is_authenticated": true,
      "oauth_email": "lisa.green@example.com",
      "oauth_vendor": "Unsafe"
    }
    ```
  - If social login account is identical with existing user's, bind.
    - Status Code: `201 CREATED`.
    - Response Body:
    ```json
    {
      "id": "11888232-3ad8-43cd-9778-bc1659488a19",
      "email": "san.zhang@example.com",
      "username": "san.zhang",
      "is_successful": true,
      "message": "`New oauth account `san.zhang@example.com` logged in using `Unsafe` account, automatically bound to User `san.zhang`.",
      "timestamp": "2024-02-05 00:01:05.093385",
      "is_authenticated": true,
      "has_openai_secret_key": false,
      "oauth_email": "san.zhang@example.com",
      "oauth_vendor": "Unsafe"
    }
    ```
  - If social login email doesn't exist in the `users` table, create new user.
    - Status Code: `201 CREATED`.
    - Response Body:
    ```json
    {
      "id": "d3bfa780-377d-4f33-ab62-49fdbd0648a1",
      "email": "san.zhang@example.com",
      "username": "ZHANG San",
      "is_successful": true,
      "message": "`New oauth account `san.zhang@example.com` logged in using `Unsafe` account. Create new User `ZHANG San`.",
      "timestamp": "2023-12-12 22:03:40.414137",
      "is_authenticated": true,
      "oauth_email": "san.zhang@example.com",
      "oauth_vendor": "Unsafe"
    }
    ```

### 4.2 OAuth Vendor Login

This method is to redirect the user to the Social Login consent page (i.e., Google, Microsoft, etc.) and automatically redirect to the callback function to grab the user information from the vendor's. Then, the login process will be performed by the EnzyHTP Web Application to set up a session and grant user with the cookie.

Vendor login consists of 2 functions: `oauth_vendor_login()` and `oauth_vendor_login_callback()`.

| Function                      | Path                                          | Method     | Description                   |
| ----------------------------- | --------------------------------------------- | ---------- | ----------------------------- |
| oauth_vendor_login()          | /api/auth/oauth/<oauth_vendor>/login          | GET / POST | OAuth Login Uri               |
| oauth_vendor_login_callback() | /api/auth/oauth/<oauth_vendor>/login/callback | GET / POST | OAuth Login Callback Function |

Here, the `oauth_vendor` is a variable. For example, if we are to login with Google, the path would be: `/api/auth/oauth/google/login`.

Before developing or testing OAuth, some preparations should be done. Please check the `README.md` file in the `/flask-server` directory or Click the Links: 1. [SSL Certificates](../README.md#3-ssl-certificates) 2. [OAuth Clients](../README.md#4-oauth-clients).

#### 4.2.1 How it works?

- For the convenience of description, Google Login is employed for instance.
- When the user click the Social Login button (e.g. Login with Google), navigate the user to `https://<HOST_DOMAIN>:<PORT>/api/auth/oauth/google/login`, which will be automatically redirected (Status: 302) to the consent page of Google.
- After the user confirmed the consent with Google, the Callback Function functions to grab the user information from Google with the authorization code.
- Then, the EnzyHTP Web Application will perform login process with the information from Google, and send returns in `application/json` format.
  - If account exist, match.
    - Status Code: `200 OK`.
    - Response Body
    ```json
    {
      "id": "082eba87-34d0-49c8-a7ae-52f3d8b540b8",
      "email": "yinjie.zhong.cn@gmail.com",
      "username": "Yinjie Zhong",
      "is_successful": true,
      "message": "User `Yinjie Zhong` logged in using `Google` account.",
      "timestamp": "2024-02-17 23:49:16.027819",
      "is_authenticated": true,
      "has_openai_secret_key": true,
      "is_openai_secret_key_valid": true,
      "openai_status_code": 200,
      "openai_response_description": "Welcome to ChatGPT! We are thrilled to have you.",
      "oauth_email": "yinjie.zhong.cn@gmail.com",
      "oauth_vendor": "Google"
    }
    ```
  - If social login account is identical with existing user's, bind.
    - Status Code: `201 CREATED`.
    - Response Body:
    ```json
    {
      "id": "ded2aacd-70a2-491e-9446-331526bd9f8a",
      "email": "yinjie.zhong.cn@gmail.com",
      "username": "Yinjie",
      "is_successful": true,
      "message": "`New oauth account `yinjie.zhong.cn@gmail.com` logged in using `Google` account, automatically bound to User `Yinjie`.",
      "timestamp": "2023-12-14 03:48:07.729680",
      "is_authenticated": true,
      "has_openai_secret_key": true,
      "is_openai_secret_key_valid": true,
      "openai_status_code": 200,
      "openai_response_description": "Welcome to ChatGPT! We are thrilled to have you.",
      "oauth_email": "yinjie.zhong.cn@gmail.com",
      "oauth_vendor": "Google"
    }
    ```
  - If social login email doesn't exist in the `users` table, create new user.
    - Status Code: `201 CREATED`.
    - Response Body:
    ```json
    {
      "id": "2e76933b-1bf0-43da-b02c-209d1c5c66bb",
      "email": "yinjie.zhong.cn@gmail.com",
      "username": "Yinjie Zhong",
      "is_successful": true,
      "message": "`New oauth account `yinjie.zhong.cn@gmail.com` logged in using `Google` account. Create new User `Yinjie Zhong`.",
      "timestamp": "2023-12-14 04:21:32.808972",
      "is_authenticated": true,
      "has_openai_secret_key": true,
      "is_openai_secret_key_valid": true,
      "openai_status_code": 200,
      "openai_response_description": "Welcome to ChatGPT! We are thrilled to have you.",
      "oauth_email": "yinjie.zhong.cn@gmail.com",
      "oauth_vendor": "Google"
    }
    ```
- Note: The validity of `openai_secret_key` is checked after each successful login.

#### 4.2.2 What to do?

- The Callback function in the development mode lets user(s) see some json strings.
- In the production mode, the server is launched via [`start.sh`](../start.sh), where the user(s) will be redirected to the page where user(s) are required to enter their OpenAI API Key, or to the dashboard if their OpenAI API Key is valid.
