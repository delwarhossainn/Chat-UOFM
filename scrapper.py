import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import tldextract
import re
from collections import deque

visited_urls = set()


def clean_text_function(text):
    return re.sub(r"\s+", " ", text).strip()  


def extract_clean_text(url, output_file):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

       
        for tag in soup(["script", "style", "nav", "footer", "header", "aside"]):
            tag.decompose()

        
        text = soup.get_text(separator=" ", strip=True)
        clean_text = clean_text_function(text)

        if clean_text:  
            with open(output_file, "a", encoding="utf-8") as file:  # Append mode
                file.write(clean_text + "\n\n")

            print(f"Scraped and saved: {url}")

    except Exception as e:
        print(f"Error scraping {url}: {e}")


def get_links(url, base_domain):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        links = set()
        for anchor in soup.find_all("a", href=True):
            full_url = urljoin(url, anchor["href"])

            extracted_domain = tldextract.extract(full_url)
            base_extracted_domain = tldextract.extract(base_domain)

            if extracted_domain.domain == base_extracted_domain.domain and extracted_domain.suffix == base_extracted_domain.suffix:
                links.add(full_url)

        return links
    except Exception as e:
        print(f"Error getting links from {url}: {e}")
        return set()


def scrape_website(base_url, base_domain, output_file):
    queue = deque([base_url])

    while queue:
        url = queue.popleft()

        if url in visited_urls:
            continue

        visited_urls.add(url)

        extract_clean_text(url, output_file)  
        links = get_links(url, base_domain)

        for link in links:
            if link not in visited_urls:
                queue.append(link)


def main():
    base_url = "https://umanitoba.ca/"
    base_domain = tldextract.extract(base_url).registered_domain
    output_file = "clean_text_data.txt"

    
    open(output_file, "w", encoding="utf-8").close()

    scrape_website(base_url, base_domain, output_file)

    print(f"Scraping completed. Data saved to '{output_file}'.")

if __name__ == "__main__":
    main()
