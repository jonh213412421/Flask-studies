import time
import qbittorrentapi
import urllib.parse
from flask import Flask, render_template, Response
import requests
import os
import subprocess
from pyngrok import ngrok
from bs4 import BeautifulSoup
import threading
import base64
import shutil

app = Flask(__name__)
http_tunnel = ngrok.connect(5000)
print(f"url:{http_tunnel.public_url}")

# roda o app
def run():
    app.run()


# ajuda
@app.route('/h')
def ajuda():
    ajuda = r"""
    Funções:<br><br>
    /math/path:expression retorna o resultado da expressão;<br>
    /nav/<path:url> retorna url;<br>
    /upload/<path:file> faz upload de arquivo local em hex;<br>
    /ls lista arquivos locais;<br>
    /tamanho/<path:link> retorna o tamanho do arquivo do link fornecido;<br>
    /download/<path:link> baixa o arquivo e retorna o hex dele;<br>
    /download_p/<path:start>/<path:end>/<path:link> baixa parte do arquivo e retorna o hex dele;<br>
    /download_torrent/<path:magnet> baixa torrent;<br>
    /video_stream/<path:magnet> baixa filme da url fornecida e mostra na página;<br>
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
        certutil -decodehex test.txt output.pdf se hex
        certutil -decode test.txt output.pdf se bs64
    """
    return juntar


# Rota para scrape. Tentar usar curl no futuro
@app.route('/nav/<path:url>')
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


# pega tamanho de arquivos
@app.route('/tamanho/<path:link>')
def tamanho(link):
    tamanho = requests.head(link).headers.get('Content-Length')
    tamanho = str(tamanho) + " bytes"
    return tamanho


# baixa arquivos e envia o hex
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


# baixa porção de arquivo e envia hex
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


# função utilizada no download de torrents
def dt(magnet):
    magnet = "magnet:?" + magnet
    processo = subprocess.Popen(
        ["aria2c", "-d", "temp", "--stream-piece-selector=inorder", "--min-split-size=1M", magnet],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    for line in processo.stdout:
        yield line
        if "SEED(0.0)" in line:
            processo.kill()
    shutil.make_archive("temp", 'zip', os.getcwd(), "temp")
    chunk = 1024 * 1024
    data = b''
    yield "\n\n"
    yield "DATA:\n\n"
    with open("temp.zip", "rb") as f:
        while True:
            chunk_data = f.read(chunk)
            if not chunk_data:
                break
            data += chunk_data
            print(chunk_data)
            conteudo = base64.b64encode(chunk_data)
            yield conteudo


# baixa torrent - passar magnet
@app.route('/donwload_torrent/<path:magnet>')
def download_torrent(magnet):
    return Response(dt(magnet), mimetype='text/plain')

@app.route('/video_stream/<path:magnet>')
def video_dw(magnet):
    magnet = "magnet:?xt=" + magnet
    conn_info = dict(
        host="localhost",
        port=8080,
        username="admin",
        password="123321",
    )
    qbt_client = qbittorrentapi.Client(**conn_info)

    try:
        qbt_client.auth_log_in()
    except qbittorrentapi.LoginFailed as e:
        print(e)

    qbt_client.torrents.add(magnet, is_sequential_download=True, download_path=os.path.join(os.getcwd(), "static"), save_path=os.path.join(os.getcwd(), "static"))
    a = qbt_client.torrents.info()
    for b in a:
        c = urllib.parse.parse_qs(urllib.parse.urlparse(b['magnet_uri']).query).get('dn', [None])[0]
        d = urllib.parse.parse_qs(urllib.parse.urlparse(magnet).query).get('dn', [None])[0]
        if c == d:
            path = b['content_path']
            print(path)
            files = os.listdir(path)
            for file in files:
                if file.endswith(".mp4") or file.endswith(".avi"):
                    video = os.path.basename(path) + "/" + file
                    print(video)
            #https://en.yts-official.mx/movies
            return render_template('index2.html', video_path=video)

def tor_status():
    conn_info = dict(
        host="localhost",
        port=8080,
        username="admin",
        password="123321",
    )

    qbt_client = qbittorrentapi.Client(**conn_info)
    a = qbt_client.torrents.info()
    while True:
        for tor in a:
            yield f"data: {tor['name']} - {tor['progress']*100:.2f}%\n\n"
            time.sleep(5)

@app.route('/torrent_status')
def torrent_progress():
    return Response(tor_status(), content_type='text/event-stream')

if __name__ == '__main__':
    # múltiplas threads
    thread = threading.Thread(target=run)
    thread.start()
    thread.join()
    
