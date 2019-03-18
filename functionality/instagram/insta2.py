
import time
from selenium import webdriver as wd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver

# The account you want to check
account = "bjsrestaurants"

# Chrome executable
chrome_binary = r"chrome.exe"   # Add your path here


def login(driver):
    username = "xxxxxxx"   # Your username
    password = "xxxxxxx!"   # Your password

    # Load page
    driver.get("https://www.instagram.com/accounts/login/?next=/explore/")

    # Login
    driver.find_element_by_xpath("//div/input[@name='username']").send_keys(username)
    driver.find_element_by_xpath("//div/input[@name='password']").send_keys(password)
    driver.find_element_by_xpath("//span/button").click()


    # Wait for the login page to load
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.LINK_TEXT, "See All")))


def scrape_followers(driver, account):
    # Load account page
    WebDriverWait(driver, 30)

    driver.get("https://www.instagram.com/{0}/".format(account))

    # Click the 'Follower(s)' link
    driver.find_element_by_partial_link_text("follower").click()

    # Wait for the followers modal to load
    xpath = "/html/body/div[4]/div/div[2]/div/div[1]"

    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, xpath)))

    SCROLL_PAUSE = 20  # Pause to allow loading of content
    driver.execute_script("followersbox = document.getElementsByClassName('_gs38e')[0];")
    last_height = driver.execute_script("return followersbox.scrollHeight;")

    # We need to scroll the followers modal to ensure that all followers are loaded
    while True:
        driver.execute_script("followersbox.scrollTo(0, followersbox.scrollHeight);")

        # Wait for page to load
        time.sleep(SCROLL_PAUSE)

        # Calculate new scrollHeight and compare with the previous
        new_height = driver.execute_script("return followersbox.scrollHeight;")
        if new_height == last_height:
            break
        last_height = new_height

    # Finally, scrape the followers

    xpath = "/html/body/div[4]/div/div[2]/div/div[2]/ul/div/li"
    followers_elems = driver.find_elements_by_xpath(xpath)

    followers_temp = [e.text for e in followers_elems]  # List of followers (username, full name, follow text)
    followers = []  # List of followers (usernames only)

    # Go through each entry in the list, append the username to the followers list
    for i in followers_temp:
        username, sep, name = i.partition('\n')
        followers.append(username)


    print("______________________________________")
    print("FOLLOWERS")

    return followers

def scrape_following(driver, account):
    # Load account page
    driver.get("https://www.instagram.com/{0}/".format(account))

    # Click the 'Following' link
    driver.find_element_by_partial_link_text("following").click()

    # Wait for the following modal to load



    xpath = "/html/body/div[4]/div/div[2]/div/div[1]"
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, xpath)))

    SCROLL_PAUSE = 20 # Pause to allow loading of content
    driver.execute_script("followingbox = document.getElementsByClassName('_gs38e')[0];")
    last_height = driver.execute_script("return followingbox.scrollHeight;")

    # We need to scroll the following modal to ensure that all following are loaded
    while True:
        driver.execute_script("followingbox.scrollTo(0, followingbox.scrollHeight);")

        # Wait for page to load
        time.sleep(SCROLL_PAUSE)

        # Calculate new scrollHeight and compare with the previous
        new_height = driver.execute_script("return followingbox.scrollHeight;")
        if new_height == last_height:
            break
        last_height = new_height

    # Finally, scrape the following
    xpath = "/html/body/div[4]/div/div[2]/div/div[2]/ul/div/li"
    following_elems = driver.find_elements_by_xpath(xpath)

    following_temp = [e.text for e in following_elems]  # List of following (username, full name, follow text)
    following = []  # List of following (usernames only)

    # Go through each entry in the list, append the username to the following list
    for i in following_temp:
        username, sep, name = i.partition('\n')
        following.append(username)

    print("\n______________________________________")
    print("FOLLOWING")
    return username


if __name__ == "__main__":
    options = wd.ChromeOptions()
    options.binary_location = chrome_binary # chrome.exe
    driver_binary = r"chromedriver.exe"
    driver = webdriver.Chrome('/usr/local/Cellar/chromedriver/2.33/bin/chromedriver')
    try:
        login(driver)
        followers = scrape_followers(driver, 'bjsrestaurants')
        thefile = open('followers.txt', 'w')
        for item in followers:
            thefile.write("%s\n" % item)

        print(followers)
        following = scrape_following(driver, 'bjsrestaurants')
        thefile = open('following.txt', 'w')
        for item in following:
            thefile.write("%s\n" % item)
        print(following)
    finally:
        driver.quit()
