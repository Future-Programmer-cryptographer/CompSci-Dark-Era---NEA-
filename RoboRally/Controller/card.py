from PIL import Image, ImageTk 

# this is for dragging and dropping cards into register slots 
class Card: 
    def __init__(self, canvas, imagePath, x, y, width, height):
        self.canvas = canvas

        # added these two for later 
        self.width = width 
        self.height = height 

        self.imagePath = imagePath
        self.image = Image.open(imagePath)
        self.imagePath= self.image.resize((width, height))
        self.photo = ImageTk.PhotoImage(self.imagePath) # this was self.image before, which was not resized 

        # use create_image to render images (not rectangle)
        # create image only needs x and y 
        self.imageId = self.canvas.create_rectangle(x,y, x+width, y+height, fill='red')  
        # self.imageId = self.canvas.create_image(x,y, image=self.photo)

        self.canvas.tag_bind(self.imageId, '<ButtonPress-1>', self.startDrag)
        self.canvas.tag_bind(self.imageId, '<B1-Motion>', self.continueDrag)
        self.canvas.tag_bind(self.imageId, '<ButtonRelease-1>', self.endDrag)

        # no register at the start 
        self.register = None
    
    def text(self):
        pass 
        # random text on cards 

    def getInformation(self):
        pass 

# can I have a card class that has the controller and view logic but can it also incorporate some model logic like card data. 
    
    def startDrag(self, event):
        self.start_x = event.x 
        self.start_y = event.y  

    def continueDrag(self, event):
        dx = event.x - self.start_x 
        dy = event.y - self.start_y 
        self.canvas.move(self.imageId, dx, dy)
        self.start_x = event.x 
        self.start_y = event.y  

    def endDrag(self, event):
        # iterate over all registers and calculate distance between card current pos and the centre of each reg 
        closestRegister = self.findClosestRegister(event.x, event.y)
        if closestRegister: 
            self.snapToRegister(closestRegister)
        else: 
            self.register = None 

    def findClosestRegister(self, x, y):
        # pythag it 
        closestRegister = None  
        closestDistance = float('inf')
        snapDistance = 100 

        for register in self.canvas.registers: 
            distance = ((x - (register.x + register.width / 2)) ** 2 + (y-(register.y + register.height/2)) ** 2 ) ** 0.5
            if distance < closestDistance and distance < snapDistance: 
                closestDistance = distance
                closestRegister = register 
        
        return closestRegister

    def snapToRegister(self, register):
        self.canvas.coords(self.imageId, register.x, register.y, register.x + register.width, register.y + register.height)
        self.register = register  