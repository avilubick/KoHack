import re

class Parser:
    def __init__(self):
        self.result = []

    def parse_gedcom(self, file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()

                if not line:
                    continue

                # Match GEDCOM structure (Level, Tag, Value)
                match = re.match(r"(\d+) (@?[A-Za-z0-9_]+@?)\s*(.*)?", line)
                if match:
                    level, tag, value = match.groups()
                    level = int(level)
                    value = value.strip() if value else ""

                    # Convert to indented text format
                    self.result.append(f"{'  ' * level}{tag}: {value}")

        return "\n".join(self.result)  # Return as plain text


