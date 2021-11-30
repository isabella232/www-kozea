import datetime
import io
import os
from datetime import date
from functools import reduce

import frontmatter
import markdown
from flask import Blueprint, render_template, request, send_from_directory
from flask_paginate import Pagination, get_page_parameter

from . import MENU_LIST
from .error import (
    FrontmatterError,
    NoDateInArticleError,
    TypeDateInArticleError,
)

ARTICLES_PER_PAGE = 5
DIR_PATH = "./www_kozea/articles"

bp = Blueprint("blog", __name__, static_url_path="", static_folder="articles")


@bp.route("/<path:filename>")
def download_file(filename):
    return send_from_directory(DIR_PATH, filename, as_attachment=True)


@bp.route("/blog/")
@bp.route("/blog/tag/<tag>")
def blog(tag=None):
    articles = build_articles()
    visible_articles = list(
        filter(
            lambda article: date.today() >= article["date"],
            get_same_tag_articles(tag, articles),
        )
    )
    sorted_visible_articles = sorted_articles(visible_articles)
    tag_list = articles_tags(articles)
    displayed_articles, pagination = paginate(sorted_visible_articles)

    return render_template(
        "blog.html",
        menu_list=MENU_LIST,
        articles=displayed_articles,
        tag_list=tag_list,
        pagination=pagination,
    )


@bp.route("/blog/<url>")
def article(url):
    articles = build_articles()
    article_path = f"{DIR_PATH}/{url}/content.md"
    my_article = build_article(article_path)
    if len(my_article["tags"]) != 0:
        tag = my_article["tags"][0]
    else:
        tag = None
    same_tag_articles = list(
        filter(
            lambda article: date.today() >= article["date"]
            and article["title"] != my_article["title"],
            get_same_tag_articles(tag, articles),
        )
    )
    sorted_same_tag_articles = sorted_articles(same_tag_articles)[:3]

    return render_template(
        "article.html",
        menu_list=MENU_LIST,
        article=my_article,
        same_tag_articles=sorted_same_tag_articles,
    )


def build_articles():
    """Take the paths to content.md files and return files information."""
    article_paths = find_article_paths(DIR_PATH)
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
    html_content = markdown.markdown(
        parsed_file.content.replace("%ARTICLE_URL%", directory)
    )
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
        "tags": tags,
        "url": directory,
    }


def parse_md_file(article_path):
    """Separate content and front matter in content.md.

    article_path -- the path to content.md file
    """
    with io.open(article_path, "r") as f:
        return frontmatter.load(f)


def sorted_articles(articles):
    """Return articles sorted by date.

    articles (list) -- articles to be sorted
    """
    return sorted(
        articles,
        key=lambda article: article["date"],
        reverse=True,
    )


def get_same_tag_articles(tag, articles):
    """Return articles with the same tag.

    tag -- tag of articles we want to display
    articles -- all articles
    """
    if tag is None:
        return articles
    else:
        return list(filter(lambda article: tag in article["tags"], articles))


def tags_to_list(tags):
    """Return a sorted tags list with unique tags from tags in content.md.

    tags (str) -- the value of the variable tags in content.md file
    """
    tag_list = []
    if tags is not None:
        first_tag_list = tags.split(",")
        for tag in first_tag_list:
            tag_list.append(tag.strip().lower())
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


def paginate(articles):
    """Return articles to be displayed per page and pagination configuration.

    articles (list) -- list of articles to paginate
    """
    page = request.args.get(get_page_parameter(), type=int, default=1)
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
