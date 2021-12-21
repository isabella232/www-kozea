import datetime

import pytest
from freezegun import freeze_time

from ..blog import (
    articles_tags,
    build_article,
    build_articles,
    count_words_in_text,
    estimate_reading_time,
    filter_date_articles,
    filter_title_articles,
    filter_visible_text,
    find_article_paths,
    get_articles_titles,
    get_main_tag,
    get_previous_and_next_articles,
    get_same_tag_articles,
    sorted_articles,
    tags_to_list,
)
from ..error import (
    FrontmatterError,
    NoDateInArticleError,
    TypeDateInArticleError,
)

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


def test_get_main_tag():
    assert get_main_tag(["foo", "bar", "baz"]) == "foo"
    assert get_main_tag([]) is None


def test_build_article():
    assert build_article(
        f"{article_base_path}/2021-11-22_avis-patients/content.md"
    ) == {
        "title": "Avis patients",
        "date": datetime.date(2021, 11, 22),
        "time": 1,
        "tags": ["allergies", "santé"],
        "md_content": "# Avis patients\n\navis",
        "html_content": "<h1>Avis patients</h1>\n<p>avis</p>",
        "url": "2021-11-22_avis-patients",
    }
    with pytest.raises(FrontmatterError):
        build_article(
            f"{article_base_path}/2021-10-20_outil-backoffice/content.md"
        )
    with pytest.raises(TypeDateInArticleError):
        build_article(
            f"{article_base_path}/2021-10-21_tiers-payants/content.md"
        )
    with pytest.raises(NoDateInArticleError):
        build_article(
            f"{article_base_path}/2021-10-25_conseil-santé/content.md"
        )


def test_build_articles():
    assert build_articles(f"{article_base_path}/2021-11-22_avis-patients") == [
        {
            "title": "Avis patients",
            "date": datetime.date(2021, 11, 22),
            "time": 1,
            "tags": ["allergies", "santé"],
            "md_content": "# Avis patients\n\navis",
            "html_content": "<h1>Avis patients</h1>\n<p>avis</p>",
            "url": "2021-11-22_avis-patients",
        }
    ]


def test_articles_tags():
    assert (
        articles_tags(
            [
                build_article(
                    f"{article_base_path}/2021-11-22_avis-patients/content.md"
                ),
                build_article(
                    f"{article_base_path}/2021-11-02_rendez-vous/content.md"
                ),
                build_article(
                    f"{article_base_path}/2021-12-10_acariens/content.md"
                ),
                build_article(
                    f"{article_base_path}/2021-11-18_4-conseils/content.md"
                ),
            ]
        )
        == ["allergies", "pharmacie", "santé"]
    )


def test_find_article_paths():
    assert find_article_paths(
        f"{article_base_path}/2021-11-22_avis-patients"
    ) == [f"{article_base_path}/2021-11-22_avis-patients/content.md"]
    assert find_article_paths(f"{article_base_path}/2021-foobar") == []


def test_get_same_tag_articles():
    assert get_same_tag_articles(
        "santé",
        [
            build_article(
                f"{article_base_path}/2021-11-22_avis-patients/content.md"
            ),
            build_article(
                f"{article_base_path}/2021-11-02_rendez-vous/content.md"
            ),
            build_article(
                f"{article_base_path}/2021-12-10_acariens/content.md"
            ),
        ],
    ) == [
        build_article(
            f"{article_base_path}/2021-11-22_avis-patients/content.md"
        ),
        build_article(f"{article_base_path}/2021-12-10_acariens/content.md"),
    ]

    assert get_same_tag_articles(
        None,
        [
            build_article(
                f"{article_base_path}/2021-11-22_avis-patients/content.md"
            ),
            build_article(
                f"{article_base_path}/2021-11-02_rendez-vous/content.md"
            ),
            build_article(
                f"{article_base_path}/2021-12-10_acariens/content.md"
            ),
        ],
    ) == [
        build_article(
            f"{article_base_path}/2021-11-22_avis-patients/content.md"
        ),
        build_article(f"{article_base_path}/2021-11-02_rendez-vous/content.md"),
        build_article(f"{article_base_path}/2021-12-10_acariens/content.md"),
    ]


def test_sorted_articles():
    assert sorted_articles(
        [
            build_article(
                f"{article_base_path}/2021-11-22_avis-patients/content.md"
            ),
            build_article(
                f"{article_base_path}/2021-12-10_acariens/content.md"
            ),
        ]
    ) == [
        build_article(f"{article_base_path}/2021-12-10_acariens/content.md"),
        build_article(
            f"{article_base_path}/2021-11-22_avis-patients/content.md"
        ),
    ]


@freeze_time("2021-11-30")
def test_filter_date_articles():
    assert (
        filter_date_articles(
            [
                build_article(
                    f"{article_base_path}/2021-12-10_acariens/content.md"
                )
            ]
        )
        == []
    )

    assert filter_date_articles(
        [
            build_article(
                f"{article_base_path}/2021-11-22_avis-patients/content.md"
            )
        ]
    ) == [
        build_article(
            f"{article_base_path}/2021-11-22_avis-patients/content.md"
        )
    ]


def test_filter_title_articles():
    assert filter_title_articles(
        [
            build_article(
                f"{article_base_path}/2021-11-22_avis-patients/content.md"
            ),
            build_article(
                f"{article_base_path}/2021-11-27_communication/content.md"
            ),
        ],
        ["foo", "test"],
    ) == [
        build_article(
            f"{article_base_path}/2021-11-22_avis-patients/content.md"
        ),
        build_article(
            f"{article_base_path}/2021-11-27_communication/content.md"
        ),
    ]

    assert filter_title_articles(
        [
            build_article(
                f"{article_base_path}/2021-11-22_avis-patients/content.md"
            ),
            build_article(
                f"{article_base_path}/2021-11-27_communication/content.md"
            ),
        ],
        ["Avis patients"],
    ) == [
        build_article(
            f"{article_base_path}/2021-11-27_communication/content.md"
        ),
    ]


def test_filter_visible_text():
    assert filter_visible_text("<p> Test <p>") == "Test"
    assert (
        filter_visible_text("<h1> Filter visible text <h1> <p> Test <p>")
        == "FiltervisibletextTest"
    )
    assert filter_visible_text("") == ""


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
        build_article(f"{article_base_path}/2021-11-02_rendez-vous/content.md"),
        [
            build_article(
                f"{article_base_path}/2021-11-22_avis-patients/content.md"
            ),
            build_article(
                f"{article_base_path}/2021-11-02_rendez-vous/content.md"
            ),
            build_article(
                f"{article_base_path}/2021-12-10_acariens/content.md"
            ),
            build_article(
                f"{article_base_path}/2021-11-18_4-conseils/content.md"
            ),
        ],
    ) == (
        build_article(
            f"{article_base_path}/2021-11-22_avis-patients/content.md"
        ),
        build_article(f"{article_base_path}/2021-12-10_acariens/content.md"),
    )

    assert (
        get_previous_and_next_articles(
            build_article(
                f"{article_base_path}/2021-11-02_rendez-vous/content.md"
            ),
            [],
        )
        == (None, None)
    )

    assert get_previous_and_next_articles(
        build_article(f"{article_base_path}/2021-11-02_rendez-vous/content.md"),
        [
            build_article(
                f"{article_base_path}/2021-11-22_avis-patients/content.md"
            ),
            build_article(
                f"{article_base_path}/2021-11-02_rendez-vous/content.md"
            ),
        ],
    ) == (
        build_article(
            f"{article_base_path}/2021-11-22_avis-patients/content.md"
        ),
        None,
    )

    assert get_previous_and_next_articles(
        build_article(f"{article_base_path}/2021-11-02_rendez-vous/content.md"),
        [
            build_article(
                f"{article_base_path}/2021-11-02_rendez-vous/content.md"
            ),
            build_article(
                f"{article_base_path}/2021-12-10_acariens/content.md"
            ),
        ],
    ) == (
        None,
        build_article(f"{article_base_path}/2021-12-10_acariens/content.md"),
    )


def test_get_articles_titles():
    assert (
        get_articles_titles(
            [
                build_article(
                    f"{article_base_path}/2021-11-02_rendez-vous/content.md"
                ),
                build_article(
                    f"{article_base_path}/2021-12-10_acariens/content.md"
                ),
                None,
            ],
        )
        == ["Prise de rendez-vous", "Les acariens"]
    )

    assert get_articles_titles([None]) == []
    assert get_articles_titles([]) == []
