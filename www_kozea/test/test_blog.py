import datetime

import pytest
from freezegun import freeze_time

from ..blog import (
    articles_tags,
    build_article,
    build_articles,
    count_words_in_text,
    different_title_articles,
    estimate_reading_time,
    find_article_paths,
    get_articles_titles,
    get_articles_with_tag,
    get_main_tag,
    get_previous_and_next_articles,
    past_articles,
    sort_articles,
    strip_html_markup,
    tags_to_list,
)
from ..error import (
    FrontmatterError,
    NoDateInArticleError,
    TypeDateInArticleError,
)

articles_base_path = "./www_kozea/test/articles"
valid_articles_base_path = f"{articles_base_path}/valid_articles"
invalid_articles_base_path = f"{articles_base_path}/invalid_articles"


def valid_article(slug):
    return build_article(f"{valid_articles_base_path}/{slug}/content.md")


def invalid_article(slug):
    return build_article(f"{invalid_articles_base_path}/{slug}/content.md")


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
    assert tags_to_list(",,,foo,  ,  , ,, ") == ["foo"]  # lot of commas
    assert tags_to_list("bar , foo, baz ") == sorted(
        ["foo", "bar", "baz"]
    )  # Trimming
    assert tags_to_list("foo bar") == ["foo bar"]


def test_get_main_tag():
    assert get_main_tag(["foo", "bar", "baz"]) == "foo"
    assert get_main_tag([]) is None


def test_build_article():
    assert valid_article("2021-11-22_avis-patients") == {
        "title": "Avis patients",
        "date": datetime.date(2021, 11, 22),
        "tags": ["allergies", "santé"],
        "md_content": "# Avis patients\n\navis",
        "html_content": '<h1 id="avis-patients">'
        "Avis patients</h1>\n<p>avis</p>",
        "time": 1,
        "url": "2021-11-22_avis-patients",
        "toc": '<div class="toc">\n<ul>\n<li>'
        '<a href="#avis-patients">Avis patients</a></li>\n</ul>\n</div>\n',
    }
    with pytest.raises(FrontmatterError):
        invalid_article("2021-10-20_backoffice")
    with pytest.raises(TypeDateInArticleError):
        invalid_article("2021-10-21_tiers-payants")
    with pytest.raises(NoDateInArticleError):
        invalid_article("2021-10-25_conseil-santé")


def test_build_articles():
    assert build_articles(f"{valid_articles_base_path}") == [
        {
            "title": "Avis patients",
            "date": datetime.date(2021, 11, 22),
            "tags": ["allergies", "santé"],
            "md_content": "# Avis patients\n\navis",
            "html_content": '<h1 id="avis-patients">'
            "Avis patients</h1>\n<p>avis</p>",
            "time": 1,
            "url": "2021-11-22_avis-patients",
            "toc": '<div class="toc">\n<ul>\n<li>'
            '<a href="#avis-patients">Avis patients</a></li>\n</ul>\n</div>\n',
        },
        {
            "title": "Communications",
            "date": datetime.date(2021, 11, 27),
            "tags": ["allergies", "santé"],
            "md_content": "# Communications\n\nCommunications",
            "html_content": '<h1 id="communications">'
            "Communications</h1>\n<p>Communications</p>",
            "time": 1,
            "url": "2021-11-27_communication",
            "toc": '<div class="toc">\n<ul>\n<li>'
            '<a href="#communications">Communications</a>'
            "</li>\n</ul>\n</div>\n",
        },
        {
            "title": "Prise de rendez-vous",
            "date": datetime.date(2021, 11, 2),
            "tags": ["pharmacie"],
            "md_content": "# Prise de rendez-vous\n\nPrise de rendez-vous",
            "html_content": '<h1 id="prise-de-rendez-vous">'
            "Prise de rendez-vous</h1>\n<p>Prise de rendez-vous</p>",
            "time": 1,
            "url": "2021-11-02_rendez-vous",
            "toc": '<div class="toc">\n<ul>\n<li>'
            '<a href="#prise-de-rendez-vous">'
            "Prise de rendez-vous</a></li>\n</ul>\n</div>\n",
        },
        {
            "title": "4 conseils",
            "date": datetime.date(2021, 11, 18),
            "md_content": "# 4 conseils\n\n4 conseils",
            "html_content": '<h1 id="4-conseils">'
            "4 conseils</h1>\n<p>4 conseils</p>",
            "time": 1,
            "tags": [],
            "url": "2021-11-18_4-conseils",
            "toc": '<div class="toc">\n<ul>\n<li>'
            '<a href="#4-conseils">4 conseils</a>'
            "</li>\n</ul>\n</div>\n",
        },
        {
            "title": "Les acariens",
            "date": datetime.date(2021, 12, 10),
            "tags": ["allergies", "santé"],
            "md_content": "# Les acariens\n\nacariens",
            "html_content": '<h1 id="les-acariens">'
            "Les acariens</h1>\n<p>acariens</p>",
            "time": 1,
            "url": "2021-12-10_acariens",
            "toc": '<div class="toc">\n<ul>\n<li>'
            '<a href="#les-acariens">Les acariens</a>'
            "</li>\n</ul>\n</div>\n",
        },
    ]
    with pytest.raises(FrontmatterError):
        build_articles(f"{invalid_articles_base_path}")


def test_articles_tags():
    assert articles_tags(build_articles(f"{valid_articles_base_path}")) == [
        "allergies",
        "pharmacie",
        "santé",
    ]


def test_find_article_paths():
    assert find_article_paths(f"{articles_base_path}") == [
        f"{invalid_articles_base_path}/2021-10-20_backoffice/content.md",
        f"{invalid_articles_base_path}/2021-10-25_conseil-santé/content.md",
        f"{invalid_articles_base_path}/2021-10-21_tiers-payants/content.md",
        f"{valid_articles_base_path}/2021-11-22_avis-patients/content.md",
        f"{valid_articles_base_path}/2021-11-27_communication/content.md",
        f"{valid_articles_base_path}/2021-11-02_rendez-vous/content.md",
        f"{valid_articles_base_path}/2021-11-18_4-conseils/content.md",
        f"{valid_articles_base_path}/2021-12-10_acariens/content.md",
    ]
    assert find_article_paths(f"{invalid_articles_base_path}/2021-foobar") == []


def test_get_articles_with_tag():
    assert get_articles_with_tag(
        "santé", build_articles(f"{valid_articles_base_path}")
    ) == [
        valid_article("2021-11-22_avis-patients"),
        valid_article("2021-11-27_communication"),
        valid_article("2021-12-10_acariens"),
    ]
    assert get_articles_with_tag(
        None,
        [build_articles(f"{valid_articles_base_path}")],
    ) == [
        build_articles(f"{valid_articles_base_path}"),
    ]


def test_sort_articles():
    assert sort_articles(
        [
            valid_article("2021-11-22_avis-patients"),
            valid_article("2021-12-10_acariens"),
        ]
    ) == [
        valid_article("2021-12-10_acariens"),
        valid_article("2021-11-22_avis-patients"),
    ]


@freeze_time("2021-11-30")
def test_past_articles():
    assert past_articles([valid_article("2021-12-10_acariens")]) == []
    assert past_articles([valid_article("2021-11-22_avis-patients")]) == [
        valid_article("2021-11-22_avis-patients")
    ]


def test_different_title_articles():
    assert different_title_articles(
        [
            valid_article("2021-11-22_avis-patients"),
            valid_article("2021-11-27_communication"),
        ],
        ["foo", "test"],
    ) == [
        valid_article("2021-11-22_avis-patients"),
        valid_article("2021-11-27_communication"),
    ]
    assert different_title_articles(
        [
            valid_article("2021-11-22_avis-patients"),
            valid_article("2021-11-27_communication"),
        ],
        ["Avis patients"],
    ) == [
        valid_article("2021-11-27_communication"),
    ]


def test_strip_html_markup():
    assert strip_html_markup("<p> Test <p>") == "Test"
    assert (
        strip_html_markup("<h1> Filter visible text <h1> <p> Test <p>")
        == "FiltervisibletextTest"
    )
    assert strip_html_markup("") == ""


def test_count_words_in_text():
    assert count_words_in_text("Test", 5) == 0.8
    assert count_words_in_text("FiltervisibletextTest", 5) == 4.2
    assert count_words_in_text("", 5) == 0


def test_estimate_reading_time():
    assert estimate_reading_time("<p> Test <p>") == 1
    assert (
        estimate_reading_time("<h1> Filter visible text <h1> <p> Test <p>") == 1
    )
    assert estimate_reading_time("") == 0


def test_get_previous_and_next_articles():
    assert get_previous_and_next_articles(
        valid_article("2021-11-02_rendez-vous"),
        build_articles(f"{valid_articles_base_path}"),
    ) == (
        valid_article("2021-11-27_communication"),
        valid_article("2021-11-18_4-conseils"),
    )
    assert (
        get_previous_and_next_articles(
            valid_article("2021-11-02_rendez-vous"),
            [],
        )
        == (None, None)
    )
    assert get_previous_and_next_articles(
        valid_article("2021-11-02_rendez-vous"),
        [
            valid_article("2021-11-22_avis-patients"),
            valid_article("2021-11-02_rendez-vous"),
        ],
    ) == (
        valid_article("2021-11-22_avis-patients"),
        None,
    )
    assert get_previous_and_next_articles(
        valid_article("2021-11-02_rendez-vous"),
        [
            valid_article("2021-11-02_rendez-vous"),
            valid_article("2021-12-10_acariens"),
        ],
    ) == (
        None,
        valid_article("2021-12-10_acariens"),
    )


def test_get_articles_titles():
    assert (
        get_articles_titles(
            [
                valid_article("2021-11-02_rendez-vous"),
                valid_article("2021-12-10_acariens"),
                None,
            ],
        )
        == ["Prise de rendez-vous", "Les acariens"]
    )
    assert get_articles_titles([None]) == []
    assert get_articles_titles([]) == []
