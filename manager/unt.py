from bs4 import BeautifulSoup
from helper.unt.category import Category
from urllib.request import urlopen, urlretrieve
import os


def scrape():

    initial_url = 'https://digital.library.unt.edu'
    article_url = initial_url + '/search/?q=&t=fulltext&sort=added_d&fq=dc_type%3A'

    # FOR EACH CATEGORY DOWNLOAD ALL THE IMAGES
    for cat in Category:
        # VARIABLE THAT DENOTE IF THERE IS NEXT PAGE, SET TO TRUE FOR THE FIRST PAGE
        next_page = True
        # DOWNLOAD ONLY 10000 ARTICLE FOR CATEGORY
        i = 1
        url = article_url + cat.value
        fpath = './Dataset/' + cat.name
        if not os.path.exists(fpath):
            os.makedirs(fpath)
        while next_page:

            print('start: ' + url)

            # OPEN THE PAGE AND PARSE THE HTML
            page = urlopen(url)
            soup = BeautifulSoup(page)

            # FIND ALL THE ARTICLES IN THE PAGE
            all_articles = soup.find_all('article')
            # ITERATE THROUGH ARTICLES
            for article in all_articles:
                if i >= 15000:
                    next_page = False
                    break
                # EACH ARTICLE IS COMPOSED OF TWO DIV, IN PREVIEW THERE IS THE LINK, IN META SOMETIMES A WARNING
                # TO CHECK
                article_preview = article.find('div', class_='result__preview')
                article_meta = article.find('div', class_='result__meta')

                # EXTRACTION OF LINK AND WARNING FIELD
                article_a = article_preview.find('a', class_='link')

                article_title_h2 = article_meta.find('h2', class_='result__title')
                article_title = article_title_h2.find('a').get('data-meta-id')
                warning = article_meta.find('div', class_='alert-warning')
                data_div = article_meta.find('div', class_='result__field--date')
                data = data_div.find('span', class_='result__value')
                data_warning = True if '2017' in data.text else False
                # IF WARNING IS ACTIVE SKIP THE SCRAPING
                if warning is None and not data_warning:
                    article_link = initial_url + article_a.get('href') + 'm1/1/'
                    next_article_page = True
                    fpath = './Dataset/' + cat.name + '/' + article_title
                    if not os.path.exists(fpath):
                        os.makedirs(fpath)
                    # WHILE THERE IS A NEXT ARTICLE PAGE SAVE LINK AND DOWNLOAD FILE
                    fname_index = 1
                    while next_article_page:
                        i += 1
                        # OPEN THE ARTICLE PAGE AND PARSE THE HTML
                        article_image_page = urlopen(article_link)
                        article_soup = BeautifulSoup(article_image_page)

                        # DOWNLOAD IMAGE
                        fname = '/' + str(fname_index) + '.jpg'
                        image_url = article_link + 'high_res_d/'
                        urlretrieve(image_url, fpath + fname)

                        # CHECK IF THERE IS ANOTHER PAGE
                        next_article_page_link = article_soup.find('a', id='ark-nav-next-top')
                        if next_article_page_link.has_attr('disabled'):
                            next_article_page = False
                        else:
                            article_link = initial_url + next_article_page_link.get('href')
                            fname_index += 1


            # CHECK IF THERE IS ANOTHER PAGE
            next_page_link = soup.find('a', id='pag-next')
            if next_page_link is not None:
                url = initial_url + '/search/' + next_page_link.get('href')
            else:
                next_page = False









