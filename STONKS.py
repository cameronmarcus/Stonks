import http.client
import json
import time
import pandas as pd
import schedule
def api_call(stock, df):
    conn = http.client.HTTPSConnection("macrotrends-finance.p.rapidapi.com")

    headers = {
        "X-RapidAPI-Key": "ENTER KEY HERE",
        "X-RapidAPI-Host": "macrotrends-finance.p.rapidapi.com",
    }

    conn.request(
        "GET", f"/quotes/history-price?symbol={stock}&range=1d", headers=headers
    )
    res = conn.getresponse()
    df1 = pd.DataFrame(json.load(res))
    df1 = df1.drop(columns=["Message", "Date"])

    conn.request(
        "GET",
        f"/statements/income?symbol={stock}&freq=Q&formstyle=dataframe",
        headers=headers,
    )
    res = conn.getresponse()
    df2 = pd.DataFrame(json.load(res)).head(1)

    stock_df = pd.concat(
        [df1.reset_index(drop=True), df2.reset_index(drop=True)], axis=1, join="inner"
    )

    stock_df.insert(0, "Stock", stock)

    if df.size == 0:
        df = stock_df
    else:
        df = pd.concat([df, stock_df], ignore_index=True)

    return df
def update():
    print("Updating Stock Data...")
    stocks = ["ESTC", "PANW", "CRWD", "CSCO", "AAPL"]
    df = pd.DataFrame()
    for stock in stocks:
        df = api_call(stock, df)

    df = df[["Open", "High", "Low", "Close", "Adj Close",
             "Volume", "Revenue", "Cost-Of-Goods-Sold", "Gross-Profit",
             "Research-And-Development-Expenses", "SG&A-Expenses",
             "Other-Operating-Income-Or-Expenses", "Operating-Expenses", "Operating-Income",
             "Total-Non-Operating-Income/Expense", "Pre-Tax-Income", "Income-Taxes", "Income-After-Taxes",
             "Other-Income", "Income-From-Continuous-Operations", "Income-From-Discontinued-Operations",
             "Net-Income", "EBITDA", "EBIT", "Basic-Shares-Outstanding", "Shares-Outstanding", "Basic-EPS",
             "EPS---Earnings-Per-Share"]]

    df.to_csv("stocks.csv", index=False)

schedule.every(1).minutes.do(update)
update()
while True:
    schedule.run_pending()
    time.sleep(1)
