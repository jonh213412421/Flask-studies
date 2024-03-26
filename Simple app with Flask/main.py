from flask import Flask, render_template, request, send_file
import subprocess
from pyhtml2pdf import converter

app = Flask(__name__) # pass name of file as an argument to function

@app.route('/') #root will return "oi"
def index():
    return render_template('index.html')

@app.route('/help')
def help():
    help = "ipconfig: returns server ip" #break line with <br>
    return help

@app.route('/ipconfig')
def ipconfig():
    ip = subprocess.run(['ipconfig'], capture_output=True, universal_newlines=True) #run ipconfig
    ip = ip.stdout
    ip = ip.replace("\n", "<br>")
    return ip

@app.route('/nave')
def nave():
    url = request.args.get('url') #gets url from GET call
    converter.convert(url, "downloaded_site.pdf") #downloads page
    return send_file("downloaded_site.pdf")

if __name__ == '__main__':
    app.run(debug=True) #run app
