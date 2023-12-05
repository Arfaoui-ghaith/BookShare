import os
from dotenv import load_dotenv
import httpx
from bs4 import BeautifulSoup
import re

# Load environment variables from .env file
load_dotenv()


def get_popular_books(startIndex=0, maxResults=9, filterBy="", searchTxt=""):
    base_url = "https://www.googleapis.com/books/v1/volumes"

    if filterBy != "" and searchTxt != "":
        params = {
            "q": f'{filterBy}:{str(searchTxt).strip()}',
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

            return books, data.get("totalItems", 0), data

    except httpx.RequestError as e:
        print(f"Request error: {e}")
        return [], 0, None
    except httpx.HTTPError as e:
        print(f"HTTP error: {e}")
        return [], 0, None


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
                "isbn_list": [isbn['identifier'] for isbn in industry_identifiers],
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


def scrape_urls(url):
    try:
        # Send an HTTP GET request to the specified URL using httpx
        with httpx.Client() as client:
            response = client.get(url)
            response.raise_for_status()  # Raise an exception for bad requests

            # Parse the HTML content of the page using BeautifulSoup
            soup = BeautifulSoup(response.text, 'html.parser')

            # Extract URLs from the page containing "http://library.lol/main/"
            library_lol_main_pattern = re.compile(r'http://library\.lol/main/')
            urls = []
            for a_tag in soup.find_all('a', href=True):
                href = a_tag['href']
                # Filter URLs containing "http://library.lol/main/"
                if library_lol_main_pattern.search(href):
                    urls.append(href)

            return urls

    except httpx.RequestError as e:
        print(f"HTTP request error: {e}")
        return []
    except Exception as e:
        print(f"Error: {e}")
        return []


def scrape_download_content(urls):
    try:
        with httpx.Client() as client:
            for url in urls:
                response = client.get(url)
                response.raise_for_status()  # Raise an exception for bad requests

                # Parse the HTML content of the page using BeautifulSoup
                soup = BeautifulSoup(response.text, 'html.parser')

                # Find the first <div> tag with id="download"
                download_div = soup.find('div', {'id': 'download'})
                if download_div:
                    # Return the content of the found <div> tag
                    return download_div.find('a').get('href')

            # If no matching <div> is found on any page
            return None

    except httpx.RequestError as e:
        print(f"HTTP request error: {e}")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None
