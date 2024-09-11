import os
from .parser import jinja_parser
CURRENT_PATH = os.environ.get('CURRENT_PATH')

class BaseHttp:
    STATUS = {
        200 : '200 OK',
        201 : "201 CREATED",
        400 : "400 BAD REQUEST",
        404 : '404 NOT FOUND',
        500 : "500 SERVER ERROR",
        301 : "Move Permanently"
    }
    def __init__(self,schema=None, content_type=None, GET=None, POST=None, content=None,hostname=None,method=None,path=None) -> None:
        self.schema = schema
        self.GET = {}
        self.POST = {}
        self.content_type = content_type
        self.hostname = hostname
        self.method = method
        self.path = path
        self.content = content


    def __repr__(self) -> str: ...

class Request (BaseHttp) : 
    """
        Build the http request 
    """
    def build(self, request):
        print('this is request : ', request)

    def __repr__(self) -> str:
        return f"\tRequest(hostname={self.hostname},method={self.method}, path={self.path})"
    
class Response (BaseHttp) : 
    """
        Build the http response 
    """

    def __init__(self,request:Request, template_name:str, context:dict={},status_code:int=200,schema='HTTP/1.1', content_type='text/html', content=None, hostname=None, method=None, path=None) -> None:
        self.request = request
        self.template_name = template_name
        self.context = context
        self.status_code = status_code

    def __bytes__(self) : 
        template_path = os.environ.get('TEMPLATE_FOLDER')
        html_file = open(os.path.join(template_path, self.template_name),'r')
        html_file = jinja_parser(
            html_file_path=os.path.join('templates/', self.template_name),
            context=self.context
        )
        text = f"""{self.request.schema} {self.STATUS[self.status_code]}\nContent-Type: text/html\n\n{html_file}"""
        return bytes(text.encode())

class _404Response (Response) : 
    """
        Rendering custom 404 page
    """
    def __init__(self, request: Request, template_name: str='404.html', context: dict = {}, status_code: int = 404, schema='HTTP/1.1', content_type='text/html', content=None, hostname=None, method=None, path=None) -> None:
        super().__init__(request, template_name, context, status_code, schema, content_type, content, hostname, method, path)

class StaticResponse (Response): 
    """
      Serve static files : css, js and image[png and jpeg]
    """
    EXTENSIONS = {
        'css' : 'text/css',
        'png' : 'images/png',
        'jpeg' : 'images/jpeg',
        'ico' : 'images/ico',
        'js' : 'text/javascript'
    }
    def __init__(self, request: Request, extension:str,template_name: str=None, context: dict = {}, status_code: int = 200, schema='HTTP/1.1', content_type=None, content=None, hostname=None, method=None, path=None) -> None:
        self.request = request
        self.content_type = self.EXTENSIONS[extension]
        super().__init__(request, template_name, context, status_code, schema, content_type, content, hostname, method, path)
        self.is_404 = False
        try : 
            static_path = os.path.join(os.environ.get('CURRENT_PATH'), os.environ.get('STATIC_FOLDER') + self.request.path)
            
            self.static_file = open(static_path,'rb')
            self.text = f"""HTTP/1.1 200\nContent-Disposition: inline\nContent-Type: {self.content_type}\n\n"""
        except FileNotFoundError:
            self.is_404 = True
            self.status_code = 404

    def __bytes__(self) : 
        if not self.is_404 :
            return bytes(self.text.encode()) + self.static_file.read()
        return bytes(_404Response(self.request))