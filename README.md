# مدیریت دخل‌وخرج | Daily Expense Tracker

یک اپلیکیشن دسکتاپ دوزبانه (فارسی و انگلیسی) برای ثبت و مدیریت درآمد و هزینه‌های روزانه، ساخته‌شده با **Python، Tkinter و SQLite**.

A bilingual Persian and English desktop application for tracking daily income and expenses, built with **Python, Tkinter, and SQLite**.

## امکانات | Features

- انتخاب زبان فارسی یا انگلیسی هنگام اجرای برنامه
- رابط کاربری راست‌چین برای فارسی و چپ‌چین برای انگلیسی
- ثبت و پیگیری درآمد و هزینه
- نمایش خلاصه موجودی، درآمد و هزینه
- پشتیبانی از تومان در حالت فارسی و دلار در حالت انگلیسی
- تاریخ شمسی در حالت فارسی و میلادی در حالت انگلیسی
- دسته‌بندی و جست‌وجوی تراکنش‌ها
- امکان انتخاب دسته «سایر» و تعریف دسته دلخواه
- حذف تراکنش‌ها
- ذخیره‌سازی محلی اطلاعات با SQLite

### Features

- Choose Persian or English at startup
- Right-to-left Persian and left-to-right English interface
- Record and track income and expenses
- View balance, income, and expense summaries
- Toman for Persian mode and USD for English mode
- Jalali dates in Persian mode and Gregorian dates in English mode
- Transaction categories and search
- Custom categories using the “Other” option
- Delete transactions
- Local data storage with SQLite

## اجرای برنامه در ویندوز | Windows Application

نسخه آماده ویندوز در فایل زیر قرار دارد:

`DailyExpenseTracker.exe`

فایل را دانلود کنید و با دوبار کلیک اجرا کنید. برای اجرای این نسخه نیازی به نصب Python نیست.

Download `DailyExpenseTracker.exe` and double-click it to run the application. Python is not required for this executable version.

## اجرای کد پایتون | Run from Source

Python 3.10 or newer is required.

```bash
python -m pip install -r requirements.txt
python daily_expense_tracker.py
```

## پیش‌نیازها | Requirements

- Python 3.10 or newer (only when running from source)
- jdatetime

## محل ذخیره اطلاعات | Data Storage

اطلاعات برنامه به‌صورت محلی در مسیر زیر ذخیره می‌شوند و نباید داخل GitHub بارگذاری شوند:

`~/.daily_expense_tracker/expenses.db`

Application data is stored locally and should not be uploaded to GitHub.

## مجوز استفاده | License

See the `LICENSE` file for license details.
