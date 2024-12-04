class Register: 
    def __init__(self, canvas, x, y, width, height):
        self.canvas = canvas 
        self.x = x 
        self.y = y 
        self.width = width 
        self.height = height 
        self.id = self.canvas.create_rectangle(x, y, x + width, y + height, fill='white')
        self.canvas.registers.append(self)