from time import sleep
import random

HIGHLIGHT_CLASSNAME = "highlight"

def slow_writing(
    element,
    text: str,
    min_delay: float = 0.05,
    max_delay: float = 0.15,
    has_mistakes=True,
    clear_element=True,
):

    if clear_element:
        element.clear()

    element.click()

    for char in text:
        element.type(char, delay=0)
        delay = random.uniform(min_delay, max_delay)

        if random.random() < 0.1:
            delay += random.uniform(0.2, 0.5)

        if has_mistakes and random.random() < 0.05:
            wrong_char = random.choice("abcdefghijklmnopqrstuvwxyz")
            element.type(wrong_char, delay=0)
            sleep(random.uniform(0.1, 0.3))
            element.press("Backspace")
            sleep(random.uniform(0.1, 0.2))

        sleep(delay)


def human_fill(element, text, clear_first=True):

    sleep(random.uniform(0.1, 0.3))

    try:
        element.click()
    except Exception as _:
        element.focus()

    sleep(random.uniform(0.1, 0.2))

    if clear_first:
        element.press("Control+a")
        sleep(random.uniform(0.1, 0.2))
        element.press("Delete")
        sleep(random.uniform(0.1, 0.2))

    slow_writing(element, text)


def highlight(element):
    element.evaluate(f"el => el.classList.add('{HIGHLIGHT_CLASSNAME}')")


def remove_highlight(element):
    element.evaluate(f"el => el.classList.remove('{HIGHLIGHT_CLASSNAME}')")

