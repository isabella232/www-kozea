class NoDateInArticleError(Exception):
    """Exception raised for no date in frontmatter article."""

    def __init__(self, article_title, message="article has no date."):
        self.article_title = article_title
        self.message = f"{article_title} {message}"
        super().__init__(self.message)


class TypeDateInArticleError(Exception):
    """Exception raised for error in date in frontmatter article."""

    def __init__(
        self,
        article_title,
        message="article does not have the correct format "
        "for the date. Correct format is YYYY-MM-DD.",
    ):
        self.article_title = article_title
        self.message = f"{article_title} {message}"
        super().__init__(self.message)


class FrontmatterError(Exception):
    """Exception raised for error in frontmatter article."""

    def __init__(self, article_title, message="article has no frontmatter."):
        self.article_title = article_title
        self.message = f"{article_title} {message}"
        super().__init__(self.message)
