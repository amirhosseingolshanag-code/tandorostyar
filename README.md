# تندرست‌یار — نسخه آماده انتشار روی Render

## انتشار روی Render

1. ZIP را Extract کنید و تمام محتویات پوشه `tandorostyar` را در ریشه یک repository جدید GitHub قرار دهید؛ `manage.py` باید در ریشه repository باشد.
2. در Render یک PostgreSQL database بسازید. دیتابیس و Web Service را در یک Region قرار دهید.
3. یک Web Service جدید بسازید و repository را متصل کنید.
4. تنظیمات سرویس:
   - Runtime: Python
   - Build Command: `bash build.sh`
   - Start Command: `gunicorn config.wsgi:application`
5. در Environment Variables این موارد را تنظیم کنید:
   - `DATABASE_URL`: مقدار **Internal Database URL** دیتابیس Render
   - `SECRET_KEY`: مقدار محرمانه قوی (Generate در Render)
   - `DEBUG`: `False`
   - `ALLOWED_HOSTS`: نام دامنه Render، مانند `tandorostyar.onrender.com`
   - `CSRF_TRUSTED_ORIGINS`: آدرس کامل HTTPS، مانند `https://tandorostyar.onrender.com`
6. Deploy را بزنید و منتظر پایان Build بمانید.

## ساخت مدیر سایت
پس از Deploy موفق، از صفحه سرویس Render بخش Shell را باز کنید و اجرا کنید:
`python manage.py createsuperuser`

پنل مدیریت: `https://YOUR-SERVICE.onrender.com/admin/`

## اجرای محلی ویندوز
```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe manage.py makemigrations
.\.venv\Scripts\python.exe manage.py migrate
.\.venv\Scripts\python.exe manage.py runserver
```

## نکات تولید
- برای سایت عمومی از PostgreSQL استفاده کنید، نه SQLite محلی.
- تصاویر در نسخه فعلی داخل `media/` ذخیره می‌شوند. فایل‌سیستم سرویس Render به‌طور پیش‌فرض پایدار نیست؛ برای نگهداری دائمی تصاویر باید Persistent Disk یا Object Storage خصوصی تنظیم شود. تصاویر بدن کاربران نباید عمومی باشند.
- قبل از استفاده واقعی، کنترل دسترسی تصاویر، محدودیت نوع و حجم فایل، سیاست حریم خصوصی و حذف داده را تکمیل کنید.
- برنامه غذایی نمونه و آموزشی است و جایگزین توصیه متخصص تغذیه نیست.
- سرویس رایگان Render ممکن است پس از ۱۵ دقیقه بی‌استفاده ماندن به خواب برود و اولین درخواست بعدی با تأخیر پاسخ دهد.
