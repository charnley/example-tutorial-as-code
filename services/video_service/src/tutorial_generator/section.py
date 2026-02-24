from typing import Callable


class SectionList:
    """
    Collects (action, text) pairs via a decorator so that narration text and
    page actions can be defined next to each other.

    Usage::

        sections = SectionList()

        @sections.add("Some narration text.")
        def section_open_site(page):
            page.goto("http://localhost:5173")

    Then pass to generate_tutorial::

        generate_tutorial(name, voice, sections.actions, sections.texts, ...)
    """

    def __init__(self):
        self._sections: list[tuple[Callable, str]] = []

    def add(self, text: str | None) -> Callable:
        """Decorator that registers a page-action function with its narration text.
        Pass None to record the section with no narration audio."""
        def decorator(func: Callable) -> Callable:
            self._sections.append((func, text))
            return func
        return decorator

    @property
    def actions(self) -> list[Callable]:
        return [action for action, _ in self._sections]

    @property
    def texts(self) -> list[str]:
        return [text for _, text in self._sections]
