import decimal, datetime
import json
import traceback

from flask.json import JSONEncoder
from sqlalchemy.ext.declarative import DeclarativeMeta

from ..model.sqlalchemy import BaseModel


def sqlalchemy_encoder(obj):
    """JSON encoder function for SQLAlchemy special classes."""
    if isinstance(obj, datetime.date):
        return obj.isoformat()
    elif isinstance(obj, decimal.Decimal):
        return float(obj)
    elif isinstance(obj, BaseModel):
        return

class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        t = type(obj)

        try:
            if isinstance(t, datetime.datetime):
                return obj.isoformat()
            elif isinstance(t, decimal.Decimal):
                return float(obj)
            elif isinstance(t, DeclarativeMeta):
                # an SQLAlchemy class
                fields = {}
                keys = [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']
                for k in keys:
                    data = getattr(obj, k)
                    dt = type(data)

                    if dt in (int, float, str, dict, list):
                        fields[k] = data
                    elif dt is datetime.datetime:
                        fields[k] = data.isoformat()
                    elif data is None:
                        fields[k] = None
                    else: # Unknown Type
                        fields[k] = str(dt)
                    # dt = type(data)
                    # try:
                    #     if isinstance(dt, datetime.datetime):
                    #         fields[field] = data.isoformat()
                    #     elif isinstance(dt, decimal.Decimal):
                    #         fields[field] = float(data)
                    #     else:
                    #         fields[field] = json.dumps(data, default=CustomJSONEncoder) # this will fail on non-encodable values, like other classes
                    # except TypeError:
                    #     fields[field] = "Unknown"
                    #     traceback.print_exc()
                # a json-encodable dict
                return fields
            
            iterable = iter(obj)
        except TypeError:
            traceback.print_exc()
            pass
        else:
            return list(iterable)

        return JSONEncoder.default(self, obj)