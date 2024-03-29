import datetime
import io
import math
import os
import re
from datetime import date
from functools import reduce

import frontmatter
import markdown
from flask import (
    Blueprint,
    current_app,
    render_template,
    request,
    send_from_directory,
)
from flask_paginate import Pagination
from jinja2 import Environment, pass_context

from . import MENU_LIST
from .error import (
    FrontmatterError,
    NoDateInArticleError,
    TypeDateInArticleError,
)

WPM = 200
WORD_LENGTH = 5
ARTICLES_PER_PAGE = 12
MAX_SIMILAR_ARTICLES = 3


bp = Blueprint("blog", __name__, static_url_path="", static_folder="articles")


def build_env():  # pragma: no cover
    @pass_context
    def image_url_filter(context, image_filename):
        return f"/{context['directory']}/{image_filename}"

    def article_url_filter(article_id):
        return f"../{article_id}"

    env = Environment()
    env.filters["article_url"] = article_url_filter
    env.filters["image_url"] = image_url_filter

    return env


env = build_env()


@bp.route("/<path:filename>")
def download_file(filename):  # pragma: no cover
    return send_from_directory(bp.static_folder, filename, as_attachment=True)


@bp.route("/blog/")
@bp.route("/blog/page/<int:page>/")
@bp.route("/blog/tag/<tag>/")
@bp.route("/blog/tag/<tag>/page/<int:page>/")
def blog(tag=None, page=1):  # pragma: no cover
    pinned_article = build_pinned_article()
    articles = build_articles(bp.static_folder)
    same_tag_articles = past_articles(get_articles_with_tag(tag, articles))
    visible_articles = different_title_articles(
        same_tag_articles, get_articles_titles([pinned_article])
    )
    sorted_visible_articles = sort_articles(visible_articles)
    tag_list = articles_tags(articles)
    displayed_articles, pagination = paginate(sorted_visible_articles, page)
    return render_template(
        "blog.html",
        menu_list=MENU_LIST,
        pinned_article=pinned_article,
        articles=displayed_articles,
        tag_list=tag_list,
        page=request.url_rule.endpoint,
        page_tag=tag,
        pagination=pagination,
    )


@bp.route("/blog/<url>/")
def article(url):  # pragma: no cover
    articles = build_articles(bp.static_folder)
    sorted_visible_articles = sort_articles(past_articles(articles))
    article_path = f"{bp.static_folder}/{url}/content.md"
    current_article = build_article(article_path)
    previous_article, next_article = get_previous_and_next_articles(
        current_article, sorted_visible_articles
    )
    excluded_articles = [current_article, previous_article, next_article]
    tag = get_main_tag(current_article["tags"])
    same_tag_articles = different_title_articles(
        get_articles_with_tag(tag, sorted_visible_articles),
        get_articles_titles(excluded_articles),
    )
    sorted_same_tag_articles = sort_articles(same_tag_articles)[
        :MAX_SIMILAR_ARTICLES
    ]

    return render_template(
        "article.html",
        menu_list=MENU_LIST,
        article=current_article,
        next_article=next_article,
        previous_article=previous_article,
        same_tag_articles=sorted_same_tag_articles,
        article_full_url=request.url,
    )


def build_articles(dir_path):
    """Take the paths to content.md files and return files information."""
    article_paths = find_article_paths(dir_path)
    return list(map(build_article, article_paths))


def find_article_paths(dir_path):
    """Return the paths to content.md files.

    dir_path -- the path to the folder where the articles are located
    """
    article_paths = []
    for subdir, dirs, files in os.walk(dir_path):
        for file in files:
            if file == "content.md":
                article_paths.append(os.path.join(subdir, file))
    return article_paths


def build_article(article_path):
    """Transform the content of content.md file to html and return it
    along with the information in content.md file.

    article_path -- the path to content.md file
    """
    directory = os.path.split(os.path.dirname(article_path))[-1]
    parsed_file = parse_md_file(article_path)
    if len(parsed_file.metadata) == 0:
        raise (FrontmatterError(directory))

    md_template = env.from_string(parsed_file.content)
    md = markdown.Markdown(extensions=["toc"])
    html_content = md.convert(md_template.render(directory=directory))
    reading_time = estimate_reading_time(html_content)
    tags = tags_to_list(parsed_file.get("tags"))
    date = parsed_file.get("date")
    if date is None:
        raise (NoDateInArticleError(directory))
    if type(date) is not datetime.date:
        raise (TypeDateInArticleError(directory))

    return {
        **parsed_file,
        "md_content": parsed_file.content,
        "html_content": html_content,
        "time": reading_time,
        "tags": tags,
        "url": directory,
        "toc": md.toc,
    }


def build_pinned_article():  # pragma: no cover
    """Retrieve the pinned article path from the configuration
    and apply build_article function to it."""
    pinned_article_url = current_app.config.get("BLOG_PINNED_ARTICLE_URL")
    pinned_article_path = f"{bp.static_folder}/{pinned_article_url}/content.md"
    return build_article(pinned_article_path)


def parse_md_file(article_path):
    """Separate content and front matter in content.md.

    article_path -- the path to content.md file
    """
    with io.open(article_path, "r") as f:
        return frontmatter.load(f)


def sort_articles(articles):
    """Return articles sorted by date.

    articles (list) -- articles to be sorted
    """
    return sorted(
        articles,
        key=lambda article: article["date"],
        reverse=True,
    )


def past_articles(articles):
    """Return list of articles dated before the current date.

    articles -- list of articles to filter
    """
    return list(
        filter(
            lambda article: date.today() >= article["date"],
            articles,
        )
    )


def different_title_articles(articles, titles):
    """Return list of articles that do not have the same
    title as the current, previous and next article.

    articles -- list of articles to filter
    titles -- titles of current previous and next article
    """
    return list(
        filter(
            lambda article: article["title"] not in titles,
            articles,
        )
    )


def get_articles_with_tag(tag, articles):
    """Return articles with the same tag.

    tag -- tag of articles we want to display
    articles -- all articles
    """
    if tag is None:
        return articles
    else:
        return list(filter(lambda article: tag in article["tags"], articles))


def get_articles_titles(articles):
    """Return list of articles titles.

    articles -- list of articles
    """
    titles = []
    for article in articles:
        if article is not None:
            title = article["title"]
            titles.append(title)
    return titles


def get_previous_and_next_articles(article, articles_list):
    """Return previous and next articles.

    index -- current article index
    articles_list -- list of articles
    """
    if article in articles_list:
        index = articles_list.index(article)
        if index != 0:
            previous_article = articles_list[index - 1]
        else:
            previous_article = None
        if index != len(articles_list) - 1:
            next_article = articles_list[index + 1]
        else:
            next_article = None
    else:
        previous_article = None
        next_article = None
    return previous_article, next_article


def tags_to_list(tags):
    """Return a sorted tags list with unique tags from tags in content.md.

    tags (str) -- the value of the variable tags in content.md file
    """
    tag_list = []
    if tags is not None:
        first_tag_list = tags.split(",")
        for tag in first_tag_list:
            tag_list.append(tag.strip().lower().capitalize())
        tag_list = sorted(list(set(tag_list)))
        if "" in tag_list:
            tag_list.remove("")
    return tag_list


def tag_list_reducer(tags_list, article):
    """Return list of all tags of all articles.

    tags_list (list) -- list of tags
    """
    tags_list.extend(article["tags"])
    return tags_list


def articles_tags(articles):
    """Return sorted and unique tags.

    articles (list) -- list of articles to get tags from
    """
    tag_list = reduce(tag_list_reducer, articles, [])
    return sorted(list(set(tag_list)))


def get_main_tag(tags_list):
    """Return main tag in tags list if existe.

    tags_list -- list of tags
    """
    if len(tags_list) != 0:
        return tags_list[0]
    else:
        return None


def paginate(articles, page):  # pragma: no cover
    """Return articles to be displayed per page and pagination configuration.

    articles (list) -- list of articles to paginate
    """
    offset = (page - 1) * ARTICLES_PER_PAGE
    total = len(articles)
    displayed_articles = articles[offset : offset + ARTICLES_PER_PAGE]
    pagination = Pagination(
        page=page,
        per_page=ARTICLES_PER_PAGE,
        total=total,
        css_framework="semantic",
    )
    return displayed_articles, pagination


def strip_html_markup(text):
    """Return a string without HTML-tags.

    text -- html content
    """
    html_tags_re = re.compile("<.*?>")
    text = re.sub(html_tags_re, "", text)
    return "".join(text.split())


def count_words_in_text(text, word_length):
    """Return the number of words in a given text.

    text -- the text we want to calculates its words
    """
    return len(text) / word_length


def estimate_reading_time(html_content):
    """Return the estimated reading time.

    html_content = HTML text
    """
    filtered_text = strip_html_markup(html_content)
    total_words = count_words_in_text(filtered_text, WORD_LENGTH)
    reading_time = math.ceil(total_words / WPM)
    return reading_time if reading_time > 0 else 1
