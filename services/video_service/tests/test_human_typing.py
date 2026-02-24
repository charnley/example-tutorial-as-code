import asyncio

from tutorial_generator import VideoTutorialGenerator
from tutorial_generator.page_funcs import human_like_select_and_fill


async def test_human_typing():
    generator = VideoTutorialGenerator()

    try:
        await generator.start(headless=False)  # Use headed mode to see the typing

        # Navigate to a simple test page with an input
        await generator.page.goto("https://www.google.com", timeout=60000)

        # Test the human-like typing
        print("Testing human-like typing...")
        await generator.page.wait_for_selector("textarea[name='q']")

        # Use the human-like fill function
        await human_like_select_and_fill(
            generator.page, "textarea[name='q']", "Playwright human typing test"
        )

        print("Typing completed!")
        await generator.page.wait_for_timeout(3000)

    except Exception as e:
        print(f"Error: {e}")
    finally:
        await generator.close()


if __name__ == "__main__":
    asyncio.run(test_human_typing())
