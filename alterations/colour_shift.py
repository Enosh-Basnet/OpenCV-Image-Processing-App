from alterations.alteration import Alteration


class ColourShift(Alteration):
    def __init__(self, region):
        super().__init__(region, "Colour Shift")