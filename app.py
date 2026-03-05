import numpy as np
from scipy.stats import t
from statistics import stdev
from scipy import stats
from flask import Flask

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
        "t_calculated": tcal,
        "t_table_positive": t_table_pos,
        "t_table_negative": t_table_neg,
        "p_value": p_value
    }


@app.route("/")
def home():
    return "Two Sample T-Test App is Running!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
