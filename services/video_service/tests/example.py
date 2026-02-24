import asyncio
from pathlib import Path

from playwright.async_api import async_playwright

SLOWMO = 100

VIEWPOINT_WIDTH = 1200
VIEWPOINT_HEIGHT = 900


async def firefox_example():
    async with async_playwright() as p:

        segment_name = "01_open_molcalc"

        # Launch Firefox browser
        browser = await p.chromium.launch(headless=True, slow_mo=SLOWMO)

        # Create browser context and page
        context = await browser.new_context(
            record_video_dir="videos/",
            viewport=dict(width=VIEWPOINT_WIDTH, height=VIEWPOINT_HEIGHT),
            record_video_size=dict(width=VIEWPOINT_WIDTH, height=VIEWPOINT_HEIGHT),
        )
        page = await context.new_page()

        # Navigate to a webpage
        await page.goto("https://molcalc.org")

        # Wait for button to be visible and click it
        await page.wait_for_selector("#searchbar")
        await page.wait_for_timeout(2000)

        await page.fill("#searchbar", "Propane")

        await page.press("#searchbar", "Enter")

        # Wait a moment to see the result
        await page.wait_for_timeout(3000)

        # Save video
        # page.video.save_as(f"videos/{segment_name}.webm")

        # Close browser
        await context.close()
        await browser.close()

        # Move the video
        video_path = await page.video.path()
        video_path = Path(video_path)

        print(video_path)

        video_path.rename(video_path.parent / Path(f"{segment_name}{video_path.suffix}"))


# Run the example
asyncio.run(firefox_example())
