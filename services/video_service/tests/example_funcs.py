import logging
from pathlib import Path

from playwright.sync_api import Page
from piper import PiperVoice

from tutorial_generator.page_funcs import human_like_select_and_fill
from tutorial_generator.video_funcs import generate_video
from tutorial_generator.speech_funcs import generate_audio
from tutorial_generator import generate_tutorial

logger = logging.getLogger(__name__)


def section_open_site(page: Page):
    page.goto("https://molcalc.org", timeout=60000)


def section_search_propane(page: Page):
    page.wait_for_selector("#searchbar")
    page.wait_for_timeout(2000)
    human_like_select_and_fill(page, "#searchbar", "Propane")
    page.press("#searchbar", "Enter")
    page.locator(".meter > span").wait_for(state="hidden")


def section_view_results(page: Page):

    page.get_by_role("link", name="Calculate Properties").scroll_into_view_if_needed()
    page.wait_for_timeout(3000)
    page.get_by_role("link", name="Calculate Properties").click()

    page.wait_for_timeout(3000)
    page.get_by_text("Indeed").click()

    page.wait_for_url("**/calculations/**")

    page.wait_for_timeout(3000)


def section_conclusion(page: Page):

    page.wait_for_timeout(3000)



def main():

    voice = PiperVoice.load("./voices/en_US-amy-medium.onnx")

    video_name = "how_to_molcalc"

    section_texts = [
        "Hi.",
        "Search for Propane",
        "View the results",
        "Damn, that looks awesome.",
    ]

    section_actions = [
        section_open_site,
        section_search_propane,
        section_view_results,
        section_conclusion,
    ]

    filename = generate_tutorial(video_name, voice, section_actions, section_texts, remove_first_section=True)

    return


if __name__ == "__main__":

    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    logger.info("Start molcalc example")

    main()

    logger.info("Finish molcalc example")
