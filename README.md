# playwright-browser-manager

A Python utility for automating browsers with Playwright. Supports persistent profiles, proxy routing, async/sync APIs, and context manager usage — with automatic process cleanup.

Supports **Brave**, **Chrome**, **Edge**, **Comet**, and **Chromium** on Windows and macOS.

---

## Installation

### From GitHub (recommended — always latest)
```bash
pip install git+https://github.com/samratpro/playwright_browser_manager.git
```

### Into your project's `requirements.txt`
```
git+https://github.com/samratpro/playwright_browser_manager.git
playwright>=1.58.0
psutil>=5.9
```
Then install with:
```bash
pip install -r requirements.txt
playwright install
```

---

## Features

- **Persistent profiles** — save and reuse browser sessions (cookies, logins, storage)
- **Profileless browsing** — auto-creates and deletes a temp profile per session
- **Proxy support** — per-profile proxy with auto country detection
- **Sync & async APIs** — use whichever fits your project
- **Context manager** — `with BrowserManager(...) as bm:` for automatic cleanup
- **Auto browser detection** — finds Brave, Comet, Edge, Chrome, or Chromium automatically
- **Robust cleanup** — kills all browser child processes via `psutil`

---

## Quick Start

### With a persistent profile (sync)
```python
from playwright_browser_manager.browser_manager import BrowserManager

manager = BrowserManager(debug_port=9221)

# First run: opens browser for manual login, saves session
if not manager.profile_exists("my_profile"):
    manager.setup_profile(
        profile_name="my_profile",
        url="https://www.facebook.com",
        wait_message="Log in, then close the browser to save your session."
    )

# Subsequent runs: reuse saved session
with BrowserManager(debug_port=9221) as manager:
    page = manager.connect_to_browser(profile_name="my_profile", url="https://www.facebook.com")
    print("Title:", page.title())
    input("Press Enter to close...")
    manager.close_browser()
```

### Without a profile (temp session, sync)
```python
from playwright_browser_manager.browser_manager import BrowserManager

# Simple visit
manager = BrowserManager(debug_port=9221)
try:
    page = manager.connect_to_browser_without_profile(url="https://example.com", headless=False)
    print("Title:", page.title())
finally:
    manager.close_browser()

# Context manager — auto closes and deletes temp profile
with BrowserManager(debug_port=9222) as manager:
    page = manager.connect_to_browser_without_profile(url="https://httpbin.org/user-agent", headless=True)
    print(page.inner_text("body")[:200])
```

### With proxy
```python
from playwright_browser_manager.browser_manager import BrowserManager

with BrowserManager(debug_port=9225) as bm:
    page = bm.connect_to_browser_with_proxy(
        profile_name="france_profile",
        proxy={
            "server": "http://gw.dataimpulse.com:823",
            "username": "your_username__cr.fr",
            "password": "your_password"
        },
        url="https://iphey.com",
        headless=False
    )
    page.wait_for_timeout(5000)
    page.screenshot(path="proof.png", full_page=True)
```

### Async — parallel tabs
```python
import asyncio
from playwright_browser_manager.browser_manager import BrowserManager

async def main():
    manager = BrowserManager(debug_port=9221)
    page = await manager.connect_to_browser_async(
        profile_name="my_profile",
        url="https://example.com",
        headless=False
    )
    context = page.context

    semaphore = asyncio.Semaphore(10)

    async def scrape(url):
        async with semaphore:
            tab = await context.new_page()
            await tab.goto(url, timeout=20000, wait_until="domcontentloaded")
            print(await tab.title())
            await tab.close()

    urls = ["https://example.com", "https://python.org", "https://httpbin.org"]
    await asyncio.gather(*[scrape(u) for u in urls])
    await manager.close_browser_async()

asyncio.run(main())
```

---

## API Reference

### `BrowserManager(base_profile_dir=None, browser_path=None, debug_port=9222)`
| Parameter | Default | Description |
|---|---|---|
| `base_profile_dir` | `C:\ChromeProfiles` / `~/ChromeProfiles` | Root folder for saved profiles |
| `browser_path` | auto-detected | Path to browser executable |
| `debug_port` | `9222` | Remote debugging port |

### Methods
| Method | Description |
|---|---|
| `profile_exists(name)` | Returns `True` if a saved profile exists |
| `setup_profile(profile_name, url, wait_message)` | Opens browser for manual login/setup |
| `connect_to_browser(profile_name, url, headless, timeout)` | Connects to browser with a saved profile (sync) |
| `connect_to_browser_without_profile(url, headless, timeout)` | Connects with a fresh temp profile (sync) |
| `connect_to_browser_with_proxy(profile_name, proxy, url, headless)` | Connects with proxy routing (sync) |
| `connect_to_browser_async(profile_name, url, headless, timeout)` | Async version of `connect_to_browser` |
| `connect_to_browser_without_profile_async(url, headless, timeout)` | Async profileless connection |
| `close_browser()` | Closes browser and cleans up all processes (sync) |
| `close_browser_async()` | Async version of `close_browser` |

---

## Profiles

Profiles are saved in `C:\ChromeProfiles\<profile_name>` (Windows) or `~/ChromeProfiles/<profile_name>` (macOS/Linux). Each profile stores cookies, localStorage, and session data so you stay logged in across runs.

---

## Troubleshooting

**`Port 9222 is in use`**
Use a different `debug_port`: `BrowserManager(debug_port=9223)`

**Page loads but content is empty**
Increase timeout: `connect_to_browser(..., timeout=60000)`

**Browser not found**
Pass the path explicitly: `BrowserManager(browser_path="C:/path/to/chrome.exe")`

**Lingering browser processes**
Call `close_browser()` in a `finally` block or use the `with` context manager.

---

## License

MIT License. See [LICENSE](LICENSE) for details.
