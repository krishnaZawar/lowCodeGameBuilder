from interpreter.interpreter import Interpreter
def main() -> None:
    with open("templates/sample3.txt", "r") as file:
        file_contents = file.read()

    try:
        interpreter = Interpreter()
        interpreter.interpret(file_contents)
    except Exception as e:
        print(f"{str(e)}")

if __name__ == '__main__':
    main()