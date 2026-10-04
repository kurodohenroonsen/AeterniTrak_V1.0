#!/usr/bin/env python3
import re
import sys

def main():
    with open("docs/usecases/index.html", "r", encoding="utf-8") as f:
        html = f.read()

    classes_in_html = set()
    for match in re.finditer(r'class=["\']([^"\']+)["\']', html):
        for cls in match.group(1).split():
            cls = cls.strip()
            if cls:
                classes_in_html.add(cls)

    # Also check scripts/portal_styles.py
    with open("scripts/portal_styles.py", "r", encoding="utf-8") as f:
        styles = f.read()

    missing = []
    found = []
    for cls in sorted(classes_in_html):
        # Ignore JS template expressions
        if "${" in cls or cls in ("?", "true", "false"):
            continue
        # In CSS, colons, slashes, dots, brackets are escaped: e.g. lg\:grid-cols-12, border-gold-500\/30, text-\[10px\]
        css_escaped = cls.replace(":", r"\:").replace("/", r"\/").replace(".", r"\.").replace("[", r"\[").replace("]", r"\]").replace("#", r"\#")
        
        # Check if selector like .foo exists in styles
        # or if class name is present in styles as a selector
        regex = r'\.' + re.escape(css_escaped) + r'([^\w-]|$)'
        if re.search(regex, styles):
            found.append(cls)
        else:
            missing.append(cls)

    print(f"Total unique classes in HTML: {len(classes_in_html)}")
    print(f"Found classes count: {len(found)}")
    print(f"Missing classes count: {len(missing)}")
    print("--- MISSING CLASSES ---")
    for m in missing:
        print(m)

if __name__ == "__main__":
    main()
