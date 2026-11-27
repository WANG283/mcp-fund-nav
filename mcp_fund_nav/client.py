"""天天基金公开接口客户端。接口为公开 JSONP/JSON，无需密钥。"""
import json, re
import httpx

HEADERS = {"User-Agent": "Mozilla/5.0 mcp-fund-nav/0.1", "Referer": "https://fund.eastmoney.com/"}

async def fetch_estimate(code: str) -> dict:
    """实时估值: https://fundgz.1234567.com.cn/js/{code}.js"""
    url = f"https://fundgz.1234567.com.cn/js/{code}.js"
    async with httpx.AsyncClient(timeout=10, headers=HEADERS) as c:
        r = await c.get(url)
    m = re.search(r"jsonpgz\((.*)\)", r.text, re.S)
    if not m:
        raise ValueError(f"no estimate data for {code}")
    d = json.loads(m.group(1))
    return {"code": d["fundcode"], "name": d["name"], "nav_date": d.get("jzrq"),
            "unit_nav": float(d["dwjz"]), "estimate_nav": float(d["gsz"]),
            "estimate_change_pct": float(d["gszzl"]), "estimate_time": d.get("gztime")}

async def fetch_history(code: str, days: int = 30) -> list:
    url = "https://api.fund.eastmoney.com/f10/lsjz"
    params = {"fundCode": code, "pageIndex": 1, "pageSize": days}
    headers = {**HEADERS, "Referer": f"https://fund.eastmoney.com/f10/jjjz_{code}.html"}
    async with httpx.AsyncClient(timeout=10, headers=headers) as c:
        r = await c.get(url, params=params)
    rows = r.json()["Data"]["LSJZList"]
    return [{"date": x["FSRQ"], "unit_nav": float(x["DWJZ"]),
             "change_pct": x["JZZZL"]} for x in rows]

async def search(keyword: str) -> list:
    url = "https://fundsuggest.eastmoney.com/FundSearch/api/FundSearchAPI.ashx"
    async with httpx.AsyncClient(timeout=10, headers=HEADERS) as c:
        r = await c.get(url, params={"m": 1, "key": keyword})
    return [{"code": x["CODE"], "name": x["NAME"], "type": x.get("FundBaseInfo", {}).get("FTYPE", "")}
            for x in r.json().get("Datas", [])[:10]]
