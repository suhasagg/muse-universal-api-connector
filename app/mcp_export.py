from .models import ConnectorManifest
def to_mcp_tools(m:ConnectorManifest):
    out=[]
    for t in m.tools:
        props={}; required=[]
        for p in t.parameters:
            props[p.name]=p.schema_; required += [p.name] if p.required else []
        if t.request_body: props["body"]={"type":"object"}
        out.append({"name":t.name,"description":f"[{t.risk.upper()}] {t.description}","inputSchema":{"type":"object","properties":props,"required":required}})
    return out
