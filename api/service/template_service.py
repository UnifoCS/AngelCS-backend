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

    def recommendate_templates(self, review):
        templates = self.get_all_templates()
        candidates = []

        review_tag_ids = [str(t.id) for t in review.tags]
        has_tag = len(review_tag_ids) > 0

        for t in templates:
            score = 0
            ok = 0

            for tc in t.conditions:
                result = False

                if has_tag and tc.operator == "in" and tc.operand1 == 'tag':
                    tag_ids = tc.operand2.split(",")
                    havings = sum([x in review_tag_ids for x in tag_ids])
                    result = havings > 0

                elif tc.operator == "in" and tc.operand1 == 'keyword':
                    keywords = tc.operand2.split(",")
                    havings = sum([k in review.content for k in keywords])
                    result = havings > 0

                elif tc.operand1 == "rating":

                    if tc.operator == "=":
                        result = review.rating == int(tc.operand2)
                    elif tc.operator == ">":
                        result = review.rating > int(tc.operand2)
                    elif tc.operator == ">=":
                        result = review.rating >= int(tc.operand2)
                    elif tc.operator == "<":
                        result = review.rating < int(tc.operand2)
                    elif tc.operator == "<=":
                        result = review.rating <= int(tc.operand2)
                    
                if result:
                    score = score + 1
                    ok = ok + 1
        
            # template conditions 을 모두 만족해야함. ok 로 카운팅
            # score는 점수
            if score > 0 and ok == len(t.conditions):
                candidates.append((t, ok))
            
        candidates = reversed(sorted(candidates, key=lambda x: x[1]))
        candidates = list(candidates)
        
        # print(candidates)

        return [c[0] for c in candidates]

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

    def add_template(self, template):
        template_model = Template(channel_id=0)
        template_model.name = template['title']
        template_model.content = template['content']

        conds = template['conditions'] 

        if 'rating' in conds:
            rating = conds['rating']
            op = rating[:2] if rating[1] == '=' else rating[0]
            opr1 = 'rating'
            opr2 = rating[2:] if rating[1] == '=' else rating[1:]

            template_model.conditions.append(
                TemplateCondition(
                    operand1=opr1,
                    operand2=opr2,
                    operator=op
                )
            )
        
        if 'tags' in conds:
            op = 'in'
            opr1 = "tag"
            opr2 = ','.join(list(map(lambda x: str(x), conds['tags'])))

            template_model.conditions.append(
                TemplateCondition(
                    operand1=opr1,
                    operand2=opr2,
                    operator=op
                )
            )
        
        if 'keywords' in conds:
            op = 'in'
            opr1 = "keyword"
            opr2 = ','.join(list(map(lambda x: str(x), conds['keywords'])))

            template_model.conditions.append(
                TemplateCondition(
                    operand1=opr1,
                    operand2=opr2,
                    operator=op
                )
            )

        self.db.add(template_model)
        self.db.commit()
        return True
    
    def delete_by_id(self, id):
        c = self.query(Template).filter_by(id=id).delete()
        self.db.commit()
        return c > 0

