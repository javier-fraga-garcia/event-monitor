import os
from typing import Annotated
from fastapi import APIRouter, Depends, BackgroundTasks, HTTPException
from google.cloud import bigquery
from auth.auth import get_token
from db.schema import Purchase
from db.crud import save_data, get_data

router = APIRouter(prefix='/api/purchase', tags=['Purchase'])

credentials = Annotated[str, Depends(get_token)]

def get_client():
    yield bigquery.Client()

db_dependency = Annotated[bigquery.Client, Depends(get_client)]

@router.get('/', response_model=list[Purchase])
async def get_purchase(client: db_dependency, auth: credentials):
    if auth != os.getenv('TOKEN_SECRET'):
        raise HTTPException(status_code=403, detail='Token not valid')
    
    purchases = get_data(client)
    if not purchases:
        raise HTTPException(status_code=404, detail='No data to query')
    return purchases
    

@router.post('/', response_model=Purchase)
async def save_purchase(auth: credentials, purchase: Purchase, client: db_dependency, backgroundTask: BackgroundTasks):
    if auth != os.getenv('TOKEN_SECRET'):
        raise HTTPException(status_code=403, detail='Token not valid')
    
    backgroundTask.add_task(save_data, client, purchase)
    return purchase
