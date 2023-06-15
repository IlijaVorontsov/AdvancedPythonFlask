

class PlayerResource:
    def __init__(self, wood:int=0, bricks:int=0, wool:int=0, grain:int=0, ore:int=0) -> None:
        self.wood = wood # attribute
        self.bricks = bricks
        self.wool = wool
        self.grain = grain
        self.ore = ore

    @property # attribute
    def total_resources(self) -> int:
        return self.wood + self.bricks + self.wool + self.grain + self.ore
    
    def probability(self, resource) -> float: # method
        return getattr(self, resource) / self.total_resources
    

ilijaRes = PlayerResource(wood=2, bricks=1, wool=1, grain=1, ore=1)
print(ilijaRes.probability('total_resources'))
print(ilijaRes.total_resources)