from pathlib import Path
from playwright.sync_api import sync_playwright

URL = "https://houseofpickle.podplay.app/community/events?location=tuggerah"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)

    page = browser.new_page()

    page.goto(URL, wait_until="networkidle")

    html = page.content()

    Path("hop_playwright.html").write_text(
        html,
        encoding="utf-8"
    )

    browser.close()

print("Playwright capture complete")
