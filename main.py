import httpx
from bs4 import BeautifulSoup
import asyncio

async def fetch_product_info(url):
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36'

    }

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        # Verifica se a resposta contém um captcha
        if "captcha" in response.text.lower():
            print("Captcha detectado, tente novamente mais tarde ou ajuste os headers.")
            return None  # Encerra a função retornando None para indicar que um captcha foi encontrado


        soup = BeautifulSoup(response.content, 'html.parser')

        # Descrição do produto
        title_element = soup.find('span', id='productTitle')
        title = title_element.get_text(strip=True) if title_element else None

        # Preço e desconto à vista
        price_savings_element = soup.find('span', {'class': 'aok-offscreen'})
        price_savings = price_savings_element.get_text(strip=True) if price_savings_element else None

        # Preço atual
        current_price_element = soup.select_one('.a-section.a-spacing-micro .a-offscreen')
        current_price = current_price_element.get_text(strip=True) if current_price_element else None

        # Preço antigo
        old_price_element = soup.select_one('.a-section.a-spacing-small.aok-align-center .a-offscreen')
        old_price = old_price_element.get_text(strip=True) if old_price_element else None

        # Detalhes - Extração de um contêiner específico
        expander_element = soup.find('div', class_='a-row a-expander-container a-expander-inline-container')
        details = expander_element.get_text(strip=True) if expander_element else 'Detalhes não encontrados'
   
        # Avaliações - extração diretamente de elementos com a classe 'a-icon-alt'
        reviews_elements = soup.select('span.a-icon-alt')
        reviews = reviews_elements[0].get_text(strip=True) if reviews_elements else None

        # URL da foto
        img_wrapper = soup.find('div', class_='imgTagWrapper')
        img_element = img_wrapper.find('img') if img_wrapper else None
        img_url = img_element['src'] if img_element and 'src' in img_element.attrs else None


        return {
            'description': title,
            'price_savings': price_savings,
            'current_price': current_price,
            'old_price': old_price,
            'details': details,
            'reviews': reviews,
            'img_url': img_url,
        }

async def main():
    # Substitua pela URL da página do produto
    url = "https://www.amazon.com.br/dp/B0BXMCSW9C"
    product_info = await fetch_product_info(url)
    print(product_info)

if __name__ == "__main__":
    asyncio.run(main())
