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
from flask import Response, url_for, request, redirect
from flask_login import login_user, logout_user, login_required, current_user
from datetime import datetime
from uuid import uuid4
from requests import get, post
from json import dumps, loads

# Here put local imports.
from . import auth
from .models import User, OAuthUser
from context import db, login_manager
from server import app

class AuthResponseInfo():
    """Authentication Response Information.
        
    Attributes:
        id (str): User ID.
        email (str): User Email Address.
        username (str): Username.
        is_successful (bool): A boolean value to show if a request have successfully achieved its purpose.
        message (str): The message to be sent.
        timestamp (str): For 'register', it is the time when the user is registered; otherwise it is the time when the operation is completed.  
        is_authenticated (bool): A boolean value to show if a user is authenticated. Set to `True` for login success, Set to `False` for login failure or logout.
    """

    def __init__(self,
            id: str,
            email: str,
            username: str =  str(),
            is_successful: bool = True,
            message: str = str(),
            timestamp = datetime.utcnow(),
            is_authenticated: bool = False,
            ) -> None:
        """Authentication Response Information.
        
        Args:
            id: User ID.
            email: User Email Address.
            username: Username.
            is_successful: A boolean value to show if a request have successfully achieved its purpose.
            message: The message to be sent.
            timestamp: For 'register', it is the time when the user is registered; otherwise it is the time when the operation is completed.  
            is_authenticated: A boolean value to show if a user is authenticated. Set to `True` for login success, Set to `False` for login failure or logout.
        """
        self.id = id
        self.email = email
        self.username = username
        self.is_successful = is_successful
        self.message = message
        self.timestamp = str(timestamp)
        self.is_authenticated = is_authenticated
        return

    def serialize(self) -> str:
        """Serialize the current instance to json string."""
        from json import dumps
        serialized_data = self.__dict__
        # for key, value in serialized_data.items():
        #     print(f"{key}: {type(value)}")
        return dumps(serialized_data)
    
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
            timestamp = datetime.utcnow(),
            is_authenticated: bool = False,
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
            timestamp: For 'register', it is the time when the user is registered; otherwise it is the time when the operation is completed.  
            is_authenticated: A boolean value to show if a user is authenticated. Set to `True` for login success, Set to `False` for login failure or logout.
        """
        super().__init__(id=id,
            email=email, username=username, is_successful=is_successful, message=message,
            timestamp=timestamp, is_authenticated=is_authenticated)
        self.oauth_email = oauth_email
        self.oauth_vendor = OAuthUser.camel_case_oauth_vendor(oauth_vendor)
        return

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
        message='Unauthorized request, please login first.',
    )
    return Response(response=response_info.serialize(), status=401, mimetype='application/json')

@auth.route('/register', methods=['POST'])
def register() -> Response:
    """New User Registration."""
    email = request.form.get('email').lower()
    username = request.form.get('username', '')
    user = User(email=email, password=request.form.get('password'), username=username)

    if (User.get_by_email(email=email)):
        response_info = AuthResponseInfo(
            id=None,
            email=email,
            username=user.username,
            is_successful=False,
            message=f'New user `{user.email}` conflicted with an existing account.',
            timestamp=datetime.utcnow())
        return Response(response=response_info.serialize(), status=400, mimetype='application/json')
    else:
        db.session.add(user)
        db.session.commit()

        response_info = AuthResponseInfo(
            id=user.id,
            email=user.email,
            username=user.username,
            message=f'New user `{user.email}` is created.',
            timestamp=user.registered_on)
        return Response(response=response_info.serialize(), status=201, mimetype='application/json')

@auth.route('/unregister', methods=['POST', 'DELETE'])
@login_required
def unregister() -> Response:
    """Unregister a Current User. Only the user him/herself is permitted to do so."""
    user = current_user
    email_to_match = request.form.get('email').lower()
    user_to_unregister = User.get_by_email(email=email_to_match)
    if (not user_to_unregister):    # Email doesn't exist.
        response_info = AuthResponseInfo(
            id=None,
            email=email_to_match,
            is_successful=False,
            message=f'Target user `{email_to_match}` does not exist.',
            is_authenticated=True)
        return Response(response=response_info.serialize(), status=403, mimetype='application/json')
    elif (user_to_unregister.id == user.id):  # User.id matched.
        response_info = AuthResponseInfo(
            id=user.id,
            email=user.email,
            is_successful=True,
            message=f'User `{user_to_unregister.email}` is unregistered.',
            is_authenticated=False)
        logout_user()
        db.session.delete(user_to_unregister)
        db.session.commit()
        return Response(response=response_info.serialize(), status=200, mimetype='application/json')
    elif (user_to_unregister.id != user.id): # User.id doesn't match.
        response_info = AuthResponseInfo(
            id=user.id,
            email=user.email,
            is_successful=False,
            message=f'You cannot unregister `{user_to_unregister.email}`.',
            is_authenticated=True)
        return Response(response=response_info.serialize(), status=403, mimetype='application/json')

@auth.route('/login', methods=['POST'])
def login() -> Response:
    """User Login."""
    email = request.form.get('email', '').lower()
    user = User.get_by_email(email=email)
    remember = bool(request.form.get('remember', False))    # Whether to remember the user(s) after the browser(s) is closed. Defaults to `False`.
    if user and user.verify_password(request.form.get('password', '')):
        is_login = login_user(user=user, remember=remember)
        response_info = AuthResponseInfo(
            id=user.id,
            email=user.email,
            username=user.username,
            message=f'The user `{user.username}` logged in.',
            is_authenticated=is_login)
        return Response(response=response_info.serialize(), status=200, mimetype='application/json')
    else:
        response_info = AuthResponseInfo(
            id=None,
            email=email,
            message=f'The user `{email}` failed to log in.',
            is_authenticated=False)
        return Response(response=response_info.serialize(), status=401, mimetype='application/json')

@auth.route('/logout', methods=['GET', 'POST'])
@login_required
def logout() -> Response:
    """User Logout."""
    user = current_user
    response_info = AuthResponseInfo(
        id=user.id,
        email=user.email,
        message=f'The user `{user.email}` logged out.',
        is_authenticated=False)
    logout_user()
    return Response(response=response_info.serialize(), status=200, mimetype='application/json')

@auth.route('/profile', methods=['GET'])
@login_required
def profile() -> Response:
    """User Profile."""
    user = current_user
    response_info = AuthResponseInfo(
        id=user.id,
        email=user.email,
        username=user.username,
        is_authenticated=True)
    return Response(response=response_info.serialize(), status=200, mimetype='application/json')

@auth.route('/change_password', methods=['POST', 'PUT'])  # Keep temporarily for the sake of compatibility. Deprecate after January 2024.
@auth.route('/password/change', methods=['POST', 'PUT'])
@login_required
def password_change() -> Response:
    """Change password."""
    old_password = request.form.get('old_password')
    new_password = request.form.get('new_password')
    user = current_user
    if (user.verify_password(old_password)):
        user.set_password(new_password)
        response_info = AuthResponseInfo(
            id=user.id,
            email=user.email,
            username=user.username,
            message=f'User `{user.username}` succeeded to change the password.',
            is_authenticated=True,
        )
        db.session.commit()
        return Response(response=response_info.serialize(), status=200, mimetype='application/json')
    else:
        response_info = AuthResponseInfo(
            id=user.id,
            email=user.email,
            username=user.username,
            is_successful=False,
            mmessage=f'User `{user.username}` failed to change the password due to unmatched old password.',
            is_authenticated=True,
        )
        return Response(response=response_info.serialize(), status=400, mimetype='application/json')

@auth.route('/password/reset', methods=['POST, PUT'])
def password_reset() -> Response:
    """Reset password (Not completed)
    The router should be commented to deactivate the method in Production environment.

    TODO: (Yinjie) send recovery code via email using SMTP. We need something like noreply@domain.com mailbox.
    """
    email_to_match = request.form.get('email').lower()
    verification_code = request.form.get('verification_code')
    new_password = request.form.get('new_password')
    user = User.get_by_email(email=email_to_match)
    if (not user):    # Email doesn't exist.
        response_info = AuthResponseInfo(
            id=None,
            email=email_to_match,
            is_successful=False,
            message=f'Target user `{email_to_match}` does not exist.',
            is_authenticated=True)
        return Response(response=response_info.serialize(), status=404, mimetype='application/json')
    elif (verification_code): # (Not completed.) Check if the code is verified.
        user.set_password(new_password)
        response_info = AuthResponseInfo(
            id=user.id,
            email=user.email,
            message=f'User `{user.email}` succeeded to change the password.',
            is_authenticated=True,
        )
        db.session.commit()
        return Response(response=response_info.serialize(), status=200, mimetype='application/json')
    else:
        response_info = AuthResponseInfo(
            id=user.id,
            email=user.email,
            is_successful=False,
            message=f'User `{user.email}` failed to reset the password due to unmatched verification code.',
            is_authenticated=True,
        )
        return Response(response=response_info.serialize(), status=400, mimetype='application/json')

## ******* The dividing line between normal login and OAuth login ****** ##

from .config import CLIENT_ID, CLIENT_SECRET, provider_cfg_dict, oauth_client_dict
from oauthlib.oauth2 import WebApplicationClient

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
    if (oauth_user and oauth_user.user_id):
        user = oauth_user.user
        login_user(user=user, remember=remember)
        oauth_response_info = OAuthResponseInfo(
            id=user.id,
            email=user.email,
            username=user.username,
            oauth_email=oauth_email,
            oauth_vendor=oauth_vendor,
            message=f'User `{user.username}` logged in using `{oauth_vendor}` account.',
            is_authenticated=True)
        return Response(response=oauth_response_info.serialize(), status=200, mimetype='application/json')
    elif (user := User.get_by_email(email=oauth_email)):
        oauth_user = OAuthUser(
            email=oauth_email,
            oauth_vendor=oauth_vendor,
            user_id=user.id)
        db.session.add(oauth_user)
        db.session.commit()
        login_user(user=user, remember=remember)
        oauth_response_info = OAuthResponseInfo(
            id=user.id,
            email=user.email,
            username=user.username,
            oauth_email=oauth_email,
            oauth_vendor=oauth_vendor,
            message=f'`New oauth account `{oauth_email}` logged in using `{oauth_vendor}` account, automatically bound to User `{user.username}`.',
            is_authenticated=True)
        return Response(response=oauth_response_info.serialize(), status=201, mimetype='application/json')
    else:
        user = User(email=oauth_email, password=str(uuid4())[:8], username=username)
        db.session.add(user)
        oauth_user = OAuthUser(email=oauth_email, oauth_vendor=oauth_vendor, user_id=user.id)
        db.session.add(oauth_user)
        db.session.commit()
        login_user(user=user, remember=remember)
        oauth_response_info = OAuthResponseInfo(
            id=user.id,
            email=user.email,
            username=username,
            oauth_email=oauth_email,
            oauth_vendor=oauth_vendor,
            message=f'`New oauth account `{oauth_email}` logged in using `{oauth_vendor}` account. Create new User `{username}`.',
            is_authenticated=True)
        return Response(response=oauth_response_info.serialize(), status=201, mimetype='application/json')

@auth.route('oauth/<oauth_vendor>/login', methods=['GET', 'POST'])
def oauth_vendor_login(oauth_vendor: str) -> Response:
    """Redirect to the OAuth Login Page of Vendor(s).

    Args:
        oauth_vendor: OAuth Vendor, e.g. `Google`, `Microsoft`, etc.
    """
    oauth_vendor = oauth_vendor.upper()
    oauth_client: WebApplicationClient = oauth_client_dict.get(oauth_vendor, None)
    provider_cfg: dict = provider_cfg_dict.get(oauth_vendor, None)

    if (oauth_client is None):
        response_info = OAuthResponseInfo(
            id=None,
            email=None,
            oauth_email=None,
            oauth_vendor=oauth_vendor,
            is_successful=False,
            message=f'OAuth vendor `{OAuthUser.camel_case_oauth_vendor(oauth_vendor)}` is not supported.',
        )
        return Response(response=response_info.serialize(), status=400, mimetype='application/json')

    authorization_endpoint = provider_cfg['authorization_endpoint']  # e.g. https://accounts.google.com/o/oauth2/v2/auth

    # Construct the request for Social login and retrieve user's profile.
    request_uri = oauth_client.prepare_request_uri(
        uri=authorization_endpoint,
        redirect_uri=request.base_url + '/callback',
        scope=['openid', 'email', 'profile'],
    )
    return redirect(request_uri)

@auth.route('oauth/<oauth_vendor>/login/callback', methods=['GET', 'POST'])
def oauth_vendor_login_callback(oauth_vendor: str) -> Response:
    """
    Callback Function of OAuth.
    Verify authorization code.
    TODO: This function is imperfect. It's better to have a dashboard or homepage for user to redirect to.
    TODO: Then, a redirect(301) response can be sent to redirect users to that page.

    Args:
        oauth_vendor: OAuth Vendor, e.g. `Google`, `Microsoft`, etc.
    """
    oauth_vendor = oauth_vendor.upper()
    oauth_client: WebApplicationClient = oauth_client_dict.get(oauth_vendor, None)
    provider_cfg: dict = provider_cfg_dict.get(oauth_vendor, None)

    if (oauth_client is None):
        response_info = OAuthResponseInfo(
            id=None,
            email=None,
            oauth_email=None,
            oauth_vendor=oauth_vendor,
            is_successful=False,
            message=f'OAuth vendor `{OAuthUser.camel_case_oauth_vendor(oauth_vendor)}` is not supported.',
        )
        return Response(
            response=response_info.serialize(),
            status=400, mimetype='application/json')

    # OAuth2 authorization code
    code = str()
    if (request.method == 'GET'):
        code = request.args.get('code', None)
    if (request.method == 'POST'):
        code = request.form.get('code', None)
    token_endpoint = provider_cfg["token_endpoint"]
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
            message=f'OAuth vendor {OAuthUser.camel_case_oauth_vendor(oauth_vendor)} caught an Invalid Grant Error.',
        )
        return Response(
            response=response_info.serialize(),
            status=400, mimetype='application/json')

    # Find and hit the URL from OAuth Vendor that provides the user's profile information.
    userinfo_endpoint = provider_cfg["userinfo_endpoint"]
    uri, headers, body = oauth_client.add_token(userinfo_endpoint)
    userinfo_response = get(uri, headers=headers, data=body)
    userinfo:dict = userinfo_response.json()

    # To make sure the email is verified.
    # The user authenticated with OAuth Vendor, authorized your app,
    # and now their email(s) is verified through OAuth Vendor(s).
    if not userinfo.get('email_verified'):
        oauth_response_info = OAuthResponseInfo(
            id=None,
            email=None,
            username=None,
            oauth_email=None,
            oauth_vendor=oauth_vendor,
            is_successful=False,
            message=f'User email is not available or not verified.',
            is_authenticated=False)
        return Response(
            response=oauth_response_info.serialize(),
            status=401, mimetype='application/json')
    
    unique_id = userinfo.get('sub')
    oauth_email = str(userinfo.get('email')).lower()
    picture = userinfo.get('picture')
    username = userinfo.get('name', None)

    remember = False
    response = __perform_oauth_login(
        oauth_email=oauth_email,
        oauth_vendor=oauth_vendor,
        username=username,
        remember=remember)
    return response
    # return redirect(f'/api/auth/profile', code=301)

@auth.route('oauth/unsafe/login', methods=['POST'])
def oauth_login_unsafe() -> Response:
    """This method is only to test if the application works properly after passing the social login.
    This method is for development mode only.
    This method cannot be used in production mode, where its router should be commented.
    """
    oauth_email = request.form.get('oauth_email').lower()
    # oauth_vendor = request.form.get('oauth_vendor')
    oauth_vendor = 'Unsafe'
    username = request.form.get('username', '')
    remember = bool(request.form.get('remember', False))
    response = __perform_oauth_login(
        oauth_email=oauth_email,
        oauth_vendor=oauth_vendor,
        username=username,
        remember=remember)
    return response
