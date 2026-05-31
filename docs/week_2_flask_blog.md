# هفته دوم – ساخت وبلاگ با Flask (دوره nab+)

این فایل شامل راهنمای گام‌به‌گام و کدهای کامل هفته دوم برای ساخت یک وبلاگ ساده، از داده‌های دستی تا اتصال به دیتابیس است.

---

## فهرست موضوعات
۱) هدف این هفته
۲) گام اول: شروع با داده‌های دستی (Mock Data)
۳) گام دوم: ساخت صفحه جزئیات پست (Dynamic Routing)
۴) گام سوم: بیس HTML و ارث‌بری قالب‌ها (Template Inheritance)
۵) گام چهارم: فرم تماس ساده (دریافت داده بدون دیتابیس)
۶) گام پنجم: ورود دیتابیس (Flask-SQLAlchemy) و ساخت مدل‌ها
۷) گام ششم: متصل کردن وبلاگ و فرم تماس به دیتابیس
۸) جمع‌بندی مفاهیم مهم هفته دوم
۹) تمرین پیشنهادی

---

## ۱) هدف این هفته
در این هفته می‌خواهیم یک سیستم وبلاگ بسیار ساده بسازیم. روند کار به این صورت است که ابتدا داده‌ها را به صورت هاردکد (دستی) در پایتون تعریف می‌کنیم و به فرانت‌اند می‌فرستیم، سپس ساختار قالب‌های HTML را بهینه می‌کنیم، یک فرم تماس ساده می‌سازیم و در نهایت با معرفی دیتابیس SQLite، تمام اطلاعات را به دیتابیس واقعی متصل می‌کنیم.

> **نکته:** در این هفته نیازی به ثبت‌نام، لاگین و مدیریت کاربران (User Authentication) نداریم و روی یادگیری مفاهیم پایه کار با داده‌ها تمرکز می‌کنیم.

---

## ۲) گام اول: شروع با داده‌های دستی (Mock Data)
در اولین مرحله، دیتابیسی در کار نیست. یک لیست از دیکشنری‌ها در پایتون می‌سازیم که نقش پست‌های وبلاگ ما را بازی می‌کنند.

### فایل `app.py`
```python
from flask import Flask, render_template

app = Flask(__name__)

# داده‌های دستی (پست‌های وبلاگ)
posts = [
    {
        "id": 1, 
        "title": "شروع کار با پایتون", 
        "content": "پایتون یکی از ساده‌ترین و محبوب‌ترین زبان‌های برنامه‌نویسی است..."
    },
    {
        "id": 2, 
        "title": "چرا وبلاگ می‌سازیم؟", 
        "content": "ساخت وبلاگ بهترین پروژه برای یادگیری مفاهیم اصلی توسعه وب است..."
    }
]

@app.route("/")
def home():
    # فرستادن لیست پست‌ها به فایل HTML
    return render_template("home.html", posts=posts)

if __name__ == "__main__":
    app.run(debug=True)
```

### فایل `templates/home.html`
```html
<!doctype html>
<html lang="fa">
<head>
    <meta charset="UTF-8">
    <title>صفحه اصلی وبلاگ</title>
</head>
<body>
    <h1>به وبلاگ ساده من خوش آمدید</h1>
    <hr>

    {# حلقه برای چرخیدن روی تک‌تک پست‌ها #}
    {% for post in posts %}
        <h2>{{ post.title }}</h2>
        <p>{{ post.content }}</p>
        <hr>
    {% endfor %}
</body>
</html>
```

---

## ۳) گام دوم: ساخت صفحه جزئیات پست (Dynamic Routing)
حالا می‌خواهیم وقتی کاربر روی یک پست کلیک می‌کند یا آدرس مشخصی مثل `/post/1` را وارد می‌کند، فقط همان پست نمایش داده شود.

### فایل `app.py`
```python
from flask import Flask, render_template

app = Flask(__name__)

posts = [
    {"id": 1, "title": "شروع کار با پایتون", "content": "پایتون یکی از ساده‌ترین و محبوب‌ترین زبان‌های برنامه‌نویسی است..."},
    {"id": 2, "title": "چرا وبلاگ می‌سازیم؟", "content": "ساخت وبلاگ بهترین پروژه برای یادگیری مفاهیم اصلی توسعه وب است..."}
]

@app.route("/")
def home():
    return render_template("home.html", posts=posts)

# مسیر پویا برای دریافت آیدی هر پست
@app.route("/post/<int:post_id>")
def post_detail(post_id):
    # پیدا کردن پست مورد نظر بر اساس آیدی در لیست دستی
    post = next((p for p in posts if p["id"] == post_id), None)
    return render_template("post.html", post=post)

if __name__ == "__main__":
    app.run(debug=True)
```

### فایل `templates/post.html`
```html
<!doctype html>
<html lang="fa">
<head>
    <meta charset="UTF-8">
    <title>{{ post.title }}</title>
</head>
<body>
    <h1>{{ post.title }}</h1>
    <p>{{ post.content }}</p>
    <br>
    <a href="/">بازگشت به صفحه اصلی</a>
</body>
</html>
```

---

## ۴) گام سوم: بیس HTML و ارث‌بری قالب‌ها (Template Inheritance)
برای اینکه کدهای تکراری HTML (مثل تگ‌های `<html>` و `<body>`) را در هر فایل دوباره ننویسیم، یک قالب پایه به نام `base.html` تعریف می‌کنیم و بقیه صفحات از آن ارث‌بری می‌کنند.

### ساختار پوشه پروژه
```text
project/
├── app.py
└── templates/
    ├── base.html
    ├── home.html
    └── post.html
```

### فایل `templates/base.html`
```html
<!doctype html>
<html lang="fa">
<head>
    <meta charset="UTF-8">
    <title>وبلاگ من</title>
</head>
<body>
    <!-- هدر ساده سایت -->
    <header>
        <nav>
            <a href="/">خانه</a> | 
            <a href="/contact">تماس با ما</a>
        </nav>
    </header>
    <hr>

    <!-- بخش متغیر صفحات دیگر -->
    {% block content %}{% endblock %}

    <hr>
    <footer>
        <p>تمامی حقوق محفوظ است © 2026</p>
    </footer>
</body>
</html>
```

### فایل به‌روزشده `templates/home.html`
```html
{% extends "base.html" %}

{% block content %}
    <h1>آخرین نوشته‌ها</h1>
    
    {% for post in posts %}
        <h2><a href="{{ url_for('post_detail', post_id=post.id) }}">{{ post.title }}</a></h2>
        <p>{{ post.content }}</p>
    {% endfor %}
{% endblock %}
```

### فایل به‌روزشده `templates/post.html`
```html
{% extends "base.html" %}

{% block content %}
    <h1>{{ post.title }}</h1>
    <p>{{ post.content }}</p>
{% endblock %}
```

---

## ۵) گام چهارم: فرم تماس ساده (دریافت داده بدون دیتابیس)
در این بخش یک فرم تماس ساده می‌سازیم تا کاربر بتواند نام و پیام خود را ارسال کند. در این مرحله فقط داده را دریافت و در کنسول چاپ می‌کنیم.

### فایل `app.py` (اضافه شدن بخش تماس)
```python
from flask import Flask, render_template, request

app = Flask(__name__)

# ... (همان داده‌های قبلی پست‌ها) ...

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        # دریافت اطلاعات ارسال شده از فرم HTML
        name = request.form.get("name")
        message = request.form.get("message")
        
        # چاپ موقت در ترمینال برای تست
        print(f"پیام جدید از {name}: {message}")
        
    return render_template("contact.html")
```

### فایل `templates/contact.html`
```html
{% extends "base.html" %}

{% block content %}
    <h1>تماس با ما</h1>
    
    <form method="POST">
        <label>نام شما:</label><br>
        <input type="text" name="name" required><br><br>
        
        <label>پیام شما:</label><br>
        <textarea name="message" required></textarea><br><br>
        
        <button type="submit">ارسال پیام</button>
    </form>
{% endblock %}
```

---

## ۶) گام پنجم: ورود دیتابیس (Flask-SQLAlchemy) و ساخت مدل‌ها
حالا نوبت به ذخیره واقعی اطلاعات می‌رسد. برای این کار از کتابخانه `flask_sqlalchemy` و دیتابیس پیش‌فرض لینوکس و پایتون یعنی `SQLite` استفاده می‌کنیم.

### نصب کتابخانه دیتابیس
```bash
pip install flask-sqlalchemy
```

### تعریف مدل‌ها
دو جدول می‌سازیم:
1. `Post`: برای ذخیره پست‌های وبلاگ (بدون اتصال به یوزر).
2. `Contact`: برای ذخیره پیام‌های فرم تماس.

```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# آدرس‌دهی فایل دیتابیس SQLite در ریشه پروژه
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# مدل پست‌های وبلاگ
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)

# مدل فرم تماس با ما
class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    message = db.Column(db.Text, nullable=False)
```

---

## ۷) گام ششم: متصل کردن وبلاگ و فرم تماس به دیتابیس
در گام آخر، تمام کدها را با هم ترکیب می‌کنیم. کدهای دستی قبلی را کاملاً حذف کرده و دستورات خواندن و نوشتن دیتابیس را جایگزین می‌کنیم.

### کد نهایی و یکپارچه `app.py`
```python
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# --- مدل‌های دیتابیس ---
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    message = db.Column(db.Text, nullable=False)

# --- ایجاد جداول دیتابیس ---
# این دستور تضمین می‌کند که اگر دیتابیس وجود نداشت، در اولین اجرا ساخته شود.
with app.app_context():
    db.create_all()
    
    # اضافه کردن چند پست نمونه در اولین اجرای دیتابیس (در صورت خالی بودن)
    if Post.query.count() == 0:
        sample1 = Post(title="اولین پست در دیتابیس", content="این متن مستقیماً از دیتابیس لود شده است.")
        sample2 = Post(title="آموزش دیتابیس در فلسک", content="کارهای دیتابیس با SQLAlchemy بسیار ساده است.")
        db.session.add(sample1)
        db.session.add(sample2)
        db.session.commit()

# --- مسیرها (Routes) ---

@app.route("/")
def home():
    # دریافت تمام پست‌ها از دیتابیس به جای لیست دستی
    all_posts = Post.query.all()
    return render_template("home.html", posts=all_posts)

@app.route("/post/<int:post_id>")
def post_detail(post_id):
    # پیدا کردن پست در دیتابیس یا نمایش خطای ۴۰۴ در صورت عدم وجود
    post = Post.query.get_or_404(post_id)
    return render_template("post.html", post=post)

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        user_name = request.form.get("name")
        user_message = request.form.get("message")
        
        # ذخیره پیام جدید در دیتابیس
        new_message = Contact(name=user_name, message=user_message)
        db.session.add(new_message)
        db.session.commit()
        
        # انتقال کاربر به صفحه اصلی پس از ارسال موفقیت‌آمیز فرم
        return redirect(url_for("home"))
        
    return render_template("contact.html")

if __name__ == "__main__":
    app.run(debug=True)
```

---

## ۸) جمع‌بندی مفاهیم مهم هفته دوم
در پایان این هفته شما به مفاهیم زیر مسلط شده‌اید:
- **داده‌های ساختاریافته در وب:** چگونگی ارسال مجموعه‌ای از داده‌ها از پایتون به تمپلیت‌های HTML.
- **ارث‌بری قالب‌ها (Template Inheritance):** استفاده از `base.html` برای جلوگیری از نوشتن کدهای تکراری فرانت‌اند.
- **پرداختن به درخواست‌های POST:** چگونگی هندل کردن متدهای ارسال فرم‌های وب.
- **مفهوم ORM و کار با دیتابیس:** ایجاد جداول، ذخیره کردن داده‌ها (`db.session.add`) و کوئری گرفتن از آن‌ها بدون استفاده از زبان مستقیم SQL.

---

## ۹) تمرین پیشنهادی
برای تسلط کامل بر مباحث این هفته، موارد زیر را انجام دهید:
1. پروژه را به طور کامل در سیستم خود راه‌اندازی و اجرا کنید.
2. یک صفحه جدید به نام `/admin` بسازید که شامل یک فرم ساده برای «اضافه کردن پست جدید به وبلاگ» باشد و بتواند پست‌های جدید را به جدول `Post` اضافه کند.
3. با استفاده از دستوراتی که در هفته اول خواندید، برای ارسال موفقیت‌آمیز فرم تماس یا افزودن پست، یک **Flash Message** به کاربر نشان دهید.
