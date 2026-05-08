import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

DATA_FILE = "books.json"


class BookTracker:
    def _init_(self, root):
        self.root = root
        self.root.title("Book Tracker - Личная кинотека")
        self.root.geometry("800x500")

        self.books = []
        self.load_data()

        # Поля ввода
        fields_frame = ttk.LabelFrame(root, text="Добавить книгу", padding=10)
        fields_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(fields_frame, text="Название:").grid(row=0, column=0, padx=5, pady=5)
        self.title_entry = ttk.Entry(fields_frame, width=30)
        self.title_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(fields_frame, text="Автор:").grid(row=0, column=2, padx=5, pady=5)
        self.author_entry = ttk.Entry(fields_frame, width=30)
        self.author_entry.grid(row=0, column=3, padx=5, pady=5)

        ttk.Label(fields_frame, text="Жанр:").grid(row=1, column=0, padx=5, pady=5)
        self.genre_entry = ttk.Entry(fields_frame, width=30)
        self.genre_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(fields_frame, text="Кол-во страниц:").grid(row=1, column=2, padx=5, pady=5)
        self.pages_entry = ttk.Entry(fields_frame, width=30)
        self.pages_entry.grid(row=1, column=3, padx=5, pady=5)

        add_btn = ttk.Button(fields_frame, text="Добавить книгу", command=self.add_book)
        add_btn.grid(row=2, column=0, columnspan=4, pady=10)

        # Фильтры
        filter_frame = ttk.LabelFrame(root, text="Фильтрация", padding=10)
        filter_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(filter_frame, text="Фильтр по жанру:").grid(row=0, column=0, padx=5, pady=5)
        self.filter_genre_entry = ttk.Entry(filter_frame, width=30)
        self.filter_genre_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(filter_frame, text="Фильтр (страниц >):").grid(row=0, column=2, padx=5, pady=5)
        self.filter_pages_entry = ttk.Entry(filter_frame, width=30)
        self.filter_pages_entry.grid(row=0, column=3, padx=5, pady=5)

        filter_btn = ttk.Button(filter_frame, text="Применить фильтр", command=self.apply_filter)
        filter_btn.grid(row=1, column=0, columnspan=2, pady=5)

        reset_btn = ttk.Button(filter_frame, text="Сбросить фильтр", command=self.reset_filter)
        reset_btn.grid(row=1, column=2, columnspan=2, pady=5)

        # Таблица с книгами
        self.tree = ttk.Treeview(root, columns=("title", "author", "genre", "pages"), show="headings")
        self.tree.heading("title", text="Название")
        self.tree.heading("author", text="Автор")
        self.tree.heading("genre", text="Жанр")
        self.tree.heading("pages", text="Страницы")
        self.tree.column("title", width=200)
        self.tree.column("author", width=150)
        self.tree.column("genre", width=150)
        self.tree.column("pages", width=100)

        scrollbar = ttk.Scrollbar(root, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(side="left", fill="both", expand=True, padx=(10, 0), pady=10)
        scrollbar.pack(side="right", fill="y", pady=10, padx=(0, 10))

        self.display_books(self.books)

        # Кнопки управления
        btn_frame = ttk.Frame(root)
        btn_frame.pack(fill="x", padx=10, pady=5)

        ttk.Button(btn_frame, text="Удалить выбранную", command=self.delete_book).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Сохранить в JSON", command=self.save_data).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Загрузить из JSON", command=self.load_data).pack(side="left", padx=5)

    def add_book(self):
        title = self.title_entry.get().strip()
        author = self.author_entry.get().strip()
        genre = self.genre_entry.get().strip()
        pages = self.pages_entry.get().strip()


# Валидация: проверка пустых полей
        if not title or not author or not genre or not pages:
            messagebox.showerror("Ошибка", "Все поля должны быть заполнены!")
            return

        # Валидация: проверка, что количество страниц - число
        if not pages.isdigit():
            messagebox.showerror("Ошибка", "Количество страниц должно быть целым положительным числом!")
            return

        pages = int(pages)

        if pages <= 0:
            messagebox.showerror("Ошибка", "Количество страниц должно быть больше 0!")
            return

        self.books.append({
            "title": title,
            "author": author,
            "genre": genre,
            "pages": pages
        })

        # Очистка полей
        self.title_entry.delete(0, tk.END)
        self.author_entry.delete(0, tk.END)
        self.genre_entry.delete(0, tk.END)
        self.pages_entry.delete(0, tk.END)

        self.display_books(self.books)
        self.save_data()
        messagebox.showinfo("Успех", "Книга добавлена!")

    def delete_book(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Ошибка", "Выберите книгу для удаления!")
            return

        for item in selected:
            values = self.tree.item(item, "values")
            for book in self.books:
                if (book["title"] == values[0] and book["author"] == values[1] and
                    book["genre"] == values[2] and str(book["pages"]) == values[3]):
                    self.books.remove(book)
                    break

        self.display_books(self.books)
        self.save_data()
        messagebox.showinfo("Успех", "Книга удалена!")

    def apply_filter(self):
        filter_genre = self.filter_genre_entry.get().strip().lower()
        filter_pages = self.filter_pages_entry.get().strip()

        filtered = self.books

        if filter_genre:
            filtered = [b for b in filtered if filter_genre in b["genre"].lower()]

        if filter_pages:
            if filter_pages.isdigit():
                filtered = [b for b in filtered if b["pages"] > int(filter_pages)]
            else:
                messagebox.showerror("Ошибка", "Фильтр по страницам должен быть числом!")

        self.display_books(filtered)

    def reset_filter(self):
        self.filter_genre_entry.delete(0, tk.END)
        self.filter_pages_entry.delete(0, tk.END)
        self.display_books(self.books)

    def display_books(self, books_list):
        # Очищаем таблицу
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Заполняем таблицу
        for book in books_list:
            self.tree.insert("", tk.END, values=(book["title"], book["author"], book["genre"], book["pages"]))

    def save_data(self):
        try:
            with open(DATA_FILE, "w", encoding="utf-8") as f:
                json.dump(self.books, f, ensure_ascii=False, indent=4)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить данные: {e}")

    def load_data(self):
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, "r", encoding="utf-8") as f:
                    self.books = json.load(f)
                self.display_books(self.books)
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось загрузить данные: {e}")
        else:
            self.books = []


# Точка входа в программу
if name == "main":
    root = tk.Tk()
    app = BookTracker(root)
    root.mainloop()

