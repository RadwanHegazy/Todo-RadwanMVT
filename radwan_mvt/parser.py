from jinja2 import Environment, FileSystemLoader
import os

def jinja_parser(html_file_path, context) : 
    env = Environment(loader=FileSystemLoader(os.environ.get("CURRENT_PATH")))
    template = env.get_template(html_file_path)
    output = template.render(context)
    return output


class RequestParser:
    """
        map http request to an object attrs
    """
    method:str
    path:str
    hostname:str
    schema:str
    data:dict={}

    def __init__(self, str_request:str) -> None:
        # print(str_request)
        split_lines = str_request.split('\n')
        # set request attrs
        first_line = split_lines[0].split(' ')
        self.method = first_line[0]
        self.path = first_line[1]
        self.schema = first_line[2]
        self.hostname = str_request.split('\n')[1].split(' ')[-1]

        # parse data from GET method
        if self.method == 'GET' : 
            if '?' in self.path :
                spliited_path = self.path.split('?')
                self.path = spliited_path[0]
                for i in spliited_path[1].split('&') :
                    splitted_param = i.split('=')
                    for j in splitted_param :
                        self.data[splitted_param[0]] = splitted_param[1]
            return
        
        # parse data from POST method
        # NOTE: not completed yet
        if self.method == "POST" : 
            posted_data = str_request.split('\n')[-1].split('&')
            for i in posted_data:
                splitted_param = i.split('=')
                for j in splitted_param:
                    self.data[splitted_param[0]] = splitted_param[1]
            return