class HeartbeatPackage:
    """Package holding a heartbeat emitted from one moment of time."""

    def __init__(self, json):

        self.AlphaId = json.get('alpha-id')
        self.AlgorithmId = json.get('algorithm-id')
        self.MachineTime = json.get('machine-time')

    def __repr__(self):
        return f'AlphaId: {self.AlphaId[0:5]}   AlgorithmId: {self.AlgorithmId[0:7]}   Heartbeat: {self.MachineTime}'