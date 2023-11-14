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
from flask import Response, url_for, request
from flask_login import login_user, logout_user, login_required, current_user
from datetime import datetime

# Here put local imports.
from . import auth
from .models import User
from context import db, login_manager

class AuthResponseInfo():
    """Authentication Response Information.
        
    Attributes:
        id (str): User ID.
        email (str): User Email Address.
        is_successful (bool): A boolean value to show if a request have successfully achieved its purpose.
        message (str): The message to be sent.
        timestamp (str): For 'register', it is the time when the user is registered; otherwise it is the time when the operation is completed.  
        is_authenticated (bool): A boolean value to show if a user is authenticated. Set to `True` for login success, Set to `False` for login failure or logout.
    """

    def __init__(self,
            id: str,
            email: str,
            is_successful: bool = True,
            message: str = str(),
            timestamp = datetime.utcnow(),
            is_authenticated: bool = False,
            ) -> None:
        """Authentication Response Information.
        
        Args:
            id: User ID.
            email: User Email Address.
            is_successful: A boolean value to show if a request have successfully achieved its purpose.
            message: The message to be sent.
            timestamp: For 'register', it is the time when the user is registered; otherwise it is the time when the operation is completed.  
            is_authenticated: A boolean value to show if a user is authenticated. Set to `True` for login success, Set to `False` for login failure or logout.
        """
        self.id = id
        self.email = email
        self.is_successful = is_successful
        self.message = message
        self.timestamp = str(timestamp)
        self.is_authenticated = is_authenticated
        return

    def serialize(self) -> str:
        """Serialize the current instance to json string."""
        from json import dumps
        return dumps(self.__dict__)
    
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
    user = User(email=email, password=request.form.get('password'))

    if (User.query.filter_by(email=email).first()):
        response_info = AuthResponseInfo(
            id=None,
            email=email,
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
            message=f'New user `{user.email}` is created.',
            timestamp=user.registered_on)
        return Response(response=response_info.serialize(), status=201, mimetype='application/json')

@auth.route('/unregister', methods=['POST', 'DELETE'])
@login_required
def unregister() -> Response:
    """Unregister a Current User. Only the user him/herself is permitted to do so."""
    user = current_user
    email_to_match = request.form.get('email').lower()
    user_to_unregister = User.query.filter_by(email=email_to_match).first()
    if (not user_to_unregister):    # Email doesn't exist.
        response_info = AuthResponseInfo(
            id=user.id,
            email=user.email,
            is_successful=False,
            message=f'Target user `{email_to_match}` does not exist.',
            is_authenticated=True)
        return Response(response=response_info.serialize(), status=403, mimetype='application/json')
    if (user_to_unregister.id == user.id):  # User.id matched.
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
    email = request.form.get('email').lower()
    user = User.query.filter_by(email=email).first()
    if user and user.validate_password(request.form.get('password')):
        login_user(user)
        response_info = AuthResponseInfo(
            id=user.id,
            email=user.email,
            message=f'The user `{user.email}` logged in.',
            is_authenticated=True)
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
        is_authenticated=True)
    return Response(response=response_info.serialize(), status=200, mimetype='application/json')

@auth.route('/change-password', methods=['POST', 'PUT'])
@login_required
def change_password() -> Response:
    """Change password."""
    old_password = request.form.get('old_password')
    new_password = request.form.get('new_password')
    user = current_user
    if (user.validate_password(old_password)):
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
            message=f'User `{user.email}` failed to change the password due to unmatched old password.',
            is_authenticated=True,
        )
        return Response(response=response_info.serialize(), status=400, mimetype='application/json')
