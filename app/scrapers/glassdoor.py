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
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
from app.api.models import JobListing, JobSearchRequest
import os
import time
import logging
import re

logger = logging.getLogger(__name__)

async def scrape_glassdoor_jobs(request: JobSearchRequest) -> List[JobListing]:
    """
    Scrape job listings from Glassdoor based on the search criteria
    """
    try:
        # Setup headless browser
        chrome_options = Options()
        if os.environ.get("HEADLESS_BROWSER", "True").lower() == "true":
            chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
        
        # Initialize the Chrome driver
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        
        # Format search query parameters - simplified to use the main Glassdoor search
        position = request.position.replace(" ", "+")
        location = request.location.replace(" ", "+") if request.location else ""
        
        # Construct a simplified Glassdoor search URL
        url = f"https://www.glassdoor.com/Job/jobs.htm?sc.keyword={position}"
        if location:
            url += f"&locT=C&locId=0&locKeyword={location}"
        
        logger.info(f"Scraping Glassdoor jobs with URL: {url}")
        driver.get(url)
        
        # Set timeout for page loading
        timeout = int(os.environ.get("SCRAPE_TIMEOUT", 60))
        
        # Handle Glassdoor sign-in popup and cookie banners
        try:
            # Wait for any modal to appear (either sign in or cookie consent)
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".modal_main,.selected,.ReactModal__Content,.gdModal"))
            )
            
            # Try to close sign-in modal if present
            try:
                close_buttons = driver.find_elements(By.CSS_SELECTOR, ".modal_closeIcon,.close,[alt='Close'],button.e1jbctw80,button[title='Close']")
                if close_buttons:
                    for button in close_buttons:
                        try:
                            button.click()
                            logger.info("Clicked a close button")
                            time.sleep(1)
                        except (ElementClickInterceptedException, NoSuchElementException):
                            continue
                
                # If we can't find the close button, try clicking outside the modal or hitting escape
                if driver.find_elements(By.CSS_SELECTOR, ".modal_main,.selected"):
                    ActionChains(driver).send_keys_to_element(driver.find_element(By.TAG_NAME, "body"), "\ue00c").perform()
                    logger.info("Sent escape key to close modal")
                    time.sleep(1)
            except Exception as e:
                logger.warning(f"Error handling Glassdoor modal: {e}")
                # Try to continue anyway
                pass
        except TimeoutException:
            # No popup appeared, continue
            logger.info("No modal detected")
            pass
        
        # Wait for job listings to load - try different selectors that Glassdoor might use
        job_listing_selectors = [
            ".jobCard",
            ".react-job-listing",
            ".css-bkasv9",  # Recent Glassdoor job card class
            "[data-test='job-link']",
            ".jobContainer",
            ".jl"
        ]
        
        # Try each selector to find job listings
        job_cards = []
        for selector in job_listing_selectors:
            try:
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                )
                # If we found job listings, break the loop
                logger.info(f"Found job listings with selector: {selector}")
                
                # Scroll to load more jobs and ensure all content is rendered
                scroll_height = 800
                for _ in range(3):
                    driver.execute_script(f"window.scrollBy(0, {scroll_height});")
                    time.sleep(1)
                
                # Extract job listings
                jobs_html = driver.page_source
                soup = BeautifulSoup(jobs_html, "html.parser")
                job_cards = soup.select(selector)
                if job_cards:
                    break
            except TimeoutException:
                continue
        
        if not job_cards:
            logger.warning("Could not find any job listings on Glassdoor")
            return []
        
        jobs = []
        for job_card in job_cards[:20]:  # Limit to first 20 jobs for speed
            try:
                # Try different selectors for job elements based on Glassdoor's structure
                title_element = (
                    job_card.select_one("a.jobTitle, a.job-title, [data-test='job-link'], .jobLink, h2.css-1h5lhqd") or 
                    job_card.select_one("h2, h3, a")
                )
                
                company_element = (
                    job_card.select_one("a.jobCompany, .job-search-card__company-name, [data-test='employer-name'], div.css-19hiur0") or
                    job_card.select_one(".employer-name, .jobInfoItem .company, .css-l2wjgv")
                )
                
                location_element = (
                    job_card.select_one("span.location, [data-test='location'], div.css-6z8o9s") or
                    job_card.select_one(".loc, .location, .subtle.loc, .css-129wfzl")
                )
                
                salary_element = (
                    job_card.select_one("span.salary, [data-test='salary'], div.css-16u8a71") or
                    job_card.select_one(".salary-estimate, .css-1xe2xac")
                )
                
                if not title_element or not company_element:
                    logger.warning("Missing essential job data, skipping")
                    continue
                
                # Extract job title and company name
                job_title = title_element.text.strip()
                company = company_element.text.strip()
                
                # Find the link - try different approaches
                link = None
                
                # Look for href attribute in nested a tags
                link_element = job_card.select_one("a[href*='/job/'], a[href*='glassdoor.com/partner/'], [data-test='job-link']")
                if link_element and 'href' in link_element.attrs:
                    link = link_element['href']
                
                # If link is relative, make it absolute
                if link and not link.startswith(('http://', 'https://')):
                    link = f"https://www.glassdoor.com{link}"
                
                # If we still don't have a link, try to construct one
                if not link:
                    # Try to get job ID
                    job_id_match = re.search(r'data-id=["\'](\d+)["\']', str(job_card))
                    if job_id_match:
                        job_id = job_id_match.group(1)
                        link = f"https://www.glassdoor.com/job-listing/{job_id}"
                
                if not link:
                    logger.warning("Could not find job link, skipping")
                    continue
                
                location = location_element.text.strip() if location_element else None
                salary = salary_element.text.strip() if salary_element else None
                
                # Try to extract job type (full-time, part-time, etc.)
                job_type_element = job_card.select_one(".jobType, [data-test='job-type'], .css-1hx540g")
                job_nature = job_type_element.text.strip() if job_type_element else None
                
                job = JobListing(
                    job_title=job_title,
                    company=company,
                    location=location,
                    salary=salary,
                    jobNature=job_nature,
                    apply_link=link,
                    source="Glassdoor"
                )
                
                jobs.append(job)
                logger.info(f"Extracted job: {job_title} at {company}")
            except Exception as e:
                logger.error(f"Error extracting job data: {e}")
                continue
        
        driver.quit()
        logger.info(f"Successfully scraped {len(jobs)} jobs from Glassdoor")
        return jobs
        
    except Exception as e:
        logger.error(f"Glassdoor scraper error: {e}")
        return [] 