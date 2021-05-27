def write(filename: str, text: str):
    with open(filename, "a") as file_object:
        file_object.write(text)
        file_object.write("\n")
