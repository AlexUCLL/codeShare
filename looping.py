

class looping_variable:
    def __init__(self, max_value):
        self.__value= 0
        self.max_value = max_value
        
    @property
    def value(self):
        return self.__value

    
    def increase(self, amount):
        self.__value+=amount
        if self.__value >= self.max_value:
         self.__value = self.__value % self.max_value