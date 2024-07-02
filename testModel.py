from model.model import Model

myModel = Model()

myModel.creaGrafo()

nNodi, nArchi = myModel.getInfoGraph()

print(f"Grafo creato con {nNodi} nodi e {nArchi} archi")