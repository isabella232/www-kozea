import datetime

from ..blog import build_article, find_article_paths, tags_to_list

article_base_path = "./www_kozea/test/articles"


def test_tags_to_list():
    assert tags_to_list("") == []
    assert tags_to_list(None) == []
    assert tags_to_list("foo") == ["foo"]
    assert tags_to_list("foo,bar") == sorted(["foo", "bar"])  # Sorted
    assert tags_to_list(",") == []  # comma
    assert tags_to_list("foo,") == ["foo"]  # Trailing comma
    assert tags_to_list("foo,foo,bar") == sorted(["foo", "bar"])  # Unicity
    assert tags_to_list("foo,FoO,bar") == sorted(
        ["foo", "bar"]
    )  # Letter case unicity
    assert tags_to_list(",foo") == ["foo"]  # Leading comma
    assert tags_to_list(",,,foo,  ,  , ,, ") == ["foo"]  # lot of comma
    assert tags_to_list("bar , foo, baz ") == sorted(
        ["foo", "bar", "baz"]
    )  # Trimming
    assert tags_to_list("foo bar") == ["foo bar"]


def test_build_article():
    assert build_article(
        f"{article_base_path}/2021-11-22_avis-patients/content.md"
    ) == {
        "title": "Avis patients",
        "date": datetime.date(2021, 11, 22),
        "tags": ["allergies", "santé"],
        "md_content": "# Avis patients\n\navis",
        "html_content": "<h1>Avis patients</h1>\n<p>avis</p>",
        "url": "2021-11-22_avis-patients",
    }


def test_find_article_paths():
    assert find_article_paths(
        f"{article_base_path}/2021-11-22_avis-patients"
    ) == [f"{article_base_path}/2021-11-22_avis-patients/content.md"]
    assert find_article_paths(f"{article_base_path}/2021-foobar") == []
