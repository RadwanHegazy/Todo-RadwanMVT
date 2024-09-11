from radwan_mvt.core import Server
import os
from urls import URLS

# write up some important env variables
os.environ.setdefault('CURRENT_PATH',os.getcwd())
os.environ.setdefault('SERVER', __name__)

# NOTE: it must named with server
server = Server(
    URLS=URLS # connect URLS conf with server
)

# run server
if __name__ == "__main__" :
    server.run()