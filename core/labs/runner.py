from core.labs.lab1 import Lab1


class Runner():
    
    def __init__(self, namespace):
        self.namespace = namespace
    
    def run(self):
        if self.namespace.labs == "lab1":
            lab1 = Lab1(self.namespace.input, self.namespace.output)
            lab1.gen_report(self.namespace.name)
            lab1.run()
    