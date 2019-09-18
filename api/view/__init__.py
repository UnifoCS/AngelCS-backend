from functools import wraps

from flask import jsonify



def json_api(func):
    """
    Route 함수의 리턴값이 dict, list일 경우 json으로 바꾸어줍니다.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        result_type = type(result)

        if result_type is dict:
            result = jsonify(result)

        if result_type is list or result_type is tuple:
            # return list, code 형태
            if len(result) > 1 and type(result[1]) is int:
                code = result[1]
                result = jsonify(result[0])
                result.status_code = code

            # return list 인 형태
            else:
                result = jsonify(result)

        return result

    wrapper.__name__ = func.__name__
    return wrapper
