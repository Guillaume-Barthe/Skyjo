class Card():

    def __init__(self,value):
        self.hidden = True
        self.value = value
    def __repr__(self):
        if self.hidden:
            texte = "hidden"
        else:
            texte = "visible"

        return "This card is "+texte+" and has value "+str(self.value)
