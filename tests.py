import pytest
from main import BooksCollector


# Фикстура: перед каждым тестом создаётся новый экземпляр BooksCollector
@pytest.fixture
def collector():
    return BooksCollector()


# ---------- Тесты для add_new_book ----------

# Проверяем, что книга с корректным названием добавляется
@pytest.mark.parametrize(
    "name",
    ["Война и мир", "Преступление и наказание", "А" * 40]
)
def test_add_new_book_adds_book_with_valid_name(collector, name):
    collector.add_new_book(name)
    assert name in collector.get_books_genre()


# Проверяем, что книга с пустым или слишком длинным названием не добавляется
@pytest.mark.parametrize(
    "name",
    ["", "А" * 41]
)
def test_add_new_book_does_not_add_book_with_invalid_length(collector, name):
    collector.add_new_book(name)
    assert name not in collector.get_books_genre()


# Проверяем, что одну и ту же книгу нельзя добавить дважды
def test_add_new_book_does_not_add_same_book_twice(collector):
    name = "Война и мир"
    collector.add_new_book(name)
    collector.add_new_book(name)

    assert len(collector.get_books_genre()) == 1


# Проверяем, что у новой книги жанр по умолчанию пустой
def test_add_new_book_sets_empty_genre_by_default(collector):
    name = "Война и мир"
    collector.add_new_book(name)

    assert collector.get_book_genre(name) == ""


# ---------- Тесты для set_book_genre и get_book_genre ----------

# Проверяем, что жанр устанавливается для существующей книги с валидным жанром
def test_set_book_genre_sets_genre_for_existing_book_with_valid_genre(collector):
    name = "Мастер и Маргарита"
    collector.add_new_book(name)
    collector.set_book_genre(name, "Фантастика")

    assert collector.get_book_genre(name) == "Фантастика"


# Проверяем: если книги нет в словаре, жанр не устанавливается
def test_set_book_genre_does_not_set_genre_for_nonexistent_book(collector):
    collector.add_new_book("Война и мир")
    collector.set_book_genre("Неизвестная книга", "Фантастика")

    # У существующей книги жанр должен остаться пустым
    assert collector.get_book_genre("Война и мир") == ""
    # Несуществующая книга не должна появиться
    assert collector.get_book_genre("Неизвестная книга") is None


# Проверяем: если жанр не входит в список допустимых, жанр не устанавливается
def test_set_book_genre_does_not_set_genre_for_invalid_genre(collector):
    collector.add_new_book("Война и мир")
    collector.set_book_genre("Война и мир", "Роман")  # жанра нет в списке genre

    assert collector.get_book_genre("Война и мир") == ""


# ---------- Тесты для get_books_with_specific_genre и get_books_genre ----------

# Проверяем, что возвращаются только книги с указанным жанром
def test_get_books_with_specific_genre_returns_only_books_of_that_genre(collector):
    collector.add_new_book("Мастер и Маргарита")
    collector.add_new_book("Собачье сердце")

    collector.set_book_genre("Мастер и Маргарита", "Фантастика")
    collector.set_book_genre("Собачье сердце", "Комедии")

    result = collector.get_books_with_specific_genre("Фантастика")

    assert result == ["Мастер и Маргарита"]


# Проверяем, что метод возвращает текущий словарь books_genre
def test_get_books_genre_returns_current_dictionary(collector):
    collector.add_new_book("Отцы и дети")

    assert collector.get_books_genre() == {"Отцы и дети": ""}


# ---------- Тесты для get_books_for_children ----------

# Проверяем, что книги с возрастным рейтингом не попадают в список для детей
def test_get_books_for_children_excludes_age_rating_genres(collector):
    collector.add_new_book("Мастер и Маргарита")
    collector.add_new_book("Преступление и наказание")
    collector.add_new_book("Конёк-Горбунок")

    collector.set_book_genre("Мастер и Маргарита", "Фантастика")
    collector.set_book_genre("Преступление и наказание", "Детективы")  # возрастной рейтинг
    collector.set_book_genre("Конёк-Горбунок", "Мультфильмы")

    result = collector.get_books_for_children()

    assert "Преступление и наказание" not in result
    assert set(result) == {"Мастер и Маргарита", "Конёк-Горбунок"}


# ---------- Тесты для работы с избранным ----------

# Проверяем, что в избранное можно добавить только книгу из словаря books_genre
def test_add_book_in_favorites_adds_only_if_book_exists_in_books_genre(collector):
    collector.add_book_in_favorites("Война и мир")
    assert collector.get_list_of_favorites_books() == []

    collector.add_new_book("Война и мир")
    collector.add_book_in_favorites("Война и мир")

    assert collector.get_list_of_favorites_books() == ["Война и мир"]


# Проверяем, что одну и ту же книгу нельзя добавить в избранное дважды
def test_add_book_in_favorites_does_not_add_twice(collector):
    collector.add_new_book("Война и мир")
    collector.add_book_in_favorites("Война и мир")
    collector.add_book_in_favorites("Война и мир")

    assert collector.get_list_of_favorites_books() == ["Война и мир"]


# Проверяем, что книга удаляется из избранного
def test_delete_book_from_favorites_removes_book_if_present(collector):
    collector.add_new_book("Война и мир")
    collector.add_book_in_favorites("Война и мир")
    collector.delete_book_from_favorites("Война и мир")

    assert collector.get_list_of_favorites_books() == []
