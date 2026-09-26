import os
from fastapi import APIRouter 
from fastapi import Depends, HTTPException, status, Response, Path, Query, Request
from slowapi import Limiter
from sqlalchemy.orm import Session 
from database import get_db 
from repositories import ItemRepository 
from schemas import ItemCriacao, ItemAtualizacao, ItemResposta 
from models import Item
from authentication import verificar_chave
ambiente = os.getenv('ENVIRONMENT', 'dev')
def obter_ip_cliente(request: Request) -> str:
    if ambiente == 'prod':
        encaminhado = request.headers.get('X-Forwarded-For')
        if encaminhado:
            return encaminhado.split(',')[-1].strip()
    if request.client:
        return request.client.host
    return 'desconhecido'
limiter = Limiter(key_func=obter_ip_cliente, default_limits=['100/minute'], key_style='endpoint')
items_router = APIRouter(tags=['itens'])
@items_router.get('/itens/{id}', response_model = ItemResposta)
@limiter.limit('100/minute')
async def encontrar_por_id(request: Request, id: int = Path(gt=0), db: Session = Depends(get_db)):
    item = ItemRepository.encontrar_por_id(db, id)
    if not item:
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND, detail = 'Item não encontrado'
        ) 
    return ItemResposta.model_validate(item)
@items_router.put('/itens/{id}', response_model= ItemResposta)
@limiter.limit('10/minute')
async def atualizar(request: Request, requisicao: ItemAtualizacao, id: int = Path(gt=0), db: Session = Depends(get_db), chave: str = Depends(verificar_chave)):
    item_db = ItemRepository.encontrar_por_id(db, id)
    if not item_db:
        raise HTTPException(status_code=404, detail='Item não encontrado!')
    item_atualizado = ItemRepository.atualizar(db, item_db, requisicao.model_dump(exclude_unset=True))
    return item_atualizado
@items_router.get('/itens/', response_model= list[ItemResposta])
@limiter.limit('100/minute')
async def obter_todos(request: Request, db: Session = Depends(get_db), limite: int = Query(20, ge=1, le=100), deslocamento: int = Query(0, ge=0)):
    itens = ItemRepository.encontrar_todos(db, limite, deslocamento)
    return [ItemResposta.model_validate(item) for item in itens]
@items_router.delete('/itens/{id}', status_code=status.HTTP_204_NO_CONTENT)
@limiter.limit('10/minute')
async def deletar_por_id(request: Request, id: int = Path(gt=0), db: Session = Depends(get_db), chave: str = Depends(verificar_chave)):
    item_db = ItemRepository.encontrar_por_id(db, id)
    if not item_db:
        raise HTTPException(status_code=404, detail='Item não localizado')
    ItemRepository.deletar_por_id(db, id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
@items_router.post('/itens/', response_model= ItemResposta, status_code=status.HTTP_201_CREATED)
@limiter.limit('10/minute')
async def criar(request: Request, requisicao: ItemCriacao, db: Session = Depends(get_db), chave: str = Depends(verificar_chave)):
    item = ItemRepository.criar_item(db, Item(**requisicao.model_dump(exclude_unset=True)))
    return ItemResposta.model_validate(item)
