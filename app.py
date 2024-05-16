from flask import Flask, render_template
from datetime import datetime
import requests

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html", launches=launches)


def fetch_spacex_launches():
    url = "https://api.spacexdata.com/v4/launches"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return []


# def is_success(Launches):
#     return Launch["success"] and not Launch["upcoming"]
# replaced by the Lambda function!


def categorize_launches(Launches):
    successful = list(filter(lambda x: x["success"] and not x["upcoming"], Launches))
    failed = list(filter(lambda x: not x["success"] and not x["upcoming"], Launches))
    upcoming = list(filter(lambda x: x["upcoming"], Launches))

    return {
        "successful": successful,
        "failed": failed,
        "upcoming": upcoming
    }


launches = categorize_launches(fetch_spacex_launches())

if __name__ == "__main__":
    app.run(debug=True)
