import asyncio
import logging
from pathlib import Path

from playwright.async_api import Page
from tutorial_generator import VideoTutorialGenerator
from tutorial_generator.page_funcs import human_like_select_and_fill

logger = logging.getLogger(__name__)


# Section functions for molcalc workflow
async def section_open_site(page: Page):
    await page.goto("https://molcalc.org", timeout=60000)


async def section_search_propane(page: Page):
    await page.wait_for_selector("#searchbar")
    await page.wait_for_timeout(2000)
    await human_like_select_and_fill(page, "#searchbar", "Propane")
    await page.press("#searchbar", "Enter")


async def section_view_results(page: Page):
    await page.wait_for_timeout(3000)


async def main():
    # Initialize the video tutorial generator
    generator = VideoTutorialGenerator(
        viewport_width=1200, viewport_height=900, slowmo=100, video_dir="videos/"
    )

    # Start the browser and recording
    await generator.start(headless=True)

    # Define sections to run
    sections = [
        ("open_site", section_open_site),
        ("search_propane", section_search_propane),
        ("view_results", section_view_results),
    ]

    # Run each section and capture timings
    for section_name, section_func in sections:
        logging.info(f"Running section: {section_name}")
        timing = await generator.run_section(section_name, section_func)
        logging.info(f"Duration: {timing.duration:.2f}s")

    # Get all timings
    timings = generator.get_timings()
    for timing in timings:
        logging.info(f"{timing['name']}: {timing['duration']:.2f}s")

    # Close browser and get video info
    result = await generator.close()

    # Rename video with segment name
    segment_name = "01_molcalc_propane_search"
    video_path = Path(result["video_path"])
    new_video_path = video_path.parent / f"{segment_name}{video_path.suffix}"
    video_path.rename(new_video_path)

    print(f"\nVideo saved to: {new_video_path}")
    print(f"Total sections: {len(result['timings'])}")


if __name__ == "__main__":
    asyncio.run(main())
