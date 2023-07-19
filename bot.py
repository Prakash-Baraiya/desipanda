from bs4 import BeautifulSoup

# HTML content stored as a string
html_content = """
<!DOCTYPE html>
<html>
<head>
    <title>Example Page</title>
</head>
<body>
    <a href="https://www.example.com">Example Link 1</a>
    <a href="https://www.example.org">Example Link 2</a>
    <!-- Add more HTML content if needed -->
</body>
</html>
"""

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

# Save the extracted data in a text file (optional for local testing)
with open("output.txt", "w") as file:
    file.write(result)

# Print the extracted data to the console
print(result)
