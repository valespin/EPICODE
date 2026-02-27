import pandas as pd
import numpy as np

# parte 1: creazione dataset
prodotti = pd.DataFrame({
     "ProdottoID": ["P_"+str(i) for i in range(1, 21)],
     "Categoria": np.random.choice(["C1", "C2", "C3", "C4", "C5"], size=20),
     "Fornitore": np.random.choice(["F1", "F2", "F3"], size=20),
     "Prezzo": np.random.uniform(4.99, 149.99, size=20)
})
prodotti.to_json("prodotti.json", orient="records")

b = 5_000
clienti = pd.DataFrame({
     "ClienteID": ["C_"+str(i) for i in range(1, b+1)],
     "Regione": np.random.choice(["Nord", "Centro", "Sud"], size=b),
     "Segmento": np.random.choice(["Premium", "Standard"], size=b)
})
clienti.to_csv("clienti.csv", index=False)

a = 100_000
date_rng = pd.date_range(start="2025-01-01", end="2025-12-31", freq="D")
ordini = pd.DataFrame({
     "ClienteID": np.random.choice(clienti["ClienteID"], size=a),
     "ProdottoID": np.random.choice(prodotti["ProdottoID"], size=a),
     "Quantità": np.random.randint(1, 500, size=a),
     "DataOrdine": np.random.choice(date_rng, size=a)
})
ordini.to_csv("ordini.csv", index=False)

df_prodotti = pd.read_json("prodotti.json")
df_clienti = pd.read_csv("clienti.csv")
df_ordini = pd.read_csv("ordini.csv")


# parte 2: unione DataFrame
df = df_ordini.merge(df_prodotti, on= "ProdottoID", how="left").merge(df_clienti, on="ClienteID", how="left")  # left join per mantere tutti gli ordini


# parte 3: ottimizzazioni
print("Utilizzo iniziale della memoria (MB):")
print(df.memory_usage(deep=True).sum()/1024**2)

df["ClienteID"] = df["ClienteID"].astype("category")
df["ProdottoID"] = df["ProdottoID"].astype("category")
df["Fornitore"] = df["Fornitore"].astype("category")
df["Prezzo"] = pd.to_numeric(df["Prezzo"], downcast="float")
df["Categoria"] = df["Categoria"].astype("category")
df["Regione"] = df["Regione"].astype("category")
df["Segmento"] = df["Segmento"].astype("category")
df["Quantità"] = pd.to_numeric(df["Quantità"], downcast="integer")
df["DataOrdine"] = pd.to_datetime(df["DataOrdine"])

print("\nUtilizzo della memoria post-ottimizzazioni (MB):")
print(df.memory_usage(deep=True).sum()/1024**2)


# parte 4: creazione colonne, filtro dati e calcolo statistiche
df["ValoreTotale"] = df["Prezzo"] * df["Quantità"]

df_filtrato = df[(df["ValoreTotale"] > 100) & (df["Regione"] == "Nord")]
df_filtrato.reset_index()

print("\nDataFrame filtrato per clienti del nord e valore totale > 100: \n", df_filtrato.head())

report = df.groupby(["Categoria", "Regione"]).agg(
    totale_vendite= pd.NamedAgg(column="ValoreTotale", aggfunc="sum"),
    media_prezzo =pd.NamedAgg(column="Prezzo", aggfunc="mean"),
    numero_ordini= pd.NamedAgg(column="ClienteID", aggfunc="count")
)
report = report.reset_index()

print("\nCalcolo metriche: \n", report.head())


# parte 5: lettura in chunk da 10_000 righe
tot_valore = 0

for chunk in pd.read_csv("ordini.csv", chunksize=10_000):
    chunk= chunk.merge(df_prodotti, on="ProdottoID", how="left")
    chunk["ValoreTotale"] = chunk["Quantità"] * chunk["Prezzo"]
    tot_valore += chunk["ValoreTotale"].sum()

print("\nValore totale finale: ", tot_valore)










