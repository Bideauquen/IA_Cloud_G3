import asyncio
import mysql.connector
import time
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

        await page.wait_for_timeout(1000)

async def get_class(page):
    classes = []
    localisations = page.locator('//a[@class="hfpxzc"]')
    for i in range(await localisations.count()):
        loc = localisations.nth(i)
        classes.append(await loc.get_attribute('href'))

    return classes

async def click_voir_plus(review_locator):
    try:
        await review_locator.locator('//button[@aria-label="Voir plus"]').first.wait_for(timeout=1000)
        await review_locator.locator('//button[@aria-label="Voir plus"]').first.click()
    except:
        pass

async def collect_avis(page, href, avis, company_name):
    balise = f'//a[@href="{href}"]'
    await click_balise(page, balise)
    time.sleep(2)
    await click_text(page, 'Présentation')
    adresse = await page.locator('//div[@class="Io6YTe fontBodyMedium kR99db "]').first.inner_text()
    time.sleep(2)

    try:
        await click_text(page, 'Avis')
        time.sleep(2)

        await scroll(page, '//div[@class="cVwbnc IlRKB"]', 10)
        avis_soup = page.locator('//div[@class="jftiEf fontBodyMedium "]')

        await process_reviews(page, avis_soup, company_name, adresse)
    except:
        pass

async def process_reviews(page, avis_soup, company_name, adresse):
    try:
        for individual_review in await avis_soup.all():
            review_data = await extract_review_data(page, individual_review, company_name, adresse)
            await insert_into_mysql(review_data, company_name)
    except Exception as e:
        print(f"Erreur lors du traitement des avis : {e}")
    
async def extract_review_data(page, individual_review, search_term, adresse):
    await click_voir_plus(individual_review)

    text = await individual_review.locator('//span[@class="wiI7pd"]').first.inner_text()
    date_nb = await individual_review.locator('//div[@class="PIpr3c"]').count()
    
    if date_nb > 0:
        date = await individual_review.locator('//div[@class="PIpr3c"]').first.inner_text()
    else:
        date = None

    user = await individual_review.locator('//div[@class="d4r55 "]').first.inner_text()
    rating_with_text = await individual_review.locator('//span[@class="kvMYJc"]').first.get_attribute('aria-label')
    rating_match = re.search(r'\d+', rating_with_text)
    rating = rating_match.group() if rating_match else None

    return {
        'user': user,
        'text': text,
        'date': date,
        'rating': rating,
        'restaurant': search_term,
        'adresse': adresse
    }

async def insert_into_mysql(review_data, company_name):
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        port=3307,
        password="password",
        database="reviews"
    )
    cursor = connection.cursor(buffered=True)

    # Vérifie si la société existe déjà dans la base de données
    query = "SELECT id FROM companies WHERE name = %s"
    cursor.execute(query, (company_name,))
    company_result = cursor.fetchone()

    if company_result is None:
        # Si la société n'existe pas, la créé
        query = """
            INSERT INTO companies (name, ecoScore, ratings, reviewCount)
            VALUES (%s, %s, %s, %s)
        """

        data = (company_name, None, None, 0)
        cursor.execute(query, data)
        connection.commit()

        # Récupère l'ID de la nouvelle société
        query = "SELECT id FROM companies WHERE name = %s"
        cursor.execute(query, (company_name,))
        company_id_result = cursor.fetchone()
        company_id = company_id_result[0]
    else:
        # Si la société existe déjà, récupère son ID
        company_id = company_result[0]

    # Vérifie si le restaurant existe déjà dans la base de données
    query = "SELECT id FROM restaurants WHERE address = %s"
    cursor.execute(query, (review_data['adresse'],))
    restaurant_result = cursor.fetchone()

    if restaurant_result is None:
        # Si le restaurant n'existe pas, le créé
        query = """
            INSERT INTO restaurants (name, company, address)
            VALUES (%s, %s, %s)
        """

        cursor.execute(query, (review_data['restaurant'], company_id, review_data['adresse']))
        connection.commit()

        # Récupère l'ID du nouveau restaurant
        query = "SELECT id FROM restaurants WHERE name = %s"
        cursor.execute(query, (review_data['restaurant'],))
        restaurant_id_result = cursor.fetchone()
        restaurant_id = restaurant_id_result[0]
    else:
        # Si le restaurant existe déjà, récupère son ID
        restaurant_id = restaurant_result[0]

    query = """
        INSERT INTO google (userName, rating, comment, date, restaurant)
        VALUES (%s, %s, %s, %s, %s)
    """
    
    data = (
        review_data['user'],
        review_data['rating'],
        review_data['text'],
        review_data['date'],
        restaurant_id
    )

    cursor.execute(query, data)
    connection.commit()
    cursor.close()
    connection.close()

async def run(playwright: Playwright, search_term) -> None:

    webkit = playwright.webkit
    browser = await webkit.launch(headless=False)
    context = await browser.new_context()
    page = await context.new_page()


    await page.goto("https://www.google.com/")

    await click_balise(page,'//button[@id="L2AGLb"]' )

#    search_term = "mc donald"
    await page.locator("[aria-label=\"Rech.\"]").type(search_term)

    await page.keyboard.press('Enter')
    await scroll(page, '//body',1)
    await page.screenshot(path="screenshot.png")

    await click_text(page, 'Maps')
    await page.wait_for_url('**google.com/maps/**')
    await scroll(page, '//div[@class="k7jAl lJ3Kh w6Uhzf miFGmb"]', 5)
    await page.screenshot(path="screenshot.png")
    hrefs = await get_class(page)
    avis = []
    
    # VRAIE BOUCLE POUR PLUS DE RESTAU
    for href in hrefs : 
     await collect_avis(page, href, avis, search_term)

    # TEMPORAIRE POUR TESTS
    # await collect_avis(page, hrefs[0], avis, search_term)
    # await collect_avis(page, hrefs[1], avis, search_term)
    # await collect_avis(page, hrefs[2], avis, search_term)
    # await collect_avis(page, hrefs[3], avis, search_term)
    
    await page.screenshot(path='screenshot.png')

#    print("HREFS", hrefs)
    # print("LEN",len(avis))
#    print("PREMIER AVIS", avis[0].nth(0))
    # print("SIZE PAR RESTO", await avis[0]['locators'].count())
    # try:
    #     await click_balise(avis[0]['locators'].nth(0), '//button[@aria-label="Voir plus"]')
    # except:
    #     pass
    # text = await avis[0]['locators'].nth(0).locator('//span[@class="wiI7pd"]').first.inner_text()
    # print(text)
    # print(avis[0]['adresse'])
    await context.close()

    await browser.close()


async def main():
    companies = [
                 'Mcdonald',
                 'KFC France']
    async with async_playwright() as playwright:

        for company_name in companies:
            await run(playwright, company_name)

asyncio.run(main())