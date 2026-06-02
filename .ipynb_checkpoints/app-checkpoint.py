from flask import Flask, render_template, flash, redirect, url_for, request

app = Flask(__name__)

app.secret_key = "a_very_secret_key"


post = [
    {
        "id": 1, 
        "title": "شروع کار با پایتون", 
        "body": "پایتون یکی از ساده‌ترین و محبوب‌ترین زبان‌های برنامه‌نویسی است..."
    },
    {
        "id": 2, 
        "title": "چرا وبلاگ می‌سازیم؟", 
        "body": "ساخت وبلاگ بهترین پروژه برای یادگیری مفاهیم اصلی توسعه وب است..."
    },
    {
        "id": 3, 
        "title": "شروع کار با [پایتون]", 
        "body": "پایتون یکی از ساده‌تر ین و محبوب‌ترین زبان‌های برنامه‌نویسی است..."
    },
    {
        "id": 4, 
        "title": "چرا s می‌سازیم؟", 
        "body": "سا خت وبلاگ بهترین پروژه برای یادگیری مفاهیم اصلی توسعه وب است..."
    }
]

# ____ ---- _____

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/blog')
def list_blog():
    return render_template("list_blog.html", posts=post)


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

