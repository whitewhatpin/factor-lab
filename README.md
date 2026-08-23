# ashare-factor-lab

A 股因子研究脚手架——正确处理 point-in-time 的因子研究基础设施。

> **免责声明：本项目仅供研究与教学使用，不构成任何投资建议。**

## 解决什么问题

中文世界里缺少一个干净、可复现、正确处理了 A 股特有陷阱的因子研究脚手架。

大多数因子研究代码在以下地方埋着隐性错误：

- 用前复权价格做滚动计算，引入了未来信息
- 财报数据按报告期对齐，而不是按实际公告日
- 回测里包含了已退市/停牌股票，产生幸存者偏差
- 涨跌停当日假设可以成交，高估了策略容量
- 新股上市首日就纳入选股池，忽略了上市初期的异常波动
- 成分股名单用最新名单回测历史，而不是历史时点的真实名单

这个框架的目标是让"用到未来信息"这件事变得困难，甚至不可能。

## 与现有方案的差异

| | ashare-factor-lab | backtrader | vectorbt | qlib |
|---|---|---|---|---|
| 定位 | 因子研究基础设施 | 策略回测框架 | 向量化回测引擎 | AI 量化平台 |
| A 股 PIT 处理 | 一等公民 | 需手动处理 | 需手动处理 | 部分内置 |
| 财报公告日对齐 | 内置 | 不支持 | 不支持 | 支持但需配置 |
| 选股池时点化 | 内置 | 不支持 | 不支持 | 部分支持 |
| 依赖复杂度 | 精简 | 精简 | 中等 | 重型 |
| 学习曲线 | 低 | 中 | 中 | 高 |

backtrader / vectorbt 是优秀的通用回测工具，但它们不处理 A 股特有的数据陷阱。qlib 功能强大但引入了完整的 ML 流水线，对于只想做干净因子研究的人来说过重。

## 快速开始

```bash
# 克隆
git clone https://github.com/whitewhatpin/ashare-factor-lab.git
cd ashare-factor-lab

# 安装依赖
uv sync

# 配置数据源
cp .env.example .env
# 编辑 .env，填入你的 Tushare token

# 下载数据（可选，也可以用合成数据跑测试）
python scripts/download_data.py

# 跑测试
pytest

# 跑一个端到端 demo
python examples/01_momentum_demo.py
```

## 文档导航

| 内容 | 位置 |
|---|---|
| 当前进度与下一步 | `NEXT.md` |
| v0.1 任务拆分 | `ROADMAP.md` |
| A 股数据陷阱详解 | `docs/pitfalls/` |
| 架构决策记录 | `docs/adr/` |

## License

[MIT](LICENSE)
