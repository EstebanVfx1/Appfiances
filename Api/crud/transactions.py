import sys
from fastapi import HTTPException
from sqlalchemy.orm import Session
from Api.models.transaction import Transaction
from Api.schemas.transactions import TransactionCreate, TransactionRead, TransactionUpdate, TransactionDelete

# ================== BLOQUE PARA CREAR UNA NUEVA TRANSACCIÓN ==================
def create_new_transaction(transaction: TransactionCreate, db: Session):
    try:
        db_transaction = Transaction(
            user_id=transaction.user_id,
            category_id=transaction.category_id,
            amount=transaction.amount,
            t_description=transaction.t_description,
            t_type=transaction.t_type
        )
        db.add(db_transaction)
        db.commit()
        db.refresh(db_transaction)
        return db_transaction
    except Exception as e:
        db.rollback()
        error_msg = f"Error al crear la transacción: {str(e)}"
        print(error_msg, file=sys.stderr)
        raise HTTPException(status_code=500, detail=error_msg)
# =============================================================================

# ================== BLOQUE PARA OBTENER UNA TRANSACCIÓN POR ID ==================
def get_transaction_by_id(id: int   , db: Session):
    transaction = db.query(Transaction).filter(Transaction.transactions_id == id).first()
    return transaction
# =============================================================================

# ================== BLOQUE PARA ACTUALIZAR UNA TRANSACCIÓN ==================
def update_transaction(transaction: TransactionUpdate, db: Session):
    db_transaction = get_transaction_by_id(transaction.transactions_id, db)
    if db_transaction is None:
        raise HTTPException(status_code=404, detail="Transaction not found")
    for key, value in vars(transaction).items():
        if value is not None:
            setattr(db_transaction, key, value)
    try:
        db.commit()
        db.refresh(db_transaction)
        return db_transaction
    except Exception as e:
        db.rollback()
        error_msg = f"Error al actualizar la transacción: {str(e)}"
        print(error_msg, file=sys.stderr)
        raise HTTPException(status_code=500, detail=error_msg)
# =============================================================================
    
# ================== BLOQUE PARA ELIMINAR UNA TRANSACCIÓN ==================
def delete_transaction(transaction: TransactionDelete, db: Session):
    db_transaction = get_transaction_by_id(transaction.transactions_id, db)
    if db_transaction is None:
        raise HTTPException(status_code=404, detail="Transaction not found")
    db.delete(db_transaction)
    try:
        db.commit()
        return db_transaction
    except Exception as e:
        db.rollback()
        error_msg = f"Error al eliminar la transacción: {str(e)}"
        print(error_msg, file=sys.stderr)
        raise HTTPException(status_code=500, detail=error_msg)
# =============================================================================
    
# ================== BOCK TO GET CATEGORIE BY ID ==================
def get_categorie_by_id (id:int,db:Session):
    categorie = db.query(Transaction).filter(Transaction.category_id==id).first()
    return categorie
# =============================================================================