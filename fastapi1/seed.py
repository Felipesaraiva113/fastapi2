import os
from pathlib import Path
from dotenv import load_dotenv
load_dotenv(Path(__file__).resolve().parent.parent / '.env', override=True)
from database import SessionLocal 
from models import Item 
from repositories import ItemRepository 
seed_habilitado = os.getenv('SEED_ENABLED', 'false').lower() == 'true'
if not seed_habilitado:
    raise SystemExit('seed desabilitado (SEED_ENABLED diferente de true)')
db = SessionLocal()
item = Item(nome='Intel Core i7 3400', preco=500, em_oferta=True) 
ItemRepository.criar_item(db, item)
db.close()
