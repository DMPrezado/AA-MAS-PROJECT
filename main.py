import MapImporter.Reader as Reader
from Ambient import Ambient
import TUIRender


def main():
    elementsList, gridDimensions =  Reader.read_map("maps\initial_positions1.txt")
    ambient = Ambient(elementsList, gridDimensions)
    TUIRender.render(ambient)
    



if __name__ == "__main__":
    main()




    