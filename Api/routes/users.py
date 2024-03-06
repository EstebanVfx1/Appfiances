from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.orm import Session
from db.connection import get_session
from Api.schemas.users import UserCreate, UserRead, Token, UserDelete
from Api.crud.users import create_new_user, get_user_by_email, get_user_by_id, authenticate_user, checkRole, update_user, checkStatus, delete_user
from core.security import create_access_token, verify_token

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_session)):
    user = await verify_token(token)
    if user is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    user_db = get_user_by_id(user, db)
    if user_db is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user_db

@router.post("/create-user/", response_model=UserRead)
async def create_user(user: UserCreate, db: Session = Depends(get_session)):
    verify_user = get_user_by_email(user.mail, db)
    print(verify_user)
    if verify_user is not None:
        raise HTTPException(status_code=404, detail="email already exists")
    return create_new_user(user,'user', db)

@router.post("/create-admin/", response_model=UserRead)
async def create_admin(user: UserCreate, current_user: UserRead = Depends(get_current_user), db: Session = Depends(get_session)):
    if current_user.user_role == "admin":
        verify_user = get_user_by_email(user.mail, db)
        if verify_user is None:
            created_admin = create_new_user(user,'admin', db=db)
            return created_admin
        else:
            raise HTTPException(status_code=404, detail="Email already exists")
    raise HTTPException(status_code=401, detail="Unauthorized user")


#Ruta para el inicio de sesión
@router.post("/login", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_session)):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid username or password", headers={"WWW-Authenticate": "Bearer"})
    access_token = create_access_token(data={"sub": user.user_id})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/get/{user_id}", response_model=UserRead)
def read_user(user_id:str, db: Session = Depends(get_session), current_user: UserRead = Depends(get_current_user)):
    if current_user.user_role == "admin" or current_user.user_id == user_id:
        user = get_user_by_id(user_id, db)
        if user is  None:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    else:
        raise HTTPException(status_code=401, detail="Unauthorized user") 
    

# ========================= BLOCK UPDATE USER =========================
@router.put("/update/", response_model=UserRead)
async def func_update_user(user: UserRead, db: Session = Depends(get_session), current_user: UserRead = Depends(get_current_user)):
    if not checkStatus(current_user.user_status):
        raise HTTPException(status_code=400, detail="Invalid status")
    checkMail = get_user_by_email(user.mail, db)
    if checkMail is not None and checkMail.mail == current_user.mail:
        raise HTTPException(status_code=400, detail="You are updating your own email address to the one you already have.")
    if checkMail is not None:
        raise HTTPException(status_code=400, detail="Email already exists")
    if not checkRole(current_user.user_role, current_user.user_id, user.user_id):
        raise HTTPException(status_code=401, detail="Unauthorized user")
    return update_user(user, db)
# =====================================================================

# ========================= BLOCK DELETE USER =========================
@router.delete("/delete/", response_model=UserRead)
async def func_delete_user(user:UserDelete,db: Session = Depends(get_session),current_user: UserRead = Depends(get_current_user)):
    if not checkStatus(current_user.user_status):
        raise HTTPException(status_code=400, detail="Invalid status")
    if not checkRole(current_user.user_role, current_user.user_id, user.user_id):
        raise HTTPException(status_code=401, detail="Unauthorized user")
    return delete_user(user, db)
# =====================================================================