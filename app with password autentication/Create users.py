def create_user():
    with open("users.txt", "a") as f:
        user = input("usuário: ")
        password = input("password: ")
        f.write("\n")
        f.write(f"{user}:{password}")
        f.close()

if __name__ == '__main__':
    while True:
        create_user()
