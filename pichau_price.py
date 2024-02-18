from playwright.sync_api import sync_playwright
import re

# instalar
# pip install playwright
# playwright install

def fetch_product_details(url):
    with sync_playwright() as p:
        # Use headless=True em ambiente de produção
        # headless=True remove a visão do navegador
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto(url)
        # Espera pelo carregamento de um elemento que contém a descrição e o preço
        page.wait_for_selector('div.MuiCardContent-root')
        # Seleciona todos os cartões de produtos na página
        cards = page.query_selector_all('div.MuiCardContent-root')

        products = []
        for card in cards:
            # Captura a descrição dentro do <h2> para cada produto
            descricao = card.query_selector('h2').inner_text()
            # Captura o preço. Note que você pode precisar ajustar o seletor dependendo da estrutura exata da página
            preco = card.query_selector('div[class*="jss"]:has-text("R$")').inner_text()
            preco = re.search(r'à vista\nR\$\s*([\d.,]+)', preco).group(1).replace('.', '').replace(',', '.')
            products.append({"name": descricao, "price": preco})
        browser.close()
        return products

dados = fetch_product_details("https://www.pichau.com.br/hardware/placa-de-video")
print(dados)
