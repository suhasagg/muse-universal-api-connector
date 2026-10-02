import httpx, urllib.parse
from .models import ConnectorManifest, ToolDefinition
from .security import assert_safe_url
from .config import settings
class ApprovalRequired(Exception): pass
async def execute(manifest:ConnectorManifest, tool:ToolDefinition, args:dict, approved:bool=False, credential:dict|None=None):
    if tool.risk in {"write","destructive"} and not approved: raise ApprovalRequired(f"{tool.risk} operation requires explicit approval")
    url=manifest.base_url+tool.path
    path_args={p.name:args[p.name] for p in tool.parameters if p.location=="path" and p.name in args}
    for k,v in path_args.items(): url=url.replace("{"+k+"}",urllib.parse.quote(str(v),safe=""))
    assert_safe_url(url,settings.execution_allow_private_networks)
    query={p.name:args[p.name] for p in tool.parameters if p.location=="query" and p.name in args}
    headers={p.name:str(args[p.name]) for p in tool.parameters if p.location=="header" and p.name in args}
    if credential: headers.update(credential.get("headers",{})); query.update(credential.get("query",{}))
    body=args.get("body")
    async with httpx.AsyncClient(timeout=settings.request_timeout_seconds,follow_redirects=False) as client:
        r=await client.request(tool.method,url,params=query,headers=headers,json=body)
        ctype=r.headers.get("content-type","")
        payload=r.json() if "json" in ctype else r.text[:100000]
        return {"status":r.status_code,"headers":{"content-type":ctype},"body":payload}
