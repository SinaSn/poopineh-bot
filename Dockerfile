# استفاده از Python 3.11 به عنوان پایه
FROM python:3.11

# تنظیم متغیرهای محیطی برای جلوگیری از ایجاد فایل‌های pyc و بافر لاگ‌ها
ENV PYTHONUNBUFFERED=1

# تعیین دایرکتوری کار
WORKDIR /app

# کپی کردن فایل‌های پروژه به داخل کانتینر
COPY . /app

# نصب وابستگی‌ها
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# اجرای بات
CMD ["python", "bot.py"]
