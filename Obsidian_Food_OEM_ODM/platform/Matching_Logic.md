---
tags:
  - platform
  - ai
  - matching
---

# AI 매칭 로직

## 입력 예시

"저당 고단백 그래놀라바를 소량으로 만들고 싶고, 온라인 공동구매로 먼저 팔아보고 싶다."

"1인분 냉동 단백질 도시락을 D2C로 테스트하고 싶고, 영양표시와 알레르기 표시까지 맞춰야 한다."

"카페 프랜차이즈에서 여름 시즌용 저당 피스타치오 쿠키를 B2B로 개발하고 싶고, 원재료 발주와 샘플 생산까지 한 번에 검토하고 싶다."

## MVP 제한

초기 매칭 로직은 전체 식품을 받지 않고 [[../mvp/MVP_Start_Casing|MVP 시작 케이싱]]의 3개 제품군만 받는다.

| product_case | 우선 매칭 DB |
|---|---|
| 건강간식 | 곡물스낵, 저당, 고단백, 개별포장 가능 공장 |
| 분말스틱 | 분말 배합, 스틱포, GMP/HACCP 가능 공장 |
| 소스 | 소스 R&D, 살균/충진, B2B 납품 가능 공장 |

## 처리 단계

1. 제품 카테고리 추출: 그래놀라바, 건강간식
2. 기능성 조건 추출: 저당, 고단백
3. 바이브 쿠킹 사양화: 레시피 초안, 원재료 BOM, 대체 원료, 목표 원가, 표시 리스크 정리
4. 규제 스크리닝: [[Regulatory_Screening_System|한국 식품 규제 스크리닝]]으로 RED/YELLOW/GREEN 플래그 생성
5. 공정 조건 추출: 배합, 성형, 굽기/건조, 개별 포장
6. 사업 유형 분류: B2C 소량 제작 또는 B2B 테스트 생산
7. 필수 인증 후보 도출: HACCP, 알레르기 관리, GMP, 라벨 검수
8. 한국 트렌드 조건 추출: 저당, HMR, 냉동, D2C, 영양표시, 수출, 케어푸드 여부
9. 공장 후보 랭킹: 카테고리 적합도, MOQ, 위치, 샘플 가능 여부, 인증, 표시 대응, 유통 대응
10. 샘플 발주서 생성: 공장에 전달할 BOM, 공정 가정, 원료 확인 질문, 규제 확인 질문, 테스트 수량 정리

## 랭킹 기준

| 기준      | 설명                   |
| ------- | -------------------- |
| 생산 적합도  | 해당 제품을 실제 생산할 수 있는가  |
| MOQ 적합도 | 사용자의 수량과 맞는가         |
| 인증 적합도  | 필요한 인증과 표시 기준을 충족하는가 |
| 지역/물류   | 납기와 물류비가 합리적인가       |
| 신뢰도     | 검증된 공장인가             |
| 투명성 적합도 | 원산지, 원재료, 알레르기, 인증, 제조방식 정보를 공개·증빙할 수 있는가 |
| 한국 규제 적합도 | 영양표시, 당알코올, 고카페인, GMO, 원산지 표시 대응이 가능한가 |
| 한국 채널 적합도 | 온라인/D2C, 냉동 배송, 편의점/PB, 돌봄기관 B2B 납품에 맞는가 |
| 개발 사양 적합도 | 바이브 쿠킹으로 생성한 BOM, 공정 조건, 목표 원가를 공장이 검토할 수 있는가 |
| 규제 대응 적합도 | 영양표시, 알레르기, 기능성 광고, HACCP/GMP, 첨가물, 포장재 증빙을 처리할 수 있는가 |

## 한국 트렌드별 매칭 가중치

| 한국 트렌드 | 가중치를 높일 필드 |
|---|---|
| [[../korea_trends/02_Low_Sugar_Blood_Glucose|저당·혈당관리]] | 대체당 원료, 당류 분석, 영양표시, 저당 레시피 경험 |
| [[../korea_trends/03_HMR_Frozen_Premium|간편식 HMR·냉동 프리미엄]] | 냉동/레토르트/즉석섭취 설비, 소분 포장, 온라인 배송 |
| [[../korea_trends/05_AI_Personalized_Nutrition_Foodtech|AI 맞춤영양·푸드테크 제조]] | 데이터 제공 수준, 원가 산출, 스마트제조, SKU 대응 |
| [[../korea_trends/06_K_Food_Export_Rice_Processed|K-푸드 수출·쌀가공]] | 수출 인증, 할랄, 글루텐프리, 다국어 라벨 |
| [[../korea_trends/08_Senior_Care_Food|고령친화식품·케어푸드]] | 연화식, 단백질 강화, 고령친화우수식품, B2B 납품 |

## 관련 노트

- [[10_Core_Idea]]
- [[platform/Vibe_Cooking_Digital_Twin]]
- [[platform/Regulatory_Screening_System]]
- [[mvp/MVP_Start_Casing]]
- [[database/Korea_OEM_ODM_Initial_DB]]
- [[platform/Factory_Data_Model]]
- [[platform/B2B_Flow]]
- [[platform/B2C_Flow]]
- [[trends/Food_ESG_Transparency]]
- [[korea_trends/00_Korea_Trend_Map]]
- [[korea_trends/Korea_Global_Comparison]]
