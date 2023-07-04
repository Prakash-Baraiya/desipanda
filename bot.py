import re

def convert_txt_to_name_link(txt_file):
    with open(txt_file, "r") as f:
        txt = f.read()

    links = re.findall(r"(.*)\s+(.*)", txt)

    with open("links.txt", "w") as f:
        for name, href in links:
            f.write(f"{name}: {href}\n")

if __name__ == "__main__":
    txt_file = "my_txt_file.txt"
    convert_txt_to_name_link(txt_file)

