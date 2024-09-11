import socket , time, importlib, os
from datetime import datetime
from .request import Request, _404Response, StaticResponse, Response
from .parser import RequestParser

SERVER_SOCKET = socket.socket(
    family=socket.AF_INET,
    type=socket.SOCK_STREAM
)

SERVER_SOCKET.setsockopt( 
    socket.SOL_SOCKET,
    socket.SO_REUSEADDR,
    1
)

SERVER_SOCKET.setblocking(1)

ACCEPTED_STATIC_EXTENSIONS = [
    'css',
    'js',
    'png',
    'jpeg',
    'jpg',
    'ico',
    'icon',
]

class WsgiServer :

    def __init__(self, host, port) -> None:
        self.host = host
        self.port = port

        self.text = f"""
[ + ] MVT-Backend Framework Running at [ {datetime.now().strftime('%d/%m/%Y, %H:%M ')} ]
[ + ] Server Running with no issues.
[ * ] Server Running at : http://{host}:{port}/\n
    """
        
        SERVER_SOCKET.bind((host, port))
        SERVER_SOCKET.listen()
        print(self.text)

        self.serve()

        
    def serve (self) : 
        while True : 
            try : 
                # listen for any client connection and accept it
                client, addr = SERVER_SOCKET.accept()
                user_info = f"{addr[0]}:{addr[1]}"

                # recive the incoming data in request
                text_request = client.recv(1500).decode('utf-8')
        
                # parse the request 
                parsed_data = RequestParser(text_request)

                # build http request
                request = Request(
                    method=parsed_data.method,
                    hostname=parsed_data.hostname,
                    path=parsed_data.path,
                    schema=parsed_data.schema,
                )
                setattr(request, parsed_data.method, parsed_data.data)


                # build http response
                response = self.make_response(request)
                print(f' [ {datetime.now().strftime('%d/%m/%Y, %H:%M:%S ')} ] {user_info} {parsed_data.method} {parsed_data.path} => {response.STATUS[response.status_code]}')

                client.sendall(bytes(response))
                client.close()

            except KeyboardInterrupt:
                print('\n[ ! ]server has been terminated')
                time.sleep(0.5)
                break
    
    def make_response (self, request:Request):
        extension = str(request.path).split('.')[-1]
        if extension in ACCEPTED_STATIC_EXTENSIONS : 
            response = StaticResponse(request, extension)
        else:
            server = importlib.import_module(os.environ.get('SERVER'))
            URLS = server.server.URLS
            if len(URLS.keys()) == 0 :
                response = Response(request,'hello.html',context={
                    'host' : server.server.get_host()
                })
            else:
                try : 
                    response = URLS[request.path](request)
                except KeyError : 
                    response = _404Response(request)
        return response
    