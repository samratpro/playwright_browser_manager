# example_uses_without_profile_sync.py
#
# Sync examples for connect_to_browser_without_profile.
#
# How it works:
#   - A fresh temporary profile folder is created automatically.
#   - The temp path is printed to the terminal.
#   - After close_browser() the temp folder is deleted automatically.
#
# No pre-existing profile is needed — just run and go.

from playwright_browser_manager.browser_manager import BrowserManager


# ============================================================================
# USE CASE 1: Simple page visit & title check
# ============================================================================
def example_1_simple_visit():
    """Open a URL, print the page title, then close."""
    print("\n" + "=" * 60)
    print("Use Case 1: Simple page visit")
    print("=" * 60)

    manager = BrowserManager(debug_port=9221)
    try:
        page = manager.connect_to_browser_without_profile(
            url="https://example.com",
            headless=False,
        )
        print(f"Page title : {page.title()}")
        input("Press Enter to close the browser...")
    finally:
        manager.close_browser()


# ============================================================================
# USE CASE 2: Multiple tabs in one session
# ============================================================================
def example_2_multiple_tabs():
    """Open several tabs inside the same temp-profile session."""
    print("\n" + "=" * 60)
    print("Use Case 2: Multiple tabs")
    print("=" * 60)

    manager = BrowserManager(debug_port=9222)
    try:
        page = manager.connect_to_browser_without_profile(
            url="https://example.com",
            headless=False,
        )
        context = page.context

        urls = [
            "https://httpbin.org/get",
            "https://ipinfo.io/json",
            "https://www.python.org",
        ]
        tabs = []
        for url in urls:
            tab = context.new_page()
            tab.goto(url, timeout=30000)
            tab.wait_for_load_state("load", timeout=30000)
            tabs.append(tab)
            print(f"  Opened: {tab.title()!r}  →  {url}")

        input("All tabs open. Press Enter to close...")
        for tab in tabs:
            tab.close()
    finally:
        manager.close_browser()


# ============================================================================
# USE CASE 3: with-statement (auto close + auto temp delete)
# ============================================================================
def example_3_context_manager():
    """Use BrowserManager as a context manager — close_browser called automatically."""
    print("\n" + "=" * 60)
    print("Use Case 3: Context manager (auto-close)")
    print("=" * 60)

    with BrowserManager(debug_port=9223) as manager:
        page = manager.connect_to_browser_without_profile(
            url="https://httpbin.org/user-agent",
            headless=True,  # headless = no visible window
        )
        print(f"Page title   : {page.title()}")
        print(f"Page content : {page.inner_text('body')[:200].strip()}")
    # close_browser() + temp folder deletion happen automatically here


# ============================================================================
# Main — uncomment the example(s) you want to run
# ============================================================================
if __name__ == "__main__":
    example_1_simple_visit()
    # example_2_multiple_tabs()
    # example_3_context_manager()
