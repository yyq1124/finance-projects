"""
基金对比分析器 📊
功能：对比多只基金的历史表现、风险收益特征

运行方式：
1. 安装依赖：pip install streamlit pandas numpy plotly
2. 运行程序：streamlit run fund_analyzer.py
3. 打开浏览器访问：http://localhost:8501
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

# 页面配置
st.set_page_config(
    page_title="基金对比分析器",
    page_icon="📊",
    layout="wide"
)

# 标题
st.title("📊 基金对比分析器")
st.markdown("对比多只基金的历史表现、风险收益特征，帮你做出更明智的投资决策")
st.markdown("---")

# 生成模拟数据（实际使用时可以接入真实API）
def generate_fund_data(fund_name, fund_type, annual_return, volatility):
    """生成基金历史数据"""
    np.random.seed(hash(fund_name) % 2**32)
    dates = pd.date_range(start='2020-01-01', end='2025-12-31', freq='D')
    
    # 生成每日收益率
    daily_return = annual_return / 252
    daily_vol = volatility / np.sqrt(252)
    
    returns = np.random.normal(daily_return, daily_vol, len(dates))
    
    # 计算累计净值
    nav = (1 + returns).cumprod()
    
    # 添加一些趋势
    if fund_type == '股票型':
        nav = nav * (1 + np.linspace(0, 0.3, len(dates)))
    elif fund_type == '债券型':
        nav = nav * (1 + np.linspace(0, 0.05, len(dates)))
    else:
        nav = nav * (1 + np.linspace(0, 0.15, len(dates)))
    
    df = pd.DataFrame({
        '日期': dates,
        '基金名称': fund_name,
        '基金类型': fund_type,
        '单位净值': nav,
        '日收益率': returns
    })
    
    return df

# 预设基金数据
fund_presets = {
    '易方达蓝筹精选': {'type': '股票型', 'return': 0.15, 'vol': 0.25},
    '招商中证白酒': {'type': '股票型', 'return': 0.12, 'vol': 0.30},
    '天弘沪深300': {'type': '混合型', 'return': 0.10, 'vol': 0.20},
    '易方达裕丰回报': {'type': '债券型', 'return': 0.05, 'vol': 0.05},
    '广发稳健增长': {'type': '混合型', 'return': 0.08, 'vol': 0.15},
    '南方中证500': {'type': '股票型', 'return': 0.11, 'vol': 0.28},
}

# 侧边栏 - 选择基金
st.sidebar.header("🔍 选择基金")
selected_funds = st.sidebar.multiselect(
    "选择要对比的基金（最多5只）",
    list(fund_presets.keys()),
    default=['易方达蓝筹精选', '天弘沪深300', '易方达裕丰回报']
)

if len(selected_funds) > 5:
    st.sidebar.error("最多只能选择5只基金进行对比")
    selected_funds = selected_funds[:5]

# 生成数据
all_data = []
for fund_name in selected_funds:
    preset = fund_presets[fund_name]
    df = generate_fund_data(fund_name, preset['type'], preset['return'], preset['vol'])
    all_data.append(df)

if not all_data:
    st.warning("请至少选择一只基金")
    st.stop()

# 合并数据
df_all = pd.concat(all_data, ignore_index=True)

# 计算指标
def calculate_metrics(df, fund_name):
    fund_df = df[df['基金名称'] == fund_name]
    returns = fund_df['日收益率'].dropna()
    
    total_return = (fund_df['单位净值'].iloc[-1] / fund_df['单位净值'].iloc[0] - 1) * 100
    annual_return = returns.mean() * 252 * 100
    volatility = returns.std() * np.sqrt(252) * 100
    sharpe = (returns.mean() * 252 - 0.03) / (returns.std() * np.sqrt(252))  # 无风险利率3%
    max_drawdown = ((fund_df['单位净值'] / fund_df['单位净值'].cummax()) - 1).min() * 100
    
    return {
        '基金名称': fund_name,
        '基金类型': fund_df['基金类型'].iloc[0],
        '累计收益率(%)': round(total_return, 2),
        '年化收益率(%)': round(annual_return, 2),
        '年化波动率(%)': round(volatility, 2),
        '夏普比率': round(sharpe, 2),
        '最大回撤(%)': round(max_drawdown, 2)
    }

metrics_list = [calculate_metrics(df_all, fund) for fund in selected_funds]
df_metrics = pd.DataFrame(metrics_list)

# 显示指标表格
st.subheader("📈 核心指标对比")
st.dataframe(
    df_metrics.style.highlight_max(color='lightgreen', subset=['累计收益率(%)', '年化收益率(%)', '夏普比率'])
              .highlight_min(color='lightcoral', subset=['年化波动率(%)', '最大回撤(%)']),
    use_container_width=True
)

st.markdown("---")

# 图表区域
col1, col2 = st.columns(2)

with col1:
    # 净值走势
    st.subheader("📉 净值走势对比")
    fig_nav = px.line(
        df_all,
        x='日期',
        y='单位净值',
        color='基金名称',
        title='基金净值走势',
        labels={'单位净值': '净值', '日期': ''}
    )
    fig_nav.update_layout(height=400, hovermode='x unified')
    st.plotly_chart(fig_nav, use_container_width=True)

with col2:
    # 收益-风险散点图
    st.subheader("🎯 收益-风险分布")
    fig_scatter = px.scatter(
        df_metrics,
        x='年化波动率(%)',
        y='年化收益率(%)',
        size='夏普比率',
        color='基金类型',
        text='基金名称',
        title='收益-风险分布（气泡大小=夏普比率）'
    )
    fig_scatter.update_traces(textposition='top center')
    fig_scatter.update_layout(height=400)
    st.plotly_chart(fig_scatter, use_container_width=True)

# 回撤分析
st.subheader("📉 回撤分析")
fig_drawdown = go.Figure()

for fund_name in selected_funds:
    fund_df = df_all[df_all['基金名称'] == fund_name]
    drawdown = (fund_df['单位净值'] / fund_df['单位净值'].cummax() - 1) * 100
    fig_drawdown.add_trace(go.Scatter(
        x=fund_df['日期'],
        y=drawdown,
        name=fund_name,
        fill='tozeroy'
    ))

fig_drawdown.update_layout(
    title='历史回撤走势',
    yaxis_title='回撤(%)',
    height=350,
    hovermode='x unified'
)
st.plotly_chart(fig_drawdown, use_container_width=True)

# 收益率分布
st.subheader("📊 日收益率分布")
fig_hist = px.histogram(
    df_all,
    x='日收益率',
    color='基金名称',
    marginal='box',
    nbins=50,
    title='日收益率分布',
    barmode='overlay'
)
fig_hist.update_layout(height=350)
st.plotly_chart(fig_hist, use_container_width=True)

# 投资建议
st.markdown("---")
st.subheader("💡 投资分析建议")

best_return_fund = df_metrics.loc[df_metrics['累计收益率(%)'].idxmax(), '基金名称']
best_sharpe_fund = df_metrics.loc[df_metrics['夏普比率'].idxmax(), '基金名称']
lowest_risk_fund = df_metrics.loc[df_metrics['最大回撤(%)'].idxmax(), '基金名称']

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("🏆 收益冠军", best_return_fund)
    
with col2:
    st.metric("🎯 风险收益比最优", best_sharpe_fund)
    
with col3:
    st.metric("🛡️ 最大回撤最小", lowest_risk_fund)

# 页脚
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #888; font-size: 12px;'>
基金对比分析器 v1.0 | 数据仅供参考，投资有风险，入市需谨慎 | 
Made with ❤️ by 袁雅琪
</div>
""")
