#! python3
# -*- encoding: utf-8 -*-
'''
@File    :   views.py
@Created :   2023/10/21 22:05
@Author  :   Zhong, Yinjie
@Version :   1.0
@Contact :   yinjie.zhong@vanderbilt.edu
'''

# Here put the import lib.
from flask import Response, jsonify, request, redirect
from flask_jwt_extended import create_access_token
from flask_login import login_user, logout_user, login_required, current_user
from datetime import datetime
from typing import Optional
from uuid import uuid4
from requests import get, post
from json import dumps, loads
from string import Template

# Here put local imports.
from config import (
    ENV,
    DEVELOPMENT,
    OAUTH_VENDOR_LOGIN_CALLBACK_REDIRECT_URI,
    JSONIFY_MIMETYPE,
    TOKEN_EXPIRES_DELTA,
)
from . import auth
from .models import User, OAuthUser, VerificationCode
from context import mongo, login_manager

db = mongo.db

def _get_client_ip() -> str:
    forwarded_for = request.headers.get("X-Forwarded-For", "")
    if forwarded_for:
        return forwarded_for.split(",")[0].strip()
    return request.remote_addr or "unknown"


def _log_login_event(
    *,
    user_id: Optional[str],
    email: Optional[str],
    username: Optional[str],
    method: str,
    is_successful: bool,
    message: str = str(),
    oauth_vendor: str = str(),
) -> None:
    try:
        record = {
            "user_id": user_id,
            "email": email,
            "username": username,
            "method": method,
            "oauth_vendor": oauth_vendor,
            "is_successful": is_successful,
            "message": message,
            "ip": _get_client_ip(),
            "user_agent": request.headers.get("User-Agent", "unknown"),
            "created_time": datetime.now(),
        }
        db.login_logs.insert_one(record)
    except Exception:
        # Avoid breaking auth flow on log failures.
        pass

@auth.route("/", methods=["GET", "POST", "PUT", "DELETE"])
def index() -> Response:
    """The index of auth module"""
    return jsonify({
        "message": "This is the Auth Module of EnzyHTP Web Application. Welcome!"
    })

class AuthResponseInfo():
    """Authentication Response Information.
        
    Attributes:
        id (str): User ID.
        email (str): User Email Address.
        username (str): Username.
        is_successful (bool): Has the request successfully achieved its purpose?
        message (str): The message to be sent.
        timestamp (str): For `register`, it is the time when the user is registered; otherwise it is the time when the operation is completed.  
        is_authenticated (bool): A boolean value to show if a user is authenticated. Set to `True` for login success, Set to `False` for login failure or logout.
        has_openai_secret_key (bool): Does the user have OpenAI Secret Key?
    """

    def __init__(self,
            id: str,
            email: str,
            username: str =  str(),
            is_successful: bool = True,
            message: str = str(),
            timestamp = datetime.__new__(datetime, 1970, 1, 1),
            is_authenticated: bool = False,
            verify_openai_secret_key: bool = False,
            **kwargs
            ) -> None:
        """Authentication Response Information.
        
        Args:
            id: User ID.
            email: User Email Address.
            username: Username.
            is_successful: Has the request successfully achieved its purpose?
            message: The message to be sent.
            timestamp: For `register`, it is the time when the user is registered; otherwise it is the time when the operation is completed.  
            is_authenticated (bool): Show if a user is authenticated. Set to `True` for login success, Set to `False` for login failure or logout.
            verify_openai_secret_key (bool): Will we verify the user's OpenAI Secret Key?
        """
        self.id = id
        self.email = email
        self.username = username
        self.is_successful = is_successful
        self.message = message
        if (timestamp == datetime.__new__(datetime, 1970, 1, 1)):
            # Here we might as well assume that 1970-01-01 is a time that will not be triggered in actual business.
            self.timestamp = str(datetime.now())
        else:        
            self.timestamp = str(timestamp)
        self.is_authenticated = is_authenticated
        if (is_authenticated):
            user: User = current_user
            self.has_openai_secret_key = user.has_openai_secret_key
        if (verify_openai_secret_key):
            self.is_openai_secret_key_valid, self.openai_status_code, self.openai_response_description = user.get_openai_secret_key_status()
            
        self.kwargs = kwargs
        return
    
    def serialize(self) -> str:
        """Serialize the current instance to json string."""
        from json import dumps
        serialized_data = self.__dict__
        for key, value in self.kwargs.items():
            serialized_data[key] = value
        del serialized_data["kwargs"]
        return dumps(serialized_data)

@login_manager.user_loader
def load_user(user_id: str) -> User:
    """A mandatory method to return a user instance based on user id.
    
    Args:
        user_id: User ID.
    """
    return User.get(id=user_id)

@login_manager.unauthorized_handler
def unauth_handler() -> Response:
    """Handle unauthorized requests toward an `@login_required` method."""
    response_info = AuthResponseInfo(
        id=None,
        email=None,
        is_successful=False,
        message="Unauthorized request, please login first.",
    )
    return Response(response=response_info.serialize(), status=401, mimetype=JSONIFY_MIMETYPE)

def notadmin_handler(user: User) -> Response:
    """Handle unauthorized requests towards a method requiring an admin user.
    
    Args:
        user (User): current user.

    Returns:
        A response instance with 403 FORBIDDEN.
    """
    response_info = AuthResponseInfo(
        id=user.id,
        email=user.email,
        username=user.username,
        is_authenticated=True,
        is_successful=False,
        message="Only admin users can access this endpoint.",
    )
    return Response(response=response_info.serialize(), status=403, mimetype=JSONIFY_MIMETYPE)

#region 3.1 Register and Unregister

@auth.route("/register", methods=["POST"])
def register() -> Response:
    """New User Registration."""
    email = request.form.get("email").lower()
    username = request.form.get("username", str())
    password_plaintext = request.form.get("password", str())
    if (len(password_plaintext) < 4):
        response_info = AuthResponseInfo(
            id=None,
            email=email,
            username=username,
            is_successful=False,
            message=f"Password should be provided!",
        )
        return Response(response=response_info.serialize(), status=400, mimetype=JSONIFY_MIMETYPE)

    user = User(email=email, password_plaintext=password_plaintext, username=username)

    if (User.get_by_email(email=email)):
        response_info = AuthResponseInfo(
            id=None,
            email=email,
            username=user.username,
            is_successful=False,
            message=f"New user `{user.email}` conflicted with an existing account.")
        return Response(response=response_info.serialize(), status=409, mimetype=JSONIFY_MIMETYPE)
    else:
        db.users.insert_one(user.as_dict())
        # db.session.add(user)
        # db.session.commit()

        response_info = AuthResponseInfo(
            id=user.id,
            email=user.email,
            username=user.username,
            message=f"New user `{user.email}` is created.",
            timestamp=user.registered_on)
        return Response(response=response_info.serialize(), status=201, mimetype=JSONIFY_MIMETYPE)

@auth.route("/unregister", methods=["POST", "DELETE"])
@login_required
def unregister() -> Response:
    """Unregister a Current User. Only the user him/herself is permitted to do so."""
    
    user: User = current_user
    email_to_match = request.form.get("email").lower()
    user_to_unregister = User.get_by_email(email=email_to_match)
    if (not user_to_unregister):    # Email doesn't exist.
        response_info = AuthResponseInfo(
            id=None,
            email=email_to_match,
            is_successful=False,
            message=f"Target user `{email_to_match}` does not exist.",
            is_authenticated=True)
        return Response(response=response_info.serialize(), status=404, mimetype=JSONIFY_MIMETYPE)
    elif (user_to_unregister.id == user.id):  # User.id matched.
        response_info = AuthResponseInfo(
            id=user.id,
            email=user.email,
            is_successful=True,
            message=f"User `{user_to_unregister.email}` is unregistered.",
            is_authenticated=False)
        logout_user()
        db.oauth_users.delete_many({"user_id": user_to_unregister.id})
        db.users.delete_one({"id": user_to_unregister.id})
        # db.session.delete(user_to_unregister)
        # db.session.commit()
        return Response(response=response_info.serialize(), status=200, mimetype=JSONIFY_MIMETYPE)
    elif (user_to_unregister.id != user.id): # User.id doesn't match.
        response_info = AuthResponseInfo(
            id=user.id,
            email=user.email,
            is_successful=False,
            message=f"You cannot unregister `{user_to_unregister.email}`.",
            is_authenticated=True)
        return Response(response=response_info.serialize(), status=403, mimetype=JSONIFY_MIMETYPE)

#endregion

#region 3.2 Login and Logout

@auth.route("/login", methods=["POST"])
def login() -> Response:
    """User Login."""
    email = request.form.get("email", str()).lower()
    user = User.get_by_email(email=email)
    remember = bool(request.form.get("remember", False))    # Whether to remember the user(s) after the browser(s) is closed. Defaults to `False`.
    if user and user.verify_password(request.form.get("password", str())):
        is_login = login_user(user=user, remember=remember)
        _log_login_event(
            user_id=user.id,
            email=user.email,
            username=user.username,
            method="password",
            is_successful=is_login,
            message=f"The user `{user.username}` logged in.",
        )
        response_info = AuthResponseInfo(
            id=user.id,
            email=user.email,
            username=user.username,
            message=f"The user `{user.username}` logged in.",
            is_authenticated=is_login,
            verify_openai_secret_key=True)
        return Response(response=response_info.serialize(), status=200, mimetype=JSONIFY_MIMETYPE)
    elif (not user):
        _log_login_event(
            user_id=None,
            email=email,
            username=None,
            method="password",
            is_successful=False,
            message=f"The user `{email}` failed to log in because user does not exist.",
        )
        response_info = AuthResponseInfo(
            id=None,
            email=email,
            message=f"The user `{email}` failed to log in because user does not exist.",
            is_authenticated=False)
        return Response(response=response_info.serialize(), status=404, mimetype=JSONIFY_MIMETYPE)
    else:
        _log_login_event(
            user_id=user.id if user else None,
            email=email,
            username=user.username if user else None,
            method="password",
            is_successful=False,
            message=f"The user `{email}` failed to log in because of a password mismatch.",
        )
        response_info = AuthResponseInfo(
            id=None,
            email=email,
            message=f"The user `{email}` failed to log in because of a password mismatch.",
            is_authenticated=False)
        return Response(response=response_info.serialize(), status=401, mimetype=JSONIFY_MIMETYPE)

@auth.route("/logout", methods=["GET", "POST"])
@login_required
def logout() -> Response:
    """User Logout."""
    user = current_user
    response_info = AuthResponseInfo(
        id=user.id,
        email=user.email,
        message=f"The user `{user.email}` logged out.",
        is_authenticated=False)
    logout_user()
    return Response(response=response_info.serialize(), status=200, mimetype=JSONIFY_MIMETYPE)

#endregion

#region 3.3 Profile

@auth.route("/profile", methods=["GET"])
@login_required
def profile() -> Response:
    """User Profile."""
    user: User = current_user
    response_info = AuthResponseInfo(
        id=user.id,
        email=user.email,
        username=user.username,
        is_authenticated=True)
    return Response(response=response_info.serialize(), status=200, mimetype=JSONIFY_MIMETYPE)

@auth.route("/profile", methods=["POST", "PUT"])
@login_required
def profile_update() -> Response:
    """Update the editable field(s) in the user profile."""
    user: User = current_user
    editable_profile_fields = ["username", "openai_secret_key"] # Only fields in the list are editable.

    updated_profile_fields = list()
    nonexistent_profile_fields = list()
    blocked_profile_fields = list()
    failed_profile_fields = list()
    openai_validation_result = None

    for field_name, field_value in request.form.items():
        if (hasattr(user, field_name)):
            if field_name in editable_profile_fields:
                if (field_value):
                    if (field_name == "openai_secret_key"):
                        openai_provided = True
                        previous_key = user.openai_secret_key
                        user.openai_secret_key = field_value
                        is_valid, openai_status_code, openai_response_description = user.get_openai_secret_key_status()
                        user.openai_secret_key = previous_key
                        openai_validation_result = (is_valid, openai_status_code, openai_response_description)

                        if (not is_valid):
                            failed_profile_fields.append(field_name)
                            continue

                    setattr(user, field_name, field_value)
                    db.users.update_one({"id": user.id}, {"$set": {field_name: field_value}})
                    # db.session.commit()
                    updated_profile_fields.append(field_name)

                continue
            else:
                blocked_profile_fields.append(field_name)
        else:
            nonexistent_profile_fields.append(field_name)

    message = str()
    if (updated_profile_fields):
        message += f"Updated field(s): {', '.join(updated_profile_fields)}. "
    if (blocked_profile_fields):
        message += f"Uneditable field(s): {', '.join(blocked_profile_fields)}. "
    if (nonexistent_profile_fields):
        message += f"Nonexistent field(s): {', '.join(nonexistent_profile_fields)}. "
    if (failed_profile_fields):
        message += f"Failed to update field(s): {', '.join(failed_profile_fields)}. "


    if (not (updated_profile_fields or blocked_profile_fields or nonexistent_profile_fields or failed_profile_fields)):
        response_info = AuthResponseInfo(
            id=user.id,
            email=user.email,
            username=user.username,
            is_successful=True,
            message=f"Nothing to be updated.",
            is_authenticated=True
        )
        return Response(response=response_info.serialize(), status=200, mimetype=JSONIFY_MIMETYPE)
    if (updated_profile_fields or failed_profile_fields):
        extra_fields = dict()
        if (openai_validation_result):
            is_valid, openai_status_code, openai_response_description = openai_validation_result
            extra_fields.update({
                "is_openai_secret_key_valid": is_valid,
                "openai_status_code": openai_status_code,
                "openai_response_description": openai_response_description,
            })
            if (is_valid):
                message = f"{message}OpenAI Secret Key validated."
            else:
                message = f"{message}OpenAI Secret Key not updated: {openai_response_description}."

        response_info = AuthResponseInfo(
            id=user.id,
            email=user.email,
            username=user.username,
            is_successful=True,
            message=message.strip(),
            is_authenticated=True,
            **extra_fields,
        )
        response_status = 200

        if (openai_validation_result and not openai_validation_result[0]):
            response_info.is_successful = False
            response_status = openai_validation_result[1] if openai_validation_result[1] else 400
        return Response(response=response_info.serialize(), status=response_status, mimetype=JSONIFY_MIMETYPE)
    else:
        response_info = AuthResponseInfo(
            id=user.id,
            email=user.email,
            username=user.username,
            is_successful=False,
            message=message,
            is_authenticated=True
        )
        return Response(response=response_info.serialize(), status=400, mimetype=JSONIFY_MIMETYPE)

@auth.route("/profile/jwt", methods=["GET"])
@login_required
def profile_jwt() -> Response:
    """Generate the JWT token."""
    user: User = current_user
    response_info = AuthResponseInfo(
        id=user.id,
        email=user.email,
        username=user.username,
        is_authenticated=True,
        access_token=create_access_token(identity=user.id, expires_delta=TOKEN_EXPIRES_DELTA),
    )
    return Response(response=response_info.serialize(), status=200, mimetype=JSONIFY_MIMETYPE)

#endregion

#region 3.4 Password

@auth.route("/password/change", methods=["POST", "PUT"])
@login_required
def password_change() -> Response:
    """Change password."""
    old_password = request.form.get("old_password")
    new_password = request.form.get("new_password")
    user: User = current_user
    if (user.verify_password(old_password)):
        user.set_password(new_password)
        response_info = AuthResponseInfo(
            id=user.id,
            email=user.email,
            username=user.username,
            message=f"User `{user.username}` succeeded to change the password.",
            is_authenticated=True,
        )
        db.users.update_one({"id": user.id}, {"$set": {"password": user.password}})
        # db.session.commit()
        return Response(response=response_info.serialize(), status=200, mimetype=JSONIFY_MIMETYPE)
    else:
        response_info = AuthResponseInfo(
            id=user.id,
            email=user.email,
            username=user.username,
            is_successful=False,
            message=f"User `{user.username}` failed to change the password due to unmatched old password.",
            is_authenticated=True,
        )
        return Response(response=response_info.serialize(), status=400, mimetype=JSONIFY_MIMETYPE)

@auth.route("/password/reset/generate", methods=["POST"])
def password_reset_generate() -> Response:
    """Generate and send verification code for password reset."""
    VerificationCode.clean_expired_records()    # Clean up expired records everytime before generating new one.
    code_length = 6
    valid_mins = 20

    email_to_match = request.form.get("email").lower()
    user = User.get_by_email(email=email_to_match)
    if (not user):    # Email doesn't exist.
        response_info = AuthResponseInfo(
            id=None,
            email=email_to_match,
            is_successful=False,
            message=f"Target user `{email_to_match}` does not exist.",
        )
        return Response(response=response_info.serialize(), status=404, mimetype=JSONIFY_MIMETYPE)
    else:
        verification_code_instance = VerificationCode(user_id=user.id, valid_minutes=valid_mins, length=code_length)
        db.verification_codes.insert_one(verification_code_instance.as_dict())
        # db.session.add(verification_code_instance)
        is_sent = verification_code_instance.send_email()
        if (is_sent):
            response_info = AuthResponseInfo(
                id=user.id,
                email=user.email,
                message=f"Verification code has been successfully sent to `{user.email}`.",
            )
            # db.session.commit()
            return Response(response=response_info.serialize(), status=200, mimetype=JSONIFY_MIMETYPE)
        else:
            
            response_info = AuthResponseInfo(
                id=user.id,
                email=user.email,
                message=f"Error raised when sending verification code to `{user.email}`.",
                is_successful=False,
            )
            return Response(response=response_info.serialize(), status=500, mimetype=JSONIFY_MIMETYPE)

@auth.route("/password/reset", methods=["POST", "PUT"])
def password_reset() -> Response:
    """Reset password (Not completed)
    The router should be commented to deactivate the method in Production environment.
    """
    email_to_match = request.form.get("email").lower()
    verification_code = request.form.get("verification_code")
    new_password = request.form.get("new_password")
    user = User.get_by_email(email=email_to_match)
    if (not user):    # Email doesn't exist.
        response_info = AuthResponseInfo(
            id=None,
            email=email_to_match,
            is_successful=False,
            message=f"Target user `{email_to_match}` does not exist.",
            is_authenticated=False)
        return Response(response=response_info.serialize(), status=404, mimetype=JSONIFY_MIMETYPE)
    elif (verification_code): # (Not completed.) Check if the code is verified.
        if (code_record:=VerificationCode.get_by_user_and_code(user=user, verification_code=verification_code)):
            if (code_record.expiration_time < datetime.now()):
                response_info = AuthResponseInfo(
                    id=user.id,
                    email=user.email,
                    is_successful=False,
                    message=f"User `{user.username}` failed to reset the password. Verification code has expired!",
                )
                return Response(response=response_info.serialize(), status=403, mimetype=JSONIFY_MIMETYPE)
            elif (code_record.is_used):
                response_info = AuthResponseInfo(
                    id=user.id,
                    email=user.email,
                    is_successful=False,
                    message=f"User `{user.username}` failed to reset the password. Verification code is used!",
                )
                return Response(response=response_info.serialize(), status=403, mimetype=JSONIFY_MIMETYPE)
            else:
                user.set_password(new_password)
                response_info = AuthResponseInfo(
                    id=user.id,
                    email=user.email,
                    message=f"User `{user.username}` succeeded to change the password.",
                )
                code_record.is_used = True
                db.users.update_one({"id": user.id}, {"$set": {"password": user.password}})
                db.verification_codes.update_one({"id": code_record.id}, {"$set": {"is_used": code_record.is_used}})
                # db.session.commit()
                return Response(response=response_info.serialize(), status=200, mimetype=JSONIFY_MIMETYPE)
        else:
            response_info = AuthResponseInfo(
                id=user.id,
                email=user.email,
                is_successful=False,
                message=f"User `{user.username}` failed to reset the password due to unmatched verification code.",
                
            )
            return Response(response=response_info.serialize(), status=403, mimetype=JSONIFY_MIMETYPE)

    else:
        response_info = AuthResponseInfo(
            id=user.id,
            email=user.email,
            is_successful=False,
            message=f"User `{user.email}` failed to reset the password due to unmatched verification code.",
        )
        return Response(response=response_info.serialize(), status=400, mimetype=JSONIFY_MIMETYPE)

#endregion

## ******* The dividing line between Email login and OAuth login ****** ##

from .oauth_config import CLIENT_ID, CLIENT_SECRET, provider_cfg_dict, oauth_client_dict, get_provider_cfg
from oauthlib.oauth2 import WebApplicationClient
    
class OAuthResponseInfo(AuthResponseInfo):
    """OAuth Response Information.
    
    Attributes (except for attributes in base class):
        oauth_vendor (str): OAuth Vendor, e.g. Google, Microsoft, etc.
    """
    def __init__(self,
            id: str,
            email: str,
            oauth_email: str,
            oauth_vendor: str,
            username: str = str(),
            is_successful: bool = True,
            message: str = str(),
            timestamp = datetime.__new__(datetime, 1970, 1, 1),
            is_authenticated: bool = False,
            verify_openai_secret_key: bool = False
            ) -> None:
        """Authentication Response Information.
        
        Args:
            id: User ID.
            email: User Email Address.
            oauth_email: OAuth Email Address (e.g. gmail of Google, outlook/hotmail of Microsoft, etc.)
            oauth_vendor: OAuth Vendor, e.g. Google, Microsoft, etc.
            username: Username.
            is_successful: A boolean value to show if a request have successfully achieved its purpose.
            message: The message to be sent.
            timestamp: For "register", it is the time when the user is registered; otherwise it is the time when the operation is completed.  
            is_authenticated: A boolean value to show if a user is authenticated. Set to `True` for login success, Set to `False` for login failure or logout.
            verify_openai_secret_key (bool): Will we verify the user's OpenAI Secret Key?
        """
        super().__init__(id=id,
            email=email, username=username, is_successful=is_successful, message=message,
            timestamp=timestamp, is_authenticated=is_authenticated, verify_openai_secret_key=verify_openai_secret_key)
        self.oauth_email = oauth_email
        self.oauth_vendor = OAuthUser.camel_case_oauth_vendor(oauth_vendor)
        return

def __perform_oauth_login(
        oauth_email: str,
        oauth_vendor: str,
        username: str = str(),
        remember: bool = False
        ) -> Response:
    """This method is to check account in application database and perform login operation.
    This method should be triggered after social login is passed.
    
    The process is:
    1. If account exists, match.
    2. If social login account is identical with existing user's, bind.
    3. If social login email doesn't exist in the `users` table, create new user.

    Args:
        oauth_email: Email address of the oauth user.
        oauth_vendor: OAuth Vendor, e.g. `Google`, `Microsoft`, etc.
        username: The username.
        remember: Whether to remember the user(s) after the browser(s) is closed. Defaults to `False`.
    """
    oauth_vendor = OAuthUser.camel_case_oauth_vendor(oauth_vendor)
    oauth_user = OAuthUser.get_by_email_and_vendor(email=oauth_email, oauth_vendor=oauth_vendor)
    if (oauth_user and oauth_user.user_id): # If account exists, match.
        user = User.get(oauth_user.user_id)
        login_user(user=user, remember=remember)
        _log_login_event(
            user_id=user.id if user else None,
            email=user.email if user else oauth_email,
            username=user.username if user else None,
            method="oauth",
            oauth_vendor=oauth_vendor,
            is_successful=True,
            message=f"User `{user.username}` logged in using `{oauth_vendor}` account.",
        )
        oauth_response_info = OAuthResponseInfo(
            id=user.id,
            email=user.email,
            username=user.username,
            oauth_email=oauth_email,
            oauth_vendor=oauth_vendor,
            message=f"User `{user.username}` logged in using `{oauth_vendor}` account.",
            is_authenticated=True,
            verify_openai_secret_key=True)
        return Response(response=oauth_response_info.serialize(), status=200, mimetype=JSONIFY_MIMETYPE)
    elif (user := User.get_by_email(email=oauth_email)):    # If social login account is identical with existing user's, bind.
        oauth_user = OAuthUser(
            email=oauth_email,
            oauth_vendor=oauth_vendor,
            user_id=user.id)
        db.oauth_users.insert_one(oauth_user.as_dict())
        # db.session.add(oauth_user)
        # db.session.commit()
        login_user(user=user, remember=remember)
        _log_login_event(
            user_id=user.id,
            email=user.email,
            username=user.username,
            method="oauth",
            oauth_vendor=oauth_vendor,
            is_successful=True,
            message=f"`New oauth account `{oauth_email}` logged in using `{oauth_vendor}` account, automatically bound to User `{user.username}`.",
        )
        oauth_response_info = OAuthResponseInfo(
            id=user.id,
            email=user.email,
            username=user.username,
            oauth_email=oauth_email,
            oauth_vendor=oauth_vendor,
            message=f"`New oauth account `{oauth_email}` logged in using `{oauth_vendor}` account, automatically bound to User `{user.username}`.",
            is_authenticated=True,
            verify_openai_secret_key=True)
        return Response(response=oauth_response_info.serialize(), status=201, mimetype=JSONIFY_MIMETYPE)
    else:       # If social login email doesn't exist in the `users` table, create new user.
        user = User(email=oauth_email, password_plaintext=str(uuid4())[:8], username=username)
        # db.session.add(user)
        db.users.insert_one(user.as_dict())
        oauth_user = OAuthUser(email=oauth_email, oauth_vendor=oauth_vendor, user_id=user.id)
        db.oauth_users.insert_one(oauth_user.as_dict())
        # db.session.add(oauth_user)
        # db.session.commit()
        login_user(user=user, remember=remember)
        _log_login_event(
            user_id=user.id,
            email=user.email,
            username=username,
            method="oauth",
            oauth_vendor=oauth_vendor,
            is_successful=True,
            message=f"`New oauth account `{oauth_email}` logged in using `{oauth_vendor}` account. Create new User `{username}`.",
        )
        oauth_response_info = OAuthResponseInfo(
            id=user.id,
            email=user.email,
            username=username,
            oauth_email=oauth_email,
            oauth_vendor=oauth_vendor,
            message=f"`New oauth account `{oauth_email}` logged in using `{oauth_vendor}` account. Create new User `{username}`.",
            is_authenticated=True,
            verify_openai_secret_key=True)
        return Response(response=oauth_response_info.serialize(), status=201, mimetype=JSONIFY_MIMETYPE)

@auth.route("oauth/<oauth_vendor>/login", methods=["GET", "POST"])
def oauth_vendor_login(oauth_vendor: str) -> Response:
    """Redirect to the OAuth Login Page of Vendor(s).

    Args:
        oauth_vendor: OAuth Vendor, e.g. `Google`, `Microsoft`, etc.
    """
    oauth_vendor = oauth_vendor.upper()
    oauth_client: WebApplicationClient = oauth_client_dict.get(oauth_vendor, None)
    provider_cfg: dict = provider_cfg_dict.get(oauth_vendor, None) or get_provider_cfg(oauth_vendor)

    if (oauth_client is None):
        response_info = OAuthResponseInfo(
            id=None,
            email=None,
            oauth_email=None,
            oauth_vendor=oauth_vendor,
            is_successful=False,
            message=f"OAuth vendor `{OAuthUser.camel_case_oauth_vendor(oauth_vendor)}` is not supported.",
        )
        return Response(response=response_info.serialize(), status=400, mimetype=JSONIFY_MIMETYPE)

    authorization_endpoint = provider_cfg.get("authorization_endpoint", None)  # e.g. https://accounts.google.com/o/oauth2/v2/auth
    if (authorization_endpoint is None):
        response_info = OAuthResponseInfo(
            id=None,
            email=None,
            oauth_email=None,
            oauth_vendor=oauth_vendor,
            is_successful=False,
            message=f"OAuth provider configuration for `{OAuthUser.camel_case_oauth_vendor(oauth_vendor)}` is unavailable.",
        )
        return Response(response=response_info.serialize(), status=503, mimetype=JSONIFY_MIMETYPE)

    # Construct the request for Social login and retrieve user's profile.
    request_uri = oauth_client.prepare_request_uri(
        uri=authorization_endpoint,
        redirect_uri=request.base_url + "/callback",
        scope=["openid", "email", "profile"],
    )
    return redirect(request_uri)

@auth.route("oauth/<oauth_vendor>/login/callback", methods=["GET", "POST"])
def oauth_vendor_login_callback(oauth_vendor: str) -> Response:
    """
    Callback Function of OAuth. (Support Google only, at present.)
    Verify authorization code.
    TODO: This function is imperfect. It's better to have a dashboard or homepage for user to redirect to.
    TODO: Then, a redirect(301) response can be sent to redirect users to that page.

    Args:
        oauth_vendor: OAuth Vendor, e.g. `Google`, `Microsoft`, etc.
    """
    oauth_vendor = oauth_vendor.upper()
    oauth_client: WebApplicationClient = oauth_client_dict.get(oauth_vendor, None)
    provider_cfg: dict = provider_cfg_dict.get(oauth_vendor, None) or get_provider_cfg(oauth_vendor)

    if (oauth_client is None):
        response_info = OAuthResponseInfo(
            id=None,
            email=None,
            oauth_email=None,
            oauth_vendor=oauth_vendor,
            is_successful=False,
            message=f"OAuth vendor `{OAuthUser.camel_case_oauth_vendor(oauth_vendor)}` is not supported.",
        )
        return Response(
            response=response_info.serialize(),
            status=400, mimetype=JSONIFY_MIMETYPE)

    if (not provider_cfg):
        response_info = OAuthResponseInfo(
            id=None,
            email=None,
            oauth_email=None,
            oauth_vendor=oauth_vendor,
            is_successful=False,
            message=f"OAuth provider configuration for `{OAuthUser.camel_case_oauth_vendor(oauth_vendor)}` is unavailable.",
        )
        return Response(
            response=response_info.serialize(),
            status=503, mimetype=JSONIFY_MIMETYPE)

    # OAuth2 authorization code
    code = str()
    if (request.method == "GET"):
        code = request.args.get("code", None)
    if (request.method == "POST"):
        code = request.form.get("code", None)
    token_endpoint = provider_cfg.get("token_endpoint", None)
    if (token_endpoint is None):
        response_info = OAuthResponseInfo(
            id=None,
            email=None,
            oauth_email=None,
            oauth_vendor=oauth_vendor,
            is_successful=False,
            message=f"OAuth provider configuration for `{OAuthUser.camel_case_oauth_vendor(oauth_vendor)}` is unavailable.",
        )
        return Response(
            response=response_info.serialize(),
            status=503, mimetype=JSONIFY_MIMETYPE)
    # print(code)

    # Prepare and send a request to get tokens.
    token_url, headers, body = oauth_client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code
    )
    token_response = post(
        token_url,
        headers=headers,
        data=body,
        auth=(CLIENT_ID[oauth_vendor], CLIENT_SECRET[oauth_vendor]),
    )

    try:
        oauth_client.parse_request_body_response(dumps(token_response.json()))
    except:
        response_info = OAuthResponseInfo(
            id=None,
            email=None,
            oauth_email=None,
            oauth_vendor=oauth_vendor,
            is_successful=False,
            message=f"OAuth vendor {OAuthUser.camel_case_oauth_vendor(oauth_vendor)} caught an Invalid Grant Error.",
        )
        return Response(
            response=response_info.serialize(),
            status=400, mimetype=JSONIFY_MIMETYPE)

    # Find and hit the URL from OAuth Vendor that provides the user's profile information.
    userinfo_endpoint = provider_cfg.get("userinfo_endpoint", None)
    if (userinfo_endpoint is None):
        response_info = OAuthResponseInfo(
            id=None,
            email=None,
            oauth_email=None,
            oauth_vendor=oauth_vendor,
            is_successful=False,
            message=f"OAuth provider configuration for `{OAuthUser.camel_case_oauth_vendor(oauth_vendor)}` is unavailable.",
        )
        return Response(
            response=response_info.serialize(),
            status=503, mimetype=JSONIFY_MIMETYPE)
    uri, headers, body = oauth_client.add_token(userinfo_endpoint)
    userinfo_response = get(uri, headers=headers, data=body)
    userinfo:dict = userinfo_response.json()

    # To make sure the email is verified.
    # The user authenticated with OAuth Vendor, authorized your app,
    # and now their email(s) is verified through OAuth Vendor(s).
    if not userinfo.get("email_verified"):
        oauth_response_info = OAuthResponseInfo(
            id=None,
            email=None,
            username=None,
            oauth_email=None,
            oauth_vendor=oauth_vendor,
            is_successful=False,
            message=f"User email is not available or not verified.",
            is_authenticated=False)
        return Response(
            response=oauth_response_info.serialize(),
            status=401, mimetype=JSONIFY_MIMETYPE)
    
    unique_id = userinfo.get("sub")
    oauth_email = str(userinfo.get("email")).lower()
    picture = userinfo.get("picture")
    username = userinfo.get("name", None)

    remember = False
    response = __perform_oauth_login(
        oauth_email=oauth_email,
        oauth_vendor=oauth_vendor,
        username=username,
        remember=remember)
    
    # return response
    return redirect(OAUTH_VENDOR_LOGIN_CALLBACK_REDIRECT_URI, code=301)

@auth.route("oauth/unsafe/login", methods=["POST"])
def oauth_unsafe_login() -> Response:
    """This method is only to test if the application works properly after passing the social login.
    This method is for development mode only.
    This method cannot be used in production mode, where its router should be commented.
    """
    oauth_email = request.form.get("oauth_email").lower()
    # oauth_vendor = request.form.get("oauth_vendor")
    oauth_vendor = "Unsafe"
    username = request.form.get("username", str())
    remember = bool(request.form.get("remember", False))

    if (ENV != DEVELOPMENT):    # If the environment is not in development mode, respond with `418 I'm a teapot`.
        oauth_response_info = OAuthResponseInfo(id=None, email=None, oauth_email=oauth_email, oauth_vendor=oauth_vendor,
            username=username, is_successful=False, message="Unsafe Login is not active in production mode.",
            is_authenticated=False, verify_openai_secret_key=False)
        return Response(response=oauth_response_info.serialize(), status=418, mimetype=JSONIFY_MIMETYPE)
    
    response = __perform_oauth_login(
        oauth_email=oauth_email,
        oauth_vendor=oauth_vendor,
        username=username,
        remember=remember)
    return response
