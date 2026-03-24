import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np
import seaborn as sns

np.random.seed(42)
n = 200

subcategories = {
    "Furniture": ["Chairs", "Tables", "Sofas"],
    "Office Supplies": ["Books", "Paper", "Pens"],
    "Technology": ["Phones", "Laptops", "Accessories"]
}

category_list = np.random.choice(["Furniture", "Office Supplies", "Technology"], n)
subcategory_list = [np.random.choice(subcategories[c]) for c in category_list]
order_dates = pd.date_range(start="2022-01-01", periods=n, freq="W")
ship_dates = order_dates + pd.to_timedelta(np.random.randint(1, 7, n), unit="d")   # timedelta per aggiunta di giorni (da 1 a 7) alla data ordine

df = pd.DataFrame({
    "Order Date"   : order_dates,
    "Ship Date"    : ship_dates,
    "Category"     : category_list,
    "Sub-Category" : subcategory_list,
    "Region"       : np.random.choice(["North", "South", "East", "West"], n),
    "Sales"        : np.random.uniform(20, 500, n).astype(np.float32),
    "Profit"       : np.random.uniform(-50, 200, n).astype(np.float32),
    "Quantity"     : np.random.randint(1, 10, n)
})

# parte 1 - pulizia dati e creazione colonna year
df = df.dropna()                   
df = df.drop_duplicates() 
df["Year"] = df["Order Date"].dt.year

# parte 2 - analisi esplorativa (EDA)
fig = plt.figure(figsize=(12, 6))
gs = gridspec.GridSpec(2, 2, figure=fig)
ax1 = fig.add_subplot(gs[0,:])
ax2 = fig.add_subplot(gs[1,0])
ax3 = fig.add_subplot(gs[1,1])

# totale vendite e profitti per anno
yearly = df.groupby("Year")[["Sales", "Profit"]].sum().round(2)

ax1.plot(yearly.index, yearly["Sales"], label="sales", marker="o", color="blue")
ax1.plot(yearly.index, yearly["Profit"], label="profit", marker="s", color="red")
ax1.set_title("Total sales and profit by years")
ax1.set_xlabel("Year")
ax1.set_ylabel("Sales (€)")
ax1.tick_params(axis="x", rotation=0)    
ax1.grid(True, axis="y", linestyle="--", alpha=0.5)
ax1.legend()


# Top 5 categorie più vendute 
top5 = df.groupby("Sub-Category")["Sales"].sum().sort_values(ascending=False).reset_index().head()

ax2.barh(top5["Sub-Category"], top5["Sales"], color="blue", alpha=0.9)
ax2.set_title("Top 5 Sub-Category for Sales")
ax2.set_xlabel("Sales (€)")
ax2.set_ylabel("Sub-Category")
ax2.grid(True, axis="x", linestyle="--", alpha=0.5)

# Mappa delle vendite per regione
region_sales = df.groupby("Region")["Sales"].sum().sort_values(ascending=False)
region_colors = {
    "North": "skyblue",
    "South": "purple",
    "East" : "orange",
    "West" : "green"
}
ax3.bar(region_sales.index, region_sales.values, 
        color=[region_colors[r] for r in region_sales.index], alpha=0.9)
ax3.set_title("Sales by region")
ax3.set_xlabel("Region")
ax3.set_ylabel("Sales (€)")
ax3.grid(True, axis="y", linestyle="--", alpha=0.5)

plt.tight_layout()
plt.show()


