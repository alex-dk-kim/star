import requests
from bs4 import BeautifulSoup
import pandas as pd
import streamlit as st

def extract_table(input_source):
    soup = BeautifulSoup(requests.get(input_source).text, "html.parser")
    table1 = soup.find("table", class_="interestRates")
    financial_list = []

    for tr in table1.find_all("tr"):
        if tr.find_all("td"):
            tds = tr.find_all("td")
            provider, products, min_deposit, max_deposit, rate = tds
            if provider.a.text:
                provider_c = provider.a.text
            else:
                provider_c = provider.img["alt"]
            products_c = products.text.replace(" ", "").strip("\n")
            min_deposit_c = min_deposit.text.replace(" ", "").strip("\n")
            max_deposit_c = max_deposit.text.replace(" ", "").strip("\n")
            rate_c = rate.text.replace(" ", "").strip("\n")
            financial_list.append({"provider":provider_c, "products": products_c, "min_deposit": min_deposit_c, "max_deposit": max_deposit_c, "rate": rate_c})
    return financial_list

def creating_st():
    st.title('NZ Saving Interest Rate')
    financial_list = extract_table("https://www.depositrates.co.nz/interest-rates/savings-accounts.html")
    df = pd.DataFrame(financial_list)
    df.set_index("provider", inplace=True)
    print(df)
    st.dataframe(df)


creating_st()