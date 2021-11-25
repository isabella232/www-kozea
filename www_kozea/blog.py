import io
import os
from datetime import datetime
from functools import reduce

import frontmatter
import markdown
from flask import Blueprint, render_template, request
from flask_paginate import Pagination, get_page_args, get_page_parameter

from . import MENU_LIST

bp = Blueprint("blog", __name__)

ARTICLE_PER_PAGE = 3


@bp.route("/blog/")
@bp.route("/blog/<tag>")
def blog(tag=None):
    tag = tag
    sorted_articles = sorted(
        build_articles(), key=lambda article: article["date"], reverse=True
    )
    if tag is None:
        sorted_tag_articles = sorted_articles
    else:
        sorted_tag_articles = sorted(
            get_tag_articles(tag, build_articles()),
            key=lambda article: article["date"],
            reverse=True,
        )

    tag_list = reduce(
        tag_list_reducer,
        sorted(
            build_articles(), key=lambda article: article["date"], reverse=True
        ),
        [],
    )
    tag_list = list(set(tag_list))
    tag_list.sort()

    page = request.args.get(get_page_parameter(), type=int, default=1)
    per_page = ARTICLE_PER_PAGE
    offset = (page - 1) * per_page

    total = len(sorted_tag_articles)
    pagination_blog = sorted_tag_articles[offset : offset + per_page]
    pagination = Pagination(page=page, per_page=ARTICLE_PER_PAGE, total=total)

    return render_template(
        "blog.html",
        menu_list=MENU_LIST,
        blogs=pagination_blog,
        tag_list=tag_list,
        pagination=pagination,
    )


@bp.route("/blog/article/<url>")
def display(url):
    article_path = "./www_kozea/article/" + url + "/content.md"
    article = build_article(article_path)
    return render_template("display.html", menu_list=MENU_LIST, article=article)


def build_articles():
    article_paths = get_article_paths()
    return map(build_article, article_paths)


def get_article_paths():
    article_paths = []
    for subdir, dirs, files in os.walk("./www_kozea/article"):
        for file in files:
            if file.endswith(".md"):
                article_paths.append(os.path.join(subdir, file))
    return article_paths


def build_article(article_path):
    directorie = os.path.split(os.path.dirname(article_path))[-1]
    full_directorie = os.path.dirname(article_path)
    # title = directorie.split("_")[1]
    title = parse_md_file(article_path).get("title")
    date = datetime.strptime(directorie.split("_")[0], "%Y-%m-%d")
    url = directorie
    md_content = article_path
    html_content = markdown.markdown(parse_md_file(article_path).content)
    author = parse_md_file(article_path).get("author")
    image = parse_md_file(article_path).get("image")
    tags = tagsToList(parse_md_file(article_path).get("tags"))
    return {
        "title": title,
        "date": date,
        "url": url,
        "md_content": md_content,
        "html_content": html_content,
        "author": author,
        "image": image,
        "tags": tags,
    }


def parse_md_file(article_path):
    md_file = article_path
    with io.open(md_file, "r") as f:
        md_file_fontmatter = frontmatter.load(f)
    return md_file_fontmatter


def get_tag_articles(tag, build_articles):
    tag_articles = []
    for article in build_articles:
        str = article["tags"]
        if tag in str:
            tag_articles.append(article)
    return tag_articles


def tagsToList(tags):
    tag_list = []
    first_tag_list = tags.split(",")
    for tag in first_tag_list:
        tag_list.append(tag.strip().lower())
    tag_list = list(set(tag_list))
    tag_list.sort()
    return tag_list


def tag_list_reducer(tags, article):
    tags.extend(article["tags"])
    return tags
