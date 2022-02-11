from bs4 import BeautifulSoup
from urllib import request
import sqlite3

# Connect to a table and cursor
conn = sqlite3.connect('database.db')
cur = conn.cursor()

# Create a table
cur.executescript('''
    DROP TABLE IF EXISTS vnexpress;
    CREATE TABLE vnexpress (
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        date TEXT,
        title TEXT UNIQUE,
        link TEXT UNIQUE,
        description TEXT
    )
''')

def get_data(url):
    # Get the links to webpags and pass them to BeautifulSoup
    page = request.urlopen(url)
    soup = BeautifulSoup(page, 'html.parser')
    # Get all new_feeds
    new_feeds = soup.find_all('div', class_='item_list_folder')
    for new_feed in new_feeds:
        try:
            article = new_feed.find('h2', class_='title_news_site').find('a')
            # Get the title of the article
            title = article.get('title')
            # Get the link to the article
            link = article.get('href')
            # Get the date of the new article
            post_date = new_feed.find('div', class_='timer_post').text.strip().split('|')[0]
            # Get the description of the new article
            descr = new_feed.find('div', class_='lead_news_site').find('a').text.strip()
        except AttributeError:
            pass
        # print(f'DATE: {post_date}')
        # print(f'TITLE: {title}')
        # print(f'LINK: {link}')
        # print(f'DESCRIPTION : {descr}')
        # print('====================')
        cur.execute('''INSERT OR IGNORE INTO vnexpress (date, title, link, description) VALUES (?, ?, ?, ?)''', (post_date, title, link, descr))
        # Save data to the table
        conn.commit()

subjects = ['travel', 'sports', 'life', 'business', 'news', 'world', 'trend', 'style', 'culture', 'economy', 'places']
for subject in subjects:
    url = f'https://e.vnexpress.net/news/{subject}'
    get_data(url)

# Close cursor and disconnect to the database
cur.close()
conn.close()
