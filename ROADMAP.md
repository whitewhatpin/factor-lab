# ROADMAP.md — v0.1 任务拆分

每个任务预估 ≤ 90 分钟，可独立 commit，不破坏主干。

---

## Phase 0: 仓库骨架（已完成）

- [x] 目录结构 + pyproject.toml + .gitignore + .env.example + LICENSE
- [x] README.md 骨架
- [x] 空的包结构 + pytest 冒烟测试

---

## Phase 1: 数据层（4 个任务）

### T1.1 合成数据生成器
**前置**: 无
**产出**: `src/ashare_factor_lab/data/synthetic.py`
**验收**: `python -c "from ashare_factor_lab.data.synthetic import make_daily_bars; df = make_daily_bars(['000001.SZ'], '2024-01-01', '2024-12-31'); assert len(df) > 0"` 通过
**内容**: 生成合成日线行情数据（OHLCV + 涨跌停标记），用于测试，不依赖 Tushare

### T1.2 DuckDB 表结构定义
**前置**: T1.1
**产出**: `src/ashare_factor_lab/data/schema.py`
**验收**: `pytest tests/test_data/test_schema.py` 通过——建表后插入合成数据再读出，字段一致
**内容**: 定义 trade_calendar / daily_bar / income_statement / stock_status 四张表的 DDL

### T1.3 Tushare 增量落地（行情 + 日历）
**前置**: T1.2
**产出**: `src/ashare_factor_lab/data/loader.py`
**验收**: 用合成数据 mock Tushare API，重复执行两次 `load_daily_bars()` 结果一致（幂等）
**内容**: Tushare → DuckDB 的增量更新逻辑，只拉新增交易日

### T1.4 财务数据落地（按公告日）
**前置**: T1.2
**产出**: `src/ashare_factor_lab/data/loader.py` 补 `load_income_statements()`
**验收**: 财务数据包含 `ann_date` 字段，测试验证不会用到公告日之前的数据
**内容**: 利润表按公告日落地，而非报告期

---

## Phase 2: PIT 层（4 个任务）

### T2.1 交易日历查询
**前置**: T1.2
**产出**: `src/ashare_factor_lab/pit/calendar.py`
**验收**: `get_trade_dates('2024-01-01', '2024-12-31')` 返回正确交易日列表，排除周末和节假日
**内容**: 封装交易日历查询，所有时间相关操作统一走这里

### T2.2 复权方式显式选择
**前置**: T1.1
**产出**: `src/ashare_factor_lab/pit/adjust.py`
**验收**: `get_price(ts_code, date, adjust='none')` 返回不复权价格；`adjust='qfq'` 时抛出 `NotImplementedError` 并说明前复权陷阱
**内容**: 复权方式必须显式声明，默认不复权。前复权在滚动研究中的陷阱写入注释

### T2.3 时点化选股池
**前置**: T2.2
**产出**: `src/ashare_factor_lab/pit/universe.py`
**验收**: `get_universe('2024-06-01')` 排除：停牌、退市、ST、上市未满 N 日的新股。用合成数据构造边界 case 验证
**内容**: 给定日期返回当日可用股票池，处理停牌/退市/ST/新股

### T2.4 涨跌停交易约束
**前置**: T2.2
**产出**: `src/ashare_factor_lab/pit/adjust.py` 补 `is_tradeable()`
**验收**: 涨停日 `is_tradeable()` 返回 False，测试验证分层回测在涨停日不建仓
**内容**: 涨跌停当日不可成交的约束判断

---

## Phase 3: 因子层（3 个任务）

### T3.1 声明式因子接口
**前置**: T2.3
**产出**: `src/ashare_factor_lab/factor/base.py`
**验收**: 定义一个 `Factor` 抽象基类，子类声明 `inputs`（需要哪些字段）、`window`（回看窗口）、`compute()` 方法。PIT 层可以在编译期检查 inputs 是否包含未来数据
**内容**: 声明式因子定义接口

### T3.2 预处理管线
**前置**: T3.1
**产出**: `src/ashare_factor_lab/factor/preprocess.py`
**验收**: `winsorize()` 去极值、`zscore()` 标准化、`neutralize()` 市值与行业中性化，各有独立测试
**内容**: 横截面去极值 / 标准化 / 中性化

### T3.3 因子计算管线
**前置**: T3.1, T3.2
**产出**: `src/ashare_factor_lab/factor/pipeline.py`
**验收**: 给定一个 Factor 子类和日期范围，输出每日横截面因子值 DataFrame，经过 PIT 层过滤
**内容**: 串起 PIT 数据 + 因子逻辑 + 预处理的完整管线

---

## Phase 4: 评估层（3 个任务）

### T4.1 IC / ICIR
**前置**: T3.3
**产出**: `src/ashare_factor_lab/evaluation/ic.py`
**验收**: 用合成数据构造已知 IC 的因子，验证计算结果与手工计算一致
**内容**: IC / ICIR / Rank IC 计算

### T4.2 分层回测
**前置**: T4.1
**产出**: `src/ashare_factor_lab/evaluation/quantile.py`
**验收**: 分 5 层回测，验证多空组合收益 = Q5 - Q1，换手率在合理范围
**内容**: 分层回测 + 换手率

### T4.3 图表报告
**前置**: T4.2
**产出**: `src/ashare_factor_lab/evaluation/report.py`
**验收**: 生成 IC 时序图 + 分层净值图 + 换手率图，输出为 PNG
**内容**: 基础图表报告生成

---

## Phase 5: 端到端 Demo（3 个任务）

### T5.1 动量因子 Demo
**前置**: T3.3, T4.3
**产出**: `src/ashare_factor_lab/factor/library/momentum.py` + `examples/01_momentum_demo.py`
**验收**: `python examples/01_momentum_demo.py` 跑通，输出 IC 报告和分层回测图
**内容**: 20 日动量因子端到端 demo

### T5.2 市值因子 Demo
**前置**: T5.1
**产出**: `src/ashare_factor_lab/factor/library/size.py` + `examples/02_size_demo.py`
**验收**: 同上
**内容**: 市值因子端到端 demo

### T5.3 估值因子 Demo
**前置**: T5.1
**产出**: `src/ashare_factor_lab/factor/library/valuation.py` + `examples/03_valuation_demo.py`
**验收**: 同上，验证财报数据按公告日对齐
**内容**: EP（ earnings / price）估值因子端到端 demo

---

## Phase 6: 文档（2 个任务）

### T6.1 陷阱文档
**前置**: Phase 2 完成
**产出**: `docs/pitfalls/` 下 6 篇文档
**验收**: 每篇文档包含：陷阱描述、错误示例、正确做法、不这么做会产生什么样的虚假高收益
**内容**: 复权陷阱 / 公告日对齐 / 幸存者偏差 / 涨跌停 / 新股 / 成分股名单

### T6.2 ADR
**前置**: 无
**产出**: `docs/adr/0001-tech-stack.md`
**验收**: 记录技术选型理由（Python 3.11+ / DuckDB / Pandas / Tushare / pytest / uv）
**内容**: 架构决策记录

---

## 明确不做（v0.1 范围外）

- 实盘对接
- 订单管理
- 机器学习模型
- Web UI
- 成分股名单历史还原（需要额外数据源，记入 v0.2）
