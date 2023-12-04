import os
from dotenv import load_dotenv
import httpx

# Load environment variables from .env file
load_dotenv()


def get_popular_books(startIndex=0, maxResults=9, filterBy="", searchTxt=""):
    base_url = "https://www.googleapis.com/books/v1/volumes"
    if filterBy is not "" and searchTxt is not "":
        params = {
            "q": f'{filterBy}:{searchTxt}',
            "orderBy": "newest",
            "startIndex": startIndex,
            "maxResults": maxResults,
            "printType": "books",
            "key": os.getenv("GOOGLE_BOOKS_API_KEY")
        }
    else:
        params = {
            "q": "search+terms",
            "orderBy": "relevance",
            "startIndex": startIndex,
            "maxResults": maxResults,
            "printType": "books",
            "key": os.getenv("GOOGLE_BOOKS_API_KEY")
        }

    try:
        with httpx.Client() as client:
            response = client.get(base_url, params=params)
            response.raise_for_status()  # Raise an exception for 4xx or 5xx errors
            data = response.json()

            # Extract relevant information from the API response
            books = []
            for item in data.get("items", []):
                volume_info = item.get("volumeInfo", {})

                # Additional book details
                image_links = volume_info.get("imageLinks", {})
                industry_identifiers = volume_info.get("industryIdentifiers", [])
                categories = volume_info.get("categories", [])
                authors = volume_info.get("authors", [])

                book_info = {
                    "id": item.get("id", "N/A"),
                    "title": volume_info.get("title", "N/A"),
                    "subtitle": volume_info.get("subtitle", "N/A"),
                    "publisher": volume_info.get("publisher", "N/A"),
                    "published_date": volume_info.get("publishedDate", "N/A"),
                    "thumbnail": image_links.get("thumbnail", "N/A"),
                    "industry_identifiers": industry_identifiers,
                    "categories": categories,
                    "authors": authors,
                    "pageCount": volume_info.get("pageCount", 0),
                }

                books.append(book_info)
                count = data.get("totalItems", 0)

            return books, count

    except httpx.RequestError as e:
        print(f"Request error: {e}")
        return []
    except httpx.HTTPError as e:
        print(f"HTTP error: {e}")
        return []


def get_book_details(id):
    base_url = f"https://www.googleapis.com/books/v1/volumes/{id}"
    params = {
        "key": os.getenv("GOOGLE_BOOKS_API_KEY")
    }

    try:
        with httpx.Client() as client:
            response = client.get(base_url, params=params)
            response.raise_for_status()  # Raise an exception for 4xx or 5xx errors
            data = response.json()

            volume_info = data.get("volumeInfo", {})

            # Additional book details
            image_links = volume_info.get("imageLinks", {})
            industry_identifiers = volume_info.get("industryIdentifiers", [])
            categories = volume_info.get("categories", [])
            authors = volume_info.get("authors", [])
            dimensions = volume_info.get("dimensions", {'height': 'N/A', 'width': 'N/A', 'thickness': 'N/A'})

            book_info = {
                "id": id,
                "title": volume_info.get("title", "N/A"),
                "subtitle": volume_info.get("subtitle", "N/A"),
                "description": volume_info.get("description", "N/A"),
                "publisher": volume_info.get("publisher", "N/A"),
                "published_date": volume_info.get("publishedDate", "N/A"),
                "thumbnail": image_links.get("thumbnail", "N/A"),
                "industry_identifiers": ', '.join(
                    [f'{isbn["type"]}-{isbn["identifier"]}' for isbn in industry_identifiers]),
                "isbn": industry_identifiers[0]['identifier'] if len(industry_identifiers) > 0 else None,
                "categories": categories,
                "authors": ', '.join(authors),
                "pageCount": volume_info.get("pageCount", 0),
                "previewLink": volume_info.get("previewLink", "N/A"),
                "language": volume_info.get("language", "N/A"),
                "dimensions": dimensions,
            }

            return book_info

    except httpx.RequestError as e:
        print(f"Request error: {e}")
        return None
    except httpx.HTTPError as e:
        print(f"HTTP error: {e}")
        return None
