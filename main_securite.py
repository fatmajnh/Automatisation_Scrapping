# main.py - Instagram Message Bot
# Educational project: Web Automation & Browser Security (M4-C1)
#by fatma ezzahra jenayah tp7 
import subprocess
import sys
import random
import time

# Auto-install playwright if not installed
try:
    from playwright.sync_api import sync_playwright
except ImportError:
    print("Installing playwright...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "playwright"])
    subprocess.check_call([sys.executable, "-m", "playwright", "install", "chromium"])
    from playwright.sync_api import sync_playwright

# ============================================
# CONFIGURATION - CHANGE THESE
# ============================================
USERNAME = "fatmaj303"
PASSWORD = "fatma123123"
MESSAGE = "Bonjour , comment cv !"
# ============================================

def random_delay(min_ms=500, max_ms=2000):
    """Human-like random delay"""
    time.sleep(random.randint(min_ms, max_ms) / 1000)

def human_type(page, text):
    """Type like a human with variable speed"""
    for char in text:
        page.keyboard.type(char)
        # Random delay between keystrokes (50-150ms like real typing)
        time.sleep(random.uniform(0.05, 0.15))

def move_mouse_naturally(page, element):
    """Move mouse to element with slight randomness"""
    box = element.bounding_box()
    if box:
        # Add slight randomness to click position within element
        x = box['x'] + box['width'] * random.uniform(0.3, 0.7)
        y = box['y'] + box['height'] * random.uniform(0.3, 0.7)
        page.mouse.move(x, y)
        random_delay(100, 300)

def main():
    with sync_playwright() as p:
        # Launch with more realistic browser settings
        browser = p.chromium.launch(
            headless=False,
            channel="chrome",
            args=[
                '--disable-blink-features=AutomationControlled',
                '--no-first-run',
                '--no-default-browser-check',
            ]
        )

        # Create context with realistic settings
        context = browser.new_context(
            viewport={"width": 1366, "height": 768},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            locale="en-US",
            timezone_id="Europe/Paris",
        )

        # Remove webdriver property that reveals automation
        context.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            });

            // Override plugins to look more realistic
            Object.defineProperty(navigator, 'plugins', {
                get: () => [1, 2, 3, 4, 5]
            });

            // Override permissions
            const originalQuery = window.navigator.permissions.query;
            window.navigator.permissions.query = (parameters) => (
                parameters.name === 'notifications' ?
                    Promise.resolve({ state: Notification.permission }) :
                    originalQuery(parameters)
            );
        """)
        # Create a new browser page (tab) inside the authenticated browser context
        # This page will inherit all context settings such as cookies, session, user-agent, and security overrides
        page = context.new_page()

        try:
            # Go to Instagram
            print("Navigating to Instagram...")
            page.goto("https://www.instagram.com/")
            page.wait_for_load_state("networkidle")
            random_delay(2000, 4000)

            # Handle cookie consent if present
            try:
                cookie_btn = page.locator("button:has-text('Allow'), button:has-text('Accept'), button:has-text('Autoriser')").first
                if cookie_btn.is_visible(timeout=3000):
                    random_delay(500, 1000)
                    cookie_btn.click()
                    random_delay(1000, 2000)
            except:
                pass

            # Check if login is needed
            if "login" in page.url or page.locator("input[name='username']").is_visible(timeout=3000):
                print("Login required...")

                # Click on username field first (like a human would)
                username_field = page.locator("input[name='username']")
                move_mouse_naturally(page, username_field)
                username_field.click()
                random_delay(300, 600)

                # Type username like a human
                human_type(page, USERNAME)
                random_delay(500, 1000)

                # Click on password field
                password_field = page.locator("input[name='password']")
                move_mouse_naturally(page, password_field)
                password_field.click()
                random_delay(300, 600)

                # Type password like a human
                human_type(page, PASSWORD)
                random_delay(800, 1500)

                # Click login button
                login_btn = page.locator("button[type='submit']")
                move_mouse_naturally(page, login_btn)
                random_delay(200, 500)
                login_btn.click()

                page.wait_for_load_state("networkidle")
                random_delay(4000, 6000)

                # Handle "Save Login Info?" popup
                try:
                    save_btn = page.locator("button:has-text('Not Now'), button:has-text('Pas maintenant'), div[role='button']:has-text('Not Now')").first
                    if save_btn.is_visible(timeout=5000):
                        random_delay(1000, 2000)
                        save_btn.click()
                        random_delay(1500, 2500)
                except:
                    pass

                # Handle notifications popup
                try:
                    notif_btn = page.locator("button:has-text('Not Now'), button:has-text('Pas maintenant')").first
                    if notif_btn.is_visible(timeout=5000):
                        random_delay(1000, 2000)
                        notif_btn.click()
                        random_delay(1500, 2500)
                except:
                    pass

                print("Login successful!")
            else:
                print("Already logged in!")

            random_delay(2000, 3000)

            # Go to messages
            print("Navigating to messages...")
            page.goto("https://www.instagram.com/direct/inbox/", timeout=60000)
            page.wait_for_load_state("domcontentloaded")
            random_delay(4000, 6000)

            
            random_delay(2000, 4000)

            # Check if "Turn On" notification popup is blocking - handle it first
            def handle_turn_on_popup():
                """Handle the Turn On notifications popup if present"""
                try:
                    buttons = page.locator("button._a9--").all()
                    for btn in buttons:
                        try:
                            text = btn.inner_text().strip()
                            if text == "Turn On" or text == "Activer":
                                random_delay(300, 600)
                                btn.click()
                                print("Notifications enabled!")
                                random_delay(800, 1200)
                                return True
                        except:
                            continue
                except:
                    pass
                return False

            # Try to handle popup if it appeared
            print("Checking for notification popup...")
            handle_turn_on_popup()
            random_delay(500, 1000)

            # Check if we're already on the inbox page
            if "/direct/inbox" in page.url or "/direct/t/" in page.url:
                print("Already on messages page!")
            else:
                # Click on the messages/DM icon (paper plane icon)
                print("Looking for messages icon...")
                try:
                    dm_selectors = [
                        "a[href='/direct/inbox/']",
                        "svg[aria-label='Messenger']",
                        "svg[aria-label='Direct']",
                        "svg[aria-label='Messages']"
                    ]

                    dm_clicked = False
                    for sel in dm_selectors:
                        try:
                            elem = page.locator(sel).first
                            if elem.is_visible(timeout=2000):
                                random_delay(500, 1000)
                                elem.click()
                                dm_clicked = True
                                print("Clicked on messages icon!")
                                random_delay(2000, 3000)
                                break
                        except:
                            continue

                    if not dm_clicked:
                        # Try clicking via JavaScript
                        try:
                            page.evaluate("""
                                const link = document.querySelector("a[href='/direct/inbox/']");
                                if (link) { link.click(); }
                                else {
                                    const path = document.querySelector("path[d*='M22.513']");
                                    if (path) {
                                        let parent = path.closest('a') || path.closest('div[role="button"]') || path.parentElement.parentElement;
                                        if (parent) parent.click();
                                    }
                                }
                            """)
                            print("Clicked on messages icon (via JS)!")
                            random_delay(2000, 3000)
                        except:
                            print("Could not click messages icon, navigating directly...")
                            page.goto("https://www.instagram.com/direct/inbox/", timeout=60000)
                            random_delay(3000, 4000)
                except Exception as e:
                    print(f"Error finding messages icon: {e}")
                    page.goto("https://www.instagram.com/direct/inbox/", timeout=60000)
                    random_delay(3000, 4000)

            # Check for Turn On popup again after navigating to messages
            random_delay(1000, 1500)
            print("Checking for notification popup again...")
            handle_turn_on_popup()

            print(f"URL: {page.url}")

            # Click on first conversation
            print("Looking for a conversation...")
            random_delay(1500, 2500)

            conversation_clicked = False
            selectors_to_try = [
                "div[class*='x1iyjqo2'] img[alt*='profile']",
                "div:has(img[alt*='profile picture'])",
                "a[href*='/direct/t/']",
                "div[role='listitem']",
                "div[class*='x9f619'] div[class*='x1iyjqo2']"
            ]

            for sel in selectors_to_try:
                try:
                    elem = page.locator(sel).first
                    if elem.is_visible(timeout=2000):
                        random_delay(500, 1000)
                        elem.click()
                        conversation_clicked = True
                        print(f"Conversation opened with: {sel}")
                        break
                except:
                    continue

            if not conversation_clicked:
                print("No conversation found!")
                input("Click manually on a conversation, then press Enter...")

            random_delay(2000, 4000)

            # Find and fill message field
            print("Looking for message field...")

            message_sent = False
            input_selectors = [
                "div[role='textbox']",
                "div[contenteditable='true']",
                "p.xat24cr",
                "div[aria-label*='Message']"
            ]

            for sel in input_selectors:
                try:
                    inp = page.locator(sel).first
                    if inp.is_visible(timeout=2000):
                        random_delay(500, 1000)
                        inp.click()
                        random_delay(300, 600)

                        # Type message like a human
                        human_type(page, MESSAGE)
                        print(f"Message typed: {MESSAGE}")

                        random_delay(800, 1500)

                        # Send with Enter
                        page.keyboard.press("Enter")
                        print("Message sent!")
                        message_sent = True
                        break
                except Exception as e:
                    print(f"Error with {sel}: {e}")
                    continue
            # Check if the message was successfully sent
            if not message_sent:
                # Inform the user that the automated sending failed
                print("Could not send message automatically.")
            # Add a final human-like delay before closing the browser
            random_delay(4000, 6000)

        except Exception as e:
            # Catch and display any unexpected error during execution
            print(f"Error: {e}")

        finally:
            # Ensure proper cleanup: close browser context and browser
            # This prevents session leaks and frees system resources
            context.close()
            browser.close()

if __name__ == "__main__":
    main()

