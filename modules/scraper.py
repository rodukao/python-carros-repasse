import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re

uc.Chrome.__del__ = lambda self: None


def busca_itens():
    url = "https://www.olx.com.br/autos-e-pecas/carros-vans-e-utilitarios?q=repasse"
    options = uc.ChromeOptions()
    options.add_argument('--headless=new')
    options.add_argument('--no-sandbox')
    options.add_argument(
        '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
    options.add_argument('--disable-dev-shm-usage')

    driver = uc.Chrome(options=options, version_main=144)
    driver.get(url)
    wait = WebDriverWait(driver, 10)

    produtos = []
    try:
        conteudo = wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, "div[class*='AdListing']")))
        itens = conteudo.find_elements(By.TAG_NAME, "section")
        for item in itens[:10]:

            try:
                produto = {}
                # Título
                produto['titulo'] = item.find_element(By.TAG_NAME, "h2").text

                # Preço
                produto['preco'] = float(item.find_element(
                    By.CSS_SELECTOR, "h3[class*='price']").text.replace(".", "").replace("R$", "").strip())

                # Km
                produto['km'] = float(item.find_element(
                    By.CSS_SELECTOR, "div[class*='detail']").text.replace(".", "").split(" ")[0])

                # Km
                titulo = item.find_element(By.TAG_NAME, "h2").text
                ano = re.search(r'\b(19\d{2}|20\d{2})\b', titulo)
                if ano:
                    produto['ano'] = int(ano.group())
                else:
                    produto['ano'] = 0

                # Link
                produto['link'] = item.find_element(
                    By.TAG_NAME, "a").get_attribute('href')

                # Add na lista
                produtos.append(produto)

            except Exception as e:
                print("Falha ao recuperar item: ", e)
                continue

    except Exception as e:
        print("Falha ao retornar itens do servidor: ", e)

    finally:
        driver.quit()

    return (produtos)


if __name__ == "__main__":
    lista_produtos = busca_itens()
    print(lista_produtos)
