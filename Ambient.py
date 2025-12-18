

from Agent import Agent
from Entities import LightHouse, Nest


class Ambient:
    def __init__(self, elements_list, gridDimensions):
        self.gridDimensions = gridDimensions
        self.elements_list = elements_list
        self.occupied_positions = self.set_occupied_positions()
        self.agent = self.set_agent()
        self.lighthouse = self.set_lighthouse()
        self.nest = self.set_nest()
        

        
        
    # ----------------------
    # SETTERS
    # ----------------------    

    def set_occupied_positions(self):
        positions = set()
        for element in self.elements_list:
            positions.add(element.coord)

    def set_agent(self):
        for element in self.elements_list:
            if isinstance(element, Agent):
                return element
        return None
    
    def set_lighthouse(self):
        for element in self.elements_list:
            if isinstance(element, LightHouse):
                return element

    def set_nest(self):
        for element in self.elements_list:
            if isinstance(element, Nest):
                return element
        


    # ----------------------
    # GETTERS
    # ----------------------   

    def get_occupied_positions(self):
        return self.occupied_positions
    
    def get_agent(self):
        return self.agent
    
    def get_lighthouse(self):
        return self.lighthouse
    
    
    

    # ----------------------
    # GetObject
    # ----------------------   
    
    def getObject(self, coord):
        width, height = self.gridDimensions

        # fora da grelha
        if coord.x < 0 or coord.y < 0 or coord.x > width or coord.y > height:
            return "Limit"

        for element in self.elements_list:
            if element.coord.equals(coord):
                return element

        return None
