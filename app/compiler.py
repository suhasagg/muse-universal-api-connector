import hashlib, json, re
from typing import Any
from .models import ConnectorManifest, ToolDefinition, ToolParameter
from .security import classify
def _name(method,path,op):
    raw=op or f"{method}_{path}"
    return re.sub(r"[^a-zA-Z0-9_]","_",raw).strip("_")[:96]
def compile_openapi(spec:dict[str,Any], connector_name:str, base_override:str|None=None)->ConnectorManifest:
    if not str(spec.get("openapi","")).startswith("3."): raise ValueError("OpenAPI 3.x required")
    servers=spec.get("servers") or []
    base=base_override or (servers[0].get("url") if servers else "")
    if not base: raise ValueError("No server URL; provide base_url_override")
    tools=[]
    for path,item in (spec.get("paths") or {}).items():
        inherited=item.get("parameters",[]) if isinstance(item,dict) else []
        for method,op in item.items():
            if method.lower() not in {"get","post","put","patch","delete","head","options"} or not isinstance(op,dict): continue
            params=[]
            for p in inherited+op.get("parameters",[]):
                if "$ref" in p: continue # production resolver is isolated extension point; unresolved refs are rejected at validation in strict mode
                params.append(ToolParameter(name=p["name"],location=p.get("in","query"),required=p.get("required",False),schema=p.get("schema",{})))
            tools.append(ToolDefinition(name=_name(method,path,op.get("operationId")),method=method.upper(),path=path,description=op.get("summary") or op.get("description","")[:500],risk=classify(method,op.get("operationId", ""),op.get("description","")),parameters=params,request_body=op.get("requestBody"),security=op.get("security",spec.get("security",[]))))
    canonical=json.dumps(spec,sort_keys=True,separators=(",",":")).encode()
    return ConnectorManifest(name=connector_name,base_url=base.rstrip("/"),tools=tools,security_schemes=((spec.get("components") or {}).get("securitySchemes") or {}),spec_hash=hashlib.sha256(canonical).hexdigest())
