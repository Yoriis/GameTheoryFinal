class ExtensiveFormNode:
    def __init__(self, player=None, actions=None, children=None, payoffs=None, info_set=None):
        self.player = player
        self.actions = actions or []
        self.children = children or {}
        self.payoffs = payoffs
        self.info_set = info_set
    
    def is_terminal(self):
        return self.payoffs is not None