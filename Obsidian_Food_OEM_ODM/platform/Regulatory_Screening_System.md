---
aliases:
  - 식품 규제 스크리닝
  - 한국 식품 규제 체크
tags:
  - platform
  - regulation
  - screening
  - mfds
  - mvp
---

# 한국 식품 규제 스크리닝 시스템

작성 기준일: 2026-07-07

## 한 줄 정의

규제 스크리닝 시스템은 바이브 쿠킹 산출물과 공장 매칭 입력을 기준으로 한국 식품 규제상 확인해야 할 표시, 원료, 첨가물, 알레르기, 영양표시, 기능성 광고, HACCP/GMP, 포장재 리스크를 자동 플래그로 분류하는 사전 점검 모듈이다.

## 원칙

이 시스템은 법률 자문이나 최종 인허가 판단을 대체하지 않는다. MVP에서는 `통과/불통과` 판정보다 `확인 필요 항목`, `공장 또는 전문가에게 물어볼 질문`, `출시 전 필수 증빙`을 만드는 역할에 집중한다.

## 스크리닝 단계

| 단계 | 질문 | 주요 데이터 |
|---|---|---|
| 1. 식품 유형 분류 | 이 제품은 식품공전상 어떤 유형인가? | 제품명, 공정, 제형, 원재료, 섭취 목적 |
| 2. 일반식품/건강기능식품 구분 | 기능성 표현이나 건강기능식품 오인 가능성이 있는가? | 효능 문구, 기능성 원료, 광고 문안 |
| 3. 원료 적합성 | 원재료가 식품 원료로 사용 가능한가? 제한 원료인가? | 원재료명, 학명, 사용 부위, 추출물 여부 |
| 4. 첨가물 적합성 | 감미료, 보존료, 향료, 색소 사용 기준이 맞는가? | 첨가물명, 사용 목적, 식품 유형 |
| 5. 알레르기 | 표시대상 알레르기 유발물질이 포함되는가? | 원재료, 복합원재료, 공장 교차오염 |
| 6. 영양표시 | 영양표시 대상 또는 강조표시 대상인가? | 식품 유형, 판매 단위, 저당/고단백/무가당 문구 |
| 7. 표시·광고 | 질병 예방·치료, 의약품 오인, 건기식 오인 문구가 있는가? | 제품명, 상세페이지, 패키지 문구 |
| 8. 제조·위생 | HACCP/GMP 필요 또는 공장 인증 확인이 필요한가? | 제품 유형, 제조공정, 공장 인증 |
| 9. 용기·포장 | 식품용 기구·용기·포장 기준을 확인해야 하는가? | 파우치, 병, 스틱, 냉동팩, 직접 접촉 재질 |
| 10. 출시 전 확인 | 법정 표시사항, 시험성적서, 인증서, 행정처분 이력 확인이 끝났는가? | 공장 서류, 라벨 시안, 시험 결과 |

## MVP 출력 등급

| 등급 | 의미 | 처리 |
|---|---|---|
| RED | 출시 또는 광고 전에 전문가·공장 확인이 반드시 필요한 위험 | 매칭 결과 상단 경고, 견적 요청서에 필수 질문 포함 |
| YELLOW | 제품 유형과 문구에 따라 규정 확인이 필요한 항목 | 체크리스트 생성, 라벨/상세페이지 문구 보류 |
| GREEN | 현재 입력 기준 큰 위험은 낮지만 증빙 보관이 필요한 항목 | 출처와 확인 일자 저장 |

## MVP 핵심 규칙

| 트리거 | 등급 | 스크리닝 내용 |
|---|---|---|
| `저당`, `무당`, `무가당`, `제로슈가` | YELLOW | 영양표시, 당류 기준, 무당·무가당 추가 정보 제공 여부 확인 |
| `고단백`, `식이섬유`, `프로틴` | YELLOW | 영양성분 강조표시 기준과 실제 분석값 확인 |
| `다이어트`, `혈당`, `장건강`, `면역`, `숙취해소` | RED | 일반식품 기능성 표시 또는 건강기능식품 오인 가능성 확인 |
| `치료`, `예방`, `염증`, `당뇨`, `고혈압`, `변비 치료` | RED | 질병 예방·치료 효능 표시·광고 금지 리스크 |
| 원재료에 우유, 대두, 밀, 견과류 등 포함 | RED | 알레르기 표시와 교차오염 관리 확인 |
| 분말·스틱 제품 | YELLOW | 일반식품인지 건강기능식품인지, GMP 필요 여부 확인 |
| 곡물스낵·과자류 | YELLOW | 식품 유형, HACCP 인증, 영양표시, 알레르기 확인 |
| 소스·드레싱 | YELLOW | 식품 유형, 살균/보존, 첨가물, 나트륨/알레르기 표시 확인 |
| 스틱포·파우치·병 포장 | YELLOW | 식품용 기구·용기·포장 기준과 재질 증빙 확인 |
| 공장 후보 | YELLOW | HACCP/GMP 인증 여부와 행정처분 이력 조회 |

## 바이브 쿠킹 연결

[[Vibe_Cooking_Digital_Twin|바이브 쿠킹]]은 레시피와 BOM을 만든 뒤 아래 필드를 규제 스크리닝으로 넘긴다.

| 필드 | 예시 |
|---|---|
| product_type_guess | 과자류, 소스류, 기타가공품, 건강기능식품 |
| ingredient_list | 현미, 대두단백, 알룰로스, 난소화성말토덱스트린 |
| additive_list | 향료, 감미료, 산도조절제, 보존료 |
| claim_list | 저당, 고단백, 식이섬유, 장건강 |
| allergen_candidates | 우유, 대두, 밀, 땅콩, 호두 |
| process_list | 배합, 성형, 굽기, 살균, 충진, 스틱포장 |
| package_material | 스틱필름, 파우치, PET병, 유리병 |
| target_channel | D2C, 공동구매, 프랜차이즈, PB |

## 공장 매칭 연결

규제 스크리닝 결과는 [[Matching_Logic|AI 매칭 로직]]의 필터와 랭킹에 반영한다.

| 스크리닝 결과 | 매칭 반영 |
|---|---|
| HACCP 필요 | HACCP 보유 공장 우선 |
| GMP 필요 가능성 | 건강기능식품전문제조업/GMP 후보 분리 |
| 알레르기 RED | 알레르기 관리·교차오염 대응 가능한 공장 우선 |
| 영양표시 필요 | 영양성분 산출·시험성적서 대응 가능 공장 우선 |
| 기능성 광고 RED | 라벨 검수 또는 표시광고 심의 경험 보유 후보 우선 |
| 포장재 확인 필요 | 포장재 성적서와 식품용 재질 증빙 가능한 후보 우선 |

## MVP별 적용

### Case 001. 저당·고단백 건강간식

- 우선 확인: 식품 유형, HACCP, 저당/고단백 강조표시, 알레르기, 영양성분 분석
- RED 예시: `혈당 개선 쿠키`, `당뇨 예방 간식`
- 견적 질문: 당류/단백질 분석 지원 여부, 알레르기 교차오염 관리, 개별포장 라벨 검수 가능 여부

### Case 002. 분말·스틱 건강식품

- 우선 확인: 일반식품/건강기능식품 구분, GMP, 기능성 표현, 원료 사용 가능 여부
- RED 예시: `면역력 치료`, `장질환 개선`, `다이어트 치료`
- 견적 질문: GMP 제조 가능 여부, 기능성 원료 사용 경험, 스틱포 단위 표시 가능 여부

### Case 003. 소스 OEM

- 우선 확인: 식품 유형, 살균/보존 공정, 첨가물, 나트륨, 알레르기, 포장재
- RED 예시: `혈압 낮추는 소스`, `염증 제거 양념`
- 견적 질문: 살균 조건, 보존료/산도조절제 사용 기준 검토, 파우치/병 포장재 증빙 가능 여부

## 데이터 모델 초안

| 테이블 | 핵심 필드 |
|---|---|
| RegulatoryRule | rule_id, scope, trigger, severity, source_url, effective_date |
| ScreeningRun | run_id, product_case, input_hash, checked_at, overall_status |
| ScreeningFinding | run_id, rule_id, severity, message, required_evidence |
| LabelClaim | product_id, claim_text, claim_type, status, reviewer |
| IngredientRegCheck | ingredient_id, food_material_status, allergen_flag, additive_flag |
| FactoryRegCapability | factory_id, haccp_status, gmp_status, label_review_support, test_report_support |

## 바로 쓸 규칙 시드

- CSV 시드: `Obsidian_Food_OEM_ODM/database/regulatory_screening_rules_seed.csv`

## 공식 확인 출처

- 식품분야 공전 온라인 서비스: https://various.foodsafetykorea.go.kr/fsd/
- 식품원료 목록: https://www.foodsafetykorea.go.kr/portal/safefoodlife/foodMeterial/foodMeterialDB.do?menu_grp=MENU_NEW04&menu_no=2968
- 2026년 영양표시제도 주요 변경사항: https://www.mfds.go.kr/brd/m_1105/view.do?seq=33773
- 식품등의 표시기준 일부개정고시 제2026-37호: https://www.mfds.go.kr/brd/m_207/view.do?seq=15167
- 일반식품의 기능성 표시제도 질의응답집: https://www.mfds.go.kr/brd/m_1060/view.do?seq=14784
- 식품 등 부당한 표시·광고: https://www.foodsafetykorea.go.kr/portal/board/board.do?menu_grp=MENU_NEW01&menu_no=4838
- 알레르기 유발 식품 표시 안내: https://www.foodsafetykorea.go.kr/portal/board/boardDetail.do?bbs_no=bbs039&menu_grp=MENU_NEW03&menu_no=4847&ntctxt_no=1093585
- HACCP 업체 정보 서비스: https://www.data.go.kr/data/15065475/openapi.do
- 식품안전나라 업체 검색: https://www.foodsafetykorea.go.kr/portal/specialinfo/searchInfoCompany.do
