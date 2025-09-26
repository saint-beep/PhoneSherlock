import os
import phonenumbers
from phonenumbers import carrier, geocoder, number_type
from playwright.sync_api import sync_playwright

os.system('cls')

phone_number = input("Enter phone number(prefix + number): ")
nr = phonenumbers.parse(phone_number)

print("Valid:", phonenumbers.is_valid_number(nr))
print("Possible:", phonenumbers.is_possible_number(nr))
print("Country:", geocoder.description_for_number(nr, "en"))
print("Carrier:", carrier.name_for_number(nr, "en"))
print("Type:", number_type(nr))

# Scrape additional info from listaabonatilor.ro
url = f"https://www.listaabonatilor.ro/numarul/{phone_number}"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto(url, timeout=15000)

    # w8 for elements to load
    page.wait_for_selector("#progress-bar-inner-text", timeout=10000)
    page.wait_for_selector("#count-comments", timeout=10000)
    page.wait_for_selector("td.td78.tooltip", timeout=10000)

    # first info
    safety_rate = page.query_selector("#progress-bar-inner-text").inner_text().strip()
    eval_count = page.query_selector("#count-comments").inner_text().strip()
    views_count = page.query_selector("td.td78.tooltip").inner_text().strip()

    print("Safety Rate:", safety_rate)
    print("Number of evaluations:", eval_count)
    print("Number of views:", views_count)

    # comments
    page.wait_for_selector("div.comments-container", timeout=10000)
    comments = page.query_selector_all("div.comment-item")

    if comments:
        print(f"\nFound {len(comments)} comments:\n")
        for i, comment in enumerate(comments, start=1):
            text_elem = comment.query_selector("p.comment-text")
            comment_text = text_elem.inner_text().strip() if text_elem else ""
            print(f"{i}. {comment_text}")
    else:
        print("\nNo comments found for this number.")

    browser.close()
