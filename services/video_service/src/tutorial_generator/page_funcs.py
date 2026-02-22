from time import sleep
import random

from playwright.sync_api import Page

def blur(page):
    page.mouse.click(0, 0)
