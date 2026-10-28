"""Core data-mining functions: K-Means, Decision Tree, Apriori."""
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score, accuracy_score, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier

NUM = ["distance_km", "delay_hours", "storage_days", "rainfall_mm"]
CAT = ["district", "variety", "month", "packaging", "transport", "road_condition", "storage_type"]


def load(path="apple_supply_chain.csv"):
    return pd.read_csv(path)


# ---------- K-Means ----------
def elbow(df, k_max=8):
    X = StandardScaler().fit_transform(df[NUM + ["loss_percent"]])
    rows = []
    for k in range(2, k_max + 1):
        km = KMeans(n_clusters=k, n_init=10, random_state=42).fit(X)
        rows.append((k, km.inertia_, silhouette_score(X, km.labels_)))
    return pd.DataFrame(rows, columns=["k", "inertia", "silhouette"])


def run_kmeans(df, k=3):
    cols = NUM + ["loss_percent"]
    X = StandardScaler().fit_transform(df[cols])
    out = df.copy()
    out["cluster"] = KMeans(n_clusters=k, n_init=10, random_state=42).fit_predict(X)
    profile = out.groupby("cluster")[cols].mean().round(2)
    profile["shipments"] = out.cluster.value_counts().sort_index()
    # label clusters by average loss
    order = profile.loss_percent.rank(method="first").astype(int)
    names = {1: "Low-risk", 2: "Medium-risk", 3: "High-risk"} if k == 3 else {i: f"Risk rank {i}" for i in range(1, k + 1)}
    out["cluster_name"] = out.cluster.map(order).map(names)
    profile["risk_label"] = order.map(names)
    return out, profile


# ---------- Decision Tree ----------
def run_tree(df, max_depth=4):
    X = pd.get_dummies(df[NUM + CAT], columns=CAT)
    y = df["loss_level"]
    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.25, random_state=42, stratify=y)
    clf = DecisionTreeClassifier(max_depth=max_depth, random_state=42).fit(Xtr, ytr)
    pred = clf.predict(Xte)
    labels = ["Low", "Medium", "High"]
    imp = pd.Series(clf.feature_importances_, index=X.columns).sort_values(ascending=False)
    return dict(model=clf, columns=list(X.columns), accuracy=accuracy_score(yte, pred),
                cm=pd.DataFrame(confusion_matrix(yte, pred, labels=labels), index=labels, columns=labels),
                importance=imp[imp > 0])


# ---------- Apriori ----------
def run_apriori(df, min_support=0.08, min_conf=0.5, min_lift=1.1):
    from mlxtend.frequent_patterns import apriori, association_rules
    d = df.copy()
    d["distance"] = pd.cut(d.distance_km, [0, 150, 350, 1000], labels=["ShortHaul", "MidHaul", "LongHaul"])
    d["delay"] = pd.cut(d.delay_hours, [-1, 3, 8, 100], labels=["LowDelay", "MedDelay", "HighDelay"])
    d["storage_dur"] = pd.cut(d.storage_days, [0, 15, 40, 100], labels=["ShortStore", "MedStore", "LongStore"])
    d["loss"] = "Loss_" + d.loss_level.astype(str)
    items = d[["packaging", "transport", "road_condition", "storage_type", "distance", "delay",
               "storage_dur", "loss"]].astype(str)
    basket = pd.get_dummies(items, prefix="", prefix_sep="").astype(bool)
    freq = apriori(basket, min_support=min_support, use_colnames=True)
    rules = association_rules(freq, metric="confidence", min_threshold=min_conf)
    rules = rules[(rules.lift >= min_lift) & rules.consequents.apply(lambda s: any(i.startswith("Loss_") for i in s))]
    rules = rules.copy()
    for c in ("antecedents", "consequents"):
        rules[c] = rules[c].apply(lambda s: ", ".join(sorted(s)))
    return rules[["antecedents", "consequents", "support", "confidence", "lift"]] \
        .sort_values("lift", ascending=False).round(3).reset_index(drop=True)
