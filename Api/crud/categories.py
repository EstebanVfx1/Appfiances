import sys

from Api.models.category import Category
from fastapi import HTTPException
from Api.schemas.categories import CategoryCreate, CategoryRead, CategoryDelete
from sqlalchemy.orm import Session

# ================== BLOCK TO GET CATEGORIE BY NAME ==================
def get_categorie_by_name (name:str,db:Session):
    categorie = db.query(Category).filter(Category.category_name==name).first()
    return categorie
# ==========================================================

# ================== BLOCK TO CREATE NEW CATEGORIE ==================
def create_new_categorie(categorie: CategoryCreate,db:Session):
    db_categorie = Category(
        category_name=categorie.category_name,
        category_description=categorie.category_description,
        category_status=categorie.category_status
    )

    try:
        db.add(db_categorie)
        db.commit()
        db.refresh(db_categorie)
        return db_categorie
    except Exception as e:
        db.rollback()
        print(f"Error al crear la categoría: {str(e)}",_file=sys.stderr)
        raise HTTPException(status_code=500, detail="Error al crear la categoría: {str(e)}")
# ==========================================================

# ================== BLOCK TO VERIFY ROLE ==================
def checkRoleForCategorie(currentrole:str): 
    if currentrole == "admin":
        return True
    else:
        return False
# ==========================================================
    
# ================== BLOCK TO GET CATEGORIE BY ID ==================
def get_categorie_by_id (id:int,db:Session):
    categorie = db.query(Category).filter(Category.category_id==id).first()
    return categorie
# ==========================================================

# ================== BLOCK TO UPDATE CATEGORIE ==================
def update_categorie(categorie: CategoryRead,db:Session):
    db_categorie = get_categorie_by_id(categorie.category_id,db)
    if db_categorie is None:
        raise HTTPException(status_code=404, detail="Category not found")
    for key, value in vars(categorie).items():
        if value is not None:
            setattr(db_categorie, key, value)
    try:
        db.commit()
        db.refresh(db_categorie)
        return db_categorie
    except Exception as e:
        db.rollback()
        print(f"Error al actualizar la categoría: {str(e)}",_file=sys.stderr)
        raise HTTPException(status_code=500, detail="Error al actualizar la categoría: {str(e)}")
# ==========================================================
    
# ================== BLOCK TO DELETE CATEGORIE ==================
def delete_categorie(id:CategoryDelete,db:Session):
    db_categorie = get_categorie_by_id(id.category_id,db)
    if db_categorie is None:
        raise HTTPException(status_code=404, detail="Category not found")
    try:
        db_categorie.category_status = 0
        db.commit()
        db.refresh(db_categorie)
        return db_categorie
    except Exception as e:
        db.rollback()
        print(f"Error al eliminar la categoría: {str(e)}",_file=sys.stderr)
        raise HTTPException(status_code=500, detail="Error al eliminar la categoría: {str(e)}")
# ==========================================================