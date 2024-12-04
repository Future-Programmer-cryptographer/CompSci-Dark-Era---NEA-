
from Controller.mainMenuController import MainMenuController 
from View.mainMenuView import MainMenuView

def main():     
    controller = MainMenuController(None) 
    view = MainMenuView(controller) 
    # view is set in the controller 
    controller.view = view 

    view.mainloop() 

main() 
