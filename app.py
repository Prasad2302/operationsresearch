import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

st.set_page_config(page_title="HAL Goal Programming Dashboard", page_icon="✈️", layout="wide")

GOALS = [{'goal': 'Total production', 'direction': '>=', 'target': 40, 'achieved': 40.59, 'deviation': 0, 'priority': 1}, {'goal': 'Total contribution', 'direction': '>=', 'target': 6000, 'achieved': 8083.9, 'deviation': 0, 'priority': 2}, {'goal': 'Labor usage', 'direction': '<=', 'target': 300, 'achieved': 232.13, 'deviation': 0, 'priority': 3}, {'goal': 'Machine usage', 'direction': '<=', 'target': 220, 'achieved': 191.54, 'deviation': 0, 'priority': 4}, {'goal': 'Material usage', 'direction': '<=', 'target': 330, 'achieved': 301.31, 'deviation': 0, 'priority': 5}]
PRODUCTS = [{'product': 'LCA Tejas Mk1A', 'production': 16, 'maximum': 20}, {'product': 'HTT-40', 'production': 0, 'maximum': 18}, {'product': 'ALH Dhruv', 'production': 12.59, 'maximum': 16}, {'product': 'LCH Prachand', 'production': 12, 'maximum': 14}]

gdf = pd.DataFrame(GOALS)
pdf = pd.DataFrame(PRODUCTS)

production = pdf["production"].sum()
contribution = gdf.loc[gdf["goal"]=="Total contribution","achieved"].iloc[0]
labor = gdf.loc[gdf["goal"]=="Labor usage","achieved"].iloc[0]
machine = gdf.loc[gdf["goal"]=="Machine usage","achieved"].iloc[0]
material = gdf.loc[gdf["goal"]=="Material usage","achieved"].iloc[0]
deviation = gdf["deviation"].sum()

st.title("✈️ HAL Defence Manufacturing")
st.subheader("Goal Programming Dashboard")
st.caption("Solver-based production planning | Goal achievement and resource utilization")

a,b,c,d,e = st.columns(5)
a.metric("Total Production", f"{production:.2f} units")
b.metric("Contribution", f"₹{contribution:,.2f} lakh")
c.metric("Total Deviation", f"{deviation:.2f}")
d.metric("Labor Usage", f"{labor:.2f}")
e.metric("Machine Usage", f"{machine:.2f}")

st.divider()

col1,col2 = st.columns(2)

with col1:
    st.markdown("### Target vs Achieved")
    fig = go.Figure()
    fig.add_bar(name="Target", x=gdf["goal"], y=gdf["target"])
    fig.add_bar(name="Achieved", x=gdf["goal"], y=gdf["achieved"])
    fig.update_layout(barmode="group", height=430, xaxis_title="", yaxis_title="Value",
                      margin=dict(l=10,r=10,t=20,b=90))
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown("### Production Mix")
    fig2 = px.bar(pdf, x="product", y="production", text="production",
                  hover_data=["maximum"])
    fig2.update_traces(texttemplate="%{text:.2f}", textposition="outside")
    fig2.update_layout(height=430, xaxis_title="", yaxis_title="Units",
                       margin=dict(l=10,r=10,t=20,b=90))
    st.plotly_chart(fig2, use_container_width=True)

st.markdown("### Goal Status")
view = gdf.copy()
view["Status"] = view["deviation"].apply(lambda x: "Achieved" if x == 0 else "Deviation")
view["Achievement %"] = (view["achieved"] / view["target"] * 100).round(2)
st.dataframe(view[["priority","goal","direction","target","achieved","deviation","Achievement %","Status"]],
             use_container_width=True, hide_index=True)

st.markdown("### Resource Utilization")
resources = pd.DataFrame({
    "Resource":["Labor","Machine","Material"],
    "Used":[labor,machine,material],
    "Limit":[300,220,330]
})
resources["Utilization %"] = resources["Used"] / resources["Limit"] * 100
st.dataframe(resources, use_container_width=True, hide_index=True)

if deviation == 0:
    st.success("All five stated goals are achieved with zero total deviation.")
else:
    st.warning(f"Total goal deviation: {deviation:.2f}")

with st.expander("Solver / Model Notes"):
    st.write(
        "Decision variables are aircraft production quantities. This dashboard uses the benchmark "
        "Goal Programming solution prepared in the Excel workbook. The original Goal Programming "
        "tab did not contain complete goal equations, so the displayed targets are explicitly "
        "documented modeling assumptions."
    )
