PROMPT_TEMPLATE = """
{requirements}
{search_information}
{format_example}
TODO: fill this
"""

OUTPUT_SCHEMA = {
    "Original Requirements": (str, ...),
    "Product Goals": (list[str], ...),
    "User Stories": (list[str], ...),
    "Competitive Analysis": (list[str], ...),
    "Competitive Quadrant Chart": (str, ...),
    "Requirement Analysis": (str, ...),
    "Requirement Pool": (list[tuple[str, str]], ...),
    "UI Design draft": (str, ...),
    "Anything UNCLEAR": (str, ...),
}
