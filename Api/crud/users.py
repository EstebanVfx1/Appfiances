import sys

from Api.models.user import User
from fastapi import HTTPException
from Api.schemas.users import UserCreate, UserRead, UserDelete
from sqlalchemy.orm import Session
from core.security import get_hashed_password, verify_password
from core.utils import generate_user_id

def create_new_user(user: UserCreate,user_role: str,db:Session):
    db_user = User(
        user_id=generate_user_id(),
        full_name=user.full_name,
        mail=user.mail,
        passhash=get_hashed_password(user.passhash),
        user_role=user_role,
        user_status=user.user_status
    )

    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except Exception as e:
        db.rollback()
        print(f"Error al crear el usuario: {str(e)}",_file=sys.stderr)
        raise HTTPException(status_code=500, detail="Error al crear el usuario: {str(e)}")

def get_user_by_email(email:str,db:Session):
    user = db.query(User).filter(User.mail==email).first()
    return user

def get_user_by_id(user_id:str,db:Session):
    user = db.query(User).filter(User.user_id==user_id).first()
    return user

def authenticate_user(username:str, password:str,db:Session):
    user = get_user_by_email(username,db)
    if not user:
        return False
    if not verify_password(password, user.passhash):
        return False
    return user

# ================== BLOCK TO VERIFY ROLE ================== 
def checkRole(currentrole:str, current_user: str, user_id:str): 
    if currentrole == "admin" or current_user == user_id:
        return True
    else:
        return False
# ==========================================================

# ================ BLOCK TO VERIFY STATUS ==================
def checkStatus(status:str):
    if status:
        return True
    else:
        return False
# ==========================================================

# ================== BLOCK TO UPDATE USER ==================
def update_user(user: UserRead, db: Session):
    db_user = get_user_by_id(user.user_id, db)
    if db_user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    for key, value in vars(user).items():
        if key == "user_role":
            if db_user.user_role == "user" and value == "admin":
                raise HTTPException(status_code=400, detail="No se puede actualizar el rol de usuario a 'admin'")
        if value is not None:
            setattr(db_user, key, value)
    db.commit()
    db.refresh(db_user)
    return db_user
# ==========================================================

# ================== BLOCK TO DELETE USER ==================
def delete_user(user_id: UserDelete, db: Session):
    print("user_id",user_id)
    db_user = get_user_by_id(user_id.user_id, db)
    print("db_user",db_user)
    if db_user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    db_user.user_status = 0
    db.commit()
    db.refresh(db_user)
    return db_user
    