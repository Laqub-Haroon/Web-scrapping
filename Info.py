import requests
from bs4 import BeautifulSoup
import streamlit as st
st.set_page_config(page_title="Deals Scraper", layout="wide")
#st.image("logo.png", use_column_width=True)
st.markdown(
    """
    <style>
    .black-strip {
        background-color: #000; 
        color: #fff; 
        padding: 10px 20px; 
        display: flex; 
        align-items: center; 
        font-size: 1.2em; 
        font-weight: bold; 
    }    
    .skyblue-header {
        background-color: skyblue;
        padding: 5px;
        border-radius: 2px;
        font-size: 20px;
        text-align: center;
    }

    .skyblue-header h3 {
        color: black;
        font-size: 18px;
    }
  
.product-container {
    width: 250px; 
    height: 450px; 
    border: 1px solid #ddd; 
    border-radius: 10px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); 
    background-color: #fff;
    padding: 10px; 
    margin: 10px; 
    display: inline-block; 
    text-align: center; 
    overflow: hidden; 
}

/* Styling for the product image */
.product-container img {
    max-width: 100%;
    max-height: 150px;
    object-fit: cover; 
    border-radius: 5px; 
}
.product-title-container {
    background-color: #f8f9fa;
    padding: 10px;
    border-radius: 5px;
    margin: 10px 0;
    height: 100px; 
    display: flex;
    justify-content: center;
    align-items: center;
}
.product-title {
    font-size: 0.6em; 
    font-weight: bold;
    color: #333;
    word-wrap: break-word; 
    text-align: center;
    margin: 0; 
}
.product-details {
    font-size: 0.9em;
    color: #555;
    line-height: 1.5;
}
.product-image-container {
    width: 100%;
    height: 140px; 
    background-color: #f0f0f0; 
    border: 1px solid #ddd;
    border-radius: 5px;
    display: flex;
    justify-content: center;
    align-items: center;
    margin-bottom: 10px; 
    overflow: hidden; 
}
.product-image-container img {
    max-width: 100%;
    max-height: 100%; 
    object-fit: contain;
}
    </style>
    """,
    unsafe_allow_html=True,
)
st.markdown("""
<div class="black-strip">
    <span>Deals Scraper</span>
</div>
""", unsafe_allow_html=True)
st.image("logo.png", use_column_width=False, width=220)
st.markdown(
    '<div class="skyblue-header"><h3>Choose a store or category and enter the page range </h3></div>',
    unsafe_allow_html=True,
)
store = ["All_store", "Flipkart", "Amazon", "Paytm", "Foodpanda", "Freecharge", "Paytmmall"]
store_name = st.selectbox("Select Store", store)
categories = [
    "All Categories",
    "Beauty And Personal Care",
    "Clothing Fashion & Apparels",
    "Electronics",
    "Grocery",
    "Mobiles & Mobile Accessories",
    "Recharge",
    "Travel Bus & Flight"
]
category_name = st.selectbox("Choose a Category", categories)

start = st.number_input('Enter start page number:', min_value=1, step=1, value=1)
end = st.number_input('Enter end page number:', min_value=start, step=1, value=start)

submit_button = st.button("Submit")

if submit_button:
    try:
        if end > 1703:
            st.error("The DealsHeaven Website has only 1703 Pages.")
        else:
            all_products = []
            for current_page in range(start, end + 1):
               
                if store_name == "All_store" and category_name == "All Categories":
                    url = f"https://dealsheaven.in/?page={current_page}"
                elif store_name == "All_store":
                    url = f"https://dealsheaven.in/category/{category_name.lower().replace(' ', '-')}/?page={current_page}"
                elif category_name == "All Categories":
                    url = f"https://dealsheaven.in/store/{store_name.lower()}?page={current_page}"
                else:
                    url = f"https://dealsheaven.in/store/{store_name.lower()}/category/{category_name.lower().replace(' ', '-')}/?page={current_page}"
                response = requests.get(url)
                if response.status_code != 200:
                    st.warning(f"Failed to retrieve page {current_page}.")
                    continue
                soup = BeautifulSoup(response.text, 'html.parser')
                all_items = soup.find_all("div", class_="product-item-detail")
                if not all_items:
                    st.warning(f"No products found on page {current_page}.")
                    break
                for item in all_items:
                    product = {}
                    product['Title'] = (
                        item.find("h3", title=True)['title'].replace("[Apply coupon] ", "").replace('"', '') 
                        if item.find("h3", title=True) else "N/A"
                    )
                    product['Image'] = item.find("img", src=True)['data-src'] if item.find("img", src=True) else None
                    product['Price'] = item.find("p", class_="price").text.strip() if item.find("p", class_="price") else "N/A"
                    product['Discount'] = item.find("div", class_="discount").text.strip() if item.find("div", class_="discount") else "N/A"
                    product['Special Price'] = (
                        item.find("p", class_="spacail-price").text.strip() if item.find("p", class_="spacail-price") else "N/A"
                    )
                    product['Link'] = item.find("a", href=True)['href'] if item.find("a", href=True) else "N/A"
                    all_products.append(product)
                for i in range(0, len(all_products), 6): 
                    cols = st.columns(6)  
                    for j, col in enumerate(cols):
                        if i + j < len(all_products):  
                            product = all_products[i + j]
                            col.markdown(
                                f"""
                                <div class="product-container">
                                    <div class="product-image-container">
                                    <img src="{product['Image']}" alt="Product Image" />
                                    </div>
                                        <div>
                                            <div class="product-title-container">
                                            <div class="product-title">{product['Title']}</div>
                                            </div>
                                            <p><b>Price:</b> {product['Price']}</p>
                                            <p><b>Discount:</b> {product['Discount']}</p>
                                            <p><b>Special Price:</b> {product['Special Price']}</p>
                                            <a href="{product['Link']}" target="_blank">View Deal</a>
                                        </div>
                                    </div>
                                </div>
                                """,
                                unsafe_allow_html=True,
                            )
    except ValueError:
        st.error("Please enter valid integers for the starting and ending page.")
