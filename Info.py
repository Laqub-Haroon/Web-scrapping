import pandas as pd
import requests
from bs4 import BeautifulSoup
import streamlit as st

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.162 Safari/537.36'}


stores = ["Flipkart", "Amazon", "Paytm", "Foodpanda", "Freecharge", "Paytmmall"]

def fetch_deals(store, start_page, end_page):
    data = []
    for page_number in range(start_page, end_page + 1):
        url = f"https://dealsheaven.in/store/{store.lower()}?page={page_number}"
        webpage = requests.get(url, headers=headers).text
        soup = BeautifulSoup(webpage, 'lxml')
        
        company = soup.find_all('div', class_='deatls-inner')
        for i in company:
            title = i.find('h3').text.strip()
            price = i.find_all(class_='price')[0].text.strip()
            rating = i.find_all(class_='star')[0].text.strip()
            website_link = i.find('a')['href']
            data.append({
                'title': title,
                'price': price,
                'rating': rating,
                'website': website_link
            }) 
    return pd.DataFrame(data)

st.title('Deals Scraper')
store = st.selectbox('Select a store:', options=stores)
start_page = st.number_input('Enter start page number:', min_value=1, step=1, value=1)
end_page = st.number_input('Enter end page number:', min_value=start_page, step=1, value=start_page)

if st.button('Submit'):
    df = fetch_deals(store, start_page, end_page) 
    csv_data = df.to_csv(index=False)
    
    st.download_button(
        label="Download CSV",
        data=csv_data,
        file_name=f'{store}_deals.csv',
        mime='text/csv'
    )

