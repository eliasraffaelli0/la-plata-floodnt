from marshmallow import Schema, fields


class EvacuationRouteCoordinateSchema(Schema):
    latitude = fields.String()
    longitude = fields.String()


class EvacuationRouteSchema(Schema):
    name = fields.String()
    description = fields.String()
    state = fields.Int()

    coordinates = fields.Nested(EvacuationRouteCoordinateSchema, many=True)


class EvacuationRoutePaginationSchema(Schema):
    page = fields.Int()
    per_page = fields.Int()
    pages = fields.Int()
    total = fields.Int()
    items = fields.Nested(EvacuationRouteSchema, many=True, data_key="recorridos")


evacuation_routes_schema = EvacuationRouteSchema(many=True)
evacuation_route_schema = EvacuationRouteSchema()
evacuation_routes_pagination_schema = EvacuationRoutePaginationSchema()
