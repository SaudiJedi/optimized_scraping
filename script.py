from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import asyncio
from asyncio import Semaphore
import time

options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

# Initialize Selenium WebDriver outside of the async function
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

async def extract_data(sem, url):
    async with sem:
        try:
            driver.get(url)
            print(driver.title)
            # Your code to extract data
            # ...
        finally:
            # No need to quit the driver here if we're reusing it
            pass

async def main():
    sem = Semaphore(5)  # Adjust this number as needed
    urls = ["https://python.org" for i in range(10)]  # Your list of URLs
    tasks = [extract_data(sem, url) for url in urls]
    await asyncio.gather(*tasks)

# Make sure to quit the driver after all tasks are done
def close_driver():
    driver.quit()

now = time.time()
asyncio.run(main())
then = time.time()
close_driver()  # Quit the driver here

print(f'runtime: {then-now} seconds')
