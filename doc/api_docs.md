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
	"type": "review_count", 
	"item": {
		"review_total_count": 10000,
		"review_replied_count": 1000,
	}
},
{
	"type": "review_average",
	"item": {
		"review_average_score": 3.5, # 리뷰 평균
		"review_average_history": [ # 리뷰 내역
			{ "date": "yyyy-MM-dd", "score": 3.5  },
		{ "date": "yyyy-MM-dd", "score": 3.4  },
		{ "date": "yyyy-MM-dd", "score": 3.3  },
		{ "date": "yyyy-MM-dd", "score": 3.2  },
		{ "date": "yyyy-MM-dd", "score": 3.1  }
		]
	}
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
	"score": 5, # 점수(int)
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
	"score": 5, # 점수(int)
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
	"message": "ㅁㄴㅇㄹ"
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
	"id": 123, # (int) 템플릿 ID
	"name": "악플러용", # 제목
	"content": "안녕하세요 [name]님. ...", # 내용
	"conditions": [ # 템플릿이 적용되기 위한 조건
		{ "type": "tag", "tag_id": 1234 }, 
		{ "type": "score", "operator": ">=", "operand": 3 } 
	]
},
... # 이하 동일 포멧
]
```