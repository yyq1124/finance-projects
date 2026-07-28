# 🧮 财务指标计算器

输入财务报表数据，自动计算各类财务指标，快速分析企业经营状况。

![Python](https://img.shields.io/badge/Python-3.8+-blue?logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red?logo=streamlit)

## ✨ 功能特点

- 📈 **盈利能力指标**：毛利率、营业利润率、净利率、ROE
- 💰 **偿债能力指标**：流动比率、速动比率、资产负债率、权益乘数
- 🔄 **运营能力指标**：总资产周转率、存货周转率、应收账款周转率、ROA
- 🎯 **杜邦分析**：ROE分解为三个驱动因素
- 💵 **现金流分析**：现金流比率、现金流/营收、现金流/净利润
- 📋 **综合评价**：100分制评分系统

## 🚀 快速开始

```bash
pip install -r requirements.txt
streamlit run financial_calculator.py
```

## 📝 指标说明

### 盈利能力
- **毛利率** = (营收-成本) / 营收
- **ROE** = 净利润 / 股东权益
- **净利率** = 净利润 / 营收

### 偿债能力
- **流动比率** = 流动资产 / 流动负债
- **速动比率** = (流动资产-存货) / 流动负债
- **资产负债率** = 总负债 / 总资产

### 杜邦分析
**ROE = 净利率 × 总资产周转率 × 权益乘数**

---

Made with ❤️ by 袁雅琪
