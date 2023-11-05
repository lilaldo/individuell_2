from flask import Flask, render_template, request
import requests

app = Flask(__name__)


@app.route("/")
@app.route("/start")
def startsida():
    return render_template('form.html')


@app.route("/elpriser", methods=["POST", "GET"])
def api_post():
    if request.method == "POST":
        selected_date = request.form["selectedDate"]
        date_parts = selected_date.split('-')
        year = date_parts[0]
        formatted_date = f"{year}/{date_parts[1]}-{date_parts[2]}"
        price = request.form["PRISKLASS"].upper()
        api_url = f"https://www.elprisetjustnu.se/api/v1/prices/{formatted_date}_{price}.json"

        try:
            response = requests.get(api_url)
            if response.status_code == 200:
                data = response.json()
                return render_template('form.html', data=data, selected_date=selected_date, year=year, price=price)
            else:
                api_error = True  # Sätt flaggvariabeln till True om API-anropet misslyckades
        except requests.exceptions.RequestException as e:
            api_error = True  # Sätt flaggvariabeln till True om API-anropet misslyckades

        # Om API-anropet misslyckades, returnera felkod.html istället
        if api_error:
            return render_template('felkod.html', year=year, error_message="API-anropet misslyckades")

    else:
        # Visa sidan som vanligt om det inte är en POST-förfrågan
        return render_template('form.html')


def page_not_found(e):
    return "404 - Sidan kunde inte hittas.", 404


if __name__ == "__main__":
    app.run(debug=True)
