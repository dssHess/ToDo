"""
----------------------------------------------------------------------------------
Entwickle eine App, mit der man ToDos verwalten kann.
Die App soll über die Konsole verwendet werden können. 
Die App soll folgende Funktionen beinhalten (Akzeptanzkriterien):

Datenbankverbindung zu einer sqlite Datenbank

Verwendung von sqlalchemy

Nutzereingabe: Hinzufügen einer neuen ToDo
Nutzereingabe: Löschen einer ToDo
Nutzereingabe: Erledigen einer ToDo
Nutzereingabe: Zeige die ToDos, die heute erledigt werden müssen
Nutzereingabe: Auflisten der ToDos, die noch zu erledigen sind

Wenn eine ToDo "erledigt" ist, soll die ToDo auf "erledigt" gesetzt werden 
durch speicherung des Erledigt Datum und Zeit

Die ToDos können ein "zu Erledigen" Datum haben

------------------------------------------------------------------------------------
"""
# # # ###########################################
# Laden der Fremdbibliotheken
# # # ###########################################

from rich.console import Console
from rich.table import Table
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker

console = Console()

# # # ###########################################
# Bitte nicht verändern!
# Datenbank Kram!
# Erzeugen einer neuen Datenbank Engine
rueckgabewert_db_erstellt = create_engine("sqlite:///ToDo.db")

# Basisklasse für Klassen
Hauptdatenbank = declarative_base()

# Öffne Verbindung zur Datenbank
Session = sessionmaker(bind=rueckgabewert_db_erstellt)

# Offene Verbindung zur Datenbank
session = Session()
# # # ###########################################

class C_ToDo(Hauptdatenbank):
    __tablename__ = "todo"

    # Feldnamen der sql-Datenbank
    db_t_todo_id = Column(Integer, primary_key=True) # Primärschlüssel (int)
    db_t_aufgabe = Column(String)                    # Kurzbezeichnung der Aufgabe (str)
    db_t_erinnerung = Column(String)                 # Wann soll ich daran erinnertung werden (datum und Zeit)
    db_t_bemerkung = Column(String)                  # Bemerkung im Klartext (str)
    db_t_faellig = Column(String)                    # Wann soll die Aufgabe erledigt werden (datum und Zeit)
    db_t_erledigt = Column(String)                   # Ist die Aufgabe erledigt (datum und Zeit)
    
    # Foreignkeys (hier keiner)
    # Beispiel db_t_sprache_id = Column(Integer, ForeignKey("sprachen.db_s_id"))
    
    def __repr__(self) -> str:
        return f"{self.db_t_aufgabe} {self.db_t_faellig}"

def F_Init_Datenbank():
    """
    Init die Datenbanken und erstelle alle Tabellen.
    See more here: https://docs.sqlalchemy.org/en/14/orm/tutorial.html
    """
    Hauptdatenbank.metadata.create_all(rueckgabewert_db_erstellt)

def F_Datenbank_speicher_aufgabe(todo: C_ToDo):
    """
    Database command to add a new todo.
    """
    session.add(todo)
    session.commit()

def F_neue_aufgabe():
    n_aufgabe      = input("Bitte geben die Aufgabe an\t: ")
    n_erinnertung  = input("Wann sol ich dich daran erinnern? (Datum und Zeit)\t: ")
    n_bemerkung    = input("Bitte geben eine Bemrkungen ein\t: ")
    n_faellig      = input("Wann ist die Aufgabe fällig? (Datum und Zeit)\t: ")
    n_neue_aufgabe = C_ToDo(db_t_aufgabe=n_aufgabe, db_t_erinnertung=n_erinnertung, db_t_bemerkung=n_bemerkung, db_t_faellig=n_faellig)
    F_Datenbank_speicher_aufgabe(n_neue_aufgabe)

def F_Datenbank_hole_alle_aufgaben():
    """
    Datenbankbefehl zum holen aller AUfgaben
    """
    return session.query(C_ToDo).all()

def F_hole_aufgabe(n_todo_id: int):
    """
    Datenbankbefehl zum holen einer AUfgaben mit einer bestimmten ID
    """
    return session.query(C_ToDo).get(n_todo_id)
    
def F_loesche_aufgabe():
    f_todo_id = int(input("Bitte gebe die ID der Aufgabe an: "))
    f_todo = F_hole_aufgabe(f_todo_id)
    console.print(f"Lösche todo {f_todo.db_t_aufgabe} {f_todo.db_t_erinnertung}.", style="red")
    session.delete(f_todo)
    session.commit()

def F_Zeige_alle_aufgaben():
    f_aufgaben = F_Datenbank_hole_alle_aufgaben()
    table = Table(show_header=True, header_style="bold green")
    table.add_column("db_t_todo_id", style="dim")
    table.add_column("db_t_aufgabe")
    table.add_column("db_t_erinnertung")
    table.add_column("db_t_bemerkung")
    table.add_column("db_t_faellig")
    
    for f_todo in f_aufgaben:
        table.add_row(str(f_todo.db_t_todo_id), f_todo.db_t_aufgabe, f_todo.db_t_erinnertung, f_todo.db_t_bemerkung, f_todo.db_t_faellig)

    console.print(table)

    return

def F_Zeige_erledigte_aufgaben():
    return

def F_Zeige_offene_aufgaben():
    return

def F_Zeige_faellige_aufgaben():
    return

def F_markiere_eine_aufgabe_als_erledigt():
    return

def F_veraendere_eine_aufgabe():
    f_todo_id = int(input("Bitte gebe die ID der Aufgabe an: "))
    f_todo = F_hole_aufgabe(f_todo_id)
    f_todo_felder = {}
    
    # Test
    print({f_todo_felder.db_t_aufgabe})
    print(f"todo \t[{f_todo_felder.db_t_aufgabe }]: ")
    # Test

    f_neuer_wert_todo = input(f"todo \t[{f_todo_felder.db_t_aufgabe }]: ")
    if f_neuer_wert_todo:
        f_todo_felder["f_todo_felder.db_t_aufgabe"] = f_neuer_wert_todo

    f_neuer_wert_erinnertung = input(f"erinnertung \t[{f_todo_felder.db_t_erinnertung}]: ")
    if f_neuer_wert_erinnertung:
        f_todo_felder["f_todo_felder.db_t_erinnertung"] = f_neuer_wert_erinnertung

    f_neuer_wert_bemerkung = input(f"Bewwertung \t[{f_todo_felder.db_t_bemerkung}]: ")
    if f_neuer_wert_bemerkung:
        f_todo_felder["f_todo_felder.db_t_bewertung"] = f_neuer_wert_bemerkung

    f_neuer_wert_faellig = input(f"Geburtstag \t[{f_todo_felder.db_t_faellig}]: ")
    if f_neuer_wert_faellig:
        f_todo_felder["f_todo_felder.db_t_geburtstagdatum"] = f_neuer_wert_faellig
  

    console.print(f"\nVerändere todo {f_todo_felder.db_t_aufgabe} {f_todo_felder.db_t_erinnertung}\nVeränderte Bemerkung \t {f_todo_felder.db_t_bemerkung}\nVeränderter Geburtstag \t {f_todo_felder.db_t_geburtstagdatum}.", style="green")
    rueckgabewert_db_erstellt(f_todo, f_todo_felder)


# # # ###########################################
# # # Main
# # # ###########################################
if __name__ == "__main__":
    F_Init_Datenbank()

g_schleife=True

while g_schleife:
    print("""
    ----------------------------------------
    Menu: 
    - (A)  Anlegen einer neuen Aufgabe
    - (L)  Löschen einer Aufgaben
    - (V)  Verändern einer Aufgabe
    - (M)  Markiere eine Aufgabe als erledigt
    - (1)  Zeige alle              Aufgaben
    - (2)  Zeige alle erledigten   Aufgaben
    - (3)  Zeige alle noch offenen Aufgaben
    - (4)  Zeige alle fällige      Aufgaben
    - (E)  Ende des Programmes
        ----------------------------------------
    """)

    g_menuauswahl = input("Wähle bitte eine Operation an: ")
    g_menuauswahl = g_menuauswahl.upper()
    
    if g_menuauswahl == "E":        
        g_schleife=False
    elif g_menuauswahl == "A":        
        F_neue_aufgabe()
    elif g_menuauswahl == "L":        
        F_loesche_aufgabe()
    elif g_menuauswahl == "V":        
        F_veraendere_eine_aufgabe()
    elif g_menuauswahl == "M":        
        F_markiere_eine_aufgabe_als_erledigt()
    elif g_menuauswahl == "1":
        F_Zeige_alle_aufgaben()
    elif g_menuauswahl == "2":        
        F_Zeige_erledigte_aufgaben()
    elif g_menuauswahl == "3":        
        F_Zeige_offene_aufgaben()
    elif g_menuauswahl == "4":        
        F_Zeige_faellige_aufgaben()
    else:
        print("""
        ----------------------------------------
        Bitte nur aus den Zeichen
        A / L / V / M / 1 / 2 / 3 / 4 / E
        wählen
        ----------------------------------------
        """)
        continue

######################
