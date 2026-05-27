# جلسه اول – شروع سریع با Flask (دوره nab+)

این فایل شامل تمام مطالب مطرح‌شده درباره شروع کار با Flask، قالب‌ها، مسیرها، فلش‌مسج، ریدایرکت و JSON است.

---

## ۱) نصب Flask

برای نصب Flask:

```bash
pip install flask
```

---

## ۲) اولین برنامه Flask (Hello World)

فایل `app.py`:

```python
from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>سلام! اولین سرور فلسک من اجرا شد.</p>"

if __name__ == "__main__":
    app.run(debug=True)
```

### توضیح خط‌به‌خط

- `from flask import Flask`  
  کلاس `Flask` را از کتابخانه Flask وارد می‌کند.
- `app = Flask(__name__)`  
  یک شیء برنامه می‌سازد.
- `@app.route("/")`  
  مسیر ریشه سایت را تعریف می‌کند.
- `def hello_world():`  
  تابعی که وقتی کاربر به `/` می‌رود اجرا می‌شود.
- `app.run(debug=True)`  
  سرور را در حالت توسعه اجرا می‌کند.

### اجرا

```bash
python app.py
```

سپس در مرورگر:

```text
http://127.0.0.1:5000
```

---

## ۳) مسیریابی پویا

مثال:

```python
@app.route("/user/<username>")
def show_user(username):
    return f"سلام کاربر عزیز، خوش آمدی: {username}"
```

اگر آدرس زیر را باز کنید:

```text
/user/Ali
```

خروجی می‌شود:

```text
سلام کاربر عزیز، خوش آمدی: Ali
```

---

## ۴) استفاده از Template در Flask

برای ساخت صفحات HTML از پوشه `templates` استفاده می‌کنیم.

### ساختار پروژه

```text
project/
├── app.py
└── templates/
    └── index.html
```

### فایل `app.py`

```python
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html", name="حاجی")

if __name__ == "__main__":
    app.run(debug=True)
```

### فایل `templates/index.html`

```html
<!doctype html>
<html lang="fa">
<head>
    <meta charset="UTF-8">
    <title>صفحه اصلی</title>
</head>
<body>
    <h1>سلام {{ name }} 👋</h1>
</body>
</html>
```

### توضیح Jinja2

- `{{ name }}`  
  مقدار متغیر `name` را داخل HTML چاپ می‌کند.
- `render_template(...)`  
  فایل HTML را با داده‌های پایتون رندر می‌کند.

---

## ۵) چند صفحه و لینک بین آن‌ها

### فایل `app.py`

```python
from flask import Flask, render_template, url_for

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

if __name__ == "__main__":
    app.run(debug=True)
```

### فایل `templates/index.html`

```html
<!doctype html>
<html lang="fa">
<head>
    <meta charset="UTF-8">
    <title>خانه</title>
</head>
<body>
    <h1>صفحه اصلی</h1>
    <a href="{{ url_for('about') }}">رفتن به صفحه درباره ما</a>
</body>
</html>
```

### فایل `templates/about.html`

```html
<!doctype html>
<html lang="fa">
<head>
    <meta charset="UTF-8">
    <title>درباره ما</title>
</head>
<body>
    <h1>درباره ما</h1>
    <a href="{{ url_for('home') }}">بازگشت به صفحه اصلی</a>
</body>
</html>
```

### چرا `url_for` بهتر است؟

چون اگر مسیر `/about` را بعداً تغییر دهید، فقط در پایتون مسیر را عوض می‌کنید و لینک‌ها خودکار به‌روز می‌شوند.

---

## ۶) Flash Messages و Redirect

### نکته مهم

برای استفاده از `flash` باید `secret_key` تنظیم شود.

### فایل `app.py`

```python
from flask import Flask, flash, redirect, url_for, render_template

app = Flask(__name__)
app.secret_key = "secret-key-خیالی"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/submit")
def submit():
    flash("عملیات با موفقیت انجام شد ✅", "success")
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)
```

### نمایش پیام در قالب HTML

```html
<!doctype html>
<html lang="fa">
<head>
    <meta charset="UTF-8">
    <title>خانه</title>
</head>
<body>
    {% with messages = get_flashed_messages(with_categories=true) %}
        {% if messages %}
            <ul>
            {% for category, message in messages %}
                <li><strong>{{ category }}:</strong> {{ message }}</li>
            {% endfor %}
            </ul>
        {% endif %}
    {% endwith %}

    <h1>صفحه اصلی</h1>
</body>
</html>
```

### توضیح

- `flash(...)`  
  یک پیام موقت برای نمایش بعدی ذخیره می‌کند.
- `redirect(...)`  
  کاربر را به مسیر دیگر می‌فرستد.
- `get_flashed_messages()`  
  پیام‌های ذخیره‌شده را در قالب می‌گیرد.

---

## ۷) ساخت JSON و API

Flask به‌راحتی می‌تواند خروجی JSON بدهد.

### فایل `app.py`

```python
from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/api/user")
def get_user():
    return jsonify({
        "id": 1,
        "name": "Ali",
        "role": "admin"
    })

if __name__ == "__main__":
    app.run(debug=True)
```

### خروجی

```json
{
  "id": 1,
  "name": "Ali",
  "role": "admin"
}
```

### کاربرد

این روش برای ساخت API، ارسال داده به فرانت‌اند، یا ارتباط با اپلیکیشن‌های دیگر استفاده می‌شود.

---

## ۸) جمع‌بندی مفاهیم مهم

- **Flask**: فریم‌ورک وب سبک و ساده برای پایتون
- **Route**: مسیرهای سایت
- **Template**: فایل HTML داینامیک
- **Jinja2**: موتور قالب Flask
- **`url_for`**: ساخت لینک امن و استاندارد
- **`flash`**: پیام موقت برای کاربر
- **`redirect`**: انتقال کاربر به صفحه دیگر
- **`jsonify`**: تولید خروجی JSON

---

## ۹) تمرین پیشنهادی

برای تمرین، این موارد را خودتان بسازید:

1. یک صفحه `contact` بسازید.
2. در آن یک فرم ساده قرار دهید.
3. بعد از ارسال فرم، یک پیام `flash` نشان دهید.
4. یک API جدید برای لیست کاربران بسازید.
5. با `url_for` بین همه صفحات لینک بزنید.

---

## ۱۰) مسیر ادامه یادگیری

در جلسه‌های بعدی می‌توانید این موضوعات را یاد بگیرید:

- کار با فرم‌ها و اعتبارسنجی
- دیتابیس با SQLite و SQLAlchemy
- لاگین و ثبت‌نام
- Session و Cookie
- Blueprint برای ساختار بهتر پروژه
- مدیریت فایل‌ها
- ساخت پروژه واقعی Flask

---

پایان فایل جلسه اول nab+
