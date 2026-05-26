from flask import Flask, render_template

app = Flask(__name__)
# ____ ---- _____


@app.route("/sum/<x>/<y>")
def sum(x,y):
    return f"<h> {x} + {y} =  {int(x) + int(y)}!</h>"

@app.route("/<names>/<num>")
def account(names, num):
    response = int(num) - 18
    return render_template("index.html", name=names, age=response) 

# ____ ----- ______

if __name__ == "__main__":
    app.run(debug=True)

