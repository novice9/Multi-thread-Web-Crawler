import OpenURL
import ParseHTML
import time
import threading
import collections

def wiki_crawler(locker, url_queue, url_visit, counter, filename, thread_id):
    # clean up the file
    f = open(filename, 'w')
    f.write(thread_id + ': Start crawling\n')
    f.close()
    
    index = 0
    for i in range(counter):
        
        timeout = 5
        while len(url_queue) == 0:
            # wait for other thread to fill up the queue
            time.sleep(5)
            timeout -= 1
            if timeout == 0:
                break
        else:
            # wait for locker
            locker.acquire()
            this_url = url_queue[0]
            url_queue.popleft()
            print(thread_id, ': Get a url from queue to work on')
            locker.release()
    
            if this_url in url_visit:
                continue
    
            locker.acquire()
            url_visit.add(this_url)
            print(thread_id, ': Update pool with visited URL')
            locker.release()
    
            response = OpenURL.open_url(this_url)
            # URL is invalid or encounter protocal error
            if response == None:
                continue
    
            # URL is redirect to other URL
            if response.status in ['301', '302'] and response.geturl() in url_visit:
                continue
    
            new_urls = ParseHTML.parse_html(response.read(), filename, format(index, '05d'))
            index += 1
    
            locker.acquire()
            for url in new_urls:
                if url in url_visit:
                    continue
                url_queue.append(url)
            print(thread_id, ': Inject all URLs into queue')
            print('Totally', len(url_queue), 'URLs are in queue\n')
            locker.release()
        
            # add delay between HTTP request
            time.sleep(2)

        
 

if __name__ == '__main__':
    locker = threading.Lock()
    
    url_queue = collections.deque(['https://en.wikipedia.org/wiki/Main_Page'])
    url_visit = set()
    
    worker1 = threading.Thread(target=wiki_crawler, name='thread-1', args=(locker, url_queue, url_visit, 8, 'thread-1.txt', 'thread-1'))
    worker1.start()
    
    worker2 = threading.Thread(target=wiki_crawler, name='thread-2', args=(locker, url_queue, url_visit, 8, 'thread-2.txt', 'thread-2'))
    worker2.start()
    
    worker3 = threading.Thread(target=wiki_crawler, name='thread-3', args=(locker, url_queue, url_visit, 8, 'thread-3.txt', 'thread-3'))
    worker3.start()
     
    worker1.join()
    worker2.join()
    worker3.join()

