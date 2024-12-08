from flask import Flask, render_template, Response
import requests
import os
import subprocess
from bs4 import BeautifulSoup
import threading
import base64
import shutil
import re

app = Flask(__name__)

# começa o ngrok. É necessário criar uma chave rsa no Termux e passar para o ngrok no seguinte link: https://dashboard.ngrok.com/ssh-keys
# ajuste a porta no localhost:5000
def ngrok():
    subprocess.Popen(["ngrok", "http", "5000"])

# roda o app
def run():
    app.run()

# ajuda
@app.route('/h')
def ajuda():
    ajuda = r"""
    Funções:<br><br>
    /math/path:expression retorna o resultado da expressão;<br>
    /scrape/<path:url> retorna url;<br>
    /upload/<path:file> faz upload de arquivo local em hex;<br>
    /ls lista arquivos locais;<br>
    /tamanho/<path:link> retorna o tamanho do arquivo do link fornecido;<br>
    /download/<path:link> baixa o arquivo e retorna o hex dele;<br>
    /download_p/<path:start>/<path:end>/<path:link> baixa parte do arquivo e retorna o hex dele;<br>
    /script_juntar retorna script para juntar arquivos.<br><br>
    """
    return ajuda

# calculadora
@app.route('/math/<path:expression>')
def math(expression):
    print(expression)
    resultado = f"Resultado: {eval(expression)}"
    return resultado

# script para juntar arquivos. Testar
@app.route('/script_juntar')
def juntar():
    juntar = r"""
        código:
        with open(r"preencher com o caminho do arquivo txt", "r") as f:
            hex = f.read()
            f.close()
        bin = bytes.fromhex(hex)
        with open(r"preencher com o caminho do arquivo de saída", "wb") as f:
            f.write(bin)
            f.close()
            
        cmd: 
        certutil -decodehex test.txt output.pdf 
    """
    return juntar

# Rota para scrape. Tentar usar curl no futuro
@app.route('/scrape/<path:url>')
def scrape_page(url):
    url = "https://" + url
    try:
        html = requests.get(url)
        soup = BeautifulSoup(html.text, 'html.parser')
        return str(soup)
    except Exception as e:
        return e

# faz upload
@app.route('/upload/<path:file>')
def upload(file):
    with open(file, "rb") as f:
        bin = f.read()
        bas64 = base64.b64encode(bin)
        f.close()
    return bas64

# show video located in static
@app.route('/video/<path:url>')
def video(url):
    video_path = url
    return render_template("index2.html", video_path=video_path)

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
    conteudo = base64.b64encode(conteudo)
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
    conteudo = base64.b64encode(conteudo)
    return conteudo

#função utilizada no download de torrents
def dt(magnet):
    processo = subprocess.Popen(
        ["aria2c", "-d", "temp", "--stream-piece-selector=inorder", "--min-split-size=1M", magnet],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    for line in processo.stdout:
        print(line, end='')  # The `end=''` prevents adding extra newlines
        if "FILE:" in line and "[METADATA]" not in line:
            path = str(line).strip("FILE: ")
            path = re.sub(r'(\.mp4).*', r'\1', path)
        if "SEED(0.0)" in line:
            processo.kill()
    shutil.make_archive("temp", 'zip', os.getcwd(), "temp")
    chunk = 1024 * 1024
    data = b''
    with open("temp.zip", "rb") as f:
        while True:
            chunk_data = f.read(chunk)
            if not chunk_data:
                break
            data += chunk_data
            print(chunk_data)
            conteudo = base64.b64encode(chunk_data)
            yield conteudo
#baixa torrent - passar magnet
@app.route('/donwload_torrent/<path:magnet>')
def download_torrent(magnet):
    return Response(dt(magnet),mimetype='text/plain')

if __name__ == '__main__':
    # múltiplas threads
    thread1 = threading.Thread(target=ngrok)
    thread1.start()
    thread2 = threading.Thread(target=run)
    thread2.start()
    thread1.join()
    thread2.join()
