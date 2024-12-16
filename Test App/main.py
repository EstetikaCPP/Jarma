from flask import Flask, request, render_template
import pickle

app = Flask(__name__)

model_SQL = None
model_XSS = None
feature_extraction_SQL = None
feature_extraction_XSS = None

@app.before_request
def load_pickle():
    global model_SQL
    global model_XSS
    global feature_extraction_SQL
    global feature_extraction_XSS
    if model_SQL is None:
        model_SQL = pickle.load(open('SqlInjectionLR.pkl', 'rb'))
    if feature_extraction_SQL is None:
        feature_extraction_SQL = pickle.load(open("Vectorizer.pkl", "rb"))
    if model_XSS is None:
        model_XSS = pickle.load(open('XSSInjectionLR.pkl', 'rb'))
    if feature_extraction_XSS is None:
        feature_extraction_XSS = pickle.load(open("Vectorizer_XSS.pkl", "rb"))


def transorm_and_predict(data):
    global model_SQL
    global model_XSS
    global feature_extraction_SQL
    global feature_extraction_XSS
    data_SQL = [data]
    data_XSS = [data]
    answ_SQL = feature_extraction_SQL.transform(data_SQL)
    if model_SQL.predict(answ_SQL)[0] == 1:
        return "SQL"
    answ_XSS = feature_extraction_XSS.transform(data_XSS)
    if model_XSS.predict(answ_XSS)[0] == 1:
        return "XSS"
    return 

@app.route("/", methods=["GET", "POST"])
def main():
    result = 123
    if request.method == "POST":
        result = transorm_and_predict(request.form["username"])
        if result == "SQL":
            error = "SQL Injection Detected!!!"
            return render_template("main.html", error=error)
        elif result == "XSS":
            error = "XSS Detected!!!"
            return render_template("main.html", error=error)
        else:
            return render_template("main.html")
    return render_template("main.html")

if __name__ == "__main__":
    app.run(debug=True)
    

