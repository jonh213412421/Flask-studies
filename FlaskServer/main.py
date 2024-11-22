from flask import Flask
from selenium.webdriver.chrome.options import Options
import requests
from bs4 import BeautifulSoup
from pyngrok import ngrok
import os

app = Flask(__name__)

ngroks = None

@app.route('/get-ngrok-address')
def start_ngrok_route():
    global ngroks
    if not ngroks:
        ngroks = ngrok.connect("5000")
        tunnels = ngroks.public_url
        return str(tunnels)
    else:
        tunnels = ngroks.public_url
        return str(tunnels)

# Rota para scrape
# exemplo: /scrape/www.exemplo.com
@app.route('/scrape/<path:url>')
def scrape_page(url):
    from selenium import webdriver
    url = "https://" + url
    options = Options()
    options.add_argument("--headless")
    webdriver = webdriver.Chrome(options=options)
    try:
        # GET a URL
        webdriver.get(url)
        soup = BeautifulSoup(webdriver.page_source, 'html.parser')
        return str(soup)
    except Exception as e:
        return f"Erro: {e}"

# faz upload
@app.route('/upload/<path:file>')
def upload(file):
    with open(file, "rb") as f:
        bin = f.read()
        hex = bin.hex()
        f.close()
    return hex

# lista dir
@app.route('/ls/<path:dir>')
def ls(dir):
    arquivos = ""
    if dir == "main":
        dir = "C:/"
        files = os.listdir(dir)
        for file in files:
            arquivos = arquivos + file + "<br>"
        arquivos = "Files: <br><br>" + arquivos
        return arquivos
    else:
        files = os.listdir(dir)
        for file in files:
            arquivos = arquivos + file + "<br>"
        arquivos = "Files: <br><br>" + arquivos
        return arquivos

#pega tamanho de arquivos
@app.route('/tamanho/<path:link>')
def tamanho(link):
    tamanho = requests.head(link).headers.get('Content-Length')
    tamanho = str(tamanho) + " bytes"
    return tamanho

#baixa arquivos e envia o hex
@app.route('/download/<path:link>')
def download(link):
    nome = str(link).split("/")[-1]
    print(nome)
    conteudo = requests.get(link).content
    with open(nome, "wb") as f:
        f.write(conteudo)
        f.close()
    conteudo = conteudo.hex()
    return conteudo

#baixa porção de arquivo e envia hex
@app.route('/download_p/<path:start>/<path:end>/<path:link>')
def dowload_p(link, start, end):
    nome = str(link).split("/")[-1]
    headers = {
        'Range': f'bytes={start}-{end}'
    }
    conteudo = requests.get(link, headers=headers).content
    with open(f"{nome}-{start}-{end}", "wb") as f:
        f.write(conteudo)
        f.close()
    conteudo = conteudo.hex()
    return conteudo

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
