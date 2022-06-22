import os
import re
import sys

import requests
from bs4 import BeautifulSoup
from markdownify import markdownify

static_folder = "./www_kozea/articles"

url = f"https://kozeagroup.wordpress.com/{sys.argv[1]}"
url_dict = re.match(
    r"https://kozeagroup.wordpress.com/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/(?P<title>\S+)/",
    url,
)

article_folder_title = url_dict["title"]
article_date = f"{url_dict['year']}-{url_dict['month']}-{url_dict['day']}"
article_folder_name = f"{article_date}_{article_folder_title}"

folderpath = os.path.join(static_folder, article_folder_name)
if not os.path.exists(folderpath):
    os.makedirs(folderpath)
    print(f"The {article_folder_name} folder has been created")

filepath = os.path.join(folderpath, "content.md")

req = requests.get(url)
if req.status_code == 200:
    content = BeautifulSoup(req.content, "html.parser")
    article_title = content.find(class_="entry-title").get_text()
    tag_list = []
    for tag in content.find_all(rel="category tag"):
        tag = tag.get_text()
        tag_list.append(tag)
    tags = ", ".join(tag_list)
    principal_image_link = content.find_all("img")[1].get("src")
    principal_image_content = requests.get(principal_image_link).content
    principal_image_path = os.path.join(
        folderpath, f"{article_folder_title}.webp"
    )
    with open(principal_image_path, "wb") as handler:
        handler.write(principal_image_content)
        print(f"The principal image {article_folder_name} has been created.")

    html = content.find("div", class_="post-content")
    images = html.find_all("img")
    for img in images:
        image_link = img.get("src")
        image_title = img.get("data-image-title")
        image_content = requests.get(image_link).content
        image_path = os.path.join(folderpath, f"{image_title}.png")
        with open(image_path, "wb") as handler:
            handler.write(image_content)
            print(f"The image {image_title} has been created.")

        img["src"] = f"/{article_folder_name}/{image_title}.png"

    for child in html.find_all("script"):
        child.decompose()

    for child in html.find_all(
        "div",
        class_=lambda x: x != "wp-block-image",
    ):
        child.decompose()

    md = markdownify(html.prettify(), heading_style="ATX")

    f = open(filepath, "w")
    f.write(
        f"""\
---
author: Laurène Jover
title: "{article_title}"
date: {article_date}
tags: {tag}
caption: {article_folder_title}.webp
---

{md}
"""
    )
    f.close()
    print("content.md file has been created and filled.")
else:
    print("Web page inaccessible.")
