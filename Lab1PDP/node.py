class Node:
    def __init__(self, value, pos,parent):
        self.__value = value
        self.__position = pos
        self.__parent=parent


    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        self.__value = value

    @property
    def position(self):
        return self.__position

    @position.setter
    def position(self, value):
        self.__position=value

    @property
    def parent(self):
        return self.__parent

    @parent.setter
    def parent(self, value):
        self.__parent=value