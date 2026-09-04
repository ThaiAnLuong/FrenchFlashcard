import requests


class ImageSearch:
    API_URL = "https://commons.wikimedia.org/w/api.php"

    def search(self, query):
        params = {
            "action": "query",
            "generator": "search",
            "gsrsearch": query,
            "gsrnamespace": 6,
            "gsrlimit": 1,
            "prop": "imageinfo",
            "iiprop": "url",
            "iiurlwidth": 800,
            "format": "json",
        }

        response = requests.get(
            self.API_URL,
            params=params,
            headers={
                "User-Agent": (
                    "FrenchFlashcard/1.0 "
                    "(vocabulary learning application)"
                )
            },
            timeout=10
        )

        response.raise_for_status()

        data = response.json()

        pages = (
            data
            .get("query", {})
            .get("pages", {})
        )

        if not pages:
            return None

        first_page = next(
            iter(pages.values())
        )

        image_info = first_page.get(
            "imageinfo",
            []
        )

        if not image_info:
            return None

        return image_info[0].get(
            "thumburl"
        )