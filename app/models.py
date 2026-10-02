from pydantic import BaseModel, Field
from typing import Any, Literal
class BuildRequest(BaseModel):
    spec: dict[str,Any]
    connector_name:str=Field(min_length=2,max_length=80,pattern=r"^[a-zA-Z0-9_-]+$")
    base_url_override:str|None=None
class ToolParameter(BaseModel):
    name:str; location:str; required:bool=False; schema_:dict[str,Any]=Field(default_factory=dict,alias="schema")
class ToolDefinition(BaseModel):
    name:str; method:str; path:str; description:str=""; risk:Literal["read","write","destructive"]="read"
    parameters:list[ToolParameter]=[]; request_body:dict[str,Any]|None=None; security:list[dict[str,list[str]]]=[]
class ConnectorManifest(BaseModel):
    name:str; version:str="1.0.0"; base_url:str; tools:list[ToolDefinition]; security_schemes:dict[str,Any]={}; spec_hash:str
class ExecuteRequest(BaseModel):
    arguments:dict[str,Any]={}; credential_ref:str|None=None; approved:bool=False
