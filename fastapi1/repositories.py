from sqlalchemy.orm import Session 
from models import Item 
class ItemRepository:
    @staticmethod 
    def encontrar_por_id(db: Session, id: int) -> Item:
        return db.query(Item).filter(Item.id == id).first()
    @staticmethod
    def atualizar(db:Session, item_db: Item, dados_novos: dict) -> Item:
        for chave, valor, in dados_novos.items():
            setattr(item_db, chave, valor)
        db.commit()
        db.refresh(item_db)
        return item_db
    @staticmethod 
    def criar_item(db: Session, item:Item) -> Item:
        db.add(item) 
        db.commit()
        return item
    @staticmethod
    def encontrar_todos(db: Session, limite: int, deslocamento: int) -> list[Item]:
        return db.query(Item).limit(limite).offset(deslocamento).all()
    @staticmethod
    def deletar_por_id(db: Session, id: int) -> None:
        item = db.query(Item).filter(Item.id == id).first()
        if item is not None:
            db.delete(item)
            db.commit()
 