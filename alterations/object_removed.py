from alterations.alteration import Alteration


class ObjectRemoved(Alteration):
    def __init__(self, region):
        super().__init__(region, "Object Removed")