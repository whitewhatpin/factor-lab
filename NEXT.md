# NEXT.md

## 当前进度

仓库骨架已搭建完成，包含：
- 目录结构（src/ashare_factor_lab/ 下 data / pit / factor / evaluation 四个模块）
- pyproject.toml（uv 管理，Python 3.11+，pandas + duckdb + tushare）
- .gitignore / .env.example / LICENSE (MIT)
- README.md 骨架
- ROADMAP.md（v0.1 全部任务拆分）
- pytest 冒烟测试通过

## 下一步

**任务 T1.1：合成数据生成器**

在 `src/ashare_factor_lab/data/synthetic.py` 实现 `make_daily_bars(ts_codes, start_date, end_date)` 函数：

1. 用 `numpy.random` 生成模拟日线行情（open / high / low / close / volume）
2. 随机标记涨跌停（±10% 或 ±20%，创业板/科创板）
3. 返回 pandas DataFrame，列为 `[ts_code, trade_date, open, high, low, close, volume, is_limit_up, is_limit_down]`

**验收标准**：
```python
from ashare_factor_lab.data.synthetic import make_daily_bars
df = make_daily_bars(['000001.SZ', '600519.SH'], '2024-01-01', '2024-12-31')
assert len(df) > 0
assert set(df.columns) == {'ts_code', 'trade_date', 'open', 'high', 'low', 'close', 'volume', 'is_limit_up', 'is_limit_down'}
```

**预估时间**: 60 分钟

## 待决策

- LICENSE 中的 Copyright 署名用什么名字？（当前占位为 whitewhatpin）
- Git commit 的 user.name / user.email 需要配置
