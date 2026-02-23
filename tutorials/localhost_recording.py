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

@sections.add("Let us learn how to navigate a simple website. But. Aaaaah! Website is too bright!")
def section_bright(page: Page):
    page.wait_for_timeout(WAIT*4)

@sections.add(None)
def section_bright(page: Page):
    page.wait_for_timeout(WAIT)
    button = page.get_by_role("button", name="Toggle theme")
    highlight(button)
    page.wait_for_timeout(WAIT)
    button.click()
    remove_highlight(button)
    page.wait_for_timeout(WAIT*0.5)

@sections.add("Better. Fuck that was bright. Anyway. Today we are going to demo some features of a website.")
def section_dark(page: Page):
    page.wait_for_timeout(WAIT*4)

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

# @sections.add("Or. Another range. Pretty good.")
def section_calendar3(page: Page):
    page.wait_for_timeout(WAIT*4)
    page.get_by_role("button", name="Monday, July 14,").click()
    blur(page)
    page.wait_for_timeout(WAIT)
    page.get_by_role("button", name="Friday, July 18,").click()
    blur(page)
    page.wait_for_timeout(WAIT)

@sections.add("So cool.")
def section_calendar4(page: Page):
    page.wait_for_timeout(WAIT*2)


@sections.add("Now. Let us sign up for an account.")
def section_signup_nav(page: Page):
    page.wait_for_timeout(WAIT)
    button = page.get_by_role("button", name="Pages")
    highlight(button)
    page.wait_for_timeout(WAIT)
    remove_highlight(button)
    button.click()
    page.wait_for_timeout(WAIT)
    signup_button = page.get_by_role("menuitem", name="Sign Up")
    highlight(signup_button)
    page.wait_for_timeout(WAIT)
    signup_button.click()
    page.wait_for_timeout(WAIT)

@sections.add("Just fill and press create")
def section_signup_fast(page: Page):
    page.wait_for_timeout(WAIT)
    page.get_by_role("textbox", name="Full Name").fill("Jane Doe")
    page.get_by_role("textbox", name="Email").fill("jane.doe@company.com")
    page.get_by_role("textbox", name="Password", exact=True).fill("password")
    page.get_by_role("textbox", name="Confirm Password").fill("password")
    page.get_by_role("button", name="Create Account").click()
    page.wait_for_timeout(WAIT)

@sections.add("What")
def section_signup_too_fast(page: Page):
    page.wait_for_timeout(WAIT*2)

@sections.add("Was it too fast?")
def section_signup_too_fast(page: Page):
    page.wait_for_timeout(WAIT*3)
    page.get_by_role("button", name="Continue").click()
    page.wait_for_timeout(WAIT)

@sections.add("Okay.")
def section_signup_redo_nav(page: Page):
    page.wait_for_timeout(WAIT*1.5)

@sections.add("Let me redo it.")
def section_signup_redo_nav(page: Page):
    page.wait_for_timeout(WAIT)
    page.reload()
    page.wait_for_timeout(WAIT)

@sections.add("First. Full name.")
def section_signup_slow_name(page: Page):
    page.wait_for_timeout(WAIT)
    human_fill(page.get_by_role("textbox", name="Full Name"), "Jane Doe")
    blur(page)
    page.wait_for_timeout(WAIT)

@sections.add("Email.")
def section_signup_slow_email(page: Page):
    human_fill(page.get_by_role("textbox", name="Email"), "jane.doe@company.com")
    blur(page)
    page.wait_for_timeout(WAIT)

@sections.add("Password.")
def section_signup_slow_password(page: Page):
    human_fill(page.get_by_role("textbox", name="Password", exact=True), "password")
    blur(page)
    page.wait_for_timeout(WAIT)
    human_fill(page.get_by_role("textbox", name="Confirm Password"), "password")
    blur(page)
    page.wait_for_timeout(WAIT)

@sections.add("Then. Create account.")
def section_signup_slow_submit(page: Page):
    button = page.get_by_role("button", name="Create Account")
    button.scroll_into_view_if_needed()
    highlight(button)
    page.wait_for_timeout(WAIT)
    remove_highlight(button)
    button.click()
    page.wait_for_timeout(WAIT*2)
    page.get_by_role("button", name="Continue").click()
    page.wait_for_timeout(WAIT)

@sections.add("Now let us navigate a email interface")
def section_sidebar1(page: Page):
    page.wait_for_timeout(WAIT)
    button = page.get_by_role("button", name="Pages")
    highlight(button)
    page.wait_for_timeout(WAIT)
    remove_highlight(button)
    button.click()
    page.wait_for_timeout(WAIT)
    sidebar_button = page.get_by_role("menuitem", name="Sidebar")
    highlight(sidebar_button)
    page.wait_for_timeout(WAIT)
    sidebar_button.click()
    page.wait_for_timeout(WAIT)

@sections.add("Notice the hover effects")
def section_sidebar2(page: Page):
    page.wait_for_timeout(WAIT)

@sections.add(None)
def section_sidebar3(page: Page):
    page.wait_for_timeout(WAIT)

@sections.add("Drafts")
def section_sidebar4(page: Page):
    page.get_by_role("button", name="Drafts").hover()
    page.wait_for_timeout(WAIT)
    page.get_by_role("button", name="Drafts").click()
    page.wait_for_timeout(WAIT*2.5)

@sections.add("Sent")
def section_sidebar6(page: Page):
    page.get_by_role("button", name="Sent").hover()
    page.wait_for_timeout(WAIT)
    page.get_by_role("button", name="Sent").click()
    page.wait_for_timeout(WAIT*2.5)

@sections.add("Junk")
def section_sidebar7(page: Page):
    page.get_by_role("button", name="Junk").hover()
    page.wait_for_timeout(WAIT)
    page.get_by_role("button", name="Junk").click()
    page.wait_for_timeout(WAIT*3)

@sections.add("Wait.")
def section_sidebar8(page: Page):
    page.wait_for_timeout(WAIT)

@sections.add("There is an email from you. I really should reply.")
def section_sidebar8(page: Page):
    page.wait_for_timeout(WAIT)

@sections.add(None)
def section_sidebar8(page: Page):
    page.wait_for_timeout(WAIT)

@sections.add("But not now.")
def section_sidebar8(page: Page):
    page.wait_for_timeout(WAIT)

@sections.add("Let us navigate back to home")
def section_end1(page: Page):
    page.wait_for_timeout(WAIT)
    page.get_by_role("button", name="Pages").click()
    page.wait_for_timeout(WAIT)
    page.get_by_role("menuitem", name="Home").click()
    page.wait_for_timeout(WAIT*2)

@sections.add(None)
def section_end2(page: Page):
    page.wait_for_timeout(WAIT)

@sections.add("Thanks for watching this tutorial")
def section_end3(page: Page):
    pass

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
