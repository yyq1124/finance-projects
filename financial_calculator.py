"""
财务指标计算器 🧮
功能：输入财报数据，自动计算各种财务指标

运行方式：
1. 安装依赖：pip install streamlit pandas numpy
2. 运行程序：streamlit run financial_calculator.py
3. 打开浏览器访问：http://localhost:8501
"""

import streamlit as st
import pandas as pd
import numpy as np

# 页面配置
st.set_page_config(
    page_title="财务指标计算器",
    page_icon="🧮",
    layout="wide"
)

# 标题
st.title("🧮 财务指标计算器")
st.markdown("输入财务报表数据，自动计算各类财务指标，快速分析企业经营状况")
st.markdown("---")

# 侧边栏 - 输入财报数据
st.sidebar.header("📊 输入财务数据")

st.sidebar.subheader("资产负债表（单位：万元）")
total_assets = st.sidebar.number_input("总资产", value=100000, step=1000)
total_liabilities = st.sidebar.number_input("总负债", value=40000, step=1000)
shareholders_equity = st.sidebar.number_input("股东权益", value=60000, step=1000)
current_assets = st.sidebar.number_input("流动资产", value=50000, step=1000)
current_liabilities = st.sidebar.number_input("流动负债", value=30000, step=1000)
inventory = st.sidebar.number_input("存货", value=15000, step=1000)

st.sidebar.subheader("利润表（单位：万元）")
revenue = st.sidebar.number_input("营业收入", value=200000, step=10000)
cost_of_goods_sold = st.sidebar.number_input("营业成本", value=140000, step=10000)
gross_profit = revenue - cost_of_goods_sold
operating_profit = st.sidebar.number_input("营业利润", value=30000, step=5000)
net_profit = st.sidebar.number_input("净利润", value=25000, step=5000)

st.sidebar.subheader("现金流量表（单位：万元）")
operating_cash_flow = st.sidebar.number_input("经营活动现金流", value=35000, step=5000)

# 计算财务指标
st.subheader("📈 盈利能力指标")

col1, col2, col3, col4 = st.columns(4)

with col1:
    gross_margin = gross_profit / revenue * 100
    st.metric("毛利率", f"{gross_margin:.2f}%")
    if gross_margin > 40:
        st.caption("✅ 优秀")
    elif gross_margin > 20:
        st.caption("⚠️ 一般")
    else:
        st.caption("⚠️ 偏低")

with col2:
    operating_margin = operating_profit / revenue * 100
    st.metric("营业利润率", f"{operating_margin:.2f}%")
    if operating_margin > 15:
        st.caption("✅ 优秀")
    elif operating_margin > 8:
        st.caption("⚠️ 一般")
    else:
        st.caption("⚠️ 偏低")

with col3:
    net_margin = net_profit / revenue * 100
    st.metric("净利率", f"{net_margin:.2f}%")
    if net_margin > 10:
        st.caption("✅ 优秀")
    elif net_margin > 5:
        st.caption("⚠️ 一般")
    else:
        st.caption("⚠️ 偏低")

with col4:
    roe = net_profit / shareholders_equity * 100
    st.metric("ROE", f"{roe:.2f}%")
    if roe > 15:
        st.caption("✅ 优秀")
    elif roe > 10:
        st.caption("⚠️ 一般")
    else:
        st.caption("⚠️ 偏低")

st.markdown("---")

# 偿债能力指标
st.subheader("💰 偿债能力指标")

col1, col2, col3, col4 = st.columns(4)

with col1:
    current_ratio = current_assets / current_liabilities
    st.metric("流动比率", f"{current_ratio:.2f}")
    if 1.5 <= current_ratio <= 3:
        st.caption("✅ 健康")
    elif current_ratio > 3:
        st.caption("⚠️ 资金利用效率低")
    else:
        st.caption("⚠️ 短期偿债压力大")

with col2:
    quick_ratio = (current_assets - inventory) / current_liabilities
    st.metric("速动比率", f"{quick_ratio:.2f}")
    if quick_ratio >= 1:
        st.caption("✅ 良好")
    else:
        st.caption("⚠️ 偏低")

with col3:
    debt_ratio = total_liabilities / total_assets * 100
    st.metric("资产负债率", f"{debt_ratio:.2f}%")
    if debt_ratio < 50:
        st.caption("✅ 保守")
    elif debt_ratio < 70:
        st.caption("⚠️ 适中")
    else:
        st.caption("⚠️ 风险较高")

with col4:
    equity_multiplier = total_assets / shareholders_equity
    st.metric("权益乘数", f"{equity_multiplier:.2f}")
    st.caption("财务杠杆水平")

st.markdown("---")

# 运营能力指标
st.subheader("🔄 运营能力指标")

col1, col2, col3, col4 = st.columns(4)

with col1:
    asset_turnover = revenue / total_assets
    st.metric("总资产周转率", f"{asset_turnover:.2f}次")
    if asset_turnover > 1:
        st.caption("✅ 高效")
    else:
        st.caption("⚠️ 有提升空间")

with col2:
    inventory_turnover = cost_of_goods_sold / inventory
    inventory_days = 365 / inventory_turnover if inventory_turnover > 0 else 0
    st.metric("存货周转率", f"{inventory_turnover:.2f}次")
    st.caption(f"存货周转天数：{inventory_days:.0f}天")

with col3:
    receivable_turnover = revenue / (current_assets * 0.3)  # 假设应收账款占流动资产30%
    receivable_days = 365 / receivable_turnover if receivable_turnover > 0 else 0
    st.metric("应收账款周转率", f"{receivable_turnover:.2f}次")
    st.caption(f"应收账款周转天数：{receivable_days:.0f}天")

with col4:
    roa = net_profit / total_assets * 100
    st.metric("ROA", f"{roa:.2f}%")
    if roa > 5:
        st.caption("✅ 良好")
    else:
        st.caption("⚠️ 偏低")

st.markdown("---")

# 杜邦分析
st.subheader("🎯 杜邦分析")

st.markdown("""
**ROE = 净利率 × 总资产周转率 × 权益乘数**
""")

col1, col2, col3, col4 = st.columns([1, 1, 1, 0.5])

with col1:
    st.metric("ROE", f"{roe:.2f}%")

with col2:
    st.metric("=", f"{net_margin:.2f}%")
    st.caption("净利率")

with col3:
    st.metric("×", f"{asset_turnover:.2f}")
    st.caption("总资产周转率")

with col4:
    st.metric("×", f"{equity_multiplier:.2f}")
    st.caption("权益乘数")

# 验证杜邦分析
dupont_roe = net_margin / 100 * asset_turnover * equity_multiplier * 100
st.info(f"杜邦分析计算结果：{dupont_roe:.2f}% （误差：{abs(roe - dupont_roe):.2f}%）")

st.markdown("---")

# 现金流分析
st.subheader("💵 现金流分析")

col1, col2, col3 = st.columns(3)

with col1:
    cash_flow_ratio = operating_cash_flow / current_liabilities
    st.metric("现金流比率", f"{cash_flow_ratio:.2f}")
    if cash_flow_ratio > 1:
        st.caption("✅ 现金流充足")
    else:
        st.caption("⚠️ 现金流紧张")

with col2:
    cash_flow_to_revenue = operating_cash_flow / revenue * 100
    st.metric("现金流/营收", f"{cash_flow_to_revenue:.2f}%")
    if cash_flow_to_revenue > 15:
        st.caption("✅ 良好")
    else:
        st.caption("⚠️ 有改善空间")

with col3:
    cash_flow_to_profit = operating_cash_flow / net_profit if net_profit > 0 else 0
    st.metric("现金流/净利润", f"{cash_flow_to_profit:.2f}")
    if cash_flow_to_profit > 1:
        st.caption("✅ 盈利质量高")
    else:
        st.caption("⚠️ 盈利质量需关注")

st.markdown("---")

# 综合评价
st.subheader("📋 综合评价")

# 评分系统
score = 0
comments = []

# 盈利能力（30分）
if gross_margin > 40:
    score += 10
    comments.append("✅ 毛利率优秀")
elif gross_margin > 20:
    score += 5
    comments.append("⚠️ 毛利率一般")

if roe > 15:
    score += 10
    comments.append("✅ ROE优秀")
elif roe > 10:
    score += 5
    comments.append("⚠️ ROE一般")

if net_margin > 10:
    score += 10
    comments.append("✅ 净利率优秀")
elif net_margin > 5:
    score += 5
    comments.append("⚠️ 净利率一般")

# 偿债能力（30分）
if 1.5 <= current_ratio <= 3:
    score += 10
    comments.append("✅ 流动比率健康")
else:
    score += 5
    comments.append("⚠️ 流动比率需关注")

if debt_ratio < 50:
    score += 10
    comments.append("✅ 负债水平保守")
elif debt_ratio < 70:
    score += 5
    comments.append("⚠️ 负债水平适中")

if quick_ratio >= 1:
    score += 10
    comments.append("✅ 速动比率良好")
else:
    score += 5
    comments.append("⚠️ 速动比率偏低")

# 运营能力（20分）
if asset_turnover > 1:
    score += 10
    comments.append("✅ 资产周转高效")
else:
    score += 5
    comments.append("⚠️ 资产周转有提升空间")

if cash_flow_ratio > 1:
    score += 10
    comments.append("✅ 现金流充足")
else:
    score += 5
    comments.append("⚠️ 现金流紧张")

# 现金流质量（20分）
if cash_flow_to_profit > 1:
    score += 10
    comments.append("✅ 盈利质量高")
else:
    score += 5
    comments.append("⚠️ 盈利质量需关注")

if cash_flow_to_revenue > 15:
    score += 10
    comments.append("✅ 现金流/营收良好")
else:
    score += 5
    comments.append("⚠️ 现金流/营收有改善空间")

# 显示评分
st.markdown(f"### 综合评分：{score}/100")

if score >= 80:
    st.success("🏆 **优秀** - 企业经营状况良好")
elif score >= 60:
    st.info("👍 **良好** - 企业经营状况稳健")
elif score >= 40:
    st.warning("⚠️ **一般** - 部分指标需要改善")
else:
    st.error("❌ **较差** - 需要重点关注和改善")

# 显示评价详情
st.markdown("**详细评价：**")
for comment in comments:
    st.markdown(f"- {comment}")

# 页脚
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #888; font-size: 12px;'>
财务指标计算器 v1.0 | 数据仅供参考，不构成投资建议 | 
Made with ❤️ by 袁雅琪
</div>
""")
