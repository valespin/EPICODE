import pandas as pd
import numpy as np
from datetime import date


# Previsioni vendite
date_rng = pd.date_range(start="2026-01-01", end="2026-03-31", freq="D")
df = pd.DataFrame({
      "Data": date_rng,
      "ID_prodotto": np.random.choice(["P1", "P2", "P3", "P4"], size=len(date_rng)),
      "Vendite": np.random.randint(50, 500, size=len(date_rng)),
      "Prezzo": np.random.uniform(10, 50, size=len(date_rng))
})

# caricamento valori mancanti e duplicati
df.loc[np.random.choice(df.index, 10, replace=False), "ID_prodotto"] = np.nan
df.loc[np.random.choice(df.index, 10, replace=False), "Vendite"] = np.nan
df.loc[np.random.choice(df.index, 10, replace=False), "Prezzo"] = np.nan
df = pd.concat([df, df.sample(15, random_state=42)], ignore_index=True)

# parte 1: caricamento ed esplorazione dati
print("DataFrame vendite (prime 5 righe): \n", df.head())
print("\nInfo: ")
df.info()
print("\nStatistiche descrittive: \n", df.describe())

# parte 2: pulizia
for col in ["Vendite", "Prezzo"]:
    df[col] = df[col].fillna(df[col].mean())

df["ID_prodotto"] = df["ID_prodotto"].fillna("sconosciuto")

df = df.drop_duplicates()

df["Data"] = pd.to_datetime(df["Data"], errors="coerce")

df["Vendite"] = pd.to_numeric(df["Vendite"], downcast="integer")
df["Prezzo"] = pd.to_numeric(df["Prezzo"], downcast="float")
df["ID_prodotto"] = df["ID_prodotto"].astype(str)

print("\nDataFrame vendite pulito: (prime 5 righe)\n", df.head())
print("\nInfo post pulizia: ")
df.info()

# parte 3: analisi esplorativa
tot_vendite = df.groupby("ID_prodotto")["Vendite"].sum()
print("\nTotale vendite per prodotto: \n", tot_vendite.round(2))

top_prodotto = tot_vendite.idxmax()
vendite_top = tot_vendite.max()
print(f"\nProdotto più venduto: {top_prodotto} con {vendite_top:.2f} vendite")

down_prodotto = tot_vendite.idxmin()
vendite_down = tot_vendite.min()
print(f"\nProdotto meno venduto: {down_prodotto} con {vendite_down:.2f} vendite")

media_gg_vendite = df.groupby("Data")["Vendite"].mean()
print("\nMedie medie giornaliere (prime 5 giornate): \n", media_gg_vendite.head())

