# app/routers/tools.py
from fastapi import APIRouter, HTTPException
from app.crud.tool import get_tools, create_tool
from app.schemas.tool import ToolCreate, Tool  # Подключаем нужные схемы

router = APIRouter()

@router.get("/tools", response_model=list[Tool])
async def get_tools_list():
    try:
        tools = get_tools()  # Эта функция должна быть в вашем CRUD файле
        return tools
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/tools", response_model=Tool)
async def add_tool(tool: ToolCreate):
    try:
        return create_tool(tool)  # Эта функция должна быть в вашем CRUD файле
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
