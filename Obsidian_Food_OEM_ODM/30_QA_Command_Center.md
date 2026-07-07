---
aliases:
  - Obsidian Q&A 허브
tags:
  - qa
  - command_center
  - obsidian
---

# Obsidian 명령어 Q&A 허브

이 노트는 식품 OEM/ODM 아이디어 vault에서 바로 질문하고, 관련 근거 노트를 빠르게 여는 작업 허브다.

## 자주 쓰는 Obsidian 명령어

`Ctrl+P`를 누른 뒤 아래 명령어 이름을 검색한다.

| 목적 | 명령어 | 쓸 때 |
|---|---|---|
| 전체 노트 검색 | Search: Search in all files | 키워드로 근거 찾기 |
| 빠른 파일 이동 | Quick switcher: Open quick switcher | 노트명으로 바로 이동 |
| 그래프 보기 | Graph view: Open graph view | 전체 연결 구조 확인 |
| 현재 노트 연결 보기 | Graph view: Open local graph | 현재 주제와 직접 연결된 노트 확인 |
| 백링크 보기 | Backlinks: Open backlinks | 이 노트를 참조하는 근거 확인 |
| 템플릿 삽입 | Templates: Insert template | 반복 질문 양식 삽입 |
| 읽기/편집 전환 | Markdown: Toggle reading view | 표와 링크를 읽기 좋게 확인 |

## 바로 쓰는 검색 명령 블록

### 공장 매칭 로직

```query
path:platform matching
```

### 저당·혈당관리

```query
path:korea_trends 저당
```

### HMR·냉동·D2C

```query
path:korea_trends 냉동
```

### 라벨·영양표시·투명성

```query
영양표시
```

### 바이브 쿠킹·재료 발주

```query
바이브 쿠킹 OR BOM OR 재료 발주
```

### 규제 스크리닝

```query
규제 OR 영양표시 OR 알레르기 OR HACCP OR GMP
```

### 수출·K-푸드·할랄

```query
수출
```

## Q&A 로그

### Q1. 이 플랫폼의 핵심 문제는 무엇인가?

식품은 제품 유형, 공정, 원료, 인증, MOQ, 보관 방식에 따라 필요한 공장 조건이 크게 달라진다. 발주자는 어떤 공장을 찾아야 하는지부터 막히고, 공장은 맞지 않는 문의를 반복해서 받는다. 핵심 해결책은 [[10_Core_Idea|AI 기반 식품 OEM/ODM 공장 매칭 플랫폼]]과 [[platform/Matching_Logic|AI 매칭 로직]]으로 제품 조건을 구조화해 공장 후보를 좁히는 것이다.

### Q2. MVP에서 먼저 검증할 질문은 무엇인가?

1. 창업자나 브랜드가 제품 아이디어를 자연어로 입력했을 때 필요한 공정, 인증, MOQ 조건을 이해하는가?
2. 공장 입장에서 문의 조건이 충분히 구체적이라 응답 비용이 줄어드는가?
3. [[korea_trends/02_Low_Sugar_Blood_Glucose|저당·혈당관리]], [[korea_trends/03_HMR_Frozen_Premium|간편식 HMR·냉동 프리미엄]], [[korea_trends/05_AI_Personalized_Nutrition_Foodtech|AI 맞춤영양·푸드테크 제조]] 중 어떤 카테고리가 초기 수요와 공장 데이터 확보가 가장 쉬운가?

### Q3. 공장 데이터에서 반드시 표준화해야 하는 필드는 무엇인가?

[[platform/Factory_Data_Model|공장 역량 데이터 모델]] 기준으로 제품군, 공정 설비, MOQ, 샘플 가능 여부, 인증, 원료 대응, 포장 방식, 라벨 검수, 원산지 증빙, 냉장·냉동 배송 대응을 우선 표준화한다. 대량 처리를 고려하면 입력 필드는 길게 늘리기보다 매칭에 직접 쓰이는 조건부터 고정 값으로 관리하는 편이 좋다.

### Q4. 한국 시장에서 우선 연결할 트렌드는 무엇인가?

우선순위는 저당·혈당관리, HMR·냉동 프리미엄, AI 맞춤영양·푸드테크 제조다. 이 세 축은 제품 기획 조건이 구체적이고, 공장 설비·라벨·배송 조건과 직접 연결되며, [[20_Trend_Map|글로벌 트렌드 맵]]의 기능성, AI 공급망, 편의성 흐름과도 맞물린다.

### Q5. 바이브 쿠킹은 플랫폼에서 어떤 역할인가?

[[platform/Vibe_Cooking_Digital_Twin|바이브 쿠킹]]은 식품 아이디어를 공장 발주 가능한 개발 사양으로 바꾸는 LLM 기반 디지털 트윈 쿠킹 모듈이다. 레시피 초안, 원재료 BOM, 대체 원료, 공정 조건, 목표 원가, 표시·인증 리스크를 먼저 구조화한 뒤 [[platform/Matching_Logic|AI 매칭 로직]]에 넘긴다. 이렇게 하면 B2B는 상품기획서에서 샘플 발주까지의 왕복을 줄이고, B2C는 소량 제작 가능한 카테고리와 최소 발주 조건을 빠르게 확인할 수 있다.

### Q6. 규제 스크리닝은 MVP에서 어디까지 해야 하는가?

[[platform/Regulatory_Screening_System|규제 스크리닝]]은 최종 법률 판단이 아니라 사전 위험 분류로 시작한다. MVP에서는 저당·고단백 건강간식, 분말·스틱, 소스 3개 케이스에 대해 영양표시, 알레르기, 기능성 광고, 원료 사용 가능성, 첨가물, HACCP/GMP, 포장재 증빙을 RED/YELLOW/GREEN으로 나누고, RED가 있으면 라벨 문구와 샘플 발주서를 보류한다.

## 새 질문 작성 양식

아래 블록을 복사해 이어 붙인다.

```markdown
### Q. 

질문:

답변:

근거 노트:
- [[]]
```

## 핵심 노트 바로가기

- [[00_Home]]
- [[10_Core_Idea]]
- [[20_Trend_Map]]
- [[platform/Vibe_Cooking_Digital_Twin]]
- [[platform/Regulatory_Screening_System]]
- [[platform/Matching_Logic]]
- [[platform/Factory_Data_Model]]
- [[korea_trends/00_Korea_Trend_Map]]
- [[korea_trends/Korea_Global_Comparison]]
