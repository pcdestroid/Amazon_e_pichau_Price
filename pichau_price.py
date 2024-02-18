from playwright.sync_api import sync_playwright
import re

# instalar
# pip install playwright
# playwright install

# Documentação
# https://playwright.dev/python/docs/intro


def fetch_product_details(url):
    with sync_playwright() as p:

        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto(url)

        page.wait_for_selector('div.MuiCardContent-root')
        cards = page.query_selector_all('div.MuiCardContent-root')

        products = []
        for card in cards:

            descricao = card.query_selector(
                'h2').inner_text().lower().replace("placa de video", "")
            descricao = descricao.replace("\n", " ").replace(
                ",", "").replace("  ", " ")

            match = re.search(r'.*?gb', descricao)
            # match = re.search(r'.{10}(?=GDDR)', descricao)
            if match:
                descricao = match.group()

            preco = card.query_selector(
                'div[class*="jss"]:has-text("R$")').inner_text()
            preco = re.search(
                r'à vista\nR\$\s*([\d.,]+)', preco).group(1).replace(".", "").replace(",", ".")

            products.append({"name": descricao, "price": preco})
        browser.close()
        return products


# dados = fetch_product_details("https://www.pichau.com.br/search?q=GTX1660")
dados = fetch_product_details(
    "https://www.pichau.com.br/hardware/placa-de-video")
print(dados)
# print(dados[0])
# print(dados[1])
