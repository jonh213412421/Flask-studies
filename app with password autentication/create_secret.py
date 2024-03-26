def create_secret():
    with open("usecret.txt", "w") as f:
        secret = input("qual é o segredo?")
        f.write(secret)
        f.close()
