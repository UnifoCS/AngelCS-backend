# Code Structure
| 기능 | 기능 |
|---|---|
| Web Framework | Flask |
| Database  | SQLAlchemy |
| Async Messaging | Celery |

AngelCS API는 원하는 Celery Broker, Database Server를 연결해서 사용가능합니다.

## 기본 구조
기본적인 MVC 구조로 되어있습니다.
- View: api/view 패키지
- Model: api/model 패키지
- Controller: api/service 패키지
- 기타 보조 기능: api/util 패키지
- 설정 파일: configs 패키지

## Service 만들기
아래 조건을 만족해야 합니다.
1. api.service의 BaseService 클래스를 상속받기
2. 이름을 Service로 끝나게 짓기
3. 이름을 Base로 시작하지 않게 짓기
4. 클래스는 api.service 패키지 안의 모듈에 선언
5. app을 받는 생성자, 별도구현 안해도 됨.

그러면 웹 서비스가 로드될 시 자동으로 app의 services에 추가됩니다. 클래스 명은 snake_case로 바뀌어서 생성됩니다.

예) DashboardService
```python
# api/service/dashboard_service.py

class DashboardService(BaseDatabaseService):

    def get_review_count(self):
        return self.query(func.count(Review.id)).scalar()
    
    ...
```

자동으로 생성된 Service는 아래처럼 접근해서 사용이 가능합니다.

```python
import api.globals as g

count = g.app.services.dashboard.get_review_count()
```

## View 만들기
웹 요청을 받고 처리하는 View를 구현하는 방법에 대해 서술합니다. 우선 api/view 패키지 안에 모듈을 만들고 bp라는 이름의 전역 Blueprint 객체를 만듭니다.

```python

bp = Blueprint(__name__, __name__)


@bp.route("/dashboard")
@json_api
def get_dashboard():
    dashboard = g.app.services.dashboard
    to_date = datetime.today() + timedelta(days=1)
    from_date = to_date - timedelta(days=5)

```

## SQLAlchemy 모델 만들기
api/model/sqlalchemy.py 에 SQLAlchemy Mapping Class들이 구현되어있습니다. 이를 이용해서 데이터베이스에 접근합니다.
<br>

### SQLAlchemy 구현 참고
[SQLAlchemy - The Database Toolkit for Python](https://www.sqlalchemy.org/)
