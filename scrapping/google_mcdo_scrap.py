import asyncio
import mysql.connector
import re

from playwright.async_api import Playwright, async_playwright

async def click_balise(page, balise):
    await page.locator(balise).first.wait_for(timeout=10000)
    await page.locator(balise).first.click()
    
async def click_text(page, text):
    await page.get_by_text(text, exact=True).first.wait_for(timeout=10000)
    await page.get_by_text(text, exact=True).first.click()
    

async def scroll(page, balise, scroll_number):
    await page.locator(balise).first.wait_for(timeout=10000)
    await page.locator(balise).first.hover()

    for page_number in range(scroll_number):

        #await page.locator('//div[@class="review-dialog-list"]').hover()

        await page.mouse.wheel(0, 100000)

        #page_number += 1

        await page.wait_for_timeout(2000)

async def get_class(page):
    classes = []
    localisations = page.locator('//a[@class="hfpxzc"]')
    for i in range(await localisations.count()):
        loc = localisations.nth(i)
        classes.append(await loc.get_attribute('href'))

    return classes

async def collect_avis(page, href, avis):
    balise = f'//a[@href="{href}"]'
    await click_balise(page, balise)
    await click_text(page, 'Avis')
    await scroll(page, '//div[@class="m6QErb DxyBCb kA9KIf dS8AEf "]', 6)
    avis_soup = page.locator('//div[@class="jftiEf fontBodyMedium "]')
    avis.append(avis_soup)

async def insert_into_mysql(review_data):
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        port=3307,
        password="password",
        database="reviews"
    )

    cursor = connection.cursor()

    query = """
        INSERT INTO google (userName, rating, comment, date)
        VALUES (%s, %s, %s, %s)
    """
    
    data = (
        review_data['user'],
        review_data['rating'],
        review_data['text'],
        review_data['date']
    )

    cursor.execute(query, data)
    connection.commit()
    cursor.close()
    connection.close()

async def run(playwright: Playwright, search_term) -> None:

    webkit = playwright.webkit
    browser = await webkit.launch()
    context = await browser.new_context()
    page = await context.new_page()

    await page.goto("https://www.google.com/")

    await click_balise(page,'//button[@id="L2AGLb"]' )

    # search_term = "mc donald"
    await page.locator("[aria-label=\"Rech.\"]").type(search_term)

    await page.keyboard.press('Enter')
    await scroll(page, '//body',1)
    await page.screenshot(path="screenshot.png")

    await click_text(page, 'Maps')
    await page.wait_for_url('**google.com/maps/**')
    await scroll(page, '//div[@class="k7jAl lJ3Kh w6Uhzf miFGmb"]', 5)
   # await page.screenshot(path="screenshot.png")
    hrefs = await get_class(page)
    avis = []

    #VRAI BOUCLE A UTILISER POUR TOUT RECUPERER
    # for href in hrefs : 
    #     await collect_avis(page, href, avis)
        
    #TEMPORAIRE POUR LES TESTS
    await collect_avis(page, hrefs[5], avis)
    await collect_avis(page, hrefs[6], avis)

    await page.screenshot(path='screenshot.png')
    
    for individual_review in await avis[0].all():
        await click_balise(individual_review, '//button[@aria-label="Voir plus"]')

        text = await individual_review.locator('//span[@class="wiI7pd"]').first.inner_text()
        date = await individual_review.locator('//div[@class="PIpr3c"]').first.inner_text()
        user = await individual_review.locator('//div[@class="d4r55 "]').first.inner_text()
        rating_with_text = await individual_review.locator('//span[@class="kvMYJc"]').first.get_attribute('aria-label')
        rating_match = re.search(r'\d+', rating_with_text)
        rating = rating_match.group() if rating_match else None

        review_data = {
            'user': user,
            'text': text,
            'date': date,
            'rating': rating,
            'restaurant': search_term
        }

        await insert_into_mysql(review_data)

#    print("HREFS", hrefs)
    # print("LEN",len(hrefs))
#    print("PREMIER AVIS", avis[0].nth(1))
    # print("SIZE PAR RESTO", await avis[0].count())
    await context.close()

    await browser.close()


async def main():
    companies = ['Hippopotamus France', 
                 'Buffalo Grill', 
                 'Flunch', 
                 'Mcdonald', 
                 'Ayako Sushi',
                 'Sushi Shop',
                 'Subway',
                 'KFC France']
    
    async with async_playwright() as playwright:

        for company_name in companies:
            await run(playwright, company_name)

asyncio.run(main())

