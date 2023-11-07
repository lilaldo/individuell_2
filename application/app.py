from flask import Flask, render_template, request, redirect, url_for
import requests

app = Flask(__name__)

"""Startsida. Fungerar på samma sätt som /elpriser men att man som användaren kommer till en tom sida ger ett mer städat intryck."""


@app.route("/")
@app.route("/start")
def startsida():
    return render_template('form.html')


"""Här definieras en route som svarar på både POST- och GET-förfrågningar till endpointen "/elpriser". 
Denna funktion kommer att köras oavsett om det är en POST- eller GET-förfrågan till denna URL."""


@app.route("/elpriser", methods=["POST", "GET"])
def api_post():
    # Koden kollas om den inkommande förfrågan är en http post, i sådana fall fortsätter koden köras.
    if request.method == "POST":
        # Datum hämtas och sparas.
        selected_date = request.form["selectedDate"]
        # Det sparade datumet delas upp genom att splitta det med ett bindesträck för att passa in i url för api:n
        date_parts = selected_date.split('-')
        year = date_parts[0]
        formatted_date = f"{year}/{date_parts[1]}-{date_parts[2]}"
        # Värdet för prisklassen hämtas upp. Metod adderad för att både input ska fungera med och utan versaler.
        price = request.form["PRISKLASS"].upper()
        # URL skapas för anropet till api och justeras beroende på input från användaren med f-string.
        api_url = f"https://www.elprisetjustnu.se/api/v1/prices/{formatted_date}_{price}.json"

        try:
            # Gör en GET-förfrågan till api med den f-strängade URL:en.
            response = requests.get(api_url)
            # Kontrollerar att svarskoden är 200, det vill säga OK.
            if response.status_code == 200:
                # Om svarskoden är 200, hämta JSON-data från API-svaret.
                data = response.json()
                # Användaren tas till form.html med data från API-svaret samt valt datum och prisklass.
                return render_template('form.html', data=data, selected_date=selected_date, year=year, price=price)
            else:
                # Om svarskoden inte är 200 markeras api_error som True.
                api_error = True
        except requests.exceptions.RequestException as e:
            # Om svarskoden inte är 200 markeras api_error som True.
            api_error = True

        # Om api_error blir True tas användaren till endpoint för errors och får där hjälp.
        if api_error:
            return render_template('felkod.html', year=year, error_message="API-anropet misslyckades")

    else:
        # Visar sidan som vanligt om det inte är en POST-förfrågan
        return render_template('form.html')


# Felhantering

"""I den här delen tas olika former av error hand om. 
Bland annat om användaren skulle komma till en okänd endpoint eller skriva in ogiltig information."""


# Skulle användaren komma till en okänd endpoint så visas ett meddelande samt en knapp för att ta sig tillbaka
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


# Om användaren på något sätt skriver datumet eller prisklassen på ett ogiltigt sätt.
@app.errorhandler(IndexError)
def indexerror(e):
    return render_template('felkod.html'), 404


"""Det svåraste med denna delen var att komma fram till logiken felhantering kontra kod."""
"""Satt i timmar och försökte hitta ett fail i pytest till index-error, det visade sig att jag glömt skriva 404 efter"""

if __name__ == "__main__":
    app.run(debug=True)

