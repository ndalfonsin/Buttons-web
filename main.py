import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin

def get_links_and_content(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        links = soup.find_all(['a', 'button'])

        all_links = []
        for link in links:
            link_info = {}
            if 'href' in link.attrs:
                href = link.get('href')
                if href.startswith('http'):
                    link_info['url'] = href
                else:
                    base_url = urlparse(url)
                    link_info['url'] = urljoin(base_url.geturl(), href)

                if link.text.strip():
                    link_info['content'] = link.text.strip()
                else:
                    link_info['content'] = 'IMG'

                all_links.append(link_info)

        return all_links
    except requests.RequestException as e:
        print("Error:", e)
        return []

def check_links(links, file):
    for link_info in links:
        if 'url' not in link_info:
            file.write(f"ALERT: Botón sin redirección: {link_info['content']}\n")
        else:
            file.write(f"Enlace válido - Botón: {link_info['content']}, URL: {link_info['url']}\n")

def save_links_to_file(filename, data):
    with open(filename, "a") as file:
        file.write(data)

base_url = input("Ingresa la URL base para escanear: ")
domain = urlparse(base_url).netloc  # Obtener el dominio de la URL base
txt_file = input("Ingresa el nombre del archivo TXT: ")

links_and_content = get_links_and_content(base_url)
with open(txt_file, "a") as file:
    file.write(f"Resultados para el dominio: {domain}\n")
    check_links(links_and_content, file)

print("¡Proceso completo! Verifica el archivo para los resultados.")
