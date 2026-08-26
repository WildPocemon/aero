#!/usr/bin/env python3
"""Replace the placeholder company details across every site in sites/.

The sites ship with a literal `<name>` placeholder wherever the company name
appears. In HTML it is written as the entity `&lt;name&gt;` so browsers render
the angle brackets instead of treating it as a tag; in attributes, JSON-LD and
JavaScript comments it appears raw. This script handles both forms.

    ./rename.py "Pacific Appliance Repair"
    ./rename.py "Pacific Appliance Repair" --phone "(858) 555-0199" \
        --email service@pacificappliance.com --area "Orange County"
    ./rename.py "Pacific Appliance Repair" --dry-run
    ./rename.py "Pacific Appliance Repair" --only hvac-01-thermaline
"""

import argparse
import html
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
SITES = ROOT / "sites"
EXTENSIONS = {".html", ".css", ".js", ".svg", ".json", ".md", ".txt", ".webmanifest"}

# Placeholders baked into the sites.
PLACEHOLDER_PHONE_DISPLAY = "(619) 555-0142"
PLACEHOLDER_PHONE_TEL = "+16195550142"
PLACEHOLDER_EMAILS = ("service@example.com", "hello@example.com", "dispatch@example.com")
PLACEHOLDER_AREA = "San Diego County"


def tel_href(phone: str) -> str:
    """Turn a display phone number into a tel: href value."""
    digits = re.sub(r"\D", "", phone)
    if not digits:
        return PLACEHOLDER_PHONE_TEL
    if len(digits) == 10:
        digits = "1" + digits
    return "+" + digits


def build_replacements(args, *, json_ld: bool) -> list[tuple[str, str]]:
    """Ordered find/replace pairs.

    `json_ld` selects how the raw `<name>` placeholder is escaped: inside a
    JSON-LD script block the name is a JSON string value, so an ampersand must
    stay literal; everywhere else it lands in HTML text or an attribute value
    and has to be entity-escaped.
    """
    pairs: list[tuple[str, str]] = []

    # Longest patterns first so `&lt;name&gt;` is consumed before a bare `<name>`.
    pairs.append(("&lt;name&gt;", html.escape(args.name, quote=False)))
    pairs.append(("<name>", args.name if json_ld else html.escape(args.name, quote=False)))

    if args.phone:
        pairs.append((PLACEHOLDER_PHONE_TEL, tel_href(args.phone)))
        pairs.append((PLACEHOLDER_PHONE_DISPLAY, args.phone))
    if args.email:
        for placeholder in PLACEHOLDER_EMAILS:
            pairs.append((placeholder, args.email))
    if args.area:
        pairs.append((PLACEHOLDER_AREA, args.area))
    return pairs


JSON_LD_BLOCK = re.compile(
    r'(<script[^>]*type=["\']application/ld\+json["\'][^>]*>)(.*?)(</script>)',
    re.DOTALL | re.IGNORECASE)


def apply(text: str, pairs) -> tuple[str, int]:
    hits = 0
    for needle, value in pairs:
        hits += text.count(needle)
        text = text.replace(needle, value)
    return text, hits


def substitute(text: str, html_pairs, json_pairs) -> tuple[str, int]:
    """Apply replacements, using the JSON-LD escaping inside ld+json blocks."""
    hits = 0
    out = []
    cursor = 0
    for match in JSON_LD_BLOCK.finditer(text):
        chunk, n = apply(text[cursor:match.start()], html_pairs)
        out.append(chunk)
        hits += n
        body, n = apply(match.group(2), json_pairs)
        out.append(match.group(1) + body + match.group(3))
        hits += n
        cursor = match.end()
    chunk, n = apply(text[cursor:], html_pairs)
    out.append(chunk)
    hits += n
    return "".join(out), hits


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("name", help="Company name to write in place of <name>")
    parser.add_argument("--phone", help=f"Display phone number (replaces {PLACEHOLDER_PHONE_DISPLAY})")
    parser.add_argument("--email", help="Contact email address")
    parser.add_argument("--area", help=f"Service area (replaces \"{PLACEHOLDER_AREA}\")")
    parser.add_argument("--only", action="append", metavar="SITE",
                        help="Limit to one site directory; repeatable")
    parser.add_argument("--dry-run", action="store_true",
                        help="Report what would change without writing")
    args = parser.parse_args()

    if not SITES.is_dir():
        print(f"error: {SITES} not found", file=sys.stderr)
        return 1

    targets = sorted(SITES.iterdir()) if not args.only else [SITES / s for s in args.only]
    missing = [t for t in targets if not t.is_dir()]
    if missing:
        print("error: no such site: " + ", ".join(m.name for m in missing), file=sys.stderr)
        return 1

    html_pairs = build_replacements(args, json_ld=False)
    json_pairs = build_replacements(args, json_ld=True)
    changed_files = 0
    total_hits = 0

    for site in targets:
        site_hits = 0
        for path in sorted(site.rglob("*")):
            if not path.is_file() or path.suffix.lower() not in EXTENSIONS:
                continue
            original = path.read_text(encoding="utf-8")
            updated, hits = substitute(original, html_pairs, json_pairs)
            site_hits += hits
            if updated != original:
                changed_files += 1
                if not args.dry_run:
                    path.write_text(updated, encoding="utf-8")
        total_hits += site_hits
        print(f"  {site.name:26s} {site_hits:4d} replacement(s)")

    verb = "would change" if args.dry_run else "changed"
    print(f"\n{total_hits} replacement(s) across {changed_files} file(s) {verb}.")
    if args.dry_run:
        print("Dry run — nothing was written.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
