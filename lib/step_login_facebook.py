

class Step(object):
    def __init__(self):
        self.status = None # None: init, True: success, False: fail

    def run(self) -> tuple:
        raise NotImplementedError


class StepList(list):
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)

    def next_step(self):
        step: Step = self.pop()
        result = step.run()



