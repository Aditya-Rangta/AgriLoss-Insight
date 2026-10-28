"""AgriLoss Insight: Apple Supply Chain Loss Pattern Analyzer (Himachal Pradesh)
Run: streamlit run app.py"""
import os
import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px
import streamlit as st
from sklearn.tree import plot_tree

import mining

st.set_page_config(page_title="AgriLoss Insight", page_icon="🍎", layout="wide")
st.title("🍎 AgriLoss Insight")
st.caption("Apple Supply Chain Loss Pattern Analyzer: Himachal Pradesh")


@st.cache_data
def get_data(uploaded):
    if uploaded is not None:
        return pd.read_csv(uploaded)
    if not os.path.exists("apple_supply_chain.csv"):
        import generate_data  # noqa: F401  (creates the csv)
    return mining.load()


up = st.sidebar.file_uploader("Upload your own CSV (same columns)", type="csv")
df = get_data(up)
st.sidebar.write(f"Rows: **{len(df)}**")
districts = st.sidebar.multiselect("District filter", sorted(df.district.unique()),
                                   default=sorted(df.district.unique()))
df = df[df.district.isin(districts)].reset_index(drop=True)

tab0, tab1, tab2, tab3, tab4 = st.tabs(
    ["📊 Overview", "🔵 K-Means", "🌳 Decision Tree", "🔗 Apriori", "💡 Insights"])

# ---------------- Overview ----------------
with tab0:
    c1, c2, c3 = st.columns(3)
    c1.metric("Avg loss %", f"{df.loss_percent.mean():.1f}")
    c2.metric("High-loss shipments", f"{(df.loss_level == 'High').mean() * 100:.1f}%")
    c3.metric("Worst district", df.groupby("district").loss_percent.mean().idxmax())
    a, b = st.columns(2)
    a.plotly_chart(px.histogram(df, x="loss_percent", nbins=30, title="Loss % distribution"),
                   use_container_width=True)
    b.plotly_chart(px.bar(df.groupby("storage_type").loss_percent.mean().reset_index(),
                          x="storage_type", y="loss_percent", title="Avg loss by storage type"),
                   use_container_width=True)
    a, b = st.columns(2)
    a.plotly_chart(px.box(df, x="packaging", y="loss_percent", title="Loss by packaging"),
                   use_container_width=True)
    b.plotly_chart(px.bar(df.groupby("district").loss_percent.mean().sort_values().reset_index(),
                          x="loss_percent", y="district", orientation="h",
                          title="Avg loss by district"), use_container_width=True)
    with st.expander("Raw data"):
        st.dataframe(df, use_container_width=True)

# ---------------- K-Means ----------------
with tab1:
    st.subheader("Cluster shipments by risk profile")
    el = mining.elbow(df)
    a, b = st.columns(2)
    a.plotly_chart(px.line(el, x="k", y="inertia", markers=True, title="Elbow method"),
                   use_container_width=True)
    b.plotly_chart(px.line(el, x="k", y="silhouette", markers=True, title="Silhouette score"),
                   use_container_width=True)
    k = st.slider("Number of clusters (k)", 2, 6, 3)
    clustered, profile = mining.run_kmeans(df, k)
    st.plotly_chart(px.scatter(clustered, x="distance_km", y="delay_hours", color="cluster_name",
                               size="loss_percent", hover_data=["district", "storage_type"],
                               title="Clusters: distance vs delay (bubble = loss %)"),
                    use_container_width=True)
    st.dataframe(profile, use_container_width=True)

# ---------------- Decision Tree ----------------
with tab2:
    st.subheader("Predict loss level (Low / Medium / High)")
    depth = st.slider("Max depth", 2, 8, 4)
    res = mining.run_tree(df, depth)
    st.metric("Test accuracy", f"{res['accuracy'] * 100:.1f}%")
    a, b = st.columns(2)
    a.write("**Confusion matrix** (rows = actual, cols = predicted)")
    a.dataframe(res["cm"])
    b.plotly_chart(px.bar(res["importance"].head(10)[::-1], orientation="h",
                          title="Top factors driving loss"), use_container_width=True)
    fig, ax = plt.subplots(figsize=(16, 7))
    plot_tree(res["model"], feature_names=res["columns"], class_names=res["model"].classes_,
              filled=True, fontsize=7, max_depth=3, ax=ax)
    st.pyplot(fig)

    st.markdown("#### Try a shipment")
    c = st.columns(4)
    inp = {
        "distance_km": c[0].number_input("Distance (km)", 30, 700, 250),
        "delay_hours": c[1].number_input("Delay (hrs)", 0.0, 48.0, 5.0),
        "storage_days": c[2].number_input("Storage days", 1, 90, 20),
        "rainfall_mm": c[3].number_input("Rainfall (mm)", 0, 220, 50),
    }
    c = st.columns(4)
    for col, key in zip(c, ["packaging", "transport", "road_condition", "storage_type"]):
        inp[key] = col.selectbox(key.replace("_", " ").title(), sorted(df[key].unique()))
    row = pd.DataFrame([{**{x: df[x].mode()[0] for x in mining.CAT}, **inp}])
    X = pd.get_dummies(row, columns=mining.CAT).reindex(columns=res["columns"], fill_value=0)
    if st.button("Predict"):
        st.success(f"Predicted loss level: **{res['model'].predict(X)[0]}**")

# ---------------- Apriori ----------------
with tab3:
    st.subheader("Association rules leading to loss")
    c = st.columns(3)
    sup = c[0].slider("Min support", 0.02, 0.3, 0.08, 0.01)
    conf = c[1].slider("Min confidence", 0.3, 0.9, 0.5, 0.05)
    lift = c[2].slider("Min lift", 1.0, 2.5, 1.1, 0.1)
    try:
        rules = mining.run_apriori(df, sup, conf, lift)
        st.write(f"{len(rules)} rules found")
        st.dataframe(rules, use_container_width=True)
        if len(rules):
            st.plotly_chart(px.scatter(rules, x="support", y="confidence", size="lift", color="lift",
                                       hover_data=["antecedents", "consequents"],
                                       title="Rules: support vs confidence"),
                            use_container_width=True)
    except ImportError:
        st.error("mlxtend not installed: run `pip install mlxtend`")

# ---------------- Insights ----------------
with tab4:
    st.subheader("Auto-generated insights")
    worst_pack = df.groupby("packaging").loss_percent.mean().idxmax()
    worst_store = df.groupby("storage_type").loss_percent.mean().idxmax()
    worst_road = df.groupby("road_condition").loss_percent.mean().idxmax()
    corr = df[mining.NUM + ["loss_percent"]].corr().loss_percent.drop("loss_percent").idxmax()
    st.markdown(f"""
- Highest average loss packaging: **{worst_pack}**
- Highest average loss storage: **{worst_store}**
- Worst road condition for loss: **{worst_road}**
- Numeric factor most correlated with loss: **{corr}**
- Shipments with delay above 8 hrs lose **{df[df.delay_hours > 8].loss_percent.mean():.1f}%** on average vs **{df[df.delay_hours <= 8].loss_percent.mean():.1f}%** otherwise.
""")
    st.info("Recommendations: shift from loose/gunny to cartons or crates, move ambient storage to cold/CA "
            "stores, and reduce transit delays on poor roads.")
