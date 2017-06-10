import OpenURL
import ParseHTML
import time
import threading
import collections

def wiki_crawler(cv, url_queue, url_visit, counter, filename, thread_id):
    # clean up the file
    f = open(filename, 'w')
    f.write(thread_id + ': Start crawling\n')
    f.close()
    
    index = 0
    for i in range(counter):
        # Consumer
        with cv:
            while (len(url_queue) == 0):
                # wait other threads to fill the queue for 10 sec
                print(thread_id, 'is currently idle and waiting for other threads to fill up the queue')
                time_out = (cv.wait(10) == False)
                
                if (time_out):
                    # turn off current thread upon time out
                    print('No url to work on,', thread_id, 'is sleeping')
                    return
                
                print(thread_id, 'is awakened from idle')
            
            this_url = url_queue[0]
            url_queue.popleft()
            print(thread_id, ': Get a url from queue to work on')
            
            if this_url in url_visit:
                print(this_url, 'is already been crawled')
                continue
    
            url_visit.add(this_url)
            print(thread_id, ': Update pool with visited URL')
        
        
        # Web Crawling
        response = OpenURL.open_url(this_url)
        
        # URL is invalid or encounter protocol error
        if response == None:
            continue
        
        # URL is redirect to other URL
        if (response.status in [301, 302]):
            print(this_url, 'is redirected to', response.geturl())
            with cv:
                if (response.geturl() in url_visit):
                    print('And', response.geturl(), 'has already been crawled')
                    continue
                
                url_visit.add(response.geturl())
        
        new_urls = ParseHTML.parse_html(response.read(), filename, format(index, '05d'))
        index += 1
        
        # Producer
        with cv:
            for url in new_urls:
                if url in url_visit:
                    continue
                url_queue.append(url)
            print(thread_id, ': Inject all URLs into queue')
            print('Totally', len(url_queue), 'URLs are in queue\n')
            cv.notify_all()
            
        # add delay between HTTP request
        time.sleep(2)

        

if __name__ == '__main__':
    locker = threading.Lock()
    cv = threading.Condition(locker)
    ready = True
    
    url_queue = collections.deque(['https://en.wikipedia.org/wiki/Main_Page'])
    url_queue.append('https://en.wikipedia.org')
    url_visit = set()
    
    worker1 = threading.Thread(target=wiki_crawler, name='thread-1', args=(cv, url_queue, url_visit, 100, 'thread-1.txt', 'thread-1'))
    worker1.start()
    
    worker2 = threading.Thread(target=wiki_crawler, name='thread-2', args=(cv, url_queue, url_visit, 100, 'thread-2.txt', 'thread-2'))
    worker2.start()
    
    worker3 = threading.Thread(target=wiki_crawler, name='thread-3', args=(cv, url_queue, url_visit, 100, 'thread-3.txt', 'thread-3'))
    worker3.start()
    
    worker1.join()
    worker2.join()
    worker3.join()
    
    print('All threads complete!')
