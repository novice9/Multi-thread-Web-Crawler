import urllib.request
import urllib.error

class OpenRedirectHandler(urllib.request.HTTPRedirectHandler):
    def http_error_301(self, req, fp, code, msg, hdrs):
        response = super(OpenRedirectHandler, self).http_error_301(req, fp, code, msg, hdrs)
        print(req.get_full_url(), 'is permanently moved to', response.geturl())
        response.status = code
        return response
    
    def http_error_302(self, req, fp, code, msg, hdrs):
        response = super(OpenRedirectHandler, self).http_error_302(req, fp, code, msg, hdrs)
        print(req.get_full_url(), 'is temporarily moved to', response.geturl())
        response.status = code
        return response

def open_url(url, data = None, timeout = 5):
    """ open a URL with our redirection handler"""
    opener = urllib.request.build_opener(OpenRedirectHandler)
    try:
        response = opener.open(url, data, timeout)
        print('    Open URL', url, 'successfully')
    except urllib.error.HTTPError as err:
        print('    HTTP error code:', err.code)
        return None
    except urllib.error.URLError as err:
        print('    URL', url, 'is invalid:', err.reason)
        return None
    else:
        return response
    
    
    
    
if __name__ == '__main__':
    print('This is a full url')
    open_url('https://en.wikipedia.org/wiki/Main_Page')
    
    print('This is a redirect url')
    open_url('https://en.wikipedia.org')
    
    print('This is a wrong url')
    open_url('https://en.wrongwiki.org')