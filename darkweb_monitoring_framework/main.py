import json
import argparse
from scrapper import scrape_site, load_keywords, load_sites
from tor_setup import get_new_identity
def scrape_and_save(keywords, sites):
    scraped_data = []

    for site in sites:
        result = scrape_site(site, keywords)
        if result:
            scraped_data.append(result)

    # Save scraped data to JSON
    with open("data/scraped_data.json", "w") as outfile:
        json.dump(scraped_data, outfile, indent=4)

    print(f"Scraped data saved to data/scraped_data.json with {len(scraped_data)} entries.")

def generate_report(scraped_data_file):
    try:
        with open(scraped_data_file, "r") as infile:
            scraped_data = json.load(infile)
        
        # Example report generation: count of entries
        report = {
            "total_entries": len(scraped_data),
            "sites_scraped": {entry['url']: entry['matches'] for entry in scraped_data}
        }

        report_file = "data/report.json"
        with open(report_file, "w") as report_outfile:
            json.dump(report, report_outfile, indent=4)

        print(f"Report generated and saved to {report_file}.")
    except FileNotFoundError:
        print(f"Error: The file {scraped_data_file} does not exist.")
    except json.JSONDecodeError:
        print("Error: Failed to decode JSON from the scraped data file.")

def main():
    get_new_identity()
    parser = argparse.ArgumentParser(description="Web Scraper CLI")
    parser.add_argument("--scrape", action="store_true", help="Execute scraping of websites.")
    parser.add_argument("--report", action="store_true", help="Generate a report from scraped data.")
    args = parser.parse_args()

    keywords = load_keywords()
    sites = load_sites()

    if args.scrape:
        scrape_and_save(keywords, sites)

    if args.report:
        generate_report("data/scraped_data.json")

if __name__ == "__main__":
    main()

