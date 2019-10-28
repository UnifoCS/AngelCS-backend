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

    def recommendate_template(self, reviews):
        templates = self.get_all_templates()
        recommends = []

        for review in reviews:
            candidates = []

            review_tag_ids = [str(t.id) for t in review.tags]
            ok = 0
            score = 0

            for t in templates:

                for tc in templates.conds:
                    if tc.operator == "tag_in":
                        tag_ids = t.operand2.split(",")
                        score = score + sum([x in review_tag_ids for x in tag_ids])
                        ok = ok + 1

                    elif tc.operator == "keyword_in":
                        keywords = t.operand2.split(",")
                        score = score + sum([k in review.content for k in keywords])
                        ok = ok + 1

                    if tc.operand1 == "rating":
                        score = score + 1
                        result = False 

                        if tc.operator == "=":
                            result = review.rating == int(t.operand2)
                        elif tc.operator == ">":
                            result = review.rating > int(t.operand2)
                        elif tc.operator == ">=":
                            result = review.rating >= int(t.operand2)
                        elif tc.operator == "<":
                            result = review.rating < int(t.operand2)
                        elif tc.operator == "<=":
                            result = review.rating <= int(t.operand2)
                        
                        if result:
                            ok = ok + 1
            
                # template conditions 을 모두 만족해야함. ok 로 카운팅
                # score는 점수
                if score > 0 and ok == len(t.conds):
                    candidates.append((t, score))
                
            candidates = sorted(candidates, lambda x: x[1])
            recommends.append(candidates)

        return recommends

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
