from abc import ABC, abstractmethod


class Pynance(ABC):
    
    '''
    Define todas las interacciones entre la API de Binance y nosotros
    '''
    
    def __init__(self):
        pass
    
    @abstractmethod
    def wallet(self):
        pass


class Spot(Pynance):

    '''
    Coleccion de funciones que se lanzan sobre cuentas en Spot
    '''
