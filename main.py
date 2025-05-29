import asyncio

from crawl4ai import AsyncWebCrawler
from dotenv import load_dotenv

from config import BASE_URL, CSS_SELECTOR, REQUIRED_KEYS
from utils.data_utils import save_projects_to_csv  # Updated function name
from utils.scraper_utils import (
    fetch_and_process_page,
    get_browser_config,
    get_llm_strategy,
)

load_dotenv()


async def crawl_projects():
    """
    Main function to crawl project data from the website.
    """
    # Initialize configurations
    browser_config = get_browser_config()
    llm_strategy = get_llm_strategy()
    session_id = "projects_crawl_session"

    # Initialize state variables
    page_number = 1
    all_projects = []
    seen_names = set()

    # Start the web crawler context
    async with AsyncWebCrawler(config=browser_config) as crawler:
        while True:
            # Fetch and process data from the current page
            projects, no_results_found = await fetch_and_process_page(
                crawler,
                page_number,
                BASE_URL,
                CSS_SELECTOR,
                llm_strategy,
                session_id,
                REQUIRED_KEYS,
                seen_names,
            )

            if no_results_found:
                print("No more projects found. Ending crawl.")
                break  # Stop crawling when "No Results Found" message appears

            if not projects:
                print(f"No projects extracted from page {page_number}.")
                break  # Stop if no projects are extracted

            # Add the projects from this page to the total list
            all_projects.extend(projects)
            page_number += 1  # Move to the next page

            # Pause between requests to be polite and avoid rate limits
            await asyncio.sleep(2)  # Adjust sleep time as needed

    # Save the collected projects to a CSV file
    if all_projects:
        save_projects_to_csv(all_projects, "project_reports.csv")  # Updated function call
        print(f"Saved {len(all_projects)} projects to 'project_reports.csv'.")
    else:
        print("No projects were found during the crawl.")

    # Display usage statistics for the LLM strategy
    llm_strategy.show_usage()


async def main():
    """
    Entry point of the script.
    """
    await crawl_projects()  # Updated function call


if __name__ == "__main__":
    asyncio.run(main())
