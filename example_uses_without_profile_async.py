# example_uses_without_profile_async.py
#
# Async examples for connect_to_browser_without_profile_async.
#
# How it works:
#   - A fresh temporary profile folder is created automatically.
#   - The temp path is printed to the terminal.
#   - After close_browser_async() the temp folder is deleted automatically.
#
# No pre-existing profile is needed — just run and go.

import asyncio
from browser_manager import BrowserManager


# ============================================================================
# USE CASE 1: Simple async page visit & title check
# ============================================================================
async def example_1_simple_visit():
    """Open a URL, print the page title, then close."""
    print("\n" + "=" * 60)
    print("Use Case 1: Simple page visit")
    print("=" * 60)

    manager = BrowserManager(debug_port=9221)
    try:
        page = await manager.connect_to_browser_without_profile_async(
            url="https://example.com",
            headless=False,
        )
        print(f"Page title : {await page.title()}")
        input("Press Enter to close the browser...")
    finally:
        await manager.close_browser_async()


# ============================================================================
# USE CASE 2: Parallel tabs with asyncio.gather
# ============================================================================
async def example_2_parallel_tabs():
    """Navigate multiple tabs in parallel using asyncio.gather."""
    print("\n" + "=" * 60)
    print("Use Case 2: Parallel tabs with gather")
    print("=" * 60)

    manager = BrowserManager(debug_port=9222)
    try:
        page = await manager.connect_to_browser_without_profile_async(
            url="https://example.com",
            headless=False,
        )
        context = page.context

        urls = [
            "https://httpbin.org/get",
            "https://ipinfo.io/json",
            "https://www.python.org",
        ]

        async def visit(url):
            tab = await context.new_page()
            await tab.goto(url, timeout=30000)
            title = await tab.title()
            print(f"  ✅ {title!r}  →  {url}")
            await tab.close()

        await asyncio.gather(*[visit(u) for u in urls])
        input("All done. Press Enter to close...")
    finally:
        await manager.close_browser_async()


# ============================================================================
# USE CASE 3: Headless scraping (no visible window)
# ============================================================================
async def example_3_headless_scrape():
    """Headless: scrape page content without any visible browser window."""
    print("\n" + "=" * 60)
    print("Use Case 3: Headless scraping")
    print("=" * 60)

    manager = BrowserManager(debug_port=9223)
    try:
        page = await manager.connect_to_browser_without_profile_async(
            url="https://httpbin.org/user-agent",
            headless=True,
        )
        body_text = await page.inner_text("body")
        print(f"Response:\n{body_text[:300].strip()}")
    finally:
        await manager.close_browser_async()


# ============================================================================
# Main — uncomment the example(s) you want to run
# ============================================================================
if __name__ == "__main__":
    asyncio.run(example_1_simple_visit())
    # asyncio.run(example_2_parallel_tabs())
    # asyncio.run(example_3_headless_scrape())
