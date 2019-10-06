from .sqlalchemy_service import BaseDatabaseService
from ..model.sqlalchemy import Template, Tag, TemplateCondition


class TemplateService(BaseDatabaseService):
    """
        리뷰 템플릿과 관련된 기능을 수행하는 클래스
        - 템플릿 생성, 삭제, 수정
        - 템플릿 가져오기
    """ 

    def get_all_templates(self):
        templates = self.query(Template).all()
        return templates


    def get_template_by_tags(self, tags):
        if not tags:
            return None
        
        t = tags[0]
        conds = self.query(TemplateCondition) \
            .filter_by(
                operand1="tag",
                operator="=",
                operand2=t.id
                ) \
            .all()
        templates = [x.template for x in conds]
        return templates
