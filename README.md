# Multi-thread-Web-Crawler

Crawl wiki pages and extract articles:

- Handler HTTP request with urllib
- Parse hypertext with Beautiful Soup
- Instantiate 3 threads with locker to crawl wiki pages
- thread_?.txt are the sample results

To install Beautiful Soup package(attached):

% tar -xzvf beautifulsoup4-4.5.3.tar.gz

% ./setup.py install

To run: (Need python version 3.6.1)

% python3 WikiCrawler.py
