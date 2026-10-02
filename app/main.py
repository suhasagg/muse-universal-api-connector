from fastapi import FastAPI,HTTPException,Header
from .models import BuildRequest,ExecuteRequest
from .compiler import compile_openapi
from .registry import registry
from .executor import execute,ApprovalRequired
app=FastAPI(title="Muse Universal API Connector Builder",version="1.0.0")
@app.get("/healthz")
async def health():return {"ok":True}
@app.post("/v1/connectors",status_code=201)
async def build(req:BuildRequest):
    try:m=compile_openapi(req.spec,req.connector_name,req.base_url_override)
    except ValueError as e:raise HTTPException(422,str(e))
    await registry.put(m); return m
@app.get("/v1/connectors")
async def ls():return await registry.list()
@app.get("/v1/connectors/{name}")
async def get(name:str):
    m=await registry.get(name)
    if not m:raise HTTPException(404,"connector not found")
    return m
@app.post("/v1/connectors/{name}/tools/{tool_name}:execute")
async def run(name:str,tool_name:str,req:ExecuteRequest):
    m=await registry.get(name)
    if not m:raise HTTPException(404,"connector not found")
    tool=next((x for x in m.tools if x.name==tool_name),None)
    if not tool:raise HTTPException(404,"tool not found")
    try:return await execute(m,tool,req.arguments,req.approved)
    except ApprovalRequired as e:raise HTTPException(409,{"code":"APPROVAL_REQUIRED","message":str(e)})
