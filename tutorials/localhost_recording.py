import logging

from playwright.sync_api import Page
from piper import PiperVoice

from tutorial_generator.element_funcs import human_fill, highlight, remove_highlight
from tutorial_generator.page_funcs import blur
from tutorial_generator import generate_tutorial, SectionList

logger = logging.getLogger(__name__)

LOCALHOST = "localhost:5173"
WAIT = 800

sections = SectionList()

@sections.add("Start")
def section_open_site(page: Page):
    page.goto(LOCALHOST, timeout=60000)

@sections.add("Aaaaah, too bright.")
def section_bright(page: Page):
    page.wait_for_timeout(2000)

@sections.add(". Better. Fuck that was bright. Anyway. Today we are going to demo some features of a cool website.")
def section_dark(page: Page):
    page.get_by_role("button", name="Toggle theme").click()
    page.wait_for_timeout(2000)

@sections.add("First. Let see how we use the menu to find the calendar")
def section_calendar1(page: Page):
    page.wait_for_timeout(WAIT)
    button = page.get_by_role("button", name="Pages")
    highlight(button)
    page.wait_for_timeout(WAIT*1.8)
    remove_highlight(button)
    button.click()
    page.wait_for_timeout(WAIT)
    button = page.get_by_role("menuitem", name="Calendar")
    highlight(button)
    page.wait_for_timeout(WAIT)
    button.click()
    page.wait_for_timeout(WAIT)

@sections.add("We can choose a range of dates.")
def section_calendar2(page: Page):
    page.wait_for_timeout(WAIT*4)
    page.get_by_role("button", name="Monday, June 9,").click()
    blur(page)
    page.wait_for_timeout(WAIT)
    page.get_by_role("button", name="Friday, June 13,").click()
    blur(page)

@sections.add("Or. Another range. Pretty good.")
def section_calendar3(page: Page):
    page.wait_for_timeout(2000)
    page.get_by_role("button", name="Monday, July 14,").click()
    blur(page)
    page.wait_for_timeout(800)
    page.get_by_role("button", name="Friday, July 18,").click()
    blur(page)
    page.wait_for_timeout(WAIT)

@sections.add("So cool.")
def section_calendar4(page: Page):
    page.wait_for_timeout(1000)

@sections.add("Moving on.")
def section_login1(page: Page):
    page.wait_for_timeout(1000)
    page.get_by_role("button", name="Pages").click()
    page.wait_for_timeout(800)
    login_button = page.get_by_role("menuitem", name="Login")
    highlight(login_button)
    page.wait_for_timeout(800)
    remove_highlight(login_button)
    login_button.click()

@sections.add("Uh, fancy feature here. A login form.")
def section_login2(page: Page):
    page.wait_for_timeout(600)
    page.get_by_role("textbox", name="Email").click()
    page.wait_for_timeout(600)
    page.get_by_role("button", name="Login", exact=True).click()
    page.wait_for_timeout(700)
    page.get_by_role("textbox", name="Email").click()
    page.wait_for_timeout(200)
    element_email = page.get_by_role("textbox", name="Email")
    human_fill(element_email, "human.man@real-email.com")
    page.wait_for_timeout(WAIT)

    page.get_by_role("textbox", name="Email").press("Tab")
    page.wait_for_timeout(WAIT)
    page.get_by_role("link", name="Forgot your password?").press("Tab")
    page.wait_for_timeout(WAIT)

    element_password = page.get_by_role("textbox", name="Password")
    human_fill(element_password, "notARealPassword")
    page.wait_for_timeout(WAIT)

    page.get_by_role("button", name="Login", exact=True).click()
    page.wait_for_timeout(WAIT)

@sections.add("I told you. So easy.")
def section_action4(page: Page):
    page.wait_for_timeout(1000)
    page.get_by_role("button", name="Pages").click()
    page.get_by_role("menuitem", name="Sign Up").click()
    page.get_by_role("textbox", name="Full Name").click()
    page.get_by_role("textbox", name="Full Name").fill("Jane Doe")
    page.get_by_role("textbox", name="Full Name").press("Tab")
    page.get_by_role("textbox", name="Email").fill("jane.doe@company.com")
    page.get_by_role("textbox", name="Email").press("Tab")
    page.get_by_role("textbox", name="Password", exact=True).fill("password")
    page.get_by_role("textbox", name="Password", exact=True).press("Tab")
    page.get_by_role("textbox", name="Confirm Password").fill("password")
    page.get_by_role("textbox", name="Confirm Password").press("Tab")
    page.get_by_role("button", name="Create Account").click()

@sections.add("I told you. So easy.")
def section_action5(page: Page):
    page.wait_for_timeout(1000)
    page.get_by_role("button", name="Pages").click()
    page.get_by_role("menuitem", name="Sidebar").click()
    page.get_by_role("button", name="Drafts").hover()
    page.get_by_role("button", name="Sent").hover()
    page.get_by_role("button", name="Junk").hover()
    page.get_by_role("button", name="Trash").hover()
    page.get_by_role("button", name="Drafts").hover()
    page.get_by_role("button", name="Drafts").click()

@sections.add("I told you. So easy.")
def section_action6(page: Page):
    page.wait_for_timeout(1000)
    page.get_by_role("button", name="Pages").click()
    page.get_by_role("menuitem", name="Home").click()
    page.wait_for_timeout(1000)


def main():

    voice = PiperVoice.load("./services/video_service/voices/en_US-amy-medium.onnx")

    video_name = "./localhost_recording"

    browser_width, browser_height = 960, 720

    filename = generate_tutorial(video_name, voice, sections.actions, sections.texts, remove_first_section=True, browser_width=browser_width, browser_height=browser_height)

    return filename


if __name__ == "__main__":

    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    logger.info("Start recording")

    main()

    logger.info("Finish recording")
