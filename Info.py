import pandas as pd
import requests
from bs4 import BeautifulSoup
import streamlit as st

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.162 Safari/537.36'}
webpage = requests.get('https://dealsheaven.in/?page=1', headers=headers).text
soup = BeautifulSoup(webpage, 'lxml')

company = soup.find_all('div', class_='deatls-inner')
title = []
price = []
Rating = []
website_links = []
for i in company:
    title.append(i.find('h3').text.strip())
    price.append(i.find_all(class_='price')[0].text.strip())
    Rating.append(i.find_all(class_='star')[0].text.strip())
    website_link = i.find('a')['href']
    website_links.append(f'<a href="{website_link}" target="_blank">Click Here</a>')  # HTML clickable link

d = {'title': title, 'price': price, 'Rating': Rating, 'website': website_links}
df = pd.DataFrame(d)

st.title('Deals Information')
#st.dataframe(df)
st.markdown("""
    <style>
    .scrollable-table {
        max-height: 400px;
        overflow-y: auto;
        overflow-x: auto;
    }
    </style>
    """, unsafe_allow_html=True)
st.markdown('<div class="scrollable-table">' + df.to_html(escape=False) + '</div>', unsafe_allow_html=True)
plain_links = [link.split('"')[1] for link in website_links]  
df['website'] = plain_links  
st.download_button(
    label="Download CSV",
    data=df.to_csv(index=False),
    file_name='output2.csv',
    mime='text/csv'
)
