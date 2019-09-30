# Backend API Document(Demo)

Created: Sep 16, 2019 8:38 PM<br>
Created By: 희규 김<br>
Last Edited By: 희규 김<br>
Last Edited Time: Sep 17, 2019 4:44 PM<br>

# 대시보드

## 대시보드 아이템 목록 가져오기

### 요청
```bash
GET /dashboard
```
### 응답

- 성공 200
```json
[
  {
    "item": {
      "review_replied_count": 200,
      "review_total_count": 6178
    },
    "type": "review_count"
  },
  {
    "item": {
      "review_average_history": [
        {
          "date": "2019-09-26",
          "rating": 3.0
        },
        {
          "date": "2019-09-27",
          "rating": 3.2
        },
        {
          "date": "2019-09-28",
          "rating": 3.4
        },
        {
          "date": "2019-09-29",
          "rating": 3.6
        },
        {
          "date": "2019-09-30",
          "rating": 3.8
        }
      ],
      "review_average_score": 3.5
    },
    "type": "review_average"
  }
]
```
# 리뷰

## 리뷰 목록 가져오기

### 요청
```bash
GET /reviews/{page}?page_size={int}&sort={enum}&order={enum}&filter={enum}
```
### Parameters

- page (Integer): 1부터 시작, 기본값 1
- page_size(Integer): 기본값 30
- sort(Enum): 정렬, 아래 값 중 하나
    - updated_date (Default)
    - created_date
    - rating
- order(Enum): 정렬 차순, 아래 값 중 하나
    - desc (Default): 내림차순
    - asc: 오름차순
- filter(Optional)
    - replied: 답글 달린 것만
    - unreplied: 답글 안달린 것만
    - 값 없음 (기본): 필터링 안함.

### 결과

- 200 success
```json
Content-Type: application/json

[
{
	"id": 123, # Review ID(int)
	"author": "", # 리뷰 작성자 이름(string)
	"rating": 5, # 점수(int)
	"updated_at": "yyyy-MM-dd", # (date, yyyy-MM-dd) 리뷰 변경일(변경하지 않았을 경우 created_at과 동일한 값)
	"created_at": "yyyy-MM-dd", # (date, yyyy-MM-dd) 리뷰 작성일
	"is_replied": false, # (boolean) 이미 답변이 달렸는가
	"tags": [ # 태그 목록, 없으면 빈 목록
		{ "id": 1234, "name": "긍정" },
		{ "id": 1234, "name": "질문" }
	]
},
... # 이하 동일 포멧
]
```

- 400 Bad Request

## 리뷰 정보 가져오기

### 요청
```bash
GET /review/{id}
```
Parameter

- id (string): 자세히 가져올 리뷰의 ID

### 응답

- 성공 200
```json
{
	"id": 123, # 리뷰 ID(int)
	"author": "", # 리뷰 작성자 이름(string)
	"content": "리뷰 내용", # 리뷰 내용(string)
	"rating": 5, # 점수(int)
	"updated_at": "yyyy-MM-dd", # (date, yyyy-MM-dd) 리뷰 변경일(변경하지 않았을 경우 created_at과 동일한 값)
	"created_at": "yyyy-MM-dd", # (date, yyyy-MM-dd) 리뷰 작성일
	"is_replied": false, # (boolean) 이미 답변이 달렸는가
	"reply_text": null, # (string, nullable) 이미 답변이 달렸으면 
	"tags": [ # 태그 목록, 없으면 빈 목록
		{ "id": 1234, "name": "긍정" }, # 태그ID, 태그이름
		{ "id": 1235, "name": "질문" }
	],
	"recommended_templates" : [ # 이 리뷰에 자동으로 추천된 답글 템플릿
		{
			"id": 123, # (int) 템플릿 ID
			"name": "악플러용", # 제목
			"content": "안녕하세요 [name]님. ...", # 내용
			"conditions": [ # 템플릿이 적용되기 위한 조건
				{ "type": "tag", "tag_id": 1234 }, 
				{ "type": "score", "operator": "<=", "operand": 3 } 
			]
		},
		... # 동일한 형식의 값들 이어짐
	]
}
```
## 리뷰에 답글 달기

### 요청
```json
POST /review/{id}/reply
Content-Type: application/json

# Body
{
	"content": "안녕하세요 ..." # 답글 텍스트
}
```
### 응답

- 성공 200

No Result

- 실패 400
```json
{
	"message": "ㅁㄴㅇㄹ",
	"error_code": 123,
	"error_name": "NO_REQUIRED_FIELD"
}
```
# 템플릿

## 템플릿 목록 가져오기

### 요청
```json
    GET /templates
```

### 응답
```json
# 템플릿 목록입니다.

[
  {
    "conditions": [
      {
        "id": 1,
        "index": 0,
        "operand1": "tag",
        "operand2": "1",
        "operator": "="
      }
    ],
    "content": "Thank you [name], We will keep doing our best :)",
    "created_date": "2019-09-26T12:48:13.932368",
    "id": 1,
    "name": "감사 리뷰 템플릿",
    "updated_date": "2019-09-26T12:48:13.932489"
  },
  {
    "conditions": [
      {
        "id": 2,
        "index": 0,
        "operand1": "tag",
        "operand2": "2",
        "operator": "="
      }
    ],
    "content": "Sorry [name], We will try more for better service.",
    "created_date": "2019-09-26T12:48:13.932368",
    "id": 2,
    "name": "사과 리뷰 템플릿",
    "updated_date": "2019-09-26T12:48:13.932489"
  }
]
```