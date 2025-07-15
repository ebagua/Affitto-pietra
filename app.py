
import streamlit as st
import calendar
import datetime

# Mesi in italiano
mesi_it = [
    "Gennaio", "Febbraio", "Marzo", "Aprile", "Maggio", "Giugno",
    "Luglio", "Agosto", "Settembre", "Ottobre", "Novembre", "Dicembre"
]

# Stagionalità base per mese (esempio prezzi base)
STAGIONALITA = {
    1: 90, 2: 90, 3: 100, 4: 110, 5: 120, 6: 130,
    7: 140, 8: 150, 9: 140, 10: 120, 11: 100, 12: 95
}

# Sovrapprezzo weekend
SOVRAPPREZZO_WEEKEND = 20

# Date festività/ponti esempio (aggiungi se vuoi)
FESTIVITA = [
    datetime.date(2025, 12, 25),
    datetime.date(2025, 1, 1),
    datetime.date(2025, 4, 25),
    datetime.date(2025, 6, 2),
]

# Percentuale commissioni Booking
COMMISSIONI = 0.25

# Lista date prenotate (esempio)
prenotazioni = []

def main():
    st.set_page_config(page_title="Calcolo Prezzi Affitto Pietra Ligure", layout="wide")
    menu = ["Calcolo Prezzi", "Calendario Prenotazioni"]
    scelta = st.sidebar.selectbox("Seleziona pagina", menu)

    if scelta == "Calcolo Prezzi":
        calcolo_prezzi()
    else:
        calendario_prenotazioni()

def calcolo_prezzi():
    st.title("📆 Calcolo Prezzi Affitto Pietra Ligure")
    oggi = datetime.date.today()

    col1, col2 = st.columns(2)

    with col1:
        mese_selezionato = st.selectbox("Seleziona mese", list(range(1, 13)), format_func=lambda x: mesi_it[x-1], index=oggi.month-1)
        anno_selezionato = st.number_input("Seleziona anno", min_value=2023, max_value=2030, value=oggi.year, step=1)
        giorni_mese = calendar.monthrange(anno_selezionato, mese_selezionato)[1]

        prezzo_base_default = STAGIONALITA.get(mese_selezionato, 100)
        prezzo_base = st.number_input("💰 Prezzo base del mese (€)", min_value=10, max_value=1000, value=prezzo_base_default, step=1)

        giorni_settimana_it = ["Lun", "Mar", "Mer", "Gio", "Ven", "Sab", "Dom"]
        st.markdown("**Prezzi giornalieri**")

        prezzi_giornalieri = []
        totale = 0
        for giorno in range(1, giorni_mese + 1):
            data_corrente = datetime.date(anno_selezionato, mese_selezionato, giorno)
            giorno_settimana = data_corrente.weekday()  # Lun=0 ... Dom=6

            prezzo = prezzo_base

            # Weekend: sabato=5, domenica=6
            if giorno_settimana >= 5:
                prezzo += SOVRAPPREZZO_WEEKEND

            # Festività
            if data_corrente in FESTIVITA:
                prezzo += 30  # sovrapprezzo festività

            prezzi_giornalieri.append(prezzo)
            totale += prezzo

        # Tabella prezzi
        import pandas as pd
        df = pd.DataFrame({
            "Giorno": list(range(1, giorni_mese + 1)),
            "Giorno della settimana": [giorni_settimana_it[(datetime.date(anno_selezionato, mese_selezionato, d).weekday())] for d in range(1, giorni_mese + 1)],
            "Prezzo (€)": prezzi_giornalieri
        })

        st.dataframe(df, height=300)

        # Guadagno netto
        guadagno_netto = totale * (1 - COMMISSIONI)

        st.markdown(f"### Totale prezzo mese: €{totale:.2f}")
        st.markdown(f"### Guadagno netto stimato (–25% commissioni Booking): €{guadagno_netto:.2f}")

    with col2:
        st.markdown("## Info e note")
        st.write("""
        - Puoi modificare il prezzo base per ogni mese.

        - Il prezzo viene aumentato nei weekend e durante festività.

        - Le festività sono esempio, puoi modificarle nel codice.

        - Guadagno netto tiene conto del 25% di commissioni.

        """)

def calendario_prenotazioni():
    import calendar
    import datetime
    import streamlit.components.v1 as components

    st.title("📅 Calendario Prenotazioni")

    oggi = datetime.date.today()
    anno = st.number_input("Anno", min_value=2023, max_value=2030, value=oggi.year, step=1)
    mese = st.selectbox("Mese", list(range(1, 13)), format_func=lambda x: mesi_it[x-1], index=oggi.month-1)

    giorni_mese = calendar.monthrange(anno, mese)[1]

    # Lista prenotazioni esempio (in realtà va collegata a database o file)
    global prenotazioni

    # Selezione date prenotate (aggiorna lista)
    date_selezionate = st.multiselect(
        "Seleziona date prenotate (seleziona i giorni occupati)",
        options=[datetime.date(anno, mese, giorno) for giorno in range(1, giorni_mese + 1)],
        format_func=lambda x: x.strftime("%d %b %Y"),
        default=prenotazioni
    )

    prenotazioni = date_selezionate

    # Costruisci calendario HTML semplice con evidenziazione
    cal = calendar.monthcalendar(anno, mese)

    html_calendar = f"<table border='1' style='border-collapse: collapse; width: 100%; text-align: center;'>"
    html_calendar += f"<tr><th colspan='7' style='background-color:#4CAF50; color: white;'>{mesi_it[mese-1]} {anno}</th></tr>"
    html_calendar += "<tr>" + "".join(f"<th>{g}</th>" for g in ["Lun", "Mar", "Mer", "Gio", "Ven", "Sab", "Dom"]) + "</tr>"

    for settimana in cal:
        html_calendar += "<tr>"
        for giorno in settimana:
            if giorno == 0:
                html_calendar += "<td></td>"
            else:
                data_corrente = datetime.date(anno, mese, giorno)
                if data_corrente in prenotazioni:
                    colore = "red"
                else:
                    colore = "lightgreen"
                html_calendar += f"<td style='background-color:{colore};'>{giorno}</td>"
        html_calendar += "</tr>"

    html_calendar += "</table>"

    components.html(html_calendar, height=250)

if __name__ == "__main__":
    main()
