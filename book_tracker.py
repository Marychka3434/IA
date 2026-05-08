import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

DATA_FILE = "books.json"


class BookTracker:
    def init(self, root):
        self.root = root
        self.root.title("Book Tracker - Трекер прочитанных книг")
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
