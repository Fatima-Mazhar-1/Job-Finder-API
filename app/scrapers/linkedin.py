import httpx
from bs4 import BeautifulSoup
from typing import List
import asyncio
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from app.api.models import JobListing, JobSearchRequest
import os
import time
import logging

logger = logging.getLogger(__name__)

async def scrape_linkedin_jobs(request: JobSearchRequest) -> List[JobListing]:
    """
    Scrape job listings from LinkedIn based on the search criteria
    """
    try:
        # Format search query parameters
        position = request.position.replace(" ", "%20")
        location = request.location.replace(" ", "%20") if request.location else ""
        
        # Setup headless browser
        chrome_options = Options()
        if os.environ.get("HEADLESS_BROWSER", "True").lower() == "true":
            chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        
        # Initialize the Chrome driver
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        
        # Construct LinkedIn Jobs URL
        url = f"https://www.linkedin.com/jobs/search/?keywords={position}"
        if location:
            url += f"&location={location}"
        
        logger.info(f"Scraping LinkedIn jobs with URL: {url}")
        driver.get(url)
        
        # Set timeout for page loading
        timeout = int(os.environ.get("SCRAPE_TIMEOUT", 60))
        wait = WebDriverWait(driver, timeout)
        
        # Wait for job listings to load
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "jobs-search__results-list")))
        
        # Scroll to load more jobs
        scroll_attempts = 3
        for _ in range(scroll_attempts):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
        
        # Extract job listings
        jobs_html = driver.page_source
        soup = BeautifulSoup(jobs_html, "html.parser")
        job_cards = soup.select(".jobs-search__results-list > li")
        
        jobs = []
        for job_card in job_cards[:20]:  # Limit to first 20 jobs for speed
            try:
                title_element = job_card.select_one(".base-search-card__title")
                company_element = job_card.select_one(".base-search-card__subtitle")
                location_element = job_card.select_one(".job-search-card__location")
                link_element = job_card.select_one("a.base-card__full-link")
                
                if not all([title_element, company_element, link_element]):
                    continue
                
                job = JobListing(
                    job_title=title_element.text.strip(),
                    company=company_element.text.strip(),
                    location=location_element.text.strip() if location_element else None,
                    apply_link=link_element["href"],
                    source="LinkedIn"
                )
                
                jobs.append(job)
            except Exception as e:
                logger.error(f"Error extracting job data: {e}")
                continue
        
        driver.quit()
        logger.info(f"Successfully scraped {len(jobs)} jobs from LinkedIn")
        return jobs
        
    except Exception as e:
        logger.error(f"LinkedIn scraper error: {e}")
        return [] 