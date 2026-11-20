
import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date, datetime
from pathlib import Path

try:
    import jdatetime
except ImportError:
    jdatetime = None

DATA_DIR = Path.home() / ".daily_expense_tracker"
DATA_DIR.mkdir(parents=True, exist_ok=True)

DB = DATA_DIR / "expenses.db"

BG = "#F3F6FB"
WHITE = "#FFFFFF"
NAVY = "#172554"
BLUE = "#2563EB"
GREEN = "#059669"
RED = "#DC2626"
MUTED = "#64748B"
BORDER = "#E2E8F0"

FONT = "Tahoma"

PERSIAN_DIGITS = str.maketrans(
    "۰۱۲۳۴۵۶۷۸۹٠١٢٣٤٥٦٧٨٩",
    "01234567890123456789"
)

EXPENSE_CATEGORIES = {
    "fa": [
        "خوراک", "حمل‌ونقل", "قبوض", "خرید",
        "درمان", "آموزش", "هدیه", "سایر"
    ],
    "en": [
        "Food", "Transport", "Bills", "Shopping",
        "Healthcare", "Education", "Gifts", "Other"
    ]
}

INCOME_CATEGORIES = {
    "fa": ["حقوق", "هدیه", "فروش", "سایر"],
    "en": ["Salary", "Gift", "Sales", "Other"]
}

CATEGORY_MAP = {
    "Food": "خوراک",
    "Transport": "حمل‌ونقل",
    "Bills": "قبوض",
    "Shopping": "خرید",
    "Healthcare": "درمان",
    "Education": "آموزش",
    "Gifts": "هدیه",
    "Other": "سایر",
    "Salary": "حقوق",
    "Sales": "فروش"
}

CATEGORY_EN = {
    value: key for key, value in CATEGORY_MAP.items()
}

TEXTS = {
    "fa": {
        "app": "مدیریت دخل‌وخرج",
        "subtitle": "مدیریت هوشمند درآمد و هزینه",
        "income": "درآمد (Income)",
        "expense": "هزینه (Expense)",
        "balance": "موجودی (Balance)",
        "total_income": "مجموع درآمد (Total Income)",
        "total_expense": "مجموع هزینه (Total Expense)",
        "transaction": "ثبت تراکنش (Add Transaction)",
        "type": "نوع تراکنش (Type)",
        "title": "عنوان (Title)",
        "category": "دسته‌بندی (Category)",
        "amount": "مبلغ (Amount)",
        "date": "تاریخ (Date)",
        "note": "یادداشت (Note)",
        "add": "＋ ثبت تراکنش (Add)",
        "clear": "پاک کردن فرم (Clear)",
        "search": "جست‌وجو / Search",
        "records": "تراکنش‌های ثبت‌شده (Transactions)",
        "delete": "حذف مورد انتخاب‌شده (Delete)",
        "footer": "اطلاعات روی همین دستگاه ذخیره می‌شود.",
        "other_name": "نام دسته‌بندی دلخواه (Custom Category)",
        "expense_type": "هزینه (Expense)",
        "income_type": "درآمد (Income)",
        "id": "شناسه (ID)",
        "success": "ثبت موفق (Success)",
        "saved": "تراکنش با موفقیت ثبت شد.",
        "invalid": "اطلاعات نامعتبر (Invalid Data)",
        "enter_title": "عنوان تراکنش را وارد کنید.",
        "invalid_amount": "مبلغ باید بیشتر از صفر باشد.",
        "invalid_date": "تاریخ واردشده معتبر نیست.",
        "enter_amount": "مبلغ را به‌درستی وارد کنید.",
        "enter_other": "لطفاً نام دسته‌بندی دلخواه را وارد کنید.",
        "select_record": "ابتدا یک تراکنش را انتخاب کنید.",
        "confirm_delete": "آیا از حذف این تراکنش مطمئن هستید؟",
        "deleted": "تراکنش با موفقیت حذف شد.",
        "delete_title": "تأیید حذف",
        "delete_success": "حذف موفق",
        "no_records": "تراکنشی پیدا نشد.",
        "currency_toman": "تومان",
        "date_note": "تاریخ شمسی",
        "welcome": "خوش آمدید",
        "choose_language": "زبان موردنظر خود را انتخاب کنید",
        "persian": "فارسی",
        "english": "English",
        "kind": "نوع",
        "no_jdatetime": "برای تاریخ شمسی، کتابخانه jdatetime را نصب کنید."
    },

    "en": {
        "app": "Daily Expense Tracker",
        "subtitle": "Smart Income and Expense Management",
        "income": "Income (درآمد)",
        "expense": "Expense (هزینه)",
        "balance": "Balance (موجودی)",
        "total_income": "Total Income (مجموع درآمد)",
        "total_expense": "Total Expense (مجموع هزینه)",
        "transaction": "Add Transaction (ثبت تراکنش)",
        "type": "Type (نوع تراکنش)",
        "title": "Title (عنوان)",
        "category": "Category (دسته‌بندی)",
        "amount": "Amount (مبلغ)",
        "date": "Date (تاریخ)",
        "note": "Note (یادداشت)",
        "add": "＋ Add Transaction (ثبت)",
        "clear": "Clear Form (پاک کردن)",
        "search": "Search / جست‌وجو",
        "records": "Transactions (تراکنش‌ها)",
        "delete": "Delete Selected (حذف)",
        "footer": "Your data is stored locally on this device.",
        "other_name": "Custom Category (نام دلخواه)",
        "expense_type": "Expense (هزینه)",
        "income_type": "Income (درآمد)",
        "id": "ID (شناسه)",
        "success": "Success (موفق)",
        "saved": "Transaction saved successfully.",
        "invalid": "Invalid Data (اطلاعات نامعتبر)",
        "enter_title": "Please enter a transaction title.",
        "invalid_amount": "Amount must be greater than zero.",
        "invalid_date": "The entered date is invalid.",
        "enter_amount": "Please enter a valid amount.",
        "enter_other": "Please enter a custom category name.",
        "select_record": "Please select a transaction first.",
        "confirm_delete": "Are you sure you want to delete this transaction?",
        "deleted": "Transaction deleted successfully.",
        "delete_title": "Confirm Delete",
        "delete_success": "Delete Successful",
        "no_records": "No transactions found.",
        "currency_toman": "Toman",
        "date_note": "Gregorian Date",
        "welcome": "Welcome",
        "choose_language": "Please select your language",
        "persian": "فارسی",
        "english": "English",
        "kind": "Type",
        "no_jdatetime": "Install jdatetime to use Persian dates."
    }
}

def normalize_digits(value):
    return str(value).translate(PERSIAN_DIGITS)


def money_format(amount, currency):
    if currency == "USD":
        return f"${amount:,.2f}"

    return f"{amount:,.0f} تومان"


def get_today(language):
    if language == "fa" and jdatetime:
        return jdatetime.date.today().strftime("%Y/%m/%d")

    return date.today().strftime("%Y/%m/%d")


def date_to_iso(value, language):

    value = normalize_digits(
        value.strip()
    ).replace("-", "/")

    parts = value.split("/")

    if len(parts) != 3:
        raise ValueError("Invalid date")

    year, month, day = map(int, parts)

    if language == "fa" and jdatetime:

        return jdatetime.date(
            year, month, day
        ).togregorian().isoformat()

    return date(
        year, month, day
    ).isoformat()


def date_from_iso(value, language):

    original = date.fromisoformat(value)

    if language == "fa" and jdatetime:

        return jdatetime.date.fromgregorian(
            date=original
        ).strftime("%Y/%m/%d")

    return original.strftime("%Y/%m/%d")

class LanguageSelector:

    def __init__(self, root):

        self.root = root
        self.language = None

        self.window = tk.Toplevel(root)

        self.window.title("Language Selection")
        self.window.geometry("420x330")
        self.window.resizable(False, False)
        self.window.configure(bg=BG)

        self.window.protocol(
            "WM_DELETE_WINDOW",
            root.destroy
        )

        self.window.transient(root)
        self.window.grab_set()

        self.center()

        tk.Label(
            self.window,
            text="🌍",
            bg=BG,
            font=("Arial", 34)
        ).pack(pady=(25, 5))

        tk.Label(
            self.window,
            text="Welcome | خوش آمدید",
            bg=BG,
            fg=NAVY,
            font=(FONT, 17, "bold")
        ).pack()

        tk.Label(
            self.window,
            text="Please select your language",
            bg=BG,
            fg=MUTED,
            font=(FONT, 10)
        ).pack(pady=8)

        tk.Label(
            self.window,
            text="لطفاً زبان خود را انتخاب کنید",
            bg=BG,
            fg=MUTED,
            font=(FONT, 10)
        ).pack(pady=(0, 18))

        buttons = tk.Frame(
            self.window,
            bg=BG
        )

        buttons.pack(fill="x", padx=35)

        tk.Button(
            buttons,
            text="🇮🇷  فارسی",
            command=lambda: self.choose("fa"),
            bg=GREEN,
            fg=WHITE,
            relief="flat",
            font=(FONT, 13, "bold"),
            pady=13,
            cursor="hand2"
        ).pack(fill="x", pady=5)

        tk.Button(
            buttons,
            text="🇺🇸  English",
            command=lambda: self.choose("en"),
            bg=BLUE,
            fg=WHITE,
            relief="flat",
            font=(FONT, 13, "bold"),
            pady=13,
            cursor="hand2"
        ).pack(fill="x", pady=5)

    def center(self):

        self.window.update_idletasks()

        width = 420
        height = 330

        x = (
            self.window.winfo_screenwidth() - width
        ) // 2

        y = (
            self.window.winfo_screenheight() - height
        ) // 2

        self.window.geometry(
            f"{width}x{height}+{x}+{y}"
        )

    def choose(self, language):

        self.language = language
        self.window.destroy()

class App:

    def __init__(self, root, language):

        self.root = root
        self.language = language

        self.rtl = language == "fa"
        self.currency = "IRR" if self.rtl else "USD"

        self.t = TEXTS[language]

        self.align = "right" if self.rtl else "left"

        self.root.title(self.t["app"])
        self.root.configure(bg=BG)

        self.root.state("zoomed")
        self.root.minsize(950, 650)

        self.db = sqlite3.connect(DB)

        self.setup_database()
        self.setup_style()
        self.build_ui()
        self.refresh()

    def setup_database(self):

        self.db.execute("""
            CREATE TABLE IF NOT EXISTS transactions(
                id INTEGER PRIMARY KEY,
                kind TEXT,
                title TEXT,
                category TEXT,
                amount INTEGER,
                tx_date TEXT,
                note TEXT
            )
        """)

        columns = [
            row[1]
            for row in self.db.execute(
                "PRAGMA table_info(transactions)"
            ).fetchall()
        ]

        if "currency" not in columns:

            self.db.execute("""
                ALTER TABLE transactions
                ADD COLUMN currency TEXT DEFAULT 'IRR'
            """)

        self.db.commit()

    def tr(self, key):
        return self.t.get(key, key)

    def category_translate(self, category):

        if self.rtl:

            return CATEGORY_MAP.get(
                category,
                category
            )

        return CATEGORY_EN.get(
            category,
            category
        )

    def stored_category(self, category):

        if self.rtl:

            return category

        return CATEGORY_MAP.get(
            category,
            category
        )

    def setup_style(self):

        style = ttk.Style()

        style.theme_use("clam")

        style.configure(
            "Treeview",
            font=(FONT, 10),
            rowheight=38,
            background=WHITE,
            fieldbackground=WHITE,
            foreground=NAVY
        )

        style.configure(
            "Treeview.Heading",
            font=(FONT, 10, "bold"),
            background="#E8EEF7",
            foreground=NAVY,
            padding=10
        )

        style.map(
            "Treeview",
            background=[("selected", "#DBEAFE")],
            foreground=[("selected", NAVY)]
        )

        style.configure(
            "TCombobox",
            font=(FONT, 10),
            padding=7
        )

    def make_label(
        self, parent, text,
        size=10, bold=False,
        bg=WHITE, fg=NAVY
    ):

        return tk.Label(
            parent,
            text=text,
            bg=bg,
            fg=fg,
            font=(
                FONT,
                size,
                "bold" if bold else "normal"
            ),
            anchor="e" if self.rtl else "w",
            justify="right" if self.rtl else "left"
        )

    def make_entry(self, parent, variable):

        return tk.Entry(
            parent,
            textvariable=variable,
            justify=self.align,
            font=(FONT, 10),
            relief="solid",
            bd=1,
            highlightthickness=1,
            highlightbackground=BORDER,
            highlightcolor=BLUE
        )

    def make_button(
        self, parent, text, command,
        color=BLUE
    ):

        return tk.Button(
            parent,
            text=text,
            command=command,
            bg=color,
            fg=WHITE,
            activebackground=color,
            activeforeground=WHITE,
            relief="flat",
            bd=0,
            font=(FONT, 9, "bold"),
            padx=14,
            pady=10,
            cursor="hand2"
        )

    def build_ui(self):


        header = tk.Frame(
            self.root,
            bg=NAVY,
            padx=25,
            pady=20
        )

        header.pack(fill="x")

        self.make_label(
            header,
            self.tr("app"),
            21,
            True,
            NAVY,
            WHITE
        ).pack(fill="x")

        self.make_label(
            header,
            self.tr("subtitle"),
            10,
            False,
            NAVY,
            "#CBD5E1"
        ).pack(fill="x", pady=(5, 0))

        main = tk.Frame(
            self.root,
            bg=BG,
            padx=22,
            pady=18
        )

        main.pack(fill="both", expand=True)

        self.cards = tk.Frame(
            main,
            bg=BG
        )

        self.cards.pack(fill="x")

        form = tk.Frame(
            main,
            bg=WHITE,
            padx=17,
            pady=16,
            highlightbackground=BORDER,
            highlightthickness=1
        )

        form.pack(fill="x", pady=15)

        self.make_label(
            form,
            self.tr("transaction"),
            12,
            True
        ).pack(fill="x", pady=(0, 13))

        self.kind = tk.StringVar(value="هزینه")
        self.title = tk.StringVar()
        self.category = tk.StringVar()
        self.amount = tk.StringVar()
        self.txdate = tk.StringVar(
            value=get_today(self.language)
        )
        self.note = tk.StringVar()
        self.other_category = tk.StringVar()

        self.field_row = tk.Frame(
            form,
            bg=WHITE
        )

        self.field_row.pack(fill="x")

        self.field_specs = [
            ("type", "kind"),
            ("title", "title"),
            ("category", "category"),
            ("amount", "amount"),
            ("date", "date")
        ]

        self.other_frame = tk.Frame(
            form,
            bg=WHITE
        )

        self.other_label = self.make_label(
            self.other_frame,
            self.tr("other_name"),
            9,
            False,
            WHITE,
            MUTED
        )

        self.other_entry = self.make_entry(
            self.other_frame,
            self.other_category
        )
        self.create_fields()

        note_frame = tk.Frame(
            form,
            bg=WHITE
        )

        note_frame.pack(fill="x", pady=(12, 0))

        self.make_label(
            note_frame,
            self.tr("note"),
            9,
            False,
            WHITE,
            MUTED
        ).pack(fill="x", pady=(0, 5))

        self.note_entry = self.make_entry(
            note_frame,
            self.note
        )

        self.note_entry.pack(
            fill="x",
            ipady=5
        )

        actions = tk.Frame(
            form,
            bg=WHITE
        )

        actions.pack(
            fill="x",
            pady=(13, 0)
        )

        self.make_button(
            actions,
            self.tr("add"),
            self.add,
            BLUE
        ).pack(side="right" if self.rtl else "left", padx=5)

        self.make_button(
            actions,
            self.tr("clear"),
            self.clear,
            "#64748B"
        ).pack(side="right" if self.rtl else "left", padx=5)

        toolbar = tk.Frame(
            main,
            bg=BG
        )

        toolbar.pack(
            fill="x",
            pady=(0, 8)
        )

        self.make_label(
            toolbar,
            self.tr("records"),
            12,
            True,
            BG,
            NAVY
        ).pack(side="right" if self.rtl else "left")

        self.search = tk.StringVar()

        search_entry = self.make_entry(
            toolbar,
            self.search
        )

        search_entry.pack(
            side="left" if self.rtl else "right",
            ipady=5
        )

        search_entry.configure(width=28)

        search_entry.bind(
            "<KeyRelease>",
            lambda event: self.table_refresh()
        )

        table_frame = tk.Frame(
            main,
            bg=WHITE,
            highlightbackground=BORDER,
            highlightthickness=1
        )

        table_frame.pack(
            fill="both",
            expand=True
        )

        self.columns = (
            "id",
            "kind",
            "title",
            "category",
            "amount",
            "currency",
            "date",
            "note"
        )

        self.tree = ttk.Treeview(
            table_frame,
            columns=self.columns,
            show="headings",
            selectmode="browse"
        )

        headings = {
            "id": self.tr("id"),
            "kind": self.tr("type"),
            "title": self.tr("title"),
            "category": self.tr("category"),
            "amount": self.tr("amount"),
            "currency": "Currency (ارز)",
            "date": self.tr("date"),
            "note": self.tr("note")
        }

        widths = {
            "id": 55,
            "kind": 105,
            "title": 145,
            "category": 125,
            "amount": 145,
            "currency": 90,
            "date": 110,
            "note": 150
        }

        for column in self.columns:

            self.tree.heading(
                column,
                text=headings[column]
            )

            self.tree.column(
                column,
                width=widths[column],
                minwidth=50,
                anchor="center",
                stretch=True
            )

        self.tree.tag_configure(
            "income",
            foreground=GREEN
        )

        self.tree.tag_configure(
            "expense",
            foreground=RED
        )

        scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.tree.yview
        )

        self.tree.configure(
            yscrollcommand=scrollbar.set
        )

        self.tree.pack(
            side="left",
            fill="both",
            expand=True,
            padx=8,
            pady=8
        )

        scrollbar.pack(
            side="right",
            fill="y",
            pady=8
        )

        footer = tk.Frame(
            main,
            bg=BG
        )

        footer.pack(
            fill="x",
            pady=(10, 0)
        )

        self.make_button(
            footer,
            self.tr("delete"),
            self.delete,
            RED
        ).pack(side="right" if self.rtl else "left")

        self.make_label(
            footer,
            self.tr("footer"),
            9,
            False,
            BG,
            MUTED
        ).pack(side="left" if self.rtl else "right")


    def create_fields(self):

        for child in self.field_row.winfo_children():
            child.destroy()

        self.kind_combo = None
        self.category_combo = None

        for caption, field_name in self.field_specs:

            cell = tk.Frame(
                self.field_row,
                bg=WHITE
            )

            cell.pack(
                side="right" if self.rtl else "left",
                expand=True,
                fill="x",
                padx=5
            )

            self.make_label(
                cell,
                self.tr(caption),
                9,
                False,
                WHITE,
                MUTED
            ).pack(fill="x", pady=(0, 5))

            if field_name == "kind":

                widget = ttk.Combobox(
                    cell,
                    textvariable=self.kind,
                    values=[
                        self.tr("expense_type"),
                        self.tr("income_type")
                    ],
                    state="readonly",
                    justify=self.align
                )

                widget.set(self.tr("expense_type"))

                self.kind_combo = widget

                widget.bind(
                    "<<ComboboxSelected>>",
                    self.on_kind_changed
                )

            elif field_name == "title":

                widget = self.make_entry(
                    cell,
                    self.title
                )

            elif field_name == "category":

                widget = ttk.Combobox(
                    cell,
                    textvariable=self.category,
                    state="readonly",
                    justify=self.align
                )

                self.category_combo = widget

            elif field_name == "amount":

                widget = self.make_entry(
                    cell,
                    self.amount
                )

            else:

                widget = self.make_entry(
                    cell,
                    self.txdate
                )

            widget.pack(
                fill="x",
                ipady=5
            )

        self.update_categories()


    def is_income(self):

        return self.kind.get() in (
            "درآمد",
            self.tr("income_type")
        )

    def update_categories(self):

        if self.is_income():

            categories = INCOME_CATEGORIES[self.language]

        else:

            categories = EXPENSE_CATEGORIES[self.language]

        self.category_combo.configure(
            values=categories
        )

        if self.category.get() not in categories:
            self.category.set(categories[0])

        self.on_category_changed()

    def on_kind_changed(self, event=None):

        self.category.set("")
        self.other_category.set("")

        self.update_categories()

    def on_category_changed(self, event=None):

        if self.category.get() in ("سایر", "Other"):

            self.other_frame.pack(
                fill="x",
                pady=(10, 0)
            )

            self.other_label.pack(
                fill="x",
                pady=(0, 5)
            )

            self.other_entry.pack(
                fill="x",
                ipady=5
            )

            self.other_entry.focus_set()

        else:

            self.other_frame.pack_forget()
            self.other_category.set("")

    def add(self):

        title = self.title.get().strip()

        amount_text = normalize_digits(
            self.amount.get().strip()
        ).replace(",", "").replace("٬", "").replace(" ", "")

        category = self.category.get().strip()

        if category in ("سایر", "Other"):

            category = self.other_category.get().strip()

            if not category:

                messagebox.showerror(
                    self.tr("invalid"),
                    self.tr("enter_other")
                )

                self.other_entry.focus_set()
                return

        if not title:

            messagebox.showerror(
                self.tr("invalid"),
                self.tr("enter_title")
            )

            return

        try:

            amount = float(amount_text)

            if amount <= 0:
                raise ValueError
            stored_amount = (
                round(amount * 100)
                if self.currency == "USD"
                else int(amount)
            )

        except (ValueError, TypeError):

            messagebox.showerror(
                self.tr("invalid"),
                self.tr("enter_amount")
            )

            return

        try:

            tx_date = date_to_iso(
                self.txdate.get(),
                self.language
            )

        except (ValueError, TypeError):

            messagebox.showerror(
                self.tr("invalid"),
                self.tr("invalid_date")
            )

            return

        kind = "درآمد" if self.is_income() else "هزینه"

        stored_category = self.stored_category(category)

        self.db.execute(
            """
            INSERT INTO transactions
            (kind, title, category, amount, tx_date, note, currency)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                kind,
                title,
                stored_category,
                stored_amount,
                tx_date,
                self.note.get().strip(),
                self.currency
            )
        )

        self.db.commit()

        self.clear()
        self.refresh()

        messagebox.showinfo(
            self.tr("success"),
            self.tr("saved")
        )

    def clear(self):

        self.title.set("")
        self.amount.set("")
        self.note.set("")
        self.other_category.set("")

        self.txdate.set(
            get_today(self.language)
        )

        if self.rtl:
            self.kind.set("هزینه")
        else:
            self.kind.set(self.tr("expense_type"))

        self.category.set("")

        self.update_categories()

    def delete(self):

        selected = self.tree.selection()

        if not selected:

            messagebox.showinfo(
                self.tr("delete"),
                self.tr("select_record")
            )

            return

        values = self.tree.item(
            selected[0],
            "values"
        )

        transaction_id = values[0]

        confirmed = messagebox.askyesno(
            self.tr("delete_title"),
            self.tr("confirm_delete")
        )

        if not confirmed:
            return

        self.db.execute(
            "DELETE FROM transactions WHERE id = ?",
            (transaction_id,)
        )

        self.db.commit()

        self.refresh()

        messagebox.showinfo(
            self.tr("delete_success"),
            self.tr("deleted")
        )

    def refresh(self):

        for child in self.cards.winfo_children():
            child.destroy()

        rows = self.db.execute(
            """
            SELECT currency, kind, SUM(amount)
            FROM transactions
            GROUP BY currency, kind
            """
        ).fetchall()

        totals = {
            "IRR": {"درآمد": 0, "هزینه": 0},
            "USD": {"درآمد": 0, "هزینه": 0}
        }

        for currency, kind, amount in rows:

            if currency not in totals:
                continue

            if kind in totals[currency]:
                totals[currency][kind] = amount or 0

        cards = []

        for currency in ("IRR", "USD"):

            income = totals[currency]["درآمد"]
            expense = totals[currency]["هزینه"]
            balance = income - expense

            if currency == "IRR":

                label_income = (
                    self.tr("total_income") + " - IRR"
                )

                label_expense = (
                    self.tr("total_expense") + " - IRR"
                )

                label_balance = (
                    self.tr("balance") + " - IRR"
                )

            else:

                label_income = (
                    self.tr("total_income") + " - USD"
                )

                label_expense = (
                    self.tr("total_expense") + " - USD"
                )

                label_balance = (
                    self.tr("balance") + " - USD"
                )

            cards.extend([
                (
                    label_balance,
                    money_format(
                        balance / 100 if currency == "USD" else balance,
                        currency
                    ),
                    BLUE
                ),
                (
                    label_income,
                    money_format(
                        income / 100 if currency == "USD" else income,
                        currency
                    ),
                    GREEN
                ),
                (
                    label_expense,
                    money_format(
                        expense / 100 if currency == "USD" else expense,
                        currency
                    ),
                    RED
                )
            ])

        for col in range(3):
            self.cards.grid_columnconfigure(
                col,
                weight=1
            )

        for index, (caption, value, color) in enumerate(cards):

            card = tk.Frame(
                self.cards,
                bg=WHITE,
                padx=14,
                pady=13,
                highlightbackground=BORDER,
                highlightthickness=1
            )

            card.grid(
                row=index // 3,
                column=index % 3,
                sticky="ew",
                padx=4,
                pady=4
            )

            self.make_label(
                card,
                caption,
                9,
                False,
                WHITE,
                MUTED
            ).pack(fill="x")

            self.make_label(
                card,
                value,
                13,
                True,
                WHITE,
                color
            ).pack(fill="x", pady=(7, 0))

        self.table_refresh()

    def table_refresh(self):

        for item in self.tree.get_children():
            self.tree.delete(item)

        query = self.search.get().strip().casefold()

        rows = self.db.execute(
            """
            SELECT id, kind, title, category,
                   amount, tx_date, note, currency
            FROM transactions
            ORDER BY tx_date DESC, id DESC
            """
        ).fetchall()

        found = 0

        for row in rows:

            (
                transaction_id,
                kind,
                title,
                category,
                amount,
                tx_date,
                note,
                currency
            ) = row

            try:

                display_date = date_from_iso(
                    tx_date,
                    self.language
                )

            except (ValueError, TypeError):

                display_date = tx_date

            if currency == "USD":

                display_amount = money_format(
                    amount / 100,
                    currency
                )

            else:

                display_amount = money_format(
                    amount,
                    currency
                )

            display_kind = (
                self.tr("income")
                if kind == "درآمد"
                else self.tr("expense")
            )

            display_category = self.category_translate(
                category
            )

            values = (
                transaction_id,
                display_kind,
                title,
                display_category,
                display_amount,
                currency,
                display_date,
                note
            )

            searchable = " ".join(
                str(value) for value in values
            ).casefold()

            if query and query not in searchable:
                continue

            tag = (
                "income"
                if kind == "درآمد"
                else "expense"
            )

            self.tree.insert(
                "",
                "end",
                values=values,
                tags=(tag,)
            )

            found += 1

        if found == 0 and query:

            pass

    def close(self):

        self.db.close()
        self.root.destroy()

if __name__ == "__main__":

    root = tk.Tk()
    #root.withdraw()

    selector = LanguageSelector(root)

    root.wait_window(selector.window)

    if selector.language is None:

        root.destroy()

    else:

        root.deiconify()

        app = App(
            root,
            selector.language
        )

        root.protocol(
            "WM_DELETE_WINDOW",
            app.close
        )

        root.mainloop()
