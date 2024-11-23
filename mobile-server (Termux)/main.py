from flask import Flask
import requests
import subprocess
import os
from bs4 import BeautifulSoup

app = Flask(__name__)

# Rota para scrape
# exemplo: /scrape/www.exemplo.com
@app.route('/scrape/<path:url>')
def scrape_page(url):
    html = subprocess.run(['curl', url], capture_output=True)
    soup = BeautifulSoup(html.stdout, 'html.parser')
    print(soup)
    return str(soup)

# faz upload
@app.route('/upload/<path:file>')
def upload(file):
    with open(file, "rb") as f:
        bin = f.read()
        hex = bin.hex()
        f.close()
    return hex

# lista dir
@app.route('/ls')
def ls():
    arquivos = "Arquivos locais:<br><br>"
    files = os.listdir()
    for arquivo in files:
        arquivos = arquivos + arquivo + "<br>"
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
    app.run(debug=True)
