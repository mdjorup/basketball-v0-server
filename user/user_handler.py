from typing import get_args

from firebase_admin.auth import UserRecord

from user.constants import UserRole


def create_user(auth, db, data: dict):
    #1) get the fields from the dictionary
    #2) 
    try:
        email : str = data["email"]
        password : str = data["password"]
        role_value : str = data.get("role", "standard")
        if role_value in get_args(UserRole):
            user : UserRecord = auth.create_user(email=email, password=password)
            auth.set_custom_user_claims(user.uid, {"role": role_value})
            db.collection("users").add({
                "email" : email,
                "password" : password,
                "role" : role_value
            })
        else:
            return {"error" : "Invalid role"}, 400
        
        return {"message": f"User {user.uid} with email {user.email} successfully created"}, 201
        
            
    except KeyError as ke:
        return {"error": f"Missing key: {ke}"}, 400
    except Exception as e:
        return {"error": f"Error: {e}"}, 500

    