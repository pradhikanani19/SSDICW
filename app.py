import numpy as np
from scipy.stats import t
from statistics import stdev
from flask import Flask, request, jsonify, send_from_directory

app = Flask(__name__)

def two_sample(a, b, alternative):

    xbar1 = np.mean(a)
    xbar2 = np.mean(b)

    sd1 = stdev(a)
    sd2 = stdev(b)

    n1 = len(a)
    n2 = len(b)

    alpha = 0.05 / 2
    df = n1 + n2 - 2

    se = np.sqrt((sd1**2) / n1 + (sd2**2) / n2)

    t_table_pos = t.ppf(1 - alpha, df)
    t_table_neg = t.ppf(alpha, df)

    tcal = ((xbar1 - xbar2) - 0) / se

    if alternative == "two-sided":
        p_value = 2 * (1 - t.cdf(abs(tcal), df))
    elif alternative == "left":
        p_value = t.cdf(tcal, df)
    elif alternative == "right":
        p_value = 1 - t.cdf(tcal, df)
    else:
        p_value = None

    return {
        "t_calculated": float(tcal),
        "t_table_positive": float(t_table_pos),
        "t_table_negative": float(t_table_neg),
        "p_value": float(p_value)
    }


@app.route("/")
def home():
    return send_from_directory(".", "index.html")


@app.route("/calculate", methods=["POST"])
def calculate():

    data = request.get_json()

    sample1 = data["sample1"]
    sample2 = data["sample2"]
    alternative = data["alternative"]

    result = two_sample(sample1, sample2, alternative)

    return jsonify(result)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)