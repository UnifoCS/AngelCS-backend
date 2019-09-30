from .sqlalchemy_service import BaseDatabaseService
from ..model.sqlalchemy import Template, Tag, TemplateCondition


class TemplateService(BaseDatabaseService):


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
