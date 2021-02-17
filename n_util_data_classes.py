from typing import List


class NEntry:
    """Represents a n-hentai doujin entry."""

    def __init__(self, digits: str, gallery_id: str, title: str, artists: List[str], tags: List[str], page_count: int, image_url_list: List[str]):
        self.digits: str = digits
        self.gallery_id: str = gallery_id
        self.title: str = title
        self.artists: List[str] = artists
        self.tags: List[str] = tags
        self.page_count: int = page_count
        self.image_url_list: List[str] = image_url_list

    def __str__(self) -> str:
        return str(self.__class__) + ": " + str(self.__dict__)


class MinimizedNEntry:
    """Holds the id and gallery id of an entry"""

    def __init__(self, n_id: str, gallery_id: str):
        self.n_id: str = n_id
        self.gallery_id: str = gallery_id

    def __str__(self) -> str:
        return str(self.__class__) + ": " + str(self.__dict__)


class NUser:
    """Represent a n-hentai user with his favorites."""

    def __init__(self, username: str, fav_count: int, page_count: int, favorite_list: List[MinimizedNEntry]):
        self.username: str = username
        self.fav_count: int = fav_count
        self.page_count: int = page_count
        self.favorite_list: List[MinimizedNEntry] = favorite_list

    def __str__(self) -> str:
        return str(self.__class__) + ": " + str(self.__dict__)
