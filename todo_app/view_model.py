from todo_app.data.mongo_db_items import Item

class ViewModel:  
    def __init__(self, retrieve_todo: list[Item], retrieve_doing: list[Item], retrieve_done: list[Item]):
        combined_lists = retrieve_todo + retrieve_doing + retrieve_done
        self._items = combined_lists
 
    @property
    def retrieve_todo(self) -> list[Item]:
        # results = [each_item for each_item in self._items if each_item.status == "To Do"]
        results: list[Item] = []   
        for each_item in self._items:
            if each_item.status == "To Do":
                results.append(each_item)
        return results
    
    @property
    def retrieve_doing(self) -> list[Item]:
        results: list[Item] = []   
        for each_item in self._items:
            if each_item.status == "Doing":
                results.append(each_item)
        return results
    
    @property
    def retrieve_done(self) -> list[Item]:
        results: list[Item] = []   
        for each_item in self._items:
            if each_item.status == "Done":
                results.append(each_item)
        return results
