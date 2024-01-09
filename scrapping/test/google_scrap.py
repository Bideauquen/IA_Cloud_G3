import asyncio

import json

from playwright.async_api import Playwright, async_playwright

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


    await page.locator(

        '//button[@id="L2AGLb"]').first.wait_for(

        timeout=10000)
    await page.locator('//button[@id="L2AGLb"]').first.click()
    search_term = "burj khalifa"
    await page.locator("[aria-label=\"Rech.\"]").type(search_term)


    await page.keyboard.press('Enter')
    await page.screenshot(path="screenshot.png")

    await page.locator(

        '//a[@data-async-trigger="reviewDialog"]').first.wait_for(

        timeout=10000)


    await page.locator('//a[@data-async-trigger="reviewDialog"]').first.click()


    pagination_limit = 3


    for page_number in range(pagination_limit):

        await page.locator('//div[@class="review-dialog-list"]').hover()

        await page.mouse.wheel(0, 100000)

        page_number += 1

        await page.wait_for_timeout(2000)


    data = await extract_data(page)


    with open('google_reviews.json', 'w') as f:

        json.dump(data, f, indent=2)

    await context.close()

    await browser.close()


async def main():
    async with async_playwright() as playwright:

        await run(playwright)

asyncio.run(main())

