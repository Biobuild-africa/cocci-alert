"""Bundle the modular source files into one self-contained HTML.

Reads:
  prototype/template.html
  prototype/src/styles.css
  prototype/src/engine.js
  prototype/src/flow_controller.js
  prototype/src/i18n.en.js
  prototype/src/i18n.yo.js
  prototype/src/demo_scenarios.js
  prototype/src/main.js

Writes:
  prototype/coccialert_live_demo.html

Usage:
  python prototype/build.py
"""

from pathlib import Path

ROOT = Path(__file__).parent
SRC  = ROOT / "src"
TEMPLATE = ROOT / "template.html"
OUT  = ROOT / "coccialert_live_demo.html"

# Order matters: engine first (defines enums and SCHEMA used by later files),
# flow_controller next (uses Droppings, SCHEMA, evaluatePartial),
# audio (independent, uses no other module),
# i18n files (use Mort, Droppings, etc), demo_scenarios (uses enums),
# main last (uses everything).
JS_FILES = [
    "engine.js",
    "flow_controller.js",
    "audio.js",
    "i18n.en.js",
    "i18n.yo.js",
    "demo_scenarios.js",
    "main.js",
]

def main():
    template = TEMPLATE.read_text(encoding="utf-8")
    styles = (SRC / "styles.css").read_text(encoding="utf-8")

    js_blocks = []
    for fname in JS_FILES:
        body = (SRC / fname).read_text(encoding="utf-8")
        js_blocks.append(f"// ============ src/{fname} ============\n{body}\n")
    js = "\n".join(js_blocks)

    out = template.replace("/* {{STYLES}} */", styles)
    out = out.replace("// {{SCRIPTS}}", js)

    OUT.write_text(out, encoding="utf-8")
    print(f"Built: {OUT}")
    print(f"  Size: {OUT.stat().st_size / 1024:.1f} KB")
    print(f"  Source files inlined: {len(JS_FILES)} JS + 1 CSS")

if __name__ == "__main__":
    main()
