from bs4 import BeautifulSoup as bs

HTML_CONTENT = """
        <div class="bg-gray-200 p-2 rounded shadow">
          <img
            alt="Photo 1"
            class="w-full h-auto object-cover rounded"
            src="https://via.placeholder.com/400"
        />
        <p></p>
        </div>
"""

def add_html(html_file, image, text):
    with open(html_file, "r", encoding="utf-8") as file:
        html_file_soup = bs(file, "html.parser")

    posts_div = html_file_soup.find("div", id="posts")
    if posts_div:
        html_content = bs(HTML_CONTENT, "html.parser")
        html_content = configure_content(html_content, image, text)
        posts_div.insert(0, html_content)
    else:
        raise ValueError("Error: No element with id 'posts' found.")

    with open(html_file, "w", encoding="utf-8") as file:
        file.write(str(html_file_soup))

def configure_content(html_content, image, text):
    first_p = html_content.find("p")
    if first_p:
        first_p.insert(0,text)
    first_img = html_content.find("img")
    if  first_img:
        first_img["src"] = image
    return html_content

add_html("index.html", "assets\Screenshot 2025-01-08 151917.png", "hello world")
add_html("index.html", "assets\Screenshot 2025-02-02 091324.png", "test2")
add_html("index.html", "assets\Screenshot 2025-04-05 114845.png", "Woah another post")