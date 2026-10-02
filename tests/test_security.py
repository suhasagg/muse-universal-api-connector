from app.security import classify
def test_risk():
 assert classify("GET")=="read"
 assert classify("POST")=="write"
 assert classify("DELETE")=="destructive"
