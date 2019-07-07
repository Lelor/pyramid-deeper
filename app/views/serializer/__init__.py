from marshmallow import Schema, fields


class VideoSchema(Schema):
    title = fields.Str(required=True)
    description = fields.Str(required=True)
    theme = fields.Str(required=True)


class EvaluationSchema(Schema):
    _id = fields.String(required=True)
    positive = fields.Boolean(required=True)
