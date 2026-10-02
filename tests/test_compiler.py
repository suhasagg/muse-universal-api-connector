from app.compiler import compile_openapi
def test_compile_and_risk():
 s={"openapi":"3.1.0","servers":[{"url":"https://api.example.com"}],"paths":{"/users/{id}":{"get":{"operationId":"getUser","parameters":[{"name":"id","in":"path","required":True,"schema":{"type":"string"}}]},"delete":{"operationId":"deleteUser"}}}}
 m=compile_openapi(s,"demo")
 assert len(m.tools)==2
 assert next(x for x in m.tools if x.name=="deleteUser").risk=="destructive"
 assert next(x for x in m.tools if x.name=="getUser").risk=="read"
