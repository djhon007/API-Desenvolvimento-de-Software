from fastapi.responses import JSONResponse
from fastapi.requests import Request


async def tratar_excecoes(request: Request, exc: Exception):
    return JSONResponse(
        status_code=400,
        content={"erro": str(exc)}
    )
