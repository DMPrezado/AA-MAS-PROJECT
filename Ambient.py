

from Agent import Agent
from Entities import LightHouse


class Ambient:
    def __init__(self, elements_list, gridDimensions):
        self.gridDimensions = gridDimensions
        self.elements_list = elements_list
        self.occupied_positions = self.set_occupied_positions()
        self.agent = self.set_agent()
        self.lighthouse = self.set_lighthouse()
#        self.nests = self.set_nests()
        
        
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
        raise RuntimeError("Agent not found")
    
    def set_lighthouse(self):
        for element in self.elements_list:
            if isinstance(element, LightHouse):
                return element
        raise RuntimeError("LightHouse not found")




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
            class LimitObj:
                type = "Limit"
                def getType(self): return "Limit"
            return LimitObj()

        for element in self.elements_list:
            if element.coord.equals(coord):
                return element

        return None
