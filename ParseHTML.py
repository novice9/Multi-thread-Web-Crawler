import bs4
import re

def write_text(soup, filename, index):
    """ extract plain text and write into file """
    topic = soup.h1
    content = soup.find(id='mw-content-text')
    
    articles = topic.get_text(' ', strip = True) + '\n'
    
    hdrs = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']
    paragraphs = content.find_all(hdrs + ['p'], recursive = False)
    
    for paragraph in paragraphs:
        if paragraph.name == 'p':
            words = paragraph.get_text(' ', strip = True)
            if words == '':
                continue
            articles += (words + '\n')
        else:
            title = [string for string in paragraph.strings]
            if title[0] == 'References':
                break
            articles += ('\n' + title[0] + '\n')
    
    f = open(filename, 'ab')
    header = 'WebPage index: ' + index + '\n'
    f.write(header.encode('utf-8', 'ignore'))
    f.write(articles.encode('utf-8', 'ignore'))
    f.close()

def wiki_links(soup, index):
    """ extract wiki links """
    links = []
    for a_tag in soup.find_all('a'):
        link = str(a_tag.get('href'))
        if re.fullmatch('/wiki/[^:]+', link):
            full_url = 'https://en.wikipedia.org' + link
            if full_url not in links:
                links.append(full_url)
    
    print('WebPage index: ' + index) 
    return links       

def parse_html(body, filename, index):
    """parse the webpage body: write text into file, and return wiki links"""
    soup = bs4.BeautifulSoup(body, 'html.parser')    
    write_text(soup, filename, index)
    return wiki_links(soup, index)
 
 
 
    
if __name__ == '__main__':
    import OpenURL
    response = OpenURL.open_url('https://en.wikipedia.org/wiki/Temperatures_Rising')
    if response != None:
        parse_html(response.read(), 'wiki-articles.txt', '000')
    
    
    
