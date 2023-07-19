from bs4 import BeautifulSoup

# Open the HTML file
with open("example.html", "r") as file:
    html_content = file.read()

# Create a BeautifulSoup object to parse the HTML content
soup = BeautifulSoup(html_content, "html.parser")

# Find all the anchor tags in the HTML
anchor_tags = soup.find_all("a")

# Iterate through each anchor tag and extract the name and link
result = ""
for tag in anchor_tags:
    name = tag.text.strip()
    link = tag.get("href")
    result += f"{name}:{link}\n"

# Save the extracted data in a text file
with open("output.txt", "w") as file:
    file.write(result)
