import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# 设置页面宽屏
st.set_page_config(page_title="大学专业投资回报率", layout="wide")

# 标题与说明
st.title("大学专业投资回报率仪表盘")
st.markdown("""
本仪表盘为**高中升学顾问**设计，旨在帮助评估不同专业和院校组合的长期经济投资回报。
""")

# 加载数据（使用 cache 提升性能）
@st.cache_data
def load_data():
    df = pd.read_csv("college_major_roi.csv")
    return df

df = load_data()

# --- 侧边栏筛选器 ---
st.sidebar.header("筛选条件")
major_cat = st.sidebar.multiselect("专业大类", options=df['major_category'].unique(), default=df['major_category'].unique())
inst_tier = st.sidebar.multiselect("院校等级", options=df['institution_tier'].unique(), default=df['institution_tier'].unique())
region = st.sidebar.multiselect("地区", options=df['region'].unique(), default=df['region'].unique())

# 过滤数据
filtered_df = df[
    (df['major_category'].isin(major_cat)) &
    (df['institution_tier'].isin(inst_tier)) &
    (df['region'].isin(region))
]

# --- 顶部 KPI 指标 ---
st.subheader("核心指标")
col1, col2, col3 = st.columns(3)

median_roi = filtered_df['net_roi_usd'].median()
positive_roi_rate = filtered_df['positive_roi'].mean() * 100
median_earnings = filtered_df['earnings_10yr_usd'].median()

with col1:
    st.metric("中位数净ROI", f"${median_roi:,.0f}")
with col2:
    st.metric("正向ROI占比", f"{positive_roi_rate:.1f}%")
with col3:
    st.metric("中位数10年总收入", f"${median_earnings:,.0f}")

# --- 中部图表 ---
st.subheader("专业大类与投资回报分析")

# 图表1：专业大类平均净ROI
fig1, ax1 = plt.subplots(figsize=(10, 4))
avg_roi = filtered_df.groupby('major_category')['net_roi_usd'].median().sort_values(ascending=False)
avg_roi.plot(kind='bar', ax=ax1, color='steelblue')
ax1.set_ylabel("中位数净ROI (USD)")
ax1.set_xlabel("专业大类")
plt.xticks(rotation=45)
st.pyplot(fig1)

# 图表2：成本与ROI散点图
fig2, ax2 = plt.subplots(figsize=(10, 4))
ax2.scatter(filtered_df['net_cost_usd'], filtered_df['net_roi_usd'], alpha=0.5, c='coral')
ax2.set_xlabel("净成本 (USD)")
ax2.set_ylabel("净ROI (USD)")
ax2.axhline(0, color='red', linestyle='--', linewidth=1) # 画出盈亏平衡线
st.pyplot(fig2)

# --- 底部数据与说明 ---
st.subheader("详细数据")
with st.expander("点击展开查看原始数据表"):
    st.dataframe(filtered_df)

st.caption("Data: Kaggle synthetic snapshot. Production refresh: annually. 数据为合成数据，仅用于趋势模拟，不代表具体个人真实未来收入。")