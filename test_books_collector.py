import pytest
from books_collector import BooksCollector


@pytest.fixture
def collector():
    return BooksCollector()



@pytest.mark.parametrize(
    "name,should_add",
    [
        ("Короткое имя", True),
        ("А" * 40, True),    
        ("А" * 41, False),   
        ("", False),
    ]
)
def test_add_new_book_various_lengths(collector, name, should_add):
    collector.add_new_book(name)
    assert (name in collector.get_books_genre()) is should_add


def test_add_new_book_duplicate_not_added(collector):
    collector.add_new_book("Гарри Поттер")
    collector.add_new_book("Гарри Поттер")
    assert len(collector.get_books_genre()) == 1



@pytest.mark.parametrize(
    "genre,expected",
    [
        ("Фантастика", "Фантастика"),
        ("Ужасы", "Ужасы"),
        ("Романтика", ""),   
)
def test_set_book_genre_sets_only_when_valid(collector, genre, expected):
    collector.add_new_book("Книга")
    collector.set_book_genre("Книга", genre)
    assert collector.books_genre["Книга"] == expected


def test_get_book_genre_returns_value_when_present(collector):
    collector.books_genre["Книга"] = "Комедии"
    assert collector.get_book_genre("Книга") == "Комедии"


def test_get_book_genre_returns_none_for_unknown(collector):
    assert collector.get_book_genre("Несуществующая") is None



def test_get_books_with_specific_genre_returns_only_matching(collector):
    collector.add_new_book("Гарри Поттер")
    collector.add_new_book("Оно")
    collector.set_book_genre("Гарри Поттер", "Фантастика")
    collector.set_book_genre("Оно", "Ужасы")
    assert collector.get_books_with_specific_genre("Фантастика") == ["Гарри Поттер"]


def test_get_books_genre_returns_dict(collector):
    collector.add_new_book("Гарри Поттер")
    result = collector.get_books_genre()
    assert isinstance(result, dict)
    assert "Гарри Поттер" in result


def test_get_books_for_children_filters_out_age_restricted(collector):
    collector.add_new_book("Оно")
    collector.add_new_book("Мадагаскар")
    collector.set_book_genre("Оно", "Ужасы")            
    collector.set_book_genre("Мадагаскар", "Мультфильмы") 
    assert collector.get_books_for_children() == ["Мадагаскар"]



def test_add_book_in_favorites_adds_once(collector):
    collector.add_new_book("Гарри Поттер")
    collector.set_book_genre("Гарри Поттер", "Фантастика")
    collector.add_book_in_favorites("Гарри Поттер")
    collector.add_book_in_favorites("Гарри Поттер")  
    assert collector.favorites == ["Гарри Поттер"]



def test_delete_book_from_favorites_removes_book(collector):
    collector.add_new_book("Гарри Поттер")
    collector.add_book_in_favorites("Гарри Поттер")
    collector.delete_book_from_favorites("Гарри Поттер")
    assert "Гарри Поттер" not in collector.favorites

---------
def test_get_list_of_favorites_books_returns_list(collector):
    collector.favorites = ["Гарри Поттер"]
    result = collector.get_list_of_favorites_books()
    assert isinstance(result, list)
    assert result == ["Гарри Поттер"]