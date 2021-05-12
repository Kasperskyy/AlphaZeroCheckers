import ResNetCheckers
import main

myNetwork = ResNetCheckers.Network()
main.selfplay(25, myNetwork.getModel())

