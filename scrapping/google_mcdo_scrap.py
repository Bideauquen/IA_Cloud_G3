import asyncio

import json

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

async def extract_data(page):
    review_box_xpath = '//div[@jscontroller="fIQYlf"] '

    review_xpath = '//span[@data-expandable-section]'

    secondary_review_xpath = '//span[@class="review-full-text"]'

    author_xpath = '//div[@class="TSUbDb"]'

    rating_xpath = '//span[@class="lTi8oc z3HNkc"]'

    await page.wait_for_selector(review_box_xpath)

    review_box = page.locator(review_box_xpath)

    data = []

    for review_box_index in range(await review_box.count()):

        result_elem = review_box.nth(review_box_index)

        review = await result_elem.locator(review_xpath).first.inner_text()

        review = review if review else await result_elem.locator(

            secondary_review_xpath).inner_text()

        author_name = await result_elem.locator(author_xpath).inner_text()

        rating = await result_elem.locator(

            rating_xpath).first.get_attribute('aria-label')

        rating = rating.split(",")[0].split(":")[1] if rating else None

        data.append({

            'author_name': author_name,

            'review': review,

            'rating': rating

        })

    return data

async def run(playwright: Playwright) -> None:

    webkit = playwright.webkit
    browser = await webkit.launch()

    context = await browser.new_context()


    page = await context.new_page()


    await page.goto("https://www.google.com/")

    await click_balise(page,'//button[@id="L2AGLb"]' )

    search_term = "mc donald"
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

    for href in hrefs : 
        await collect_avis(page, href, avis)


    await page.screenshot(path='screenshot.png')

#    print("HREFS", hrefs)
    print("LEN",len(hrefs))
#    print("PREMIER AVIS", avis[0].nth(1))
    print("SIZE PAR RESTO", await avis[0].count())
    await context.close()

    await browser.close()


async def main():
    async with async_playwright() as playwright:

        await run(playwright)

asyncio.run(main())

