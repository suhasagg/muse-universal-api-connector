import ipaddress, socket, urllib.parse, re
from fastapi import HTTPException
WRITE={"POST","PUT","PATCH"}; DESTRUCTIVE={"DELETE"}
def classify(method:str, operation_id:str="", desc:str=""):
    m=method.upper(); text=(operation_id+" "+desc).lower()
    if m in DESTRUCTIVE or re.search(r"delete|remove|revoke|terminate|cancel", text): return "destructive"
    if m in WRITE: return "write"
    return "read"
def assert_safe_url(url:str, allow_private:bool=False):
    p=urllib.parse.urlparse(url)
    if p.scheme not in {"https","http"}: raise HTTPException(400,"Only HTTP(S) targets are supported")
    if not p.hostname: raise HTTPException(400,"Missing target host")
    try:
        for x in socket.getaddrinfo(p.hostname,p.port or (443 if p.scheme=='https' else 80)):
            ip=ipaddress.ip_address(x[4][0])
            if not allow_private and (ip.is_private or ip.is_loopback or ip.is_link_local or ip.is_reserved):
                raise HTTPException(400,"Private/link-local target denied by SSRF policy")
    except socket.gaierror: raise HTTPException(400,"Target DNS resolution failed")
