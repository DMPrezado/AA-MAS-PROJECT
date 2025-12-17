
import MapImporter.Reader as Reader
import Ambient


'''
    Maps escolhido aqui -> passar para o configuration.py
'''



class Simulator:
    
    def __init__(self):
        
        # --------------------------
        # Init do ambiente a partir do ficheiro de mapas
        # --------------------------
        ## o mapa é generico aqui. o escolhido depende dos modos no configuration.py
        elementsList, gridDimensions =  Reader.read_map("Maps/foraging_map.txt")
        self.ambient = Ambient(elementsList, gridDimensions)
        
        # --------------------------
        # cria 1 agente
        # --------------------------
        
        
        
        
        # --------------------------
        # Treina o agente
        # --------------------------
        
    
        # --------------------------
        # Testa o agente (com ambientes diferentes?) (muitos testes + render a cada passo)
        # --------------------------
        
        
        # --------------------------
        # Plot dos resultados da aprendizagem e dos testes.
        # --------------------------
        
        