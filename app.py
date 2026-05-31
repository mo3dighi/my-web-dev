from flask import Flask, render_template, flash, redirect, url_for, request

app = Flask(__name__)

app.secret_key = "a_very_secret_key"
# ____ ---- _____

@app.route('/')
def home():
    return render_template("index.html")


@app.route('/contact', methods=['POST','GET'])
def contact():
    if request.method == "POST":
        name = request.form.get('fulname')
        if not name:
            flash('اسم را وارد کنید ❌', "danger")
        else:
            flash(f"{name} جان با فورم با موفقیت ثبت شد ✅", "success")

    return render_template("contact.html")
 

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/submit')
def submit():
    flash("عملیات با موفقیت انجام شد ✅", "danger")
    return redirect(url_for('home'))
# ____ ----- ______

if __name__ == "__main__":
    app.run(debug=True)

