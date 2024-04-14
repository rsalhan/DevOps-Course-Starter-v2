# from todo_app.data.trello_items import Item
from todo_app.data.mongo_db_items import Item
from todo_app.view_model import ViewModel

def test_view_model_done_doing_todo_statuses():
    # Arrange: Create an instance of ViewModel containing some example Item objects with various statuses.
    retrieve_todo = [Item("01", "A", "To Do"),Item("02", "B", "To Do"),Item("03", "C", "To Do")]
    retrieve_doing = [Item("04", "D", "Doing"),Item("05", "E", "Doing")]
    retrieve_done = [Item("06", "F", "Done")]

    view_model = ViewModel(retrieve_todo, retrieve_doing, retrieve_done)

    # Act: Get the result of the view model’s new done_items property (though this will actually be an empty list for now).
    done_items = view_model.retrieve_done
    doing_items = view_model.retrieve_doing
    todo_items = view_model.retrieve_todo
    
    # Assert: Write one or more assert statements checking the result of the “Act” step equals what you want.
    assert len(done_items) == 1
    assert done_items[0].status == 'Done'

    assert len(doing_items) == 2
    assert doing_items[0].status == 'Doing'
    assert doing_items[1].status == 'Doing'

    assert len(todo_items) == 3
    for i in range(3):
        assert todo_items[i].status == 'To Do'

