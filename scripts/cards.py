
class Card:
    
    def __init__(self, tag:str, name:str, description:str, price:int, limit:int):
        self.tag = tag
        self.name = name
        self.description = description
        self.price = price
        self.limit = limit


class Cards:

    TAG_MEGA = 'mega'
    TAG_FUSION = 'fusion'
    TAG_INTERCAMBIO = 'intercambio'
    TAG_PREEVO = 'preevo'
    TAG_COMIENZO = 'comienzo'
    TAG_2_POWERHOUSE = '2_powerhouse'
    TAG_TICKET_TIPO = 'ticket_tipo'
    TAG_ADICIONAL_1 = 'adicional_1'
    TAG_ADICIONAL_2 = 'adicional_2'
    TAG_ADICIONAL_3 = 'adicional_3'
    TAGS_ADICIONAL = [TAG_ADICIONAL_1, TAG_ADICIONAL_2, TAG_ADICIONAL_3]
    TAG_SELECTIVA = 'selectiva'

    @staticmethod
    def get_tag_adicional(rolls:int) -> str:
        return Cards.TAGS_ADICIONAL[rolls-1]

    @staticmethod
    def get_all_cards():
        cards = {}

        tag = Cards.TAG_MEGA
        name = 'ESPABILA, MEGAEVOLUCIONA'
        description = 'REALIZA UNA TIRADA DONDE SÓLO PUEDEN APARECER POKÉMON CON MEGA-EVOLUCIÓN.' 
        price = 6000
        limit = 0
        cards[tag] = Card(tag,name,description,price,limit)

        tag = Cards.TAG_FUSION
        name = 'FUSIÓN ALEATORIA'
        description = 'ELIGE 2 POKÉMON, ELIMINALOS PARA REALIZAR UNA TIRADA ALEATORIA.' 
        price = 400
        limit = 0
        cards[tag] = Card(tag,name,description,price,limit)

        tag = Cards.TAG_INTERCAMBIO
        name = 'INTERCAMBIO PRODIGIOSO'
        description = 'ELIGE 1 POKÉMON DE TUS 20, INTERCAMBIALO POR OTRO AL AZAR.' 
        price = 600
        limit = 0
        cards[tag] = Card(tag,name,description,price,limit)
        
        tag = Cards.TAG_PREEVO
        name = 'LA PRE-EVO ES MEJOR'
        description = 'PUEDES CAMBIAR UNO DE TUS POKÉMON POR SU PRE-EVOLUCIÓN.' 
        price = 1500
        limit = 0
        cards[tag] = Card(tag,name,description,price,limit)
        
        tag = Cards.TAG_COMIENZO
        name = 'NUEVO COMIENZO'
        description = 'ANTES DE GASTAR TU TIRADA Nº18, REINICIA TODAS TUS TIRADAS.' 
        price = 3200
        limit = 1
        cards[tag] = Card(tag,name,description,price,limit)
        
        tag = Cards.TAG_2_POWERHOUSE
        name = '2 ES MEJOR QUE 1'
        description = 'PODRÁS UTILIZAR 2 POKÉMON DE LA CATEGORÍA \"PESOS PESADOS\" EN EL EQUIPO EN LUGAR DE 1.' 
        price = 7000
        limit = 1
        cards[tag] = Card(tag,name,description,price,limit)
        
        tag = Cards.TAG_TICKET_TIPO
        name = 'TIQUET ELEMENTAL'
        description = 'OBTIENES UN TICKET ADICIONAL PARA FORZAR EL TIPO DEL POKÉMON.' 
        price = 400
        limit = 0
        cards[tag] = Card(tag,name,description,price,limit)
        
        tag = Cards.TAG_ADICIONAL_1
        name = 'TIRADA ADICIONAL 1'
        description = 'OBTIENES UNA TIRADA ADICIONAL.' 
        price = 800
        limit = 1
        cards[tag] = Card(tag,name,description,price,limit)
        
        tag = Cards.TAG_ADICIONAL_2
        name = 'TIRADA ADICIONAL 2'
        description = 'OBTIENES DOS TIRADAS ADICIONALES.' 
        price = 1400
        limit = 1
        cards[tag] = Card(tag,name,description,price,limit)
        
        tag = Cards.TAG_ADICIONAL_3
        name = 'TIRADA ADICIONAL 3'
        description = 'OBTIENES TRES TIRADAS ADICIONALES.' 
        price = 2000
        limit = 1
        cards[tag] = Card(tag,name,description,price,limit)
        
        tag = Cards.TAG_SELECTIVA
        name = 'TIRADA SELECTIVA'
        description = 'HAZ UNA TIRADA DE 6 POKÉMON, PUEDES DESECHAR HASTA 5 SIN GASTAR TIRADAS.' 
        price = 3000
        limit = 1
        cards[tag] = Card(tag,name,description,price,limit)

        return cards
