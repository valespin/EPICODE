# --------------PROGETTO 3---------------------------

# --------------PARTE 1 -----------------------------
nome = "Mario Rossi"
eta = 34
saldo = 2500.75
vip = True
destinazioni = ["Parigi", "Londra", "Monaco", "Tokyo", "Madrid"]
costo_viaggio = {
    "Parigi": 700.0,
    "Londra": 600.0,
    "Monaco": 550.0,
    "Tokyo": 2200.0,
    "Madrid": 450.0
}

# --------------PARTE 2------------------------------
class Cliente:
    def __init__(self, nome, eta, vip):
        self.nome = nome
        self.eta = eta
        self.vip = bool(vip)
    def info (self):
        print(
            f"\nSCHEDA CLIENTE\n"
            f"- nome: {self.nome}\n"
            f"- eta: {self.eta}\n"
            f"- vip: {self.vip}"
        )
    
class Viaggio:
    def __init__ (self, destinazione, prezzo, durata):
        self.destinazione = destinazione
        self.prezzo = prezzo
        self.durata = durata

class Prenotazione: 
    def __init__(self, cliente, viaggio):
        self.cliente = cliente
        self.viaggio = viaggio
    
    def importo (self):
        if self.cliente.vip:
            return self.viaggio.prezzo * 0.9     
        else:
            return self.viaggio.prezzo
    def dettaglio (self):
        print(
            f"\nDETTAGLI PRENOTAZIONE\n"
            f"- cliente: {self.cliente.nome} --> vip: {self.cliente.vip}\n"
            f"- destinazione: {self.viaggio.destinazione}\n"
            f"- durata: {self.viaggio.durata}gg\n"
            f"- prezzo base: {self.viaggio.prezzo:.2f}€\n"
            f"- importo finale: {self.importo():.2f}€"
        )

c1 = Cliente("Mario Rossi", 34, True)
c2 = Cliente("Rosa Bianchi", 40, False)
c3 = Cliente("Luigi Falco", 20, False)

c1.info()
c2.info()
c3.info()

v1 = Viaggio("Parigi", 700.0, 5)
v2= Viaggio("Madrid", 450.0, 6)
v3= Viaggio("Tokyo", 2200.0, 7)

p1 = Prenotazione(c3, v2)
p2 = Prenotazione(c2, v3)
p3 = Prenotazione(c1, v1)

p1.dettaglio()
p2.dettaglio()
p3.dettaglio()

# --------------PARTE 3------------------------------
import numpy as np

simula_prenotazioni = np.random.uniform(200, 2000, size = 100)
simula_prenotazioni = np.round(simula_prenotazioni, 2)
print("\nSTATISTICHE su 100 prenotazioni con costo tra 200 e 2000€: ")
print(f"prezzo medio: {np.mean(simula_prenotazioni):.2f}€")
print(f"prezzo minimo: {np.min(simula_prenotazioni):.2f}€")
print(f"prezzo massimo: {np.max(simula_prenotazioni):.2f}€")
print(f"deviazione standard: {np.std(simula_prenotazioni)}")

media = np.mean(simula_prenotazioni)
percentuale_sopra = np.mean(simula_prenotazioni > media) * 100
print(f"Percentuale sopra la media: {percentuale_sopra:.2f}%")

# --------------PARTE 4------------------------------
import pandas as pd

dati = {
    "Cliente": ["Mario Rossi", "Rosa Bianchi", "Luigi Falco", "Giulia Salis", "Antonio DeRuvo", "Anna Russo"],
    "Destinazione": ["Parigi", "Tokyo", "Madrid", "Madrid", "Parigi", "Parigi"],
    "Prezzo": [700.0, 2200.0, 450.0, 500.0, 780.0, 799.0],
    "Giorno_partenza": ["2026-02-10", "2026-09-20", "2026-06-15", "2026-07-13", "2026-12-24", "2026-12-29"],
    "Durata": [5, 7, 6, 5, 5, 6],
    "Incasso": [630.0, 220.0, 450.0, 450.0, 768.0, 799.0]
}

df = pd.DataFrame(dati)
print("\n", df)

print(f"\nIncasso totale: {df["Incasso"].sum()}€")
print(f"\nIncasso medio per destinazione: \n{df.groupby("Destinazione")["Incasso"].mean().round(2)}€")   # raggruppa per destinazione, prendi la colonna incasso e fai la media

top3 = (df.groupby("Destinazione").size().sort_values(ascending=False).head(3))           # raggruppa per destinazione, conta quante volte appare, metti in ordine decrescente e prendi i primi 3
print("\nTop 3 destinazioni più vendute: \n", top3)

# --------------PARTE 5------------------------------
import matplotlib.pyplot as plt

incasso_medio_destinazione= df.groupby("Destinazione")["Incasso"].mean().round(2)

incasso_medio_destinazione.plot(
    kind= "bar",
    title= "Incasso per destinazione",
    color= "skyblue"
)

plt.xlabel("Destinazione")                 
plt.ylabel("Incassi (€)")
plt.grid(True, axis="y", linestyle="--", alpha= 0.7)
plt.show()

df["Giorno_partenza"] = pd.to_datetime(df["Giorno_partenza"])           # conversione della str in data per ordine cronologico e non alfabetico
df = df.sort_values("Giorno_partenza")

plt.figure(figsize=(8,6))
plt.plot(df["Giorno_partenza"], df["Incasso"], marker= "o", linestyle="-", color="blue")
plt.title("Andamento giornaliero degli incassi")
plt.xlabel("Giorno di partenza")
plt.xticks(rotation=45)                 # rotazione etichette per maggiore visibilità
plt.ylabel("Incasso (€)")
plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.show()


vendite_per_destinazione = df["Destinazione"].value_counts()

plt.pie(
    vendite_per_destinazione,
    labels = vendite_per_destinazione.index,
    autopct= "%1.0f%%",
    colors=["yellow", "orange", "red"],
    shadow= True
)
plt.title("% vendite per destinazione")
plt.show()

# --------------PARTE 6------------------------------
categorie = {
    "Parigi": "Europa",
    "Tokyo": "Asia",
    "Madrid": "Europa"
}
df["Categorie"] = df["Destinazione"].map(categorie)    # per sostituire le desrinazioni del df con categorie

print("\nAssociazione destinazioni/categorie: \n", df)

incasso_per_categoria = df.groupby("Categorie")["Incasso"].sum()
durata_media_viaggio = df.groupby("Categorie")["Durata"].mean()

print("\nIncasso per categoria (€): \n", incasso_per_categoria)
print("\nDurata media dei viaggi per categoria (gg): \n", durata_media_viaggio)

df.to_csv("prenotazioni_analizzate.csv", index=False)

# --------------PARTE 7------------------------------

def top_n_clienti_per_prenotazione(df, n):
    return(df["Cliente"].value_counts().head(n))

top4_clienti = top_n_clienti_per_prenotazione(df, 4)
print("\nI 4 clienti con più prenotazioni: \n", top4_clienti)

plt.figure(figsize=(8,10))
plt.subplot(2,1,1)
plt.bar(incasso_per_categoria.index, incasso_per_categoria, color="orange")
plt.title("Incasso medio per categoria")
plt.xlabel("Categorie")
plt.ylabel("Incasso (€)")

plt.subplot(2,1,2)
plt.plot(durata_media_viaggio.index, durata_media_viaggio, color="blue")
plt.title("Durata media viaggi per categoria")
plt.xlabel("Categorie")
plt.ylabel("Durata (gg)")

plt.show()




              





        