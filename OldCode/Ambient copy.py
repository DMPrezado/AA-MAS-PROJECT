# Ambient.py

import Coord
from LightHouse import LightHouse
from Obstacle import Obstacle
import tkinter as tk

class Ambient:
    def __init__(self, grid_size, lighthouse=None, obstacles=None, agents=None):
        self.grid_size = grid_size  # (width, height)
        self.lighthouse = lighthouse
        self.obstacles = obstacles if obstacles is not None else []
        self.agents = agents if agents is not None else []

        # posições ocupadas
        self.occupiedPositions = set()
        self._rebuild_occupied()



    # --------------------------
    # GETTERS
    # --------------------------
    def getLightHouse(self):
        return self.lighthouse

    def getAgentsList(self):
        return self.agents





    # --------------------------
    # POSIÇÕES LIVRES
    # --------------------------
    def freePositions(self):
        free_positions = []
        width, height = self.grid_size

        for x in range(width):
            for y in range(height):
                if (x, y) not in self.occupiedPositions:
                    free_positions.append(Coord.Coord(x, y))
        return free_positions




    # --------------------------
    # UTIL: coord -> tuple
    # --------------------------
    def _coord_to_tuple(self, coord):
        if isinstance(coord, Coord.Coord):
            return coord.getX(), coord.getY()
        elif isinstance(coord, tuple):
            return coord
        else:
            raise TypeError("coord deve ser Coord ou (x,y)")




    # --------------------------
    # OBJETO NUMA POSIÇÃO
    # --------------------------
    def getObject(self, coord):
        x, y = self._coord_to_tuple(coord)
        width, height = self.grid_size

        # fora da grelha
        if x < 0 or y < 0 or x >= width or y >= height:
            class LimitObj:
                type = "Limit"
                def getType(self): return "Limit"
            return LimitObj()

        # farol
        if self.lighthouse is not None and self.lighthouse.getCoord().as_tuple() == (x, y):
            return self.lighthouse

        # agentes
        for a in self.agents:
            if a.getCoord().as_tuple() == (x, y):
                return a

        # obstáculos
        for o in self.obstacles:
            if o.getCoord().as_tuple() == (x, y):
                return o

        return None




