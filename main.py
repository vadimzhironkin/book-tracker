import json
import os

DB_FILE = "books.json"

def load_books():
    if not os.path.exists(DB_FILE) or os.path.getsize(DB_FILE) == 0: 
        return []
    with open(DB_FILE, "r", encoding="utf-8") as f: 
        return json.load(f)

def save_books(books):
    with open(DB_FILE, "w", encoding="utf-8") as f: 
        json.dump(books, f, ensure_ascii=False, indent=4)

def add_book():
    print("\n--- Добавление книги ---")
    author = input("Введите автора: ").strip()
    title = input("Введите название: ").strip()
    books = load_books()
    
    # Проверка на дубликаты (Закрывает Issue #1)
    for book in books:
        if book['author'].lower() == author.lower() and book['title'].lower() == title.lower():
            print("Ошибка: Такая книга уже есть!")
            return
            
    try:
        rating = int(input("Введите оценку (1-5): "))
        if not (1 <= rating <= 5): 
            print("Оценка должна быть от 1 до 5!")
            return
    except ValueError: 
        print("Ошибка ввода числа")
        return
        
    date_read = input("Введите дату прочтения: ").strip()
    books.append({"author": author, "title": title, "rating": rating, "date_read": date_read})
    save_books(books)
    print("Книга успешно добавлена!")

def show_all_books():
    books = load_books()
    if not books: 
        print("Список пуст.")
        return
    for i, b in enumerate(books, 1): 
        print(f"{i}. {b['author']} — «{b['title']}» | Оценка: {b['rating']}/5 | Дата: {b['date_read']}")

def show_average_rating():
    books = load_books()
    if not books: 
        print("Нет книг для расчета.")
        return
    print(f"Средняя оценка всех книг: {sum(b['rating'] for b in books) / len(books):.2f}")

def show_author_stats():
    books = load_books()
    if not books:
        print("Нет данных.")
        return
    stats = {}
    for b in books: 
        stats[b['author']] = stats.get(b['author'], 0) + 1
    for author, count in stats.items(): 
        print(f"Автор: {author} | Прочитано книг: {count}")

def delete_book():
    books = load_books()
    if not books: 
        print("Список пуст.")
        return
    show_all_books()
    try:
        choice = int(input("Номер книги для удаления: "))
        if 1 <= choice <= len(books):
            removed = books.pop(choice - 1)
            save_books(books)
            print(f"Книга «{removed['title']}» удалена!")
        else:
            print("Неверный номер.")
    except ValueError: 
        print("Ошибка ввода")

def main():
    while True:
        print("\n=== Меню трекера книг ===")
        print("1. Добавить книгу\n2. Показать все книги\n3. Показать среднюю оценку\n4. Статистика по авторам\n5. Удалить книгу\n6. Выход")
        c = input("Выберите пункт меню (1-6): ")
        if c == "1": add_book()
        elif c == "2": show_all_books()
        elif c == "3": show_average_rating()
        elif c == "4": show_author_stats()
        elif c == "5": delete_book()
        elif c == "6": 
            print("Выход из программы.")
            break

if __name__ == "__main__":
    main()
