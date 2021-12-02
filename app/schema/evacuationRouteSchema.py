from marshmallow import Schema, fields

from app.models.evacuationRoute import EvacuationRoute


# class EvacuationRouteCoordinateSchema(Schema):
#     id = fields.Int()
#     latitude = fields.Str()
#     longitude = fields.Str()


class EvacuationRouteSchema(Schema):
    id = fields.Int()
    name = fields.Str()
    description = fields.Str()
    state = fields.Int()
    # coordinates = fields.Nested(
    #     EvacuationRouteCoordinateSchema, many=True, data_key="coordenadas"
    # )


class EvacuationRoutePaginationSchema(Schema):
    page = fields.Int()
    per_page = fields.Int()
    total = fields.Int()
    items = fields.Nested(EvacuationRouteSchema, many=True, data_key="Points")


evacuation_routes_schema = EvacuationRouteSchema(many=True)
evacuation_route_schema = EvacuationRouteSchema()
evacuation_routes_pagination_schema = EvacuationRoutePaginationSchema()
