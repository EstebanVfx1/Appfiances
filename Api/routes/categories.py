from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from db.connection import get_session
from Api.schemas.categories import CategoryCreate, CategoryRead, CategoryDelete
from Api.schemas.users import UserRead
from Api.crud.users import checkStatus
from Api.crud.categories import create_new_categorie, get_categorie_by_name, checkRoleForCategorie, update_categorie, delete_categorie
from Api.routes.users import get_current_user

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")

# ================== BLOCK TO CREATE NEW CATEGORIE ==================
@router.post("/create-categorie/", response_model=CategoryRead)
async def create_categorie(categorie: CategoryCreate, current_user: UserRead = Depends(get_current_user) , db: Session = Depends(get_session)):
    if not checkStatus(current_user.user_status):
        raise HTTPException(status_code=400, detail="Invalid status")
    if not checkRoleForCategorie(current_user.user_role):
        raise HTTPException(status_code=401, detail="Unauthorized user")
    if not get_categorie_by_name(categorie.category_name, db):
        return create_new_categorie(categorie, db)
    raise HTTPException(status_code=404, detail="Category already exists")
# ==========================================================

# ================== BLOCK TO GET CATEGORIE BY NAME ==================
@router.post("/get-categorie/", response_model=CategoryRead)
async def get_categorie(name:str, current_user: UserRead = Depends(get_current_user) , db: Session = Depends(get_session)):
    if not checkStatus(current_user.user_status):
        raise HTTPException(status_code=400, detail="Invalid status")
    if not checkRoleForCategorie(current_user.user_role):
        raise HTTPException(status_code=401, detail="Unauthorized user")
    categorie = get_categorie_by_name(name, db)
    if categorie:
        return categorie
    raise HTTPException(status_code=404, detail="Category not found")
# ==========================================================

# ================== BLOCK TO UPDATE CATEGORIE ==================
@router.put("/update-categorie/", response_model=CategoryRead)
async def def_dupdate_categorie(categorie: CategoryRead, current_user: UserRead = Depends(get_current_user) , db: Session = Depends(get_session)):
    if not checkStatus(current_user.user_status):
        raise HTTPException(status_code=400, detail="Invalid status")
    if not checkRoleForCategorie(current_user.user_role):
        raise HTTPException(status_code=401, detail="Unauthorized user")
    if not get_categorie_by_name(categorie.category_name, db):
        raise HTTPException(status_code=404, detail="Category not found")
    return update_categorie(categorie, db)
# ==========================================================

# ================== BLOCK TO DELETE CATEGORIE ==================
@router.delete("/delete-categorie/", response_model=CategoryRead)
async def def_delete_categorie(categorie: CategoryDelete, current_user: UserRead = Depends(get_current_user) , db: Session = Depends(get_session)):
    if not checkStatus(current_user.user_status):
        raise HTTPException(status_code=400, detail="Invalid status")
    if not checkRoleForCategorie(current_user.user_role):
        raise HTTPException(status_code=401, detail="Unauthorized user")
    return delete_categorie(categorie, db)
# ==========================================================



    