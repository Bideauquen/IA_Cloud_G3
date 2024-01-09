from bs4 import BeautifulSoup
import mysql.connector

html_content_trustPilot = ['''<article class="paper_paper__1PY90 paper_outline__lwsUX card_card__lQWDv card_noPadding__D8PcU styles_reviewCard__hcAvl" data-service-review-card-paper="true"><div class="styles_reviewCardInner__EwDq2"><aside aria-label="Informations sur sertaki" class="styles_consumerInfoWrapper__KP3Ra"><div class="styles_consumerDetailsWrapper__p2wdr"><div class="avatar_avatar__hmBp6 avatar_yellow__p_g1i" data-consumer-avatar="true" style="width:44px;min-width:44px;height:44px;min-height:44px"><span class="typography_heading-xs__jSwUz typography_appearance-default__AAY17 typography_disableResponsiveSizing__OuNP7 avatar_avatarName__ehkAr">SE</span></div><a class="link_internal__7XN06 link_wrapper__5ZJEx styles_consumerDetails__ZFieb" data-consumer-profile-link="true" href="/users/53d22365000064000180d4f3" name="consumer-profile" rel="nofollow" target="_self"><span class="typography_heading-xxs__QKBS8 typography_appearance-default__AAY17" data-consumer-name-typography="true">sertaki</span><div class="styles_consumerExtraDetails__fxS4S" data-consumer-reviews-count="1"><span class="typography_body-m__xgxZ_ typography_appearance-subtle__8_H2l" data-consumer-reviews-count-typography="true">1<!-- --> avis</span><div class="typography_body-m__xgxZ_ typography_appearance-subtle__8_H2l styles_detailsIcon__Fo_ua" data-consumer-country-typography="true"><svg class="icon_icon__ECGRl" fill="currentColor" height="14px" viewbox="0 0 16 16" width="14px" xmlns="http://www.w3.org/2000/svg"><path clip-rule="evenodd" d="M3.404 1.904A6.5 6.5 0 0 1 14.5 6.5v.01c0 .194 0 .396-.029.627l-.004.03-.023.095c-.267 2.493-1.844 4.601-3.293 6.056a18.723 18.723 0 0 1-2.634 2.19 11.015 11.015 0 0 1-.234.154l-.013.01-.004.002h-.002L8 15.25l-.261.426h-.002l-.004-.003-.014-.009a13.842 13.842 0 0 1-.233-.152 18.388 18.388 0 0 1-2.64-2.178c-1.46-1.46-3.05-3.587-3.318-6.132l-.003-.026v-.068c-.025-.2-.025-.414-.025-.591V6.5a6.5 6.5 0 0 1 1.904-4.596ZM8 15.25l-.261.427.263.16.262-.162L8 15.25Zm-.002-.598a17.736 17.736 0 0 0 2.444-2.04c1.4-1.405 2.79-3.322 3.01-5.488l.004-.035.026-.105c.018-.153.018-.293.018-.484a5.5 5.5 0 0 0-11 0c0 .21.001.371.02.504l.005.035v.084c.24 2.195 1.632 4.109 3.029 5.505a17.389 17.389 0 0 0 2.444 2.024Z" fill-rule="evenodd"></path><path clip-rule="evenodd" d="M8 4a2.5 2.5 0 1 0 0 5 2.5 2.5 0 0 0 0-5ZM4.5 6.5a3.5 3.5 0 1 1 7 0 3.5 3.5 0 0 1-7 0Z" fill-rule="evenodd"></path></svg><span>FR</span></div></div></a></div></aside><hr class="divider_divider__M85e9 styles_cardDivider__42s_0 divider_appearance-subtle__DkHcP"/><section aria-disabled="false" class="styles_reviewContentwrapper__zH_9M"><div class="styles_reviewHeader__iU9Px" data-service-review-rating="4"><div class="star-rating_starRating__4rrcf star-rating_medium__iN6Ty"><img alt="Noté 4 sur 5 étoiles" src="https://cdn.trustpilot.net/brand-assets/4.1.0/stars/stars-4.svg"/></div><div class="typography_body-m__xgxZ_ typography_appearance-subtle__8_H2l styles_datesWrapper__RCEKH"><time class="" data-service-review-date-time-ago="true" datetime="2014-07-25T15:43:59.000Z">25 juil. 2014</time></div></div><div aria-hidden="false" class="styles_reviewContent__0Q2Tg" data-review-content="true"><a class="link_internal__7XN06 typography_appearance-default__AAY17 typography_color-inherit__TlgPO link_link__IZzHN link_notUnderlined__szqki" data-review-title-typography="true" href="/reviews/53d27b3f00006400029a5360" rel="nofollow" target="_self"><h2 class="typography_heading-s__f7029 typography_appearance-default__AAY17" data-service-review-title-typography="true">pas toujours de glace</h2></a><p class="typography_body-l__KUYFJ typography_appearance-default__AAY17 typography_color-black__5LYEn" data-service-review-text-typography="true">Effectivement, rarement de la glace le soir..</p><p class="typography_body-m__xgxZ_ typography_appearance-default__AAY17" data-service-review-date-of-experience-typography="true"><b class="typography_body-m__xgxZ_ typography_appearance-default__AAY17 typography_weight-heavy__E1LTj" weight="heavy">Date de l'expérience<!-- -->:</b> <!-- -->25 juillet 2014</p></div></section></div></article>
<article class="paper_paper__1PY90 paper_outline__lwsUX card_card__lQWDv card_noPadding__D8PcU styles_reviewCard__hcAvl" data-service-review-card-paper="true"><div class="styles_reviewCardInner__EwDq2"><aside aria-label="Informations sur Véronique REPECZKY" class="styles_consumerInfoWrapper__KP3Ra"><div class="styles_consumerDetailsWrapper__p2wdr"><div class="avatar_avatar__hmBp6 avatar_green__y0Z46" data-consumer-avatar="true" style="width:44px;min-width:44px;height:44px;min-height:44px"><span class="typography_heading-xs__jSwUz typography_appearance-default__AAY17 typography_disableResponsiveSizing__OuNP7 avatar_avatarName__ehkAr">VR</span></div><a class="link_internal__7XN06 link_wrapper__5ZJEx styles_consumerDetails__ZFieb" data-consumer-profile-link="true" href="/users/4f9347140000640001180955" name="consumer-profile" rel="nofollow" target="_self"><span class="typography_heading-xxs__QKBS8 typography_appearance-default__AAY17" data-consumer-name-typography="true">Véronique REPECZKY</span><div class="styles_consumerExtraDetails__fxS4S" data-consumer-reviews-count="17"><span class="typography_body-m__xgxZ_ typography_appearance-subtle__8_H2l" data-consumer-reviews-count-typography="true">17<!-- --> avis</span><div class="typography_body-m__xgxZ_ typography_appearance-subtle__8_H2l styles_detailsIcon__Fo_ua" data-consumer-country-typography="true"><svg class="icon_icon__ECGRl" fill="currentColor" height="14px" viewbox="0 0 16 16" width="14px" xmlns="http://www.w3.org/2000/svg"><path clip-rule="evenodd" d="M3.404 1.904A6.5 6.5 0 0 1 14.5 6.5v.01c0 .194 0 .396-.029.627l-.004.03-.023.095c-.267 2.493-1.844 4.601-3.293 6.056a18.723 18.723 0 0 1-2.634 2.19 11.015 11.015 0 0 1-.234.154l-.013.01-.004.002h-.002L8 15.25l-.261.426h-.002l-.004-.003-.014-.009a13.842 13.842 0 0 1-.233-.152 18.388 18.388 0 0 1-2.64-2.178c-1.46-1.46-3.05-3.587-3.318-6.132l-.003-.026v-.068c-.025-.2-.025-.414-.025-.591V6.5a6.5 6.5 0 0 1 1.904-4.596ZM8 15.25l-.261.427.263.16.262-.162L8 15.25Zm-.002-.598a17.736 17.736 0 0 0 2.444-2.04c1.4-1.405 2.79-3.322 3.01-5.488l.004-.035.026-.105c.018-.153.018-.293.018-.484a5.5 5.5 0 0 0-11 0c0 .21.001.371.02.504l.005.035v.084c.24 2.195 1.632 4.109 3.029 5.505a17.389 17.389 0 0 0 2.444 2.024Z" fill-rule="evenodd"></path><path clip-rule="evenodd" d="M8 4a2.5 2.5 0 1 0 0 5 2.5 2.5 0 0 0 0-5ZM4.5 6.5a3.5 3.5 0 1 1 7 0 3.5 3.5 0 0 1-7 0Z" fill-rule="evenodd"></path></svg><span>FR</span></div></div></a></div></aside><hr class="divider_divider__M85e9 styles_cardDivider__42s_0 divider_appearance-subtle__DkHcP"/><section aria-disabled="false" class="styles_reviewContentwrapper__zH_9M"><div class="styles_reviewHeader__iU9Px" data-service-review-rating="1"><div class="star-rating_starRating__4rrcf star-rating_medium__iN6Ty"><img alt="Noté 1 sur 5 étoiles" src="https://cdn.trustpilot.net/brand-assets/4.1.0/stars/stars-1.svg"/></div><div class="typography_body-m__xgxZ_ typography_appearance-subtle__8_H2l styles_datesWrapper__RCEKH"><time class="" data-service-review-date-time-ago="true" datetime="2012-04-22T00:19:59.000Z">22 avr. 2012</time></div></div><div aria-hidden="false" class="styles_reviewContent__0Q2Tg" data-review-content="true"><a class="link_internal__7XN06 typography_appearance-default__AAY17 typography_color-inherit__TlgPO link_link__IZzHN link_notUnderlined__szqki" data-review-title-typography="true" href="/reviews/4f934eaf00006400021c2f9b" rel="nofollow" target="_self"><h2 class="typography_heading-s__f7029 typography_appearance-default__AAY17" data-service-review-title-typography="true">mac do Venette NUL</h2></a><p class="typography_body-l__KUYFJ typography_appearance-default__AAY17 typography_color-black__5LYEn" data-service-review-text-typography="true">Plusieurs fois dans l'année, on s'arrête, et après avoir commandé, on demande le dessert : PAS<br/>Ils vendent des sandwiches prévus avec bacon, sans bacon, et quand on les appelle ils sont à peine aimables...et au lieu d'un s<br/>Ceci est une expétrience personnelle et répétées chez ce commerçant, ce n'est pas diffamatoire, ce n'est que la VERITE</p><p class="typography_body-m__xgxZ_ typography_appearance-default__AAY17" data-service-review-date-of-experience-typography="true"><b class="typography_body-m__xgxZ_ typography_appearance-default__AAY17 typography_weight-heavy__E1LTj" weight="heavy">Date de l'expérience<!-- -->:</b> <!-- -->22 avril 2012</p></div></section></div></article>''']

def parse_trustPilot_review(article):
    reviewData = {}

    # Extrait le nom de l'utilisateur
    userName = article.find('span', class_='typography_heading-xxs__QKBS8')
    reviewData['userName'] = userName.get_text(strip=True) if userName else None
    
    # Extrait le titre de la review
    reviewTitle = article.find('h2', class_='typography_heading-s__f7029')
    reviewData['reviewTitle'] = reviewTitle.get_text(strip=True) if reviewTitle else None

    # Extrait la note
    rating = article.find('div', class_='star-rating_starRating__4rrcf')
    reviewData['rating'] = int(rating.img['alt'][5]) if rating and rating.img['alt'][5].isdigit() else None

    # Extrait le commentaire
    comment = article.find('p', class_='typography_body-l__KUYFJ')
    reviewData['comment'] = comment.get_text(strip=True) if comment else None

    # Extrait la date de l'expérience
    date = article.find('p', class_='typography_body-m__xgxZ_')
    reviewData['date'] = date.get_text(strip=True) if date else None

    return reviewData

def parse_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    articles = soup.find_all('article', class_='paper_paper__1PY90')

    reviews = []
    for article in articles:
        review = parse_trustPilot_review(article)
        reviews.append(review)

    return reviews

def insert_into_mysql(review):
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        port = 3307,
        password="password",
        database="reviews"
    )

    cursor = connection.cursor()

    query = """
        INSERT INTO reviews (userName, reviewTitle, rating, comment, date, source)
        VALUES (%s, %s, %s, %s, %s, %s)
    """

    data = (
        review['userName'],
        review['reviewTitle'],
        review['rating'],
        review['comment'],
        review['date'],
        "TrustPilot"
    )

    cursor.execute(query, data)

    connection.commit()
    cursor.close()
    connection.close()

for idx, html_article in enumerate(html_content_trustPilot, 1):
    reviews = parse_html(html_article)

    # Entre les reviews dans MySQL
    for review in reviews:
        insert_into_mysql(review)

# for idx, html_article in enumerate(html_content_trustPilot, 1):
#     reviews = parse_html(html_article)

#     for i, review in enumerate(reviews, 1):
#         print(f"Page {idx}, Review {i}:")
#         print(f"User Name: {review['userName']}")
#         print(f"Rating: {review['rating']}")
#         print(f"Title: {review['reviewTitle']}")
#         print(f"Comment: {review['comment']}")
#         print(f"Date: {review['date']}")
#         print("=" * 50)
    