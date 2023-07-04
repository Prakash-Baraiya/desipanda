import bs4

def convert_html_to_txt(html_file):
    with open(html_file, "r") as f:
        html = f.read()

    soup = bs4.BeautifulSoup(html, "html.parser")

    links = []
    for link in soup.findAll("a"):
        name = link["name"]
        href = link["href"]
        links.append((name, href))

    with open("links.txt", "w") as f:
        for name, href in links:
            f.write(f"{name}: {href}\n")

if __name__ == "__main__":
    html_file = "my_html_file.html"
    convert_html_to_txt(html_file)

