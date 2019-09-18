

class BaseEntity(dict):
    
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)


class Review (BaseEntity):
    id = 0
    
    author = None
    content = None
    score = 0
    
    created_at = None
    updated_at = None
    
    is_replied = False
    
    tags = []


class Tag (BaseEntity):
    id = 0
    name = None # string


class Template (BaseEntity):
    id = 0
    name = ""
    content = ""

    conditions = []


class TemplateCondition (BaseEntity):
    type_id = None

    # 자세한 구현 우선 생략