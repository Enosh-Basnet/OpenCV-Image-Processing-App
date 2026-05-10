from alterations.alteration import Alteration


class ObjectAdded(Alteration):
    def __init__(self, region):
        super().__init__(region, "Object Added")