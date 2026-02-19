# --------------PROGETTO 2---------------------------

# --------------PARTE 1 - 2 - 4 - 5-----------------------------
import numpy as np

class Analisi:
    def __init__ (self, tipo, valore):
        self.tipo = tipo
        self.valore = float(valore)
    def valuta(self):
        if self.tipo == "glicemia":
            return "nella norma" if self.valore <= 75 else "fuori norma"
        elif self.tipo == "colesterolo":
            return "nella norma" if self.valore >= 110 else "fuori norma"
        elif self.tipo == "emoglobina":
            return "nella norma" if self.valore >= 100 else "fuori norma"
        elif self.tipo == "vit_B12":
            return "nella norma" if self.valore <= 800 else "fuori norma"
        elif self.tipo == "ferro":
            return "nella norma" if self.valore <= 20 else "fuori norma"
        elif self.tipo == "creatinina":
            return "nella norma" if self.valore <= 1.2 else "fuori norma"
        elif self.tipo == "mioglobina":
            return "nella norma" if self.valore <= 85 else "fuori norma"
        else:
            return "Tipologia non disponibile"
    def __str__(self):
        return f"{self.tipo}: {self.valore} ({self.valuta()})"

class Paziente:
    def __init__(self, nome, cognome, cod_fisc, età, peso):
        self.nome = nome
        self.cognome = cognome
        self.cod_fisc = cod_fisc
        self.età = età
        self.peso = float(peso)
        self.analisi = []
        self.risultato_analisi = np.array([])

    def scheda_personale(self):
        print(
            f"\nSCHEDA PAZIENTE: \n"
            f"nome: {self.nome}\n"
            f"cognome: {self.cognome}\n"
            f"C.F.: {self.cod_fisc}\n"
            f"età: {self.età}\n"
            f"peso: {self.peso}"
        )

    def aggiungi_analisi(self, *analisi):
        self.analisi.extend(analisi)             # popola la lista self.analisi[]
        valori = [a.valore for a in analisi]     # popola array risultato_analisi
        if valori:
            self.risultato_analisi = np.append(self.risultato_analisi, valori)
    
    def mostra_analisi(self):
        print(f"\nAnalisi di {self.nome} {self.cognome}: ")
        for a in self.analisi:
            print(f"- {a}")
        print(f"- Valori numerici delle analisi: {self.risultato_analisi}")

    def statistiche_analisi(self):
        print(
            f"\nSTATISTICHE analisi di {self.nome} {self.cognome}: \n"
            f"Media: {np.mean(self.risultato_analisi)}\n"
            f"Max: {np.max(self.risultato_analisi)}\n"
            f"Min: {np.min(self.risultato_analisi)}\n"
            f"Dev. std.: {np.std(self.risultato_analisi)}"
        )

class Medico:
    def __init__(self, nome, cognome, specializzazione):
        self.nome = nome
        self.cognome = cognome
        self.specializzazione = specializzazione
    def visita_paziente(self, paziente):
        print(
            f"\nVISITA: \n"
            f"Medico: {self.nome} {self.cognome} ({self.specializzazione})\n"
            f"Paziente: {paziente.nome} {paziente.cognome}"
        )

        
p1 = Paziente(
    "Mario", "Rossi", "RSSMRA81H02F205T",
    45, 80
    )

p2 = Paziente(
    "Laura", "Bianchi", "BNCLRA96C59B157O",
    30, 50.5
    )

p3 = Paziente(
    "Simone", "Giorgi", "GRGSMN52R08G224E",
    54, 98.5
    )

p4 = Paziente(
    "Silvia", "Digioia", "DGISLV01A70L219U",
    25, 40.7
    )

p5 = Paziente(
    "Flavia", "Artusi", "RTSFLV88E56D969U",
    38, 59.5
    )

a1 = Analisi("glicemia", 100)
a2 = Analisi("colesterolo", 90)
a3 = Analisi("emoglobina", 100)
a4 = Analisi("vit_B12", 780.5)
a5 = Analisi("ferro", 0)
a6 = Analisi("creatinina", 1.1)
a7 = Analisi("mioglobina", 160)
a8 = Analisi("uricemia", 200)

p1.aggiungi_analisi(a3, a1, a2)
p2.aggiungi_analisi(a3, a4, a5)
p3.aggiungi_analisi(a2, a6, a8)
p4.aggiungi_analisi(a3, a6, a7)
p5.aggiungi_analisi(a1, a2, a6)

m1 = Medico("Giovanni", "Ricco", "Cardiologia")
m2 = Medico("Annalisa", "Labate", "Ematologia")
m3 = Medico("Carla", "Ponti", "Chirurgia")

p1.scheda_personale()
p2.scheda_personale()
p3.scheda_personale()
p4.scheda_personale()
p5.scheda_personale()

p1.mostra_analisi()
p2.mostra_analisi()
p3.mostra_analisi()
p4.mostra_analisi()
p5.mostra_analisi()

p1.statistiche_analisi()
p2.statistiche_analisi()
p3.statistiche_analisi()
p4.statistiche_analisi()
p5.statistiche_analisi()

m2.visita_paziente(p2)
m1.visita_paziente(p3)
m3.visita_paziente(p1)


# --------------PARTE 3------------------------------

val = np.random.uniform(70, 140, size = 10)
val = np.round(val, 2)            
print("\nEstrazione valori glicemia per 10 pazienti: ", val)
print("STATISTICHE:")
print("Media: ", np.mean(val))
print("Valore max: ", np.max(val))
print("Valore min: ", np.min(val))
print("Deviazione std: ", np.std(val))


              





        