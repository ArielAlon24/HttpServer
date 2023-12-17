class HtmlUtils:
    @staticmethod
    def string_to_html(string: str) -> str:
        replacements = {
            "&": "&amp;",
            "'": "&#39;",
            '"': "&quot;",
            "\t": "&emsp;",
            "<": "&lt;",
            ">": "&gt;",
            "\n": "<br>",
        }

        for escape, html in replacements.items():
            string = string.replace(escape, html)

        return string
