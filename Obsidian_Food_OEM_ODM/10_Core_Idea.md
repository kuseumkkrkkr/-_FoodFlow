---
tags:
  - idea
  - platform
  - oem_odm
---

# AI 기반 식품 OEM/ODM 공장 매칭 플랫폼

## 한 줄 정의

만들고 싶은 식품을 입력하면 생산 가능한 공장, 예상 MOQ, 인증/설비 조건, 지역, 샘플 가능 여부를 AI가 매칭해주는 식품 제조 발주 플랫폼.

## 문제

식품은 제품마다 필요한 공장 조건이 크게 다르다. 같은 간식이라도 냉동, 레토르트, 발효, 액상, 분말, 베이커리, HMR 여부에 따라 설비와 인허가, 최소 발주량, 납기, 원료 대응력이 달라진다. 초보 창업자는 어떤 공장을 찾아야 하는지부터 막히고, 공장은 자신에게 맞지 않는 문의를 반복해서 받는다.

## 해결

사용자가 만들고 싶은 식품을 자연어로 입력하면 [[platform/Vibe_Cooking_Digital_Twin|바이브 쿠킹]]이 레시피 초안, 원재료 BOM, 공정 조건, 표시·인증 체크리스트를 먼저 만든다. 이후 [[platform/Matching_Logic|AI 매칭 로직]]이 제품 유형을 분류하고, [[platform/Factory_Data_Model|공장 역량 데이터]]와 비교해 적합한 OEM/ODM 업체를 추천한다.

## 서비스 분리

- [[platform/B2B_Flow|B2B 제작부]]: 브랜드, 유통사, 프랜차이즈, 스타트업의 제품 개발과 대량 발주
- [[platform/B2C_Flow|B2C 제작부]]: 소규모 제작, 테스트 판매, 공동구매, 크리에이터/커뮤니티형 제품 제작
- [[platform/Vibe_Cooking_Digital_Twin|바이브 쿠킹]]: LLM 기반 디지털 트윈 쿠킹으로 제품 아이디어를 재료 발주와 샘플 개발 가능한 사양으로 변환
- [[platform/Regulatory_Screening_System|규제 스크리닝]]: 한국 식품 규제 기준으로 표시, 원료, 알레르기, 영양표시, 기능성 광고, HACCP/GMP 리스크를 사전 플래그 처리

## 첫 MVP 범위

첫 MVP는 전체 식품 OEM/ODM을 대상으로 하지 않는다. [[mvp/MVP_Start_Casing|MVP 시작 케이싱]] 기준으로 `저당·고단백 건강간식`, `분말·스틱 건강식품`, `소스 OEM` 3개 케이스만 먼저 검증한다. 공장 후보는 [[database/Korea_OEM_ODM_Initial_DB|한국 식품 OEM/ODM 초기 DB]]에서 시작한다.

## 트렌드 연결

### 글로벌 트렌드

- [[trends/Functional_Personalized_Food|기능성·개인맞춤 식품]]: 기능성 원료와 효능 조건이 다양해질수록 공장 매칭 난도가 올라간다.
- [[trends/AI_Transparent_Supply_Chain|AI·투명 공급망 제조]]: AI와 데이터 기반 공급망 투명성이 식품 제조의 기본 경쟁력이 된다.
- [[trends/Clean_Label_Responsible_Sourcing|클린라벨·책임소싱]]: 성분, 원산지, 인증, 제조 공정 설명이 가능한 공장이 더 중요해진다.
- [[trends/Food_ESG_Transparency|식품 ESG·투명성]]: 소비자는 투명한 제품 정보와 인증·원산지·알레르기 정보를 구매 신뢰의 근거로 보기 때문에, 플랫폼은 공장 연결과 함께 제조정보 신뢰도를 제공해야 한다.

### 한국 트렌드

- [[korea_trends/00_Korea_Trend_Map|2026 대한민국 식품 트렌드 맵]]: 국내 시장은 1인 가구, 고물가, 영양표시 규제, 온라인 식품 구매, K-푸드 수출, 초고령사회가 핵심 변수다.
- [[korea_trends/02_Low_Sugar_Blood_Glucose|저당·혈당관리·로우스펙]]: 저당 원료, 대체당, 영양표시 대응이 공장 매칭 조건이 된다.
- [[korea_trends/03_HMR_Frozen_Premium|간편식 HMR·냉동 프리미엄]]: 냉동, 즉석섭취, RMR, 건강 도시락 제조 역량을 분류해야 한다.
- [[korea_trends/05_AI_Personalized_Nutrition_Foodtech|AI 맞춤영양·푸드테크 제조]]: 공장 데이터 표준화와 AI 매칭의 필요성을 직접 뒷받침한다.
- [[korea_trends/06_K_Food_Export_Rice_Processed|K-푸드 수출·라면·쌀가공]]: 수출 인증, 현지 표시, 할랄, 글루텐프리 같은 조건을 공장 필터에 포함해야 한다.
- [[korea_trends/08_Senior_Care_Food|고령친화식품·케어푸드]]: 연화식, 단백질 강화 반찬, 돌봄기관 B2B 납품이 새로운 발주 카테고리가 된다.

한국과 글로벌 트렌드의 차이는 [[korea_trends/Korea_Global_Comparison|한국 vs 글로벌 식품 트렌드 비교분석]]에서 관리한다.

## 아이디어명 후보

1. AI 기반 식품 OEM/ODM 공장 매칭 플랫폼
2. 푸드팩토리 매칭 AI
3. 식품 제조 발주 AI 플랫폼
4. 소량부터 대량까지 식품 공장 매칭 플랫폼
