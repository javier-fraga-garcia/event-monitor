from fastapi import Request, HTTPException

async def get_token(req: Request) -> str:
    token = req.headers.get('x-token')
    if not token:
        raise HTTPException(status_code=403, detail='Not Authorized')
    return token