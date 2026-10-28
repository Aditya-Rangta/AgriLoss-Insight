"""Synthetic apple supply-chain dataset for Himachal Pradesh.
Run: python generate_data.py  -> creates apple_supply_chain.csv
(Replace with real survey / NHB / APMC data later; column names can stay same.)"""
import numpy as np, pandas as pd

rng = np.random.default_rng(42)
N = 1500

district = rng.choice(["Shimla", "Kullu", "Kinnaur", "Mandi", "Chamba", "Sirmaur"], N,
                      p=[.35, .22, .15, .10, .08, .10])
variety = rng.choice(["Royal Delicious", "Red Delicious", "Golden Delicious", "Gala", "Fuji"], N,
                     p=[.35, .25, .15, .15, .10])
packaging = rng.choice(["Cardboard Carton", "Wooden Box", "Plastic Crate", "Gunny/Loose"], N,
                       p=[.45, .20, .20, .15])
transport = rng.choice(["Truck", "Pickup", "Tempo"], N, p=[.5, .3, .2])
storage = rng.choice(["CA Store", "Cold Store", "Ambient"], N, p=[.15, .40, .45])
road = rng.choice(["Good", "Average", "Poor"], N, p=[.3, .45, .25])
month = rng.choice(["Aug", "Sep", "Oct", "Nov"], N, p=[.15, .35, .35, .15])

distance = np.clip(rng.normal(280, 130, N), 30, 700).round()
delay = np.clip(rng.gamma(2, 3, N), 0, 48).round(1)
storage_days = np.clip(rng.normal(25, 15, N), 1, 90).round()
rain = np.clip(rng.normal(60, 40, N), 0, 220).round()

loss = 3 + 0.012 * distance + 0.35 * delay + 0.05 * storage_days + 0.02 * rain
loss += \
        pd.Series(packaging).map({"Cardboard Carton": 0, "Wooden Box": 1.5, "Plastic Crate": 0.8, "Gunny/Loose": 5}).values
loss += pd.Series(storage).map({"CA Store": -3, "Cold Store": -1.5, "Ambient": 3}).values
loss += pd.Series(road).map({"Good": 0, "Average": 1.5, "Poor": 3.5}).values
loss += pd.Series(transport).map({"Truck": 0, "Pickup": 1, "Tempo": 2}).values
loss += pd.Series(variety).map({"Royal Delicious": 0, "Red Delicious": -0.5, "Golden Delicious": 1.5,
                                "Gala": 1, "Fuji": -1}).values
loss += rng.normal(0, 2, N)
loss = np.clip(loss, 1, 45).round(2)

df = pd.DataFrame(dict(district=district, variety=variety, month=month, packaging=packaging,
                       transport=transport, road_condition=road, storage_type=storage,
                       distance_km=distance, delay_hours=delay, storage_days=storage_days,
                       rainfall_mm=rain, loss_percent=loss))
df["loss_level"] = pd.cut(df.loss_percent, [0, 12, 20, 100], labels=["Low", "Medium", "High"])
df.to_csv("apple_supply_chain.csv", index=False)
print(df.shape, df.loss_level.value_counts().to_dict())
