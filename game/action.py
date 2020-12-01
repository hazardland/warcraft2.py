class Action:
    def __init__(
            self,
            unit,
            params,
            speed=None,
            time=None,
            delay=None,
            pause=None):

        self.unit = unit
        self.delay = delay
        self.speed = speed
        self.time = time
        self.arrived = False
        self.finished = False
        self.pause = pause
        self.starts = {}
        self.steps = {}
        self.targets = {}
        for key, value in params.items():
            self.starts[key] = self.unit.__dict__[key]
            if isinstance(value, tuple):
                if self.speed is not None:
                    sign = -1 if value[0] < 0 else 1
                    self.steps[key] = self.speed
                else:
                    self.steps[key] = value[0]/self.time
                self.targets[key] = self.unit.__dict__[key]+value[0]
            else:
                if isinstance(value, (int, float)):
                    if self.speed is not None:
                        sign = -1 if (value-self.unit.__dict__[key]) < 0 else 1
                        self.steps[key] = self.speed * sign
                    else:
                        self.steps[key] = (value-self.unit.__dict__[key])/self.time
                self.targets[key] = value

        #print(self.starts)
        #print(self.steps)
        #print(self.targets)

    def update(self, delta):

        if not self.finished and self.delay is not None and self.delay > 0:
            self.delay -= delta
            return True

        if not self.finished:
            if self.steps:
                self.arrived = True
                for key, value in self.steps.items():
                    if self.speed is not None:
                        new = self.unit.__dict__[key] + delta/value
                    else:
                        new = self.unit.__dict__[key] + value*delta

                    if value < 0:
                        if new < self.targets[key]:
                            continue
                    else:
                        if new > self.targets[key]:
                            continue

                    #print(key, new)
                    self.arrived = False
                    self.unit.__dict__[key] = new


        if self.time is not None and self.time > 0:
            self.time -= delta

        if not self.finished and ((self.time is not None and self.time <= 0) or self.arrived):
            self.finished = True
            #print(self.arrived)
            #print(self.time)
            for key, value in self.targets.items():
                self.unit.__dict__[key] = value
            #print('finished', (self.pause is not None))
            return self.pause is not None


        if self.finished and self.pause is not None and self.pause > 0:
            self.pause -= delta
            if self.pause <= 0:
                return False


        return True
