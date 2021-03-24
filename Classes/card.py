### This is the implementation of the card class. ###


class Card():
    '''
    A Card object contains two attribute, self.hidden describe the state of the card,
    whether it has been discovered by the player or not. The value is the actual value
    of the card.

    the repr method enables the print(card) command and tells the user the values
    of each attribute of the card
     '''

    def __init__(self,value):
        self.hidden = True
        self.value = value

    def __repr__(self):
        if self.hidden:
            texte = "hidden"
        else:
            texte = "visible"

        return "This card is "+texte+" and has value "+str(self.value)
