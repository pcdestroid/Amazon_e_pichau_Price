from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto('https://www.amazon.com.br/s?k=RTX3060')

    names_elements = page.query_selector_all('.a-size-base-plus')
    prices_elements = page.query_selector_all('.a-price-whole')

    names = [element.inner_text() for element in names_elements]
    prices = [element.inner_text() for element in prices_elements]

    products = [{'name': name, 'price': price}
                for name, price in zip(names, prices)]

    print(products)

    browser.close()
