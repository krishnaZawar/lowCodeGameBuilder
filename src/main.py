from lexer.lexer import Lexer
def main() -> None:
    with open("testFile.txt", "r") as file:
        file_contents = file.read()

if __name__ == '__main__':
    main()