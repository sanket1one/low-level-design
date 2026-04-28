"""
Let's you create complex object step by step


An object has many optional fields, and most callers only need a subset.

# Before

req = HttpRequest(
    url,                 # url
    method,              # method
    headers,             # headers
    None,                # body
    None,                # query_params
    30000                # timeout_ms
)


# After

req = (HttpRequest.Builder(url)
       .method("POST")
       .add_header("key", "val")
       .build())
"""



class HttpRequest:
    def __init__(self, builder):
        self.url = builder._url
        self.method = builder._method
        self.headers = dict(builder._headers)  # defensive copy
        self.query_params = dict(builder._query_params)
        self.body = builder._body
        self.timeout = builder._timeout

    def __str__(self):
        return (f"HttpRequest(url='{self.url}', method='{self.method}', "
                f"headers={self.headers}, query_params={self.query_params}, "
                f"body='{self.body}', timeout={self.timeout})")
    
    class Builder:
        def __init__(self, url):
            self._url = url  # required
            self._method = "GET"
            self._headers = {}
            self._query_params = {}
            self._body = None
            self._timeout = 30000
        
        def method(self, method):
            self._method = method
            return self

        def add_header(self, key, value):
            self._headers[key] = value
            return self
        
        def add_query_param(self, key, value):
            self._query_params[key] = value
            return self
        
        def body(self, body):
            self._body = body
            return self

        def timeout(self, timeout):
            self._timeout = timeout
            return self

        def build(self):
            return HttpRequest(self)


# Email Builder

class Email:
    def __init__(self, builder):
        self.to = builder._to
        self.subject = builder._subject
        self.cc = list(builder._cc)
        self.bcc = list(builder._bcc)
        self.body = builder._body
        self.priority = builder._priority
        self.attachments = list(builder._attachments)
    
    class Builder:
        def __init__(self, to, subject):
            self._to = to
            self._subject = subject
            self._cc = []
            self._bcc = []
            self._body = None
            self._priority = "normal"
            self._attachments = []
        
        def cc(self, cc):
            self._cc.append(cc)
            return self

        def bcc(self, bcc):
            self._bcc.append(bcc)
            return self

        def body(self, body):
            self._body = body
            return self

        def priority(self, priority):
            self._priority = priority
            return self

        def attachment(self, attachment):
            self._attachments.append(attachment)
            return self

        def build(self):
            return Email(self)

email1 = Email.Builder("alice@example.com", "Meeting Tomorrow") \
        .body("Let's meet at 10am in conference room B.") \
        .build()

        