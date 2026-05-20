"""Playwright visual test — Routes Des Vins
Tests all 7 pages at desktop (1440×900), tablet (768×1024), mobile (390×844).
Saves screenshots to ./pw_screenshots/ and prints a findings report.
"""

import os, time, json
from playwright.sync_api import sync_playwright

BASE   = "http://localhost:3000"
OUTDIR = os.path.join(os.path.dirname(__file__), "pw_screenshots")
os.makedirs(OUTDIR, exist_ok=True)

PAGES = [
    ("home",     "/"),
    ("event",    "/event.html"),
    ("route",    "/route.html"),
    ("formules", "/formules.html"),
    ("tickets",  "/tickets.html"),
    ("faq",      "/faq.html"),
    ("over-ons", "/over-ons.html"),
]

VIEWPORTS = [
    ("desktop", 1440, 900),
    ("tablet",  768,  1024),
    ("mobile",  390,  844),
]

findings = []

def check(page, name, vp_name):
    issues = []

    # --- Nav ---
    nav = page.query_selector(".nav")
    if nav:
        nav_box = nav.bounding_box()
        if nav_box and nav_box["height"] > 100:
            issues.append(f"Nav unusually tall: {nav_box['height']}px")

    # --- Hamburger visible only on mobile ---
    hamburger = page.query_selector(".nav-hamburger")
    if hamburger:
        is_visible = hamburger.is_visible()
        if vp_name == "desktop" and is_visible:
            issues.append("Hamburger visible on desktop (should be hidden)")
        if vp_name == "mobile" and not is_visible:
            issues.append("Hamburger NOT visible on mobile (should show)")

    # --- Horizontal overflow (layout breakage) ---
    page_width = page.viewport_size["width"]
    scroll_width = page.evaluate("document.documentElement.scrollWidth")
    if scroll_width > page_width + 5:
        issues.append(f"Horizontal overflow: scrollWidth={scroll_width} > viewport={page_width}")

    # --- Hero h1 ---
    h1 = page.query_selector("h1")
    if h1:
        h1_box = h1.bounding_box()
        if h1_box and h1_box["width"] > page_width:
            issues.append(f"H1 wider than viewport ({h1_box['width']:.0f}px)")

    # --- Buttons / CTAs not cut off (skip those inside scrollable wrappers) ---
    btns = page.query_selector_all(".btn-primary, .btn-secondary, .btn-ghost")
    for btn in btns:
        if not btn.is_visible():
            continue
        # Skip buttons inside overflow-x:auto/scroll wrappers (tables etc.)
        inside_scroll = btn.evaluate("""el => {
            let p = el.parentElement;
            while (p && p !== document.body) {
                const ox = getComputedStyle(p).overflowX;
                if (ox === 'auto' || ox === 'scroll') return true;
                p = p.parentElement;
            }
            return false;
        }""")
        if inside_scroll:
            continue
        box = btn.bounding_box()
        if box and (box["x"] < 0 or box["x"] + box["width"] > page_width + 5):
            issues.append(f"Button overflows viewport: x={box['x']:.0f} w={box['width']:.0f}")
            break

    # --- Cards visible ---
    cards = page.query_selector_all(".card, .formula-card, .country-card")
    off = 0
    for card in cards:
        if not card.is_visible():
            continue
        box = card.bounding_box()
        if box and box["x"] + box["width"] > page_width + 20:
            off += 1
    if off:
        issues.append(f"{off} card(s) overflow viewport width")

    # --- Footer visible ---
    footer = page.query_selector("footer")
    if not footer:
        issues.append("No <footer> found")

    # --- Countdown on home ---
    if name == "home":
        cd = page.query_selector("#cd-days")
        if not cd:
            issues.append("Countdown #cd-days not found")

    return issues


def run():
    with sync_playwright() as pw:
        browser = pw.chromium.launch()

        for vp_name, vp_w, vp_h in VIEWPORTS:
            ctx = browser.new_context(viewport={"width": vp_w, "height": vp_h})
            page = ctx.new_page()

            for page_name, path in PAGES:
                url = BASE + path
                page.goto(url, wait_until="networkidle", timeout=20000)
                # Scroll through the page in small steps to trigger IntersectionObserver
                page.evaluate("""
                    () => new Promise(resolve => {
                        const height = document.documentElement.scrollHeight;
                        const step   = window.innerHeight * 0.4;
                        let pos = 0;
                        function next() {
                            window.scrollTo(0, pos);
                            pos += step;
                            if (pos < height + window.innerHeight) {
                                setTimeout(next, 80);
                            } else {
                                window.scrollTo(0, 0);
                                setTimeout(resolve, 400);
                            }
                        }
                        next();
                    })
                """)
                # Force all reveal elements visible for accurate screenshots
                page.evaluate("""
                    () => document.querySelectorAll('.reveal,.reveal-left,.reveal-scale')
                             .forEach(el => el.classList.add('visible'))
                """)
                time.sleep(0.6)  # wait for CSS transitions (0.6s duration)

                shot_name = f"{page_name}-{vp_name}.png"
                shot_path = os.path.join(OUTDIR, shot_name)
                page.screenshot(path=shot_path, full_page=True)

                issues = check(page, page_name, vp_name)
                findings.append({
                    "page": page_name,
                    "viewport": vp_name,
                    "issues": issues,
                    "screenshot": shot_name,
                })
                status = "OK" if not issues else f"{len(issues)} issue(s)"
                print(f"  [{vp_name:8}] {page_name:10} — {status}")

            ctx.close()

        browser.close()

    # Print summary
    print("\n" + "="*60)
    print("VISUAL TEST REPORT — Routes Des Vins")
    print("="*60)
    all_ok = True
    for f in findings:
        if f["issues"]:
            all_ok = False
            print(f"\n⚠️  {f['page']} @ {f['viewport']}")
            for iss in f["issues"]:
                print(f"   - {iss}")
    if all_ok:
        print("\n✅ All pages pass at all viewports — no layout issues found.")
    print("="*60)

    with open(os.path.join(OUTDIR, "report.json"), "w") as fh:
        json.dump(findings, fh, indent=2)
    print(f"\nScreenshots saved to: {OUTDIR}/")


if __name__ == "__main__":
    run()
