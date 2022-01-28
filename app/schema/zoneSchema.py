from marshmallow import Schema, fields


class ZoneCoordinateSchema(Schema):
    latitude = fields.String()
    longitude = fields.String()


class ZoneSchema(Schema):
    name = fields.String()
    color = fields.String()
    zone_code = fields.String()
    state = fields.Int()

    coordinates = fields.Nested(ZoneCoordinateSchema, many=True)


class ZonePaginationSchema(Schema):
    page = fields.Int()
    per_page = fields.Int()
    pages = fields.Int()
    total = fields.Int()
    items = fields.Nested(ZoneSchema, many=True, data_key="zonas")


zone_schema = EvacuationRouteSchema(many=True)
zone_schema = EvacuationRouteSchema()
zone_pagination_schema = EvacuationRoutePaginationSchema()
