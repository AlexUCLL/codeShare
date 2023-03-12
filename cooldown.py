class Cooldown:
    
    def __init__(self, cooldown) -> None:
        self.ready=False
        self.cd=cooldown
        self.ogcd=cooldown

    def update(self, elapsed_seconds):
        self.cd-=elapsed_seconds
        if self.cd<=0:
            self.ready=True

    def reset(self):
        self.ready=False
        self.cd=self.ogcd