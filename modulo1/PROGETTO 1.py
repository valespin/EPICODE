# --------------PROGETTO 1---------------------------

# --------------PARTE 1------------------------------
titolo = "Il Signore degli anelli"
copie = 5
prezzo = 19.5
disp = True

print(f"Titoilo: {titolo}", type(titolo))
print(f"N. copie: {copie}", type(copie))
print(f"Prezzo: {prezzo} €", type(prezzo))
print(f"Disponibilità: {disp}", type(disp))

# --------------PARTE 2------------------------------
libri = [
    "Il Signore degli anelli", 
    "Il Trono di Spade",
    "Le Cronache di Narnia", 
    "Le nebbie di Avalon", 
    "Il mago"
    ]

copie_disp = { 
    "Il signore degli anelli": 5,
    "Il Trono di Spade": 7,
    "Le cronache di Narnia": 10,
    "Le nebbie di Avalon": 2,
    "Il mago": 1}

print("Lista libri:")
print(libri)
print("Copie disponibili:")
print(copie_disp)

minorenni = {
    "Ritella A.",
    "Russo G.",
    "Di Chito R.",
    "Ronchi A.",
    "Rosa D."
}
maggiorenni = {
    "Bianchi S.",
    "Rossi A.",
    "De Iure I.",
    "Verna V.",
    "Vivaldi E."
}
over_75 = {
    "Rossi A.",
    "Vivaldi E.",
    "Ricci S.",
    "Spinelli S.",
    "De Ruvo T."
}
totale = minorenni | maggiorenni | over_75
print(totale)

# --------------PARTE 3------------------------------
class Libro:
    def __init__(self, titolo, autore, anno, copie):
        self.titolo = titolo
        self.autore = autore
        self.anno = anno
        self.copie = copie
    def info(self):
        print(f"LIBRO\ntitolo: {self.titolo},\nautore: {self.autore},\nanno: {self.anno},\ncopie disponibili: {self.copie}")
    
class Utente:
    def __init__(self, nome, età, id_utente : str):
        self.nome = nome
        self.età = età
        self.id_utente = id_utente
    def scheda(self):
        print("SCHEDA UTENTE")
        print("Nome: ", self.nome)
        print("Età: ", self.età) 
        print("ID utente: ", self.id_utente)
class Prestito:
    def __init__(self, utente : Utente, libro : Libro, giorni):
        self.utente = utente
        self.libro = libro
        self.giorni = giorni
    def dettagli(self):
        print("DETTAGLIO PRESTITO")
        print("Utente:", self.utente.nome)
        print("ID utente: ", self.utente.id_utente)
        print("Libro: ", self.libro.titolo)
        print("Autire: ", self.libro.autore)
        print("Giorni di prestito: ", self.giorni)

libro1 = Libro("Il Signore degli Anelli", "J. R. R. Tolkien", 1954, 5)
utente1 = Utente("De Iure I.", 45, "U001")
prestito1 = Prestito(utente1, libro1, 90)
libro1.info()
utente1.scheda()
prestito1.dettagli()


# --------------PARTE 4------------------------------
prestiti_effettuati = []    
    
def presta_libro(utente, libro, giorni):
    if libro.copie == 0:
        print(f"Errore: {libro.titolo} non disponibile")
    else:
        libro.copie -= 1
        prestito = Prestito(utente, libro, giorni)
        prestiti_effettuati.append(prestito)
        print(f"Presito effettuato: {utente.nome} ha preso {libro.titolo} per {giorni} giorni")

libro2 = Libro("Il Trono di Spade", "George R. R. Martin", 1996, 7)
libro3 = Libro("Le cronache di Narnia", "C. S. Lewis", 1950, 10)
libro4 = Libro("Il mago", "W. S. Maugham", 1908, 1)

utente2 = Utente("Rossi A.", 76, "U002")
utente3 = Utente("Ritella A.", 11, "U003")
utente4 = Utente("Bianchi S.", 27, "U004")

presta_libro(utente2, libro4, 120)
presta_libro(utente3, libro3, 150)
presta_libro(utente4, libro2, 60)
presta_libro(utente4, libro4, 120)

print("COPIE DISPONIBILI AGGIORNATE:")
for libro in [libro2, libro3, libro4]:
    libro.info()

print("PRESTITI EFFETTUATI:")
for prestito in prestiti_effettuati:
    prestito.dettagli()







              





        