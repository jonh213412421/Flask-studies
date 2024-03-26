from Flask_app import app_run
import ip_changer

if __name__ == '__main__':
    port = input("Qual porta deseja utilizar? ")
    address = ip_changer.ipv6_get()
    print(f"endereço de ip: {address}")
    app_run(address, port)

