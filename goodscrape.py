from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


async def scrape(book_search="Wizard of Earthsea"):
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-extensions")
    # options.add_argument("--headless=chrome")
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-certificate-errors-spki-list')
    options.add_argument('--ignore-ssl-errors')
    options.add_argument('log-level=3')
    options.add_argument('--window-size=1920,1080')
    # options.add_argument("--window-size=2560,1440")
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-gpu')
    options.add_argument("--no-proxy-server")
    options.add_argument("--proxy-server='direct://'")
    options.add_argument("--proxy-bypass-list=*")
    # options.add_argument('user-agent="MQQBrowser/26 Mozilla/5.0 (Linux; U; Android 2.3.7; zh-cn; MB200 Build/GRJ22; CyanogenMod-7) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1"')
    driver = webdriver.Chrome(options)

    

    driver.get("https://www.goodreads.com/search?utf8=%E2%9C%93&search_type=books")

    # element = WebDriverWait(driver, 200).until(
    #     EC.presence_of_element_located((By.ID, "searchBox__input--navbar"))
    # )

    # element = WebDriverWait(driver, 200).until(
    #     EC.presence_of_element_located((By.ID, "search_query_main"))
    # )

    # element = WebDriverWait(driver, 20).until(
    #     EC.presence_of_element_located((By.CLASS_NAME, "searchBox__input--navbar"))
    # )

    # driver.find_element(By.CLASS_NAME, "searchBox__input--navbar").send_keys(book_search)
    # driver.find_element(By.CLASS_NAME, "searchBox__icon--navbar").click()

    # wait statement
    
    # handle popup
    try:
        # try to click on the booktitle
        driver.find_element(By.ID, "search_query_main").send_keys(book_search)
    except:
        # closes pop-up that may occur
        print("search bar not found, trying other search bar in header")
        driver.find_element(By.CLASS_NAME, "gr-h3--noMargin").click()
        webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
        driver.find_element(By.CLASS_NAME, "searchBox__input--navbar").send_keys(book_search)
    


    # driver.find_element(By.ID, "search_query_main").send_keys(book_search)
    driver.find_element(By.CLASS_NAME, "searchBox__button").click()


    # element = WebDriverWait(driver, 50).until(
    #     EC.presence_of_element_located((By.ID, "searchBox__input--navbar"))
    # )
    

    # driver.get("https://www.goodreads.com/search?q=eragon&qid=1EgsK06bG0")

    

    book_info = {}

    # click on the first result
    try:
        # try to click on the booktitle
        driver.find_element(By.CLASS_NAME, "bookTitle").click()
    except:
        # closes pop-up that may occur
        driver.find_element(By.CLASS_NAME, "gr-h3--noMargin").click()
        webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
        driver.find_element(By.CLASS_NAME, "bookTitle").click()


    # time.sleep(20) #sleep


    title = driver.find_element(By.CLASS_NAME, "Text__title1").text
    book_info["title"] = title

    author = driver.find_element(By.CLASS_NAME, "ContributorLink__name").text
    book_info["author"] = author

    rating = driver.find_element(By.CLASS_NAME, "RatingStatistics__rating").text
    book_info["rating"] = rating

    page_count = driver.find_element(By.CLASS_NAME, "FeaturedDetails").find_element(By.TAG_NAME, "p").text
    book_info["page_count"] = page_count

    link = driver.current_url.split("?")[0]
    book_info["link"] = link

    description = driver.find_element(By.CLASS_NAME, "DetailsLayoutRightParagraph__widthConstrained").find_element(By.TAG_NAME, "span").text
    if description.startswith("An alternate cover edition"):
        print("removing unneccessary starting text about alt cover")
        description = description.split('\n', 1)[1]
        description = description.strip()
    if len(description) > 1024:
        print(len(description))
        description = description[:1021] + "..."
        print(len(description))
    book_info["description"] = description

    # rating_count = driver.find_element(By.CLASS_NAME, "RatingStatistics__meta").find_element(By.TAG_NAME, "span").text
    # book_info["rating_count"] = rating_count

    book_image = driver.find_element(By.CLASS_NAME, "ResponsiveImage").get_attribute("src")
    book_info["book_image"] = book_image


    print(book_info)

    if len(book_info) != 7:
        raise Exception("Error: incorrect number of info found on book")

    return book_info
