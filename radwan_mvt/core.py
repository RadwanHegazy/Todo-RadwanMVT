from .wsgi import WsgiServer
import os

class Server:

    def __init__(
            self,
            URLS:dict={},
            TEMPLATES_FOLDER_NAME:str='templates',
            STATIC_FOLDER_NAME:str='static',
    ) -> None:
        
        CURRENT_PATH = os.environ.get('CURRENT_PATH')
        
        TEMPLATES_FOLDER_NAME = os.path.join(CURRENT_PATH, TEMPLATES_FOLDER_NAME)
        
        self.URLS = URLS
        os.environ.setdefault('TEMPLATE_FOLDER', TEMPLATES_FOLDER_NAME)
        os.environ.setdefault("STATIC_FOLDER", STATIC_FOLDER_NAME )
        
        

    def run (self, host='localhost', port=8080) : 
        self.host = host
        self.port = port
        WsgiServer(host, port)
        

    def get_host(self) : 
        return f"http://{self.host}:{self.port}"
