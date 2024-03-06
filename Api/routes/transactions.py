from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from db.connection import get_session
from Api.schemas.transactions import TransactionCreate, TransactionRead, TransactionUpdate, TransactionDelete
from Api.schemas.users import UserRead
from Api.crud.users import checkStatus
from Api.crud.transactions import create_new_transaction, update_transaction, delete_transaction, get_transaction_by_id
from Api.crud.categories import checkRoleForCategorie
from Api.routes.users import get_current_user

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")

# ================== BLOCK TO CREATE NEW TRANSACTION ==================
@router.post("/create-transaction/", response_model=TransactionRead)
async def create_transaction(transaction: TransactionCreate, current_user: UserRead = Depends(get_current_user) , db: Session = Depends(get_session)):
    if not checkStatus(current_user.user_status):
        raise HTTPException(status_code=400, detail="Invalid status")
    if not checkRoleForCategorie(current_user.user_role):
        raise HTTPException(status_code=401, detail="Unauthorized user")
    return create_new_transaction(transaction, db)
# ==========================================================

# ================== BLOCK TO GET TRANSACTION BY ID ==================
@router.post("/get-transaction/", response_model=TransactionRead)
async def get_transaction(id:int, current_user: UserRead = Depends(get_current_user) , db: Session = Depends(get_session)):
    if not checkStatus(current_user.user_status):
        raise HTTPException(status_code=400, detail="Invalid status")
    if not checkRoleForCategorie(current_user.user_role):
        raise HTTPException(status_code=401, detail="Unauthorized user")
    transaction = get_transaction_by_id(id, db)
    if transaction:
        return transaction
    raise HTTPException(status_code=404, detail="Transaction not found")
# ==========================================================

# ================== BLOCK TO UPDATE TRANSACTION ==================
@router.put("/update-transaction/", response_model=TransactionRead)
async def def_dupdate_transaction(transaction: TransactionUpdate, current_user: UserRead = Depends(get_current_user) , db: Session = Depends(get_session)):
    if not checkStatus(current_user.user_status):
        raise HTTPException(status_code=400, detail="Invalid status")
    if not checkRoleForCategorie(current_user.user_role):
        raise HTTPException(status_code=401, detail="Unauthorized user")
    return update_transaction(transaction, db)
# ==========================================================

# ================== BLOCK TO DELETE TRANSACTION ==================
@router.delete("/delete-transaction/", response_model=TransactionRead)
async def def_delete_transaction(transaction: TransactionDelete, current_user: UserRead = Depends(get_current_user) , db: Session = Depends(get_session)):
    if not checkStatus(current_user.user_status):
        raise HTTPException(status_code=400, detail="Invalid status")
    if not checkRoleForCategorie(current_user.user_role):
        raise HTTPException(status_code=401, detail="Unauthorized user")
    return delete_transaction(transaction, db)
# ==========================================================