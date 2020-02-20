数据库属性与中文名对应
=====================

stock_basics
----------------
- code: 代码
- name: 名称
- industry: 所属行业
- area: 地区
- pe: 市盈率
- outstanding: 流通股本(亿)
- totals: 总股本(亿)
- totalAssets: 总资产(万)
- liquidAssets: 流动资产
- fixedAssets: 固定资产
- reserved: 公积金
- reservedPerShare: 每股公积金
- eps: 每股收益
- bvps: 每股净资
- pb: 市净率
- timeToMarket: 上市日期
- undp: 未分利润
- perundp:  每股未分配
- rev: 收入同比(%)
- profit: 利润同比(%)
- gpr: 毛利率(%)
- npr: 净利润率(%)
- holders: 股东人数


stock_hist
-----------------
- _id: 默认主键
- date: 日期
- open: 开盘价
- high: 最高价
- close: 收盘价
- low: 最低价
- volume: 成交量
- price_change: 价格变动
- p_change: 涨跌幅
- ma5: 5日均价
- ma10: 10日均价
- ma20: 20日均价
- v_ma5: 5日均量
- v_ma10: 10日均量
- v_ma20: 20日均量
- turnover: 换手率[注：指数无此项](实际上tushare.org接口未返回换手率)
