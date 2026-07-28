"""
投资组合模拟器 💼
功能：模拟不同资产配置的投资组合表现

运行方式：
1. 安装依赖：pip install streamlit pandas numpy plotly
2. 运行程序：streamlit run portfolio_simulator.py
3. 打开浏览器访问：http://localhost:8501
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# 页面配置
st.set_page_config(
    page_title="投资组合模拟器",
    page_icon="💼",
    layout="wide"
)

# 标题
st.title("💼 投资组合模拟器")
st.markdown("模拟不同资产配置的投资组合表现，找到最适合你的风险收益平衡点")
st.markdown("---")

# 资产类别
asset_classes = {
    '股票': {'return': 0.10, 'vol': 0.20, 'color': '#FF6B6B'},
    '债券': {'return': 0.04, 'vol': 0.05, 'color': '#4ECDC4'},
    '现金': {'return': 0.02, 'vol': 0.01, 'color': '#95E1D3'},
    '商品': {'return': 0.06, 'vol': 0.15, 'color': '#F38181'},
    'REITs': {'return': 0.08, 'vol': 0.12, 'color': '#AA96DA'},
}

# 侧边栏 - 资产配置
st.sidebar.header("⚖️ 资产配置")
st.sidebar.markdown("调整各类资产的配置比例（总和需为100%）")

weights = {}
total = 0
for asset in asset_classes.keys():
    w = st.sidebar.slider(
        f"{asset} 配置比例",
        0, 100, 20 if asset == '股票' else 0,
        key=asset
    )
    weights[asset] = w
    total += w

if total != 100:
    st.sidebar.error(f"⚠️ 当前配置总和为 {total}%，需要调整为 100%")
    st.warning(f"请调整资产配置，当前总和为 **{total}%**，需要为 **100%**")
    st.stop()
else:
    st.sidebar.success(f"✅ 配置总和为 {total}%")

# 投资参数
st.sidebar.markdown("---")
st.sidebar.header("📅 投资参数")
initial_investment = st.sidebar.number_input("初始投资金额（元）", value=100000, step=10000)
years = st.sidebar.slider("投资年限", 1, 30, 10)

# 计算投资组合指标
portfolio_return = sum(weights[asset] / 100 * asset_classes[asset]['return'] 
                       for asset in asset_classes)
portfolio_vol = np.sqrt(sum(
    (weights[asset] / 100) ** 2 * asset_classes[asset]['vol'] ** 2
    for asset in asset_classes
))

sharpe = (portfolio_return - 0.03) / portfolio_vol if portfolio_vol > 0 else 0

# 模拟投资路径
np.random.seed(42)
months = years * 12
daily_returns = np.random.normal(portfolio_return / 252, portfolio_vol / np.sqrt(252), months * 22)

# 计算净值曲线
nav = [initial_investment]
for r in daily_returns:
    nav.append(nav[-1] * (1 + r))

nav_df = pd.DataFrame({
    '日期': pd.date_range(start='2024-01-01', periods=len(nav), freq='D'),
    '组合净值': nav
})

# 显示核心指标
st.subheader("📊 投资组合概览")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("预期年化收益", f"{portfolio_return*100:.2f}%")
    
with col2:
    st.metric("预期年化波动", f"{portfolio_vol*100:.2f}%")
    
with col3:
    st.metric("夏普比率", f"{sharpe:.2f}")
    
with col4:
    final_value = nav[-1]
    total_return = (final_value / initial_investment - 1) * 100
    st.metric("预期终值", f"¥{final_value:,.0f}", f"{total_return:.1f}%")

st.markdown("---")

# 资产配置饼图
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("🥧 资产配置")
    pie_data = pd.DataFrame({
        '资产类别': list(weights.keys()),
        '配置比例': list(weights.values())
    })
    pie_data = pie_data[pie_data['配置比例'] > 0]
    
    fig_pie = px.pie(
        pie_data,
        values='配置比例',
        names='资产类别',
        color='资产类别',
        color_discrete_map={k: v['color'] for k, v in asset_classes.items()}
    )
    fig_pie.update_traces(textposition='inside', textinfo='percent+label')
    fig_pie.update_layout(height=400)
    st.plotly_chart(fig_pie, use_container_width=True)

with col2:
    st.subheader("📈 净值增长曲线")
    fig_nav = px.area(
        nav_df,
        x='日期',
        y='组合净值',
        title=f'{years}年投资组合净值走势'
    )
    fig_nav.update_layout(height=400, yaxis_title='组合净值（元）')
    st.plotly_chart(fig_nav, use_container_width=True)

# 收益分布
st.subheader("📊 收益分布分析")
col1, col2 = st.columns(2)

with col1:
    # 年度收益分布
    yearly_returns = []
    for year in range(years):
        start_idx = year * 252
        end_idx = (year + 1) * 252
        if end_idx < len(daily_returns):
            year_return = np.prod(1 + daily_returns[start_idx:end_idx]) - 1
            yearly_returns.append(year_return * 100)
    
    if yearly_returns:
        yearly_df = pd.DataFrame({
            '年份': [f'第{i+1}年' for i in range(len(yearly_returns))],
            '收益率(%)': yearly_returns
        })
        
        fig_bar = px.bar(
            yearly_df,
            x='年份',
            y='收益率(%)',
            color='收益率(%)',
            color_continuous_scale=['red', 'yellow', 'green'],
            title='年度收益率分布'
        )
        fig_bar.update_layout(height=350)
        st.plotly_chart(fig_bar, use_container_width=True)

with col2:
    # 月度收益热力图
    monthly_returns = []
    for month in range(min(years * 12, len(daily_returns) // 22)):
        start_idx = month * 22
        end_idx = (month + 1) * 22
        if end_idx < len(daily_returns):
            month_return = np.prod(1 + daily_returns[start_idx:end_idx]) - 1
            monthly_returns.append(month_return * 100)
    
    if monthly_returns:
        # 整理成热力图格式
        monthly_df = pd.DataFrame({
            '月份': [f'第{i//12+1}年{i%12+1}月' for i in range(len(monthly_returns))],
            '收益率(%)': monthly_returns
        })
        
        fig_heatmap = go.Figure(data=go.Heatmap(
            z=[monthly_returns],
            x=monthly_df['月份'],
            y=['月度收益'],
            colorscale='RdYlGn',
            text=[[f'{r:.1f}%' for r in monthly_returns]],
            texttemplate='%{text}',
            showscale=False
        ))
        fig_heatmap.update_layout(
            title='月度收益率热力图',
            height=350,
            xaxis_tickangle=-45
        )
        st.plotly_chart(fig_heatmap, use_container_width=True)

# 风险分析
st.markdown("---")
st.subheader("⚠️ 风险分析")

col1, col2, col3 = st.columns(3)

# 最大回撤
max_drawdown = 0
peak = nav[0]
for value in nav:
    if value > peak:
        peak = value
    drawdown = (peak - value) / peak
    if drawdown > max_drawdown:
        max_drawdown = drawdown

with col1:
    st.metric("最大回撤", f"{max_drawdown*100:.2f}%")
    st.caption("历史上最大的跌幅")

with col2:
    # 亏损概率
    loss_days = sum(1 for r in daily_returns if r < 0)
    loss_prob = loss_days / len(daily_returns) * 100
    st.metric("日亏损概率", f"{loss_prob:.1f}%")
    st.caption("任意一天亏损的概率")

with col3:
    # VaR (95%)
    var_95 = np.percentile(daily_returns, 5)
    var_amount = initial_investment * abs(var_95)
    st.metric("95% VaR", f"¥{var_amount:,.0f}")
    st.caption("95%概率下最大单日亏损")

# 投资建议
st.markdown("---")
st.subheader("💡 投资建议")

if portfolio_return > 0.08:
    st.success("🎯 这是一个**进取型**组合，适合长期投资、能承受较大波动的投资者")
elif portfolio_return > 0.05:
    st.info("🎯 这是一个**平衡型**组合，在风险和收益之间取得了较好的平衡")
else:
    st.warning("🎯 这是一个**保守型**组合，适合风险厌恶型投资者，但长期可能跑不赢通胀")

# 风险提示
st.markdown("""
**风险提示：**
- 本模拟基于历史数据和假设，不代表未来实际收益
- 投资有风险，入市需谨慎
- 建议根据个人风险承受能力和投资目标做出决策
- 定期调整资产配置，保持组合的平衡
""")

# 页脚
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #888; font-size: 12px;'>
投资组合模拟器 v1.0 | 数据仅供参考，不构成投资建议 | 
Made with ❤️ by 袁雅琪
</div>
""")
