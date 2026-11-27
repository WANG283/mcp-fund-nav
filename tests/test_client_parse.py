import re, json
def test_jsonpgz_parse():
    sample = 'jsonpgz({"fundcode":"022431","name":"test","jzrq":"2026-11-26","dwjz":"1.0000","gsz":"1.0100","gszzl":"1.00","gztime":"2026-11-27 11:30"});'
    m = re.search(r"jsonpgz\((.*)\)", sample, re.S)
    d = json.loads(m.group(1))
    assert d["fundcode"] == "022431" and float(d["gsz"]) == 1.01
