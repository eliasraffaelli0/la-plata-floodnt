from app.models.zone import Zone
from app.models.zone_coordinate import ZoneCoordinate


class ZoneValidator:
    def __init__(self, zone):
        self.errors = {}
        self.zone = zone

    def validate_username(self):
        zone_is_registered = Zone.query.filter(Zone.name == self.zone.name).first()
        if zone_is_registered:
            self.zone = zone_is_registered
            # actualizar
            self.__update_zone()
        # crear

    def __update_zone(self):
        coordinates = ZoneCoordinate.query.filter(
            ZoneCoordinate.id == self.zone.id
        ).all()
