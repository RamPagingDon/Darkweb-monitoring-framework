import re
import logging
from bs4 import BeautifulSoup
from tor_setup import get_tor_session

# Configure logging
logging.basicConfig(filename="logs/monitoring.log", level=logging.INFO, format="%(asctime)s - %(message)s")

# Load keywords from config file
def load_keywords():
    with open("config/keywords.txt", "r") as file:
        return [line.strip() for line in file]

# Load onion sites from config file
def load_sites():
    with open("config/sites.txt", "r") as file:
        return [line.strip() for line in file]

# Scraping function
def scrape_site(url, keywords):
    session = get_tor_session()
    try:
        response = session.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        # Simple data extraction
        text_content = soup.get_text()
        # Count occurrences of each keyword
        matches = {keyword: len(re.findall(keyword, text_content, re.IGNORECASE)) for keyword in keywords}

        # Save matches if found
        if any(count > 0 for count in matches.values()):
            logging.info(f"Matches found on {url}: {matches}")
            return {"url": url, "matches": matches}
        else:
            logging.info(f"No matches found on {url}")
            return None
    except Exception as e:
        logging.error(f"Failed to scrape {url}: {e}")
        return None
