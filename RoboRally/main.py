
from controller import MainMenuController 
from model import MainMenuModel
from view import MainMenuView

def main():     
    model = MainMenuModel() 
    controller = MainMenuController(model, None) 
    view = MainMenuView(controller) 
    # view is set in the controller 
    controller.view = view 

    view.mainloop() 

main() 
