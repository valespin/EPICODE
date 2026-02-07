# --------------PROGETTO FINALE----------------------


# --------------PARTE 2------------------------------
import pandas as pd

df = pd.read_csv("vendite.csv", encoding="latin-1")      # ho dovuto specificare l'encoding perchè il csv non è salvato in UTF-8

print("\nPrime 5 righe: \n", df.head())                                   
print("\nForma DataFrame: ", df.shape) 
print("\nInfo generali: ")
df.info()


# --------------PARTE 3------------------------------

df["Incasso"] = df["Quantità"]*df["Prezzo_unitario"]

print("\nAggiunta colonna incasso: \n", df.head())

incasso_tot = df["Incasso"].sum().round(2)
incasso_medio_per_negozio = df.groupby("Negozio")["Incasso"].mean().round(2)
top3_prodotti = df.groupby("Prodotto")["Quantità"].sum().sort_values(ascending=False).head(3)
incasso_medio_per_negozio_prodotto = df.groupby(["Negozio", "Prodotto"])["Incasso"].mean()

print("\nIncasso totale della catena (€): ", incasso_tot)
print("\nIncasso medio per negozio (€): \n", incasso_medio_per_negozio)
print("\nTop 3 prodotti più venduti: \n", top3_prodotti)
print("\nIncasso medio per negozio e prodotto (€): \n", incasso_medio_per_negozio_prodotto)


# --------------PARTE 4------------------------------
import numpy as np

q = df["Quantità"].to_numpy()

media= np.mean(q).round(2)
massimo= np.max(q)
minimo= np.min(q)
dev_std = np.std(q)
percentuale_sopra_media= np.mean(q > media) * 100

print("\nQuantità media venduta: ", media)
print("\nQuantità massima venduta: ", massimo)
print("\nQuantità minima venduta: ", minimo)
print("\nDeviazione standard: ", dev_std)

p = df["Prezzo_unitario"].to_numpy()

array_2D = np.column_stack((q, p))
incasso = array_2D[:,0] * array_2D[:,1]

i = df["Incasso"].to_numpy()

confronto = np.allclose(incasso, i)

print("\nL'incasso calcolato è corretto?: ", confronto)


# --------------PARTE 5------------------------------
import matplotlib.pyplot as plt

incasso_tot_negozio = df.groupby("Negozio")["Incasso"].sum()

incasso_tot_negozio.plot(
    kind= "bar",
    title= "Incasso totale per negozio",
    color= "skyblue",
    edgecolor="black"
)
plt.xlabel("Negozio")                 
plt.ylabel("Incassi (€)")
plt.grid(True, axis="y", linestyle="--", alpha= 0.7)
plt.tight_layout()  
plt.show()


incasso_per_prodotto = df.groupby("Prodotto")["Incasso"].sum()

plt.pie(
    incasso_per_prodotto,
    labels = incasso_per_prodotto.index,
    autopct= "%1.1f%%",
)
plt.title("Percentuale d'incasso per prodotto")
plt.tight_layout()  
plt.show()

df["Data"] = pd.to_datetime(df["Data"])           # conversione della str in data per ordine cronologico e non alfabetico
df = df.sort_values("Data")

incasso_giornaliero = df.groupby("Data")["Incasso"].sum()

plt.figure(figsize=(10,6))
plt.plot(
    incasso_giornaliero.index, 
    incasso_giornaliero.values, 
    marker= "o", 
    linestyle="--", 
    linewidth= 2, 
    color="blue"
)
plt.title("Andamento giornaliero degli incassi della catena")
plt.xlabel("data")
plt.xticks(rotation=45)                 # rotazione etichette per maggiore visibilità
plt.ylabel("Incasso (€)")
plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.tight_layout()
plt.show()

# --------------PARTE 6------------------------------
categorie = {
    "Laptop": "Informatica",
    "Smartphone": "Informatica",
    "TV": "Elettrodomestici",
    "Cuffie": "Informatica",
    "Tablet": "Informatica",
    "Smartwatch": "Informatica"
}
df["Categoria"] = df["Prodotto"].map(categorie)

print("\nAssociazione prodotto/categoria: \n", df)

incasso_tot_categorie = df.groupby("Categoria")["Incasso"].sum().round(2)
quantità_media_categoria = df.groupby("Categoria")["Quantità"].mean().round(2)

print("\nIncasso totale per categoria (€): \n", incasso_tot_categorie)
print("\nQuantità media venduta per categoria: \n", quantità_media_categoria)

df.to_csv("vendite_analizzate.csv", index=False)

# --------------PARTE 7------------------------------
incasso_medio_categorie = df.groupby("Categoria")["Incasso"].mean().round(2)

fig, ax1 = plt.subplots(figsize=(8,6))

ax1.bar(
    incasso_medio_categorie.index,
    incasso_medio_categorie.values,
    color="orange",
    alpha= 0.7,
    label= "Incasso medio (€)"
)
ax1.set_xlabel("Categorie")
ax1.set_ylabel("Incasso medio (€)")
ax1.tick_params(axis="y", labelcolor="orange")

ax2 = ax1.twinx()
ax2.plot(
    quantità_media_categoria.index,
    quantità_media_categoria.values,
    color="blue",
    marker="o",
    linestyle="--",
    label="Quantità media"
)
ax2.set_ylabel("Quantità media venduta")
ax2.tick_params(axis="y", labelcolor="blue")
plt.title("incasso medio e quantità media per categoria")
plt.tight_layout()
plt.show()


def top_n_prodotti_per_incasso(df, n):
    return(df.groupby("Prodotto")["Incasso"].sum().sort_values(ascending= True).head(n))

top_3_prodotti = top_n_prodotti_per_incasso(df, 3)
print("\nI 3 prodotti con maggior incasso: \n", top_3_prodotti)






              





        