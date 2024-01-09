from bs4 import BeautifulSoup
import mysql.connector

html_content_trustPilot = ['''<article class="paper_paper__1PY90 paper_outline__lwsUX card_card__lQWDv card_noPadding__D8PcU styles_reviewCard__hcAvl " data-service-review-card-paper="true"><div class="styles_reviewCardInner__EwDq2"><aside class="styles_consumerInfoWrapper__KP3Ra" aria-label="Informations sur Leprince Coquelicot"><div class="styles_consumerDetailsWrapper__p2wdr"><div class="avatar_imageWrapper__8wdWb" style="width:44px;height:44px;min-width:44px;min-height:44px"><span style="box-sizing:border-box;display:inline-block;overflow:hidden;width:initial;height:initial;background:none;opacity:1;border:0;margin:0;padding:0;position:relative;max-width:100%"><span style="box-sizing:border-box;display:block;width:initial;height:initial;background:none;opacity:1;border:0;margin:0;padding:0;max-width:100%"><img style="display:block;max-width:100%;width:initial;height:initial;background:none;opacity:1;border:0;margin:0;padding:0" alt="" aria-hidden="true" src="data:image/svg+xml,%3csvg%20xmlns=%27http://www.w3.org/2000/svg%27%20version=%271.1%27%20width=%2744%27%20height=%2744%27/%3e"></span><img alt="" data-consumer-avatar-image="true" src="https://user-images.trustpilot.com/6599784d4d259800120048bb/73x73.png" decoding="async" data-nimg="intrinsic" style="position:absolute;top:0;left:0;bottom:0;right:0;box-sizing:border-box;padding:0;border:none;margin:auto;display:block;width:0;height:0;min-width:100%;max-width:100%;min-height:100%;max-height:100%"></span></div><a href="/users/6599784d4d259800120048bb" rel="nofollow" name="consumer-profile" target="_self" class="link_internal__7XN06 link_wrapper__5ZJEx styles_consumerDetails__ZFieb" data-consumer-profile-link="true"><span class="typography_heading-xxs__QKBS8 typography_appearance-default__AAY17" data-consumer-name-typography="true">Leprince Coquelicot</span><div class="styles_consumerExtraDetails__fxS4S" data-consumer-reviews-count="1"><span class="typography_body-m__xgxZ_ typography_appearance-subtle__8_H2l" data-consumer-reviews-count-typography="true">1<!-- --> avis</span><div class="typography_body-m__xgxZ_ typography_appearance-subtle__8_H2l styles_detailsIcon__Fo_ua" data-consumer-country-typography="true"><svg viewBox="0 0 16 16" fill="currentColor" class="icon_icon__ECGRl" xmlns="http://www.w3.org/2000/svg" width="14px" height="14px"><path fill-rule="evenodd" clip-rule="evenodd" d="M3.404 1.904A6.5 6.5 0 0 1 14.5 6.5v.01c0 .194 0 .396-.029.627l-.004.03-.023.095c-.267 2.493-1.844 4.601-3.293 6.056a18.723 18.723 0 0 1-2.634 2.19 11.015 11.015 0 0 1-.234.154l-.013.01-.004.002h-.002L8 15.25l-.261.426h-.002l-.004-.003-.014-.009a13.842 13.842 0 0 1-.233-.152 18.388 18.388 0 0 1-2.64-2.178c-1.46-1.46-3.05-3.587-3.318-6.132l-.003-.026v-.068c-.025-.2-.025-.414-.025-.591V6.5a6.5 6.5 0 0 1 1.904-4.596ZM8 15.25l-.261.427.263.16.262-.162L8 15.25Zm-.002-.598a17.736 17.736 0 0 0 2.444-2.04c1.4-1.405 2.79-3.322 3.01-5.488l.004-.035.026-.105c.018-.153.018-.293.018-.484a5.5 5.5 0 0 0-11 0c0 .21.001.371.02.504l.005.035v.084c.24 2.195 1.632 4.109 3.029 5.505a17.389 17.389 0 0 0 2.444 2.024Z"></path><path fill-rule="evenodd" clip-rule="evenodd" d="M8 4a2.5 2.5 0 1 0 0 5 2.5 2.5 0 0 0 0-5ZM4.5 6.5a3.5 3.5 0 1 1 7 0 3.5 3.5 0 0 1-7 0Z"></path></svg><span>FR</span></div></div></a></div></aside><hr class="divider_divider__M85e9 styles_cardDivider__42s_0 divider_appearance-subtle__DkHcP"><section class="styles_reviewContentwrapper__zH_9M" aria-disabled="false"><div class="styles_reviewHeader__iU9Px" data-service-review-rating="1"><div class="star-rating_starRating__4rrcf star-rating_medium__iN6Ty"><img alt="Noté 1 sur 5 étoiles" src="https://cdn.trustpilot.net/brand-assets/4.1.0/stars/stars-1.svg"></div><div class="typography_body-m__xgxZ_ typography_appearance-subtle__8_H2l styles_datesWrapper__RCEKH"><time datetime="2024-01-06T17:57:09.000Z" class="" data-service-review-date-time-ago="true" title="samedi 6 janvier 2024 à 18:57:09">ll y a 2 jours</time></div></div><div class="styles_reviewContent__0Q2Tg" aria-hidden="false" data-review-content="true"><a href="/reviews/6599785555b650faf68c07e5" rel="nofollow" target="_self" class="link_internal__7XN06 typography_appearance-default__AAY17 typography_color-inherit__TlgPO link_link__IZzHN link_notUnderlined__szqki" data-review-title-typography="true"><h2 class="typography_heading-s__f7029 typography_appearance-default__AAY17" data-service-review-title-typography="true">Mac Do Oyonnax</h2></a><p class="typography_body-l__KUYFJ typography_appearance-default__AAY17 typography_color-black__5LYEn" data-service-review-text-typography="true">Mac Do Oyonnax : Lamentable ! Presque 40 min d'attente pour une commande en salle avec une personne autiste (alors que nous avions demandé à être servis assez vite). Frites froides, erreur sur les menus et boissons livrées à part ! Assurément un des pires Mac Do de France !</p><p class="typography_body-m__xgxZ_ typography_appearance-default__AAY17" data-service-review-date-of-experience-typography="true"><b class="typography_body-m__xgxZ_ typography_appearance-default__AAY17 typography_weight-heavy__E1LTj" weight="heavy">Date de l'expérience<!-- -->:</b> <!-- -->06 janvier 2024</p></div></section><hr class="divider_divider__M85e9 styles_cardDivider__42s_0 divider_appearance-subtle__DkHcP"><div class="styles_wrapper__GfGYg styles_actionsWrapper__q1pnO"><button class="buttons_actionButtons__cCIZv buttons_button__uNj0b button_button__T34Lr button_appearance-link__ANr2s" name="find-useful" type="button" data-find-useful-button="true"><span class="typography_body-l__KUYFJ typography_appearance-subtle__8_H2l link_link__IZzHN link_notUnderlined__szqki"><svg viewBox="0 0 16 16" fill="currentColor" class="icon_icon__ECGRl" xmlns="http://www.w3.org/2000/svg" width="14px" height="14px"><path fill-rule="evenodd" clip-rule="evenodd" d="M7.94.94A1.5 1.5 0 0 1 10.5 2a20.774 20.774 0 0 1-.384 4H14.5A1.5 1.5 0 0 1 16 7.5v.066l-1.845 6.9-.094.095A1.5 1.5 0 0 1 13 15H9c-.32 0-.685-.078-1.038-.174-.357-.097-.743-.226-1.112-.349l-.008-.003c-.378-.126-.74-.246-1.067-.335C5.44 14.047 5.18 14 5 14v.941l-5 .625V6h5v.788c.913-.4 1.524-1.357 1.926-2.418A10.169 10.169 0 0 0 7.5 1.973 1.5 1.5 0 0 1 7.94.939ZM8 2l.498.045v.006l-.002.013a4.507 4.507 0 0 1-.026.217 11.166 11.166 0 0 1-.609 2.443C7.396 5.951 6.541 7.404 5 7.851V13c.32 0 .685.078 1.038.174.357.097.743.226 1.112.349l.008.003c.378.126.74.246 1.067.335.335.092.594.139.775.139h4a.5.5 0 0 0 .265-.076l1.732-6.479A.5.5 0 0 0 14.5 7H8.874l.138-.61c.326-1.44.49-2.913.488-4.39a.5.5 0 0 0-1 0v.023l-.002.022L8 2ZM4 7H1v7.434l3-.375V7Zm-1.5 5.75a.25.25 0 1 0 0-.5.25.25 0 0 0 0 .5Zm-.75-.25a.75.75 0 1 1 1.5 0 .75.75 0 0 1-1.5 0Z"></path></svg><span class="typography_body-m__xgxZ_ typography_appearance-inherit__D7XqR styles_usefulLabel__qz3JV">Utile</span></span></button><span><button class="buttons_actionButtons__cCIZv buttons_button__uNj0b button_button__T34Lr button_appearance-link__ANr2s" name="share-review" type="button" data-share-review-button="true"><span class="typography_body-l__KUYFJ typography_appearance-subtle__8_H2l link_link__IZzHN link_notUnderlined__szqki"><svg viewBox="0 0 16 16" fill="currentColor" class="icon_icon__ECGRl" xmlns="http://www.w3.org/2000/svg" width="14px" height="14px"><path fill-rule="evenodd" clip-rule="evenodd" d="M13 1a2 2 0 1 0 0 4 2 2 0 0 0 0-4Zm-3 2a3 3 0 1 1 .583 1.778L5.867 7.115a3 3 0 0 1 0 1.77l4.716 2.337a3 3 0 1 1-.45.893L5.417 9.778a3 3 0 1 1 0-3.556l4.716-2.337A3.002 3.002 0 0 1 10 3ZM1 8a2 2 0 1 1 4 0 2 2 0 0 1-4 0Zm10 5a2 2 0 1 1 4 0 2 2 0 0 1-4 0Z"></path></svg><span class="typography_body-m__xgxZ_ typography_appearance-inherit__D7XqR">Partager</span></span></button></span><div class="styles_actionsRightSide__Bzast"><button class="styles_iconButton__em4q3" aria-label="Signaler cet avis" data-report-review-button="true"><svg viewBox="0 0 16 16" class="icon_icon__ECGRl icon_appearance-default___4uy_" xmlns="http://www.w3.org/2000/svg" width="16px" height="16px" data-report-icon="true"><path fill-rule="evenodd" clip-rule="evenodd" d="M3 .25V0H2v16h1V9.25h11.957l-4.5-4.5 4.5-4.5H3Zm0 1v7h9.543l-3.5-3.5 3.5-3.5H3Z"></path></svg></button></div></div></div></article>
                <article class="paper_paper__1PY90 paper_outline__lwsUX card_card__lQWDv card_noPadding__D8PcU styles_reviewCard__hcAvl " data-service-review-card-paper="true"><div class="styles_reviewCardInner__EwDq2"><aside class="styles_consumerInfoWrapper__KP3Ra" aria-label="Informations sur Chloé"><div class="styles_consumerDetailsWrapper__p2wdr"><div class="avatar_avatar__hmBp6 avatar_orange__cwwGs" style="width:44px;min-width:44px;height:44px;min-height:44px" data-consumer-avatar="true"><span class="typography_heading-xs__jSwUz typography_appearance-default__AAY17 typography_disableResponsiveSizing__OuNP7 avatar_avatarName__ehkAr">CH</span></div><a href="/users/62fa2b7263085200149d2334" rel="nofollow" name="consumer-profile" target="_self" class="link_internal__7XN06 link_wrapper__5ZJEx styles_consumerDetails__ZFieb" data-consumer-profile-link="true"><span class="typography_heading-xxs__QKBS8 typography_appearance-default__AAY17" data-consumer-name-typography="true">Chloé</span><div class="styles_consumerExtraDetails__fxS4S" data-consumer-reviews-count="3"><span class="typography_body-m__xgxZ_ typography_appearance-subtle__8_H2l" data-consumer-reviews-count-typography="true">3<!-- --> avis</span><div class="typography_body-m__xgxZ_ typography_appearance-subtle__8_H2l styles_detailsIcon__Fo_ua" data-consumer-country-typography="true"><svg viewBox="0 0 16 16" fill="currentColor" class="icon_icon__ECGRl" xmlns="http://www.w3.org/2000/svg" width="14px" height="14px"><path fill-rule="evenodd" clip-rule="evenodd" d="M3.404 1.904A6.5 6.5 0 0 1 14.5 6.5v.01c0 .194 0 .396-.029.627l-.004.03-.023.095c-.267 2.493-1.844 4.601-3.293 6.056a18.723 18.723 0 0 1-2.634 2.19 11.015 11.015 0 0 1-.234.154l-.013.01-.004.002h-.002L8 15.25l-.261.426h-.002l-.004-.003-.014-.009a13.842 13.842 0 0 1-.233-.152 18.388 18.388 0 0 1-2.64-2.178c-1.46-1.46-3.05-3.587-3.318-6.132l-.003-.026v-.068c-.025-.2-.025-.414-.025-.591V6.5a6.5 6.5 0 0 1 1.904-4.596ZM8 15.25l-.261.427.263.16.262-.162L8 15.25Zm-.002-.598a17.736 17.736 0 0 0 2.444-2.04c1.4-1.405 2.79-3.322 3.01-5.488l.004-.035.026-.105c.018-.153.018-.293.018-.484a5.5 5.5 0 0 0-11 0c0 .21.001.371.02.504l.005.035v.084c.24 2.195 1.632 4.109 3.029 5.505a17.389 17.389 0 0 0 2.444 2.024Z"></path><path fill-rule="evenodd" clip-rule="evenodd" d="M8 4a2.5 2.5 0 1 0 0 5 2.5 2.5 0 0 0 0-5ZM4.5 6.5a3.5 3.5 0 1 1 7 0 3.5 3.5 0 0 1-7 0Z"></path></svg><span>FR</span></div></div></a></div></aside><hr class="divider_divider__M85e9 styles_cardDivider__42s_0 divider_appearance-subtle__DkHcP"><section class="styles_reviewContentwrapper__zH_9M" aria-disabled="false"><div class="styles_reviewHeader__iU9Px" data-service-review-rating="1"><div class="star-rating_starRating__4rrcf star-rating_medium__iN6Ty"><img alt="Noté 1 sur 5 étoiles" src="https://cdn.trustpilot.net/brand-assets/4.1.0/stars/stars-1.svg"></div><div class="typography_body-m__xgxZ_ typography_appearance-subtle__8_H2l styles_datesWrapper__RCEKH"><time datetime="2024-01-07T20:51:56.000Z" class="" data-service-review-date-time-ago="true" title="dimanche 7 janvier 2024 à 21:51:56">ll y a 1 jours</time></div></div><div class="styles_reviewContent__0Q2Tg" aria-hidden="false" data-review-content="true"><a href="/reviews/659af2cc07bffba5983bb20a" rel="nofollow" target="_self" class="link_internal__7XN06 typography_appearance-default__AAY17 typography_color-inherit__TlgPO link_link__IZzHN link_notUnderlined__szqki" data-review-title-typography="true"><h2 class="typography_heading-s__f7029 typography_appearance-default__AAY17" data-service-review-title-typography="true">problème avec les livraisons</h2></a><p class="typography_body-l__KUYFJ typography_appearance-default__AAY17 typography_color-black__5LYEn" data-service-review-text-typography="true">2 fois d’affilée que l’on commande en livraison et que le livreur part à l’opposé de notre domicile avec notre commande, résultat repas froid et les réclamations sont fastidieuses, il faut envoyer rib etc… une honte</p><p class="typography_body-m__xgxZ_ typography_appearance-default__AAY17" data-service-review-date-of-experience-typography="true"><b class="typography_body-m__xgxZ_ typography_appearance-default__AAY17 typography_weight-heavy__E1LTj" weight="heavy">Date de l'expérience<!-- -->:</b> <!-- -->07 janvier 2024</p></div></section><hr class="divider_divider__M85e9 styles_cardDivider__42s_0 divider_appearance-subtle__DkHcP"><div class="styles_wrapper__GfGYg styles_actionsWrapper__q1pnO"><button class="buttons_actionButtons__cCIZv buttons_button__uNj0b button_button__T34Lr button_appearance-link__ANr2s" name="find-useful" type="button" data-find-useful-button="true"><span class="typography_body-l__KUYFJ typography_appearance-subtle__8_H2l link_link__IZzHN link_notUnderlined__szqki"><svg viewBox="0 0 16 16" fill="currentColor" class="icon_icon__ECGRl" xmlns="http://www.w3.org/2000/svg" width="14px" height="14px"><path fill-rule="evenodd" clip-rule="evenodd" d="M7.94.94A1.5 1.5 0 0 1 10.5 2a20.774 20.774 0 0 1-.384 4H14.5A1.5 1.5 0 0 1 16 7.5v.066l-1.845 6.9-.094.095A1.5 1.5 0 0 1 13 15H9c-.32 0-.685-.078-1.038-.174-.357-.097-.743-.226-1.112-.349l-.008-.003c-.378-.126-.74-.246-1.067-.335C5.44 14.047 5.18 14 5 14v.941l-5 .625V6h5v.788c.913-.4 1.524-1.357 1.926-2.418A10.169 10.169 0 0 0 7.5 1.973 1.5 1.5 0 0 1 7.94.939ZM8 2l.498.045v.006l-.002.013a4.507 4.507 0 0 1-.026.217 11.166 11.166 0 0 1-.609 2.443C7.396 5.951 6.541 7.404 5 7.851V13c.32 0 .685.078 1.038.174.357.097.743.226 1.112.349l.008.003c.378.126.74.246 1.067.335.335.092.594.139.775.139h4a.5.5 0 0 0 .265-.076l1.732-6.479A.5.5 0 0 0 14.5 7H8.874l.138-.61c.326-1.44.49-2.913.488-4.39a.5.5 0 0 0-1 0v.023l-.002.022L8 2ZM4 7H1v7.434l3-.375V7Zm-1.5 5.75a.25.25 0 1 0 0-.5.25.25 0 0 0 0 .5Zm-.75-.25a.75.75 0 1 1 1.5 0 .75.75 0 0 1-1.5 0Z"></path></svg><span class="typography_body-m__xgxZ_ typography_appearance-inherit__D7XqR styles_usefulLabel__qz3JV">Utile</span></span></button><span><button class="buttons_actionButtons__cCIZv buttons_button__uNj0b button_button__T34Lr button_appearance-link__ANr2s" name="share-review" type="button" data-share-review-button="true"><span class="typography_body-l__KUYFJ typography_appearance-subtle__8_H2l link_link__IZzHN link_notUnderlined__szqki"><svg viewBox="0 0 16 16" fill="currentColor" class="icon_icon__ECGRl" xmlns="http://www.w3.org/2000/svg" width="14px" height="14px"><path fill-rule="evenodd" clip-rule="evenodd" d="M13 1a2 2 0 1 0 0 4 2 2 0 0 0 0-4Zm-3 2a3 3 0 1 1 .583 1.778L5.867 7.115a3 3 0 0 1 0 1.77l4.716 2.337a3 3 0 1 1-.45.893L5.417 9.778a3 3 0 1 1 0-3.556l4.716-2.337A3.002 3.002 0 0 1 10 3ZM1 8a2 2 0 1 1 4 0 2 2 0 0 1-4 0Zm10 5a2 2 0 1 1 4 0 2 2 0 0 1-4 0Z"></path></svg><span class="typography_body-m__xgxZ_ typography_appearance-inherit__D7XqR">Partager</span></span></button></span><div class="styles_actionsRightSide__Bzast"><button class="styles_iconButton__em4q3" aria-label="Signaler cet avis" data-report-review-button="true"><svg viewBox="0 0 16 16" class="icon_icon__ECGRl icon_appearance-default___4uy_" xmlns="http://www.w3.org/2000/svg" width="16px" height="16px" data-report-icon="true"><path fill-rule="evenodd" clip-rule="evenodd" d="M3 .25V0H2v16h1V9.25h11.957l-4.5-4.5 4.5-4.5H3Zm0 1v7h9.543l-3.5-3.5 3.5-3.5H3Z"></path></svg></button></div></div></div></article>''']

def parse_review(article):
    review_data = {}

    # Extrait le nom de l'utilisateur
    userName = article.find('span', class_='typography_heading-xxs__QKBS8')
    review_data['userName'] = userName.get_text(strip=True) if userName else None
    
    # Extrait le nom de l'utilisateur
    reviewTitle = article.find('h2', class_='typography_heading-s__f7029')
    review_data['reviewTitle'] = reviewTitle.get_text(strip=True) if reviewTitle else None

    # Extrait la note
    rating = article.find('div', class_='star-rating_starRating__4rrcf')
    review_data['rating'] = int(rating.img['alt'][5]) if rating and rating.img['alt'][5].isdigit() else None

    # Extrait le commentaire
    comment = article.find('p', class_='typography_body-l__KUYFJ')
    review_data['comment'] = comment.get_text(strip=True) if comment else None

    # Extrait la date de l'expérience
    date = article.find('p', class_='typography_body-m__xgxZ_')
    review_data['date'] = date.get_text(strip=True) if date else None

    return review_data

def parse_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    articles = soup.find_all('article', class_='paper_paper__1PY90')

    reviews = []
    for article in articles:
        review = parse_review(article)
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
        INSERT INTO reviews (userName, reviewTitle, rating, comment, date)
        VALUES (%s, %s, %s, %s, %s)
    """

    data = (
        review['userName'],
        review['reviewTitle'],
        review['rating'],
        review['comment'],
        review['date']
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
    