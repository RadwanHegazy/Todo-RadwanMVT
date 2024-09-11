from radwan_mvt.request import Response, Request
from orm import todo_manager
from datetime import datetime

def index (request:Request) : 


    if request.method == "GET" : 
        is_done = request.GET.get('done', None)
        del_todo = request.GET.get('del', None)
        
        if is_done : 
            todo_manager.update_by_id(id=int(is_done), fields=('is_done', 1))
        
        if del_todo : 
            todo_manager.delete(Todo_id=int(del_todo))
        
        response = Response(request,'todo/index.html')
    
    if request.method == "POST" :
        todo_name = request.POST.get('todo','None')
        data = {
            'text' : str(todo_name).replace('+',' '),
            'is_done' : False,
            'created_at' : datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
        }
        
        todo_manager.insert(**data)

        response = Response(request,'todo/index.html')
    
    context = {
        'todos' : todo_manager.all()
    }
    response.context = context
    return response