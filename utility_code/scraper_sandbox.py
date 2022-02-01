# import asyncio
# from playwright.async_api import async_playwright
# from playwright.async_api import async_playwright
# playwright = await async_playwright().start()

# browser = await playwright.chromium.launch()
# page = await browser.new_page()
# await page.goto("http://whatsmyuseragent.org/")

from playwright.sync_api import sync_playwright
from playwright.sync_api import sync_playwright

playwright = sync_playwright().start()

browser = playwright.chromium.launch()
page = browser.new_page()
page.goto("http://whatsmyuseragent.org/")