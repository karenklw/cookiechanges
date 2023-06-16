import csv
from selenium import webdriver

def check_cookie_changes(url):
    # Configure Selenium to use Chrome browser
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Run Chrome in headless mode (without UI)
    driver = webdriver.Chrome(options=options)

    # Navigate to the URL
    driver.get(url)

    # Capture the initial state of the cookies
    initial_cookies = driver.get_cookies()

    # Pause for user interaction
    input("Please interact with the website manually and press Enter to continue...")

    # Capture the updated state of the cookies
    updated_cookies = driver.get_cookies()

    # Compare initial and updated cookie values to identify changes (if any)
    # FIXME: find a site that disrespects user's choices to verify that changed cookies are being written to CSV
    changed_cookies = []
    for initial_cookie in initial_cookies:
        cookie_name = initial_cookie['name']
        initial_value = initial_cookie['value']
        for updated_cookie in updated_cookies:
            if (
                updated_cookie['name'] == cookie_name
                and updated_cookie['value'] != initial_value
            ):
                changed_cookie = {
                    'Cookie Name': cookie_name,
                    'Initial Value': initial_value,
                    'Updated Value': updated_cookie['value']
                }
                changed_cookies.append(changed_cookie)
                break

    # Write results to a CSV file
    if changed_cookies:
        with open('cookie_changes.csv', 'w', newline='') as csvfile:
            fieldnames = ['URL', 'Cookie Name', 'Initial Value', 'Updated Value']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for changed_cookie in changed_cookies:
                changed_cookie['URL'] = url
                writer.writerow(changed_cookie)

        print("Cookie changes detected. Results written to 'cookie_changes.csv'.")
    else:
        print("No cookie changes detected.")

    # Close the browser
    driver.quit()

# TODO: replace URL with the one you're checking
check_cookie_changes('https://www.lefigaro.fr/')
