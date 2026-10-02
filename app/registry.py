import asyncio
from .models import ConnectorManifest
class Registry:
    def __init__(self): self._d={}; self._lock=asyncio.Lock()
    async def put(self,m:ConnectorManifest):
        async with self._lock:self._d[m.name]=m
    async def get(self,n): return self._d.get(n)
    async def list(self): return list(self._d.values())
registry=Registry()
