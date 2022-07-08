'''
User creation and information
'''
from werkzeug.security import generate_password_hash
from sqlalchemy.orm import Session

from app.models.users import Users

def post_user(db_session:Session, username, password, name, email):
    '''
    doc
    '''
    # generate password hash
    pass_hash = generate_password_hash(password)

    # new user instance
    new_user = Users(username=username, password=pass_hash, name=name, email=email)

    # fazer query pro alchemy
    if query_user(username, db_session):
        return {'message': 'Username already exists'}, 400
    if query_email(email, db_session):
        return {'message': 'Email already exists'}, 400

    try:
        db_session.add(new_user)
        db_session.commit()
        db_session.refresh(new_user)
        result = new_user
        return {'message': 'User successfully registred', 'data': result}, 201
    except Exception:
        return {'message': 'unable to create', 'data': {}}, 500

def update_user(db_session:Session, user_id, username, password, name, email):
    '''
    doc
    '''
    updated_user = db_session.query(Users).get(user_id)

    if not updated_user:
        return {'message': 'user not found', 'data': {}}, 404
    if query_user(username, db_session):
        return {'message': 'Unable to update. Unavailable username'}, 400
    if query_email(email, db_session):
        return {'message': 'Unable to update. Unavailable e-mail'}, 400

    pass_hash = generate_password_hash(password)

    try:
        updated_user.username = username
        updated_user.password = pass_hash
        updated_user.name = name
        updated_user.email = email

        db_session.commit()

        result = {"username": updated_user.username, "password": updated_user.password,
                "name": updated_user.name, "email": updated_user.email}

        return {'message': 'User successfully updated', 'data': result}, 200

    except Exception:
        return {'message': 'Unable to update', 'data': {}}, 500

def delete_user(user_id, db_session):
    '''
       Delete a user according to a given id
    '''
    user = db_session.query(Users).get(user_id)

    if not user:
        return {'message': 'User not found', 'data': {}}, 404

    if user:
        try:
            db_session.delete(user)
            db_session.commit()

            result = {"username": user.username, "password": user.password,
                    "name": user.name, "email": user.email}

            return {'message': 'User successifully deleted', 'data': result}, 200

        except Exception:
            return {'message': 'Unable to delete', 'data': {}}, 500

    return {'message': 'Unable to delete', 'data': {}}, 500

def get_users(db_session:Session):
    '''
       List information about all available users on database
    '''
    users = db_session.query(Users).all()
    if users:
        result = users
        return {'message': 'Successfully feched', 'data': result}, 200

    return {'message': 'Unable to get data', 'data': {}}, 500

def get_user(user_id, db_session:Session):
    '''
       List information about a specific user according to a given id
    '''
    user = db_session.query(Users).get(user_id)

    if not user:
        return {'message': 'User not found', 'data': {}}, 404

    if user:
        result = {"username": user.username, "password": user.password,
                "name": user.name, "email": user.email}

        return {'message': 'Successfully feched', 'data': result}, 200

    return {'message': 'Unable to get data', 'data': {}}, 500

def query_user(username, db_session:Session):
    '''
       Verify the user exists on database according to the given username
    '''
    try:
        return db_session.query(Users).filter(Users.username == username).one()
    except Exception:
        return None

def query_email(email, db_session:Session):
    '''
       Verify the e-mail exists on database according to the given e-mail
    '''
    try:
        return db_session.query(Users).filter(Users.email == email).one()
    except Exception:
        return None
