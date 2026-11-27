# mcp-fund-nav

一个面向 AI Agent 的 **MCP (Model Context Protocol) 服务器**：让 Claude / Qoder / Cline 等
支持 MCP 的客户端直接查询中国公募基金的实时估值、历史净值和基本信息。

## 为什么做这个
基金净值数据散落在各家网站上，Agent 很难直接调用。本项目把天天基金的公开接口
封装成标准的 MCP Tools，Agent 一行配置就能查净值、算持有收益。

## Tools
| Tool | 说明 |
|---|---|
| `get_fund_estimate(code)` | 单只基金实时估值（估算净值、估算涨幅、估值时间） |
| `get_fund_history(code, days)` | 最近 N 天单位净值历史 |
| `batch_estimate(codes)` | 批量查询多只基金估值，返回组合当日盈亏估算 |
| `search_fund(keyword)` | 按名称/代码搜索基金 |

## 快速开始
```bash
pip install .
# 或直接运行
python -m mcp_fund_nav
```

## MCP 客户端配置（Qoder / Claude / Cline 通用）
```json
{
  "mcpServers": {
    "fund-nav": {
      "command": "python",
      "args": ["-m", "mcp_fund_nav"]
    }
  }
}
```

## 数据与免责
数据来自天天基金公开接口，仅供个人学习与信息查询，不构成投资建议。
净值估算与实际公布净值可能有偏差，以基金公司公布为准。

## License
MIT
