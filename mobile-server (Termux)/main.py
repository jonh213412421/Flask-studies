from flask import Flask
import requests
import os
import subprocess
from bs4 import BeautifulSoup
import threading

app = Flask(__name__)

# começa o ngrok. É necessário criar uma chave rsa no Termux e passar para o ngrok no seguinte link: https://dashboard.ngrok.com/ssh-keys
# ajuste a porta no localhost:5000
def ngrok():
    subprocess.Popen(["ssh", "-R", "443:localhost:5000", "v2@connect.ngrok-agent.com", "http"])

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
        def hex_to_binary(hex_value):
        binary_value = bin(int(hex_value, 16))[2:]
        return binary_value.zfill(8)
        
        input_file_path = 'input.txt'
        output_file_path = 'output.txt'
        

        with open(input_file_path, 'r') as input_file:
            hex_values = input_file.readlines()
        
        binary_values = []
        
        for hex_value in hex_values:
            hex_value = hex_value.strip()
            if hex_value:
                binary_value = hex_to_binary(hex_value)
                binary_values.append(binary_value)
        
        with open(output_file_path, 'w') as output_file:
            for binary_value in binary_values:
                output_file.write(binary_value + '\n')
    """
    return juntar

# Rota para scrape. Tentar usar curl no futuro
@app.route('/scrape/<path:url>')
def scrape_page(url):
    url = "https://" + url
    try:
        html = requests.get(url)
        soup = BeautifulSoup(html.text, 'html.parser')
        print(soup)
        return str(soup)
    except Exception as e:
        return e

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
    # múltiplas threads
    thread1 = threading.Thread(target=ngrok)
    thread1.start()
    thread2 = threading.Thread(target=run)
    thread2.start()
    thread1.join()
    thread2.join()
