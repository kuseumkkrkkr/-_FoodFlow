---
tags:
  - database
  - factory
  - oem_odm
  - korea
  - mvp_seed
---

# 한국 식품 OEM/ODM 초기 DB

작성 기준일: 2026-07-07

이 DB는 첫 MVP 검증용 시드다. 공개 검색으로 확인한 후보만 넣었고, 실제 계약·견적·표시 가능 여부는 `검증 필요` 상태로 둔다. 초기 MVP는 [[../mvp/MVP_Start_Casing|저당·고단백 건강간식/분말·스틱/소스]] 중심으로 사용한다.

현재 누적 후보: `460개`

이번 확장 배치의 기준은 다음과 같다.

- `공식/공공 출처 우선`: 업체 공식 페이지, 푸드이음, 공개 전시/매칭 페이지 순서로 신뢰도를 둔다
- `MVP 우선`: 저당·고단백 스낵, 분말·스틱, 소스·HMR 소스에 바로 연결되는 후보를 A/B로 둔다
- `과장 방지`: 플랫폼에 제조사로 등재됐지만 OEM/ODM이 직접 명시되지 않은 곳은 `미확인`으로 둔다
- `컨택 검증`: MOQ, 샘플 가능 여부, 표시·광고 검토, HACCP/GMP 인증서 제공 여부는 상담 전까지 확정하지 않는다

## 사용 규칙

- `MVP 적합도 A`: 첫 매칭 테스트에 바로 넣을 후보
- `MVP 적합도 B`: 보조 카테고리 또는 2차 검증 후보
- `MVP 적합도 C`: DB 확장용 후보
- 모든 후보는 `source_url`을 필수로 가진다. 출처가 없으면 DB에 넣지 않는다
- 출처는 `공식 페이지 > 공공 DB > 전시/매칭 플랫폼 > 보도/기업정보` 순서로 우선한다
- 공개 페이지에 MOQ가 없으면 `미확인`으로 둔다
- 업체별 인증, 품목, MOQ는 실제 상담 전 반드시 재확인한다

## 초기 후보 테이블

| ID | 업체명 | 1차 카테고리 | 공개 확인 내용 | 지역 | MVP 적합도 | 다음 액션 | 출처 |
|---|---|---|---|---|---|---|---|
| F001 | 노바렉스 | 건강기능식품 ODM/OEM | 제품 기획, 개발, 생산, 품질관리, 출하까지 ODM/OEM 제공 | 충북 오송권 추정, 상세 확인 필요 | B | 대형 B2B용으로 분리 | https://www.novarex.co.kr/ko/?mCode=business%2Fproduction |
| F002 | 코스맥스엔비티 | 건강기능식품 ODM/OEM/OBM | 트렌드 분석, 상품 기획, 개발, 생산, 출하까지 토탈 솔루션 제공 | 본사 성남, 공장 이천 | B | 분말·개인맞춤 케이스 검증 | https://www.cosmaxnbt.com/business/business_information.jsp |
| F003 | 코스맥스바이오 | 건강기능식품 OEM/ODM | 건강기능식품 OEM·ODM 제조 및 컨설팅, 소재·제형 R&D | 본사/공장 제천, 판교 사무소 | B | 제형/소재 상담 가능 여부 확인 | https://www.cosmaxbio.com/ |
| F004 | 콜마비앤에이치 | 건강기능식품 ODM | 건강기능식품 ODM 기업, 세종·음성 공장 공개 | 세종, 음성 | B | 대형 B2B와 기능성 원료 케이스로 분리 | https://kolmarbnh.co.kr/ |
| F005 | 한국네츄럴팜 | 건강기능식품 OEM/ODM | GMP, HACCP 기반 건강기능식품 OEM·ODM | 미확인 | A | 분말·정제·스틱 가능 범위 확인 | https://www.koreanaturalpharm.com/index |
| F006 | 데이앤바이오 | 건강기능식품/일반식품 OEM | GMP, HACCP, 분말·환·정제·캡슐·스틱포·PTP 포장 공개 | 미확인 | A | 소량 MOQ와 일반식품 가능 범위 확인 | https://daynbio.com/ |
| F007 | 채움바이오 | 건강식품 OEM/ODM | 정제, 분말, 스틱 제형과 소량 생산 메시지 공개 | 미확인 | A | MOQ 1,000개 조건과 견적 폼 확인 | https://cheumbio.com/kr |
| F008 | FAST OEM | 건강기능식품 OEM/ODM/CDMO | 초기 사업자, 소량 생산, 제형 개발, 원료 제안, 포장 지원 메시지 공개 | 미확인 | A | 초기 창업자 플로우 벤치마크 | https://www.fast-oem.com/ |
| F009 | 한미사이언스 | 음료/두유/환자용 영양식 | 두유, 음료, 환자용 고형영양식 HACCP 항목 공개 | 미확인 | B | 음료·두유 케이스 별도 분리 | https://hanmiscience.co.kr/science/handler/Business-Oem |
| F010 | 주식회사 제이스 | 소스 OEM/ODM | HACCP 기반 소스 개발, 레시피 기획부터 양산·수출까지 지원 | 미확인 | A | 소스 Case 003 후보로 상담 항목 설계 | https://hjace.co.kr/oem-odm |
| F011 | 소담푸드 | 소스 OEM/ODM | 맞춤 소스 개발, 소량 테스트부터 대량 생산까지 지원 | 미확인 | A | 샘플 개발 프로세스 확인 | https://sodamkorea.com/oem |
| F012 | 청우에프앤비 | 수산식품 OEM/ODM | 신제품 공동개발, 맞춤 레시피, 포장 단위 조정, HACCP 기반 생산 | 전남 화순 | C | 수산 카테고리는 MVP 후순위 | https://cwfnb.com/oem-odm/ |
| F013 | 만샘골 | 국탕·밀키트·수육 OEM/ODM | HACCP 기반 국탕류 원팩·밀키트·수육 B2B 납품 | 인천 서구 | B | HMR 후순위 케이스로 보관 | https://www.manssam.com/2 |
| F014 | 진앤푸드 | 냉장 도시락/반찬/HMR OEM | 냉장 도시락, 반찬류, 덮밥·소스 완제품 OEM 공개 | 미확인 | B | 냉장 HMR은 2차 케이스로 분리 | https://www.factory-platform.com/manufacturer?category_code=12&tpf=product%2Flist |
| F015 | 에스와이솔루션 | 곡물스낵 OEM | 곡물칩·곡물스낵, 저당·제로슈가·고단백 OEM 가능, HACCP/ISO/비건/할랄 공개 | 미확인 | A | Case 001 최우선 후보 | https://factory-platform.com/manufacturer?category_code=14&tpf=product%2Flist |
| F016 | 최고존 | 업소용 소스 OEM/ODM | 업소용 소스 OEM·ODM, HACCP 시설 공개 | 미확인 | B | 소스 후보 보강 | https://xn--299a063cvod.com/ |
| F017 | 블루피노 | 탄산음료 OEM/ODM | 탄산음료 OEM, 협업 제품 개발, 농산물 활용 탄산음료 제조 공개 | 미확인 | C | 음료는 별도 카테고리로 후순위 | https://blupino.com/partner |
| F018 | 비티씨 | 분말 OEM/ODM | 푸드이음 기준 생산품목 분말, OEM/ODM | 전북 익산 | A | 공공 DB 기반 연락처 확인 | https://www.foodpolis.kr/fbip/co/fe/search/sub/oemodm?type=search5 |
| F019 | 주식회사 성진바이오 | 환·분말 OEM/ODM | 푸드이음 기준 생산품목 환·분말, OEM/ODM | 경기 포천 | A | 분말·환 소량 가능 여부 확인 | https://www.foodpolis.kr/fbip/co/fe/search/sub/oemodm?type=search5 |
| F020 | 주식회사 새한그레인 | 곡물스낵 OEM/ODM | 푸드이음 상세 기준 곡물 기반 건강 스낵 OEM/ODM 전문기업, HACCP/FSSC22000 공개 | 경남 김해 | A | 곡물 스낵 Case 001 후보로 MOQ 확인 | https://www.foodpolis.kr/fbip/co/fe/inst/view.do?instId=853de26e-1e4a-49b5-8107-19894e01707b |
| F021 | 주식회사 대두식품 | 쌀가루/프리믹스 OEM/ODM | 푸드이음 상세 기준 쌀가루 개발 및 OEM/ODM 생산 방식 공개 | 전북 군산 | B | 쌀가루·프리믹스 원료 후보 확인 | https://www.foodpolis.kr/fbip/co/fe/inst/view.do?instId=aad0c381-f284-4235-91c6-8c091438e569 |
| F022 | 예그린식품 | 식품 OEM/ODM | 푸드이음 기준 OEM/ODM 등재 | 경기 시흥 | C | 생산품목 추가 확인 | https://www.foodpolis.kr/fbip/co/fe/search/sub/oemodm?type=search5 |
| F023 | 락토코리아(주) | 분말/프리믹스 OEM/ODM | 푸드이음 상세 기준 튀김가루·부침가루·치킨튀김가루, OEM/ODM 생산 방식, HACCP 공개 | 충남 청양 | B | 프리믹스·분말 원료 후보 확인 | https://www.foodpolis.kr/fbip/co/fe/inst/view.do?instId=065abad4-c178-4ccd-b511-23ec877b2961 |
| F024 | 거류영농조합법인 | 원료소재 OEM/ODM | 푸드이음 기준 원료 소재 OEM/ODM 등재 | 경남 고성 | C | 농산 원료와 완제품 생산 가능 여부 확인 | https://www.foodpolis.kr/fbip/co/fe/search/sub/oemodm?type=search5 |
| F025 | (주)나루아토 | 원료소재 OEM/ODM | 푸드이음 상세 기준 OEM/ODM 생산 능력, 디저트 원료, HACCP 확인 | 경남 진주 | C | 소재 카테고리와 샘플 대응 여부 확인 | https://www.foodpolis.kr/fbip/co/fe/inst/view.do?instId=a590f167-0e56-45e4-ad40-6ff996bb2bf4 |
| F026 | (주)희망그린식품 | 원료소재 OEM/ODM | 푸드이음 등재 및 공개 문의 사례에서 분말/과립 스틱 문의 확인 | 경기 안성 | B | 커피·분말 스틱 OEM 가능 범위 확인 | https://speranzafood.co.kr/_NBoard/board.php?bo_table=inquiry |
| F027 | 선해수산 | 수산스낵/건어포 OEM/ODM | 푸드이음 상세 기준 명태 연육 가공품·황태 스틱, HACCP/FSSC22000/FDA 공개 | 전북 익산 | C | 수산스낵·건어포 OEM/ODM 후보 확인 | https://www.foodpolis.kr/fbip/co/fe/inst/view.do?instId=67237c17-eb93-4e52-83b3-a97a5a79b849 |
| F028 | (주)신비바이오 | 건강기능식품/일반식품 OEM | 소량 다품종, GMP/HACCP, 정제·액상·분말·스틱·환 제형 공개 | 미확인 | A | 소량 MOQ와 일반식품/건기식 분리 상담 | https://sinbibio.co.kr/ |
| F029 | 우리바이오(주) | 건강기능식품 OEM/ODM | 건강기능식품 OEM/ODM, 천연물 원료, 제형별 맞춤 공정 공개 | 미확인 | B | 제형과 소량 대응 여부 확인 | https://www.wooreebio.co.kr/oem-odm/ |
| F030 | 관주식품 | 동결건조/분말 OEM/ODM | 분말, 분말스틱, 식품원료, 동결건조 OEM/ODM 공개 | 미확인 | A | 분말 스틱과 원료 소싱 범위 확인 | https://gwanjufood.co.kr/page_HHwY60 |
| F031 | (주)상상바이오 | 건강기능식품 소량 OEM/ODM | QOEM 기준 소량 생산, 컨셉 기반 ODM, GMP/HACCP/FDA/SQF 공개 | 서울/충남 당진/전남 화순 | A | 스타트업 소량생산 MVP 최우선 상담 | https://www.qoem.co.kr/OEM |
| F032 | 이앤에스(주) | 분말/스틱 OEM/ODM | 유동층 과립 기반 분말 스틱 라인, GMP/HACCP 공개 | 경기 안성 | A | 분말 스틱 MOQ와 원료 발주 방식 확인 | https://enscorp.co.kr/production-management/ |
| F033 | (주)에스엘에스 | 건강기능식품/건강지향식품 OEM/ODM | GMP/HACCP 시설과 기획·개발·생산·품질관리·출하 전 과정 공개 | 미확인 | B | 제형과 소량 대응 여부 확인 | https://slsltd.co.kr/oem-odm/ |
| F034 | 한국바이오팜 | 건강기능식품 OEM/ODM | 건강기능식품 전문 제조, OEM/ODM, GMP/HACCP 공개 | 미확인 | B | 대형 건기식 ODM 후보로 분리 | https://koreabiopharm.co.kr/oem-odm |
| F035 | 엔바이오 | 건강기능식품/음료 OEM/ODM | 이중제형 특허, 건강기능식품, 혼합음료·과채음료 OEM/ODM 공개 | 미확인 | B | 이중제형과 음료 케이스 분리 | https://n-bio.co.kr/business/oem/ |
| F036 | 삼진푸드 | 소스/분말/농축 OEM/ODM | 소스, 분말, 농축, 완제품 1,000가지 이상과 B2B ODM/OEM 공개 | 충북 진천 | A | 소스 Case 003 대형 후보로 상담 | https://samjinfoods.co.kr/ceo-message |
| F037 | 매일식품 | 밀키트/HMR 소스 OEM | 밀키트·HMR 요리소스 맞춤 제조 메시지 공개 | 미확인 | A | HMR·프랜차이즈 소스 상담 | https://maeilfoods.com/media-center/promotional-videos/ |
| F038 | 하비랑 | HACCP 식품 OEM/ODM | OEM/ODM 제조 전문과 HACCP 기반 개발·생산 공개 | 미확인 | B | 주력 품목과 MOQ 확인 | https://www.habirang.co.kr/ |
| F039 | 찬들푸드 | 소스/축산물 OEM/ODM | 소스류 및 축산물 가공 HACCP, 기획·개발·생산·유통 공개 | 미확인 | B | 소스와 육가공 동시 생산 범위 확인 | https://chandle.co.kr/kor/ |
| F040 | 농업회사법인 크레이지피넛 주식회사 | 견과 스프레드/페이스트 OEM/ODM | 맞춤형 견과류 스프레드·페이스트 OEM/ODM 공개 | 미확인 | A | 저당·클린라벨 스프레드 케이스 검증 | https://www.factory-platform.com/manufacturer?category_code=12&tpf=product%2Flist |
| F041 | (주)청우식품 | 소스/시즈닝 제조 | HACCP 기반 소스·시즈닝·향신료 제조 노하우 공개 | 미확인 | A | 프랜차이즈 소스 OEM 여부 확인 | https://www.factory-platform.com/manufacturer?category_code=12&tpf=product%2Flist |
| F042 | 주식회사 화미 | 식자재/소스 제조 | 자체 제조시설과 식자재 포트폴리오 공개 | 미확인 | B | B2B 식자재 제조 범위와 OEM 가능 여부 확인 | https://www.factory-platform.com/manufacturer?category_code=12&tpf=product%2Flist |
| F043 | 소스나라 | 맞춤형 소스 OEM | 분말/엑기스 OEM 맞춤형 소스 제조 공개 | 미확인 | A | 소량 MOQ와 샘플 제작 리드타임 확인 | https://www.factory-platform.com/manufacturer?category_code=12&tpf=product%2Flist |
| F044 | (주)동원홈푸드 | 식품제조/푸드서비스 | 식품제조, 식자재유통, 푸드서비스 토탈 솔루션 공개 | 미확인 | B | 대형 B2B 후보로 별도 분리 | https://www.factory-platform.com/manufacturer?category_code=12&tpf=product%2Flist |
| F045 | (주)스마일에프앤디 | 육가공/건강기능/소스 제조 | 육가공·건강기능식품 전문 제조기업으로 공개 | 미확인 | B | 소스와 건강기능 품목의 실제 제조 구분 확인 | https://www.factory-platform.com/manufacturer?category_code=12&tpf=product%2Flist |
| F046 | (주)엠제이푸드 | 소스/육수 제조 | 막국수 양념, 육수, 명태회 무침 전문 제조업체 공개 | 미확인 | B | 냉면·막국수 프랜차이즈 소스 후보 확인 | https://www.factory-platform.com/manufacturer?category_code=12&tpf=product%2Flist |
| F047 | (주)쿠커페이스 | 소량 샘플/소분/식품첨가물 제조 | 스타트업·기획성 소량 샘플 제작 지원 공개 | 미확인 | A | MVP 샘플 제작 파트너 가능성 확인 | https://www.factory-platform.com/manufacturer?category_code=12&tpf=product%2Flist |
| F048 | 그램웰 | 간편 육수 제조 | HACCP 간편 육수 전문 제조업체 공개 | 미확인 | B | 육수 스틱/소스 제형 가능 여부 확인 | https://www.factory-platform.com/manufacturer?category_code=12&tpf=product%2Flist |
| F049 | 젠푸드 | 소스/음료/레토르트 제조 | 소스류, 음료류, 레토르트 식품 및 식품첨가물 전문 제조 공개 | 미확인 | B | 레토르트 소스 Case 003 후보 검증 | https://www.factory-platform.com/manufacturer?category_code=12&tpf=product%2Flist |
| F050 | (주)엠에스푸드 | 사골엑기스/소스 제조 | HACCP 기반 사골엑기스 전문 제조기업 공개 | 미확인 | B | 육수·엑기스 소스 후보로 상담 | https://www.factory-platform.com/manufacturer?category_code=12&tpf=product%2Flist |
| F051 | 주식회사 미쓰리 | 분말 소스 OEM/ODM | 떡볶이·요리 분말소스, OEM/ODM 의뢰 가능, HACCP/FSSC22000/VEGAN 공개 | 경기 광주 | A | 분말 소스 Case 003 최우선 상담 | https://biz.megashow.co.kr/shop/new_detail.php?uid=51645 |
| F052 | 농업회사법인 (주)찬누리비앤에프 | HMR/가공식품 후보 | HACCP 기반 전통식품/HMR/가공식품 파트너 등재 | 미확인 | B | HMR/전통식품 생산품목과 OEM 가능 여부 확인 | https://factory-platform.com/manufacturer?category_code=14&tpf=product%2Flist |
| F053 | 꿈틀식품 | 농수산 가공/원료 후보 | 농수산물 가공/원료, 생산·품질관리 데이터베이스 보유 메시지 공개 | 미확인 | C | 주력 품목과 OEM 가능 여부 확인 | https://factory-platform.com/manufacturer?category_code=14&tpf=product%2Flist |
| F054 | 푸드스토어 | 축산 가공 OEM/PB | 육가공 OEM 및 PB상품 생산 공개 | 미확인 | C | 육가공 PB/OEM은 MVP 후순위로 보관 | https://factory-platform.com/manufacturer?category_code=14&tpf=product%2Flist |
| F055 | (주)상신종합식품 | 돈까스/가공식품 OEM/ODM | 냉동식품 OEM/ODM 식품회사, HACCP/FSSC22000 공개 | 미확인 | C | 냉동식품 대형 후보로 분리 | https://ss-food.com/page/about/brand.php |
| F056 | (주)한만두식품 | 만두 OEM/ODM | OEM/ODM 공급 전문기업, HACCP 공개 | 미확인 | C | 냉동 만두 카테고리 확장 후보 | https://www.hanmandoo.com/research/research_010100.html |
| F057 | 주식회사 한국제면 | 생면 제조 | HACCP 기반 생면 전문 제조업체 공개 | 미확인 | C | 면류 OEM 가능 여부 확인 | https://factory-platform.com/manufacturer?category_code=14&tpf=product%2Flist |
| F058 | 완도바다식품 | 해조류 가공식품 | HACCP 기반 해조류 가공 전문 기업 공개 | 완도 | C | 해조류 원료·완제품 가능 범위 확인 | https://factory-platform.com/manufacturer?category_code=14&tpf=product%2Flist |
| F059 | (주)제이엘푸드 | 국밥/탕류 원팩 제조 | 국밥, 탕류 원팩 전문 제조회사 공개 | 미확인 | B | HMR 원팩 Case 후순위 검증 | https://factory-platform.com/manufacturer?category_code=14&tpf=product%2Flist |
| F060 | (주)대호식품 | 파우더 OEM/ODM | 파우더 OEM/ODM, 주요 생산품목, HACCP 생산 설비 공개 | 미확인 | A | 카페 파우더·스틱 분말 Case 002 후보 상담 | https://daehofood.co.kr/oem |
| F061 | RASA F&B | 분말 음료 OEM/ODM | 분말음료 전용 공장, ODM 계약, HACCP 인증 공개 | 경기 양주 | A | B2B 카페 파우더와 음료베이스 ODM 후보 확인 | https://teamad1009.cafe24.com/ |
| F062 | 대동고려삼(주) | 홍삼/건강기능식품 OEM/ODM | 홍삼제품 제조, 건강기능식품/건강지향식품, GMP/HACCP 공개 | 미확인 | B | 홍삼·건강식품 대형 후보로 분리 | https://ddkorea.co.kr/wp/?page_id=122 |
| F063 | 헬스앤라이프 | 건강식품 OEM/ODM | OEM/ODM 전문 기업, 건강즙/과채가공품, GMP/HACCP 이력 공개 | 미확인 | B | 건강즙·액상 제품 후보로 분리 | https://health-life.co.kr/%ED%9A%8C%EC%82%AC%EC%86%8C%EA%B0%9C/%ED%9A%8C%EC%82%AC%EA%B0%9C%EC%9A%94/ |
| F064 | (주)베지스타 | HMR/밀키트 OEM/ODM | HMR 제조, 밀키트 OEM/ODM, HACCP 인증 보도 | 인천/괴산 | B | 신선편이·밀키트 Case 확장 후보 검증 | https://www.e2news.com/news/articleView.html?idxno=242218 |
| F065 | 프레시지 | HMR/밀키트 OEM/ODM | 신선 HMR 공장과 대기업 브랜드 OEM/ODM 생산 기업정보 공개 | 경기 용인 | B | 대형 HMR 플랫폼 후보로 별도 분리 | https://www.albamon.com/jobs/detail-company/xeVlkp4onvGo3xo2oA2sWQ%3D%3D |
| F066 | 멜로시라바이오 | 건강기능식품 OEM/ODM | 건강기능식품 OEM/ODM, 자동화설비, HACCP/GMP 공개 | 미확인 | B | 건기식 제형과 MOQ 확인 | https://melosirabio.kr/default/online/03.php?sub=2&top=3 |
| F067 | 비앤비엘 | 건강식품/건강기능식품 OEM/ODM | GMP/HACCP 시설 기반 건강식품·건강기능식품 OEM/ODM 공개 | 미확인 | B | 원료 개발형 ODM 후보로 상담 | https://bnbl.info/ |
| F068 | 셀플러스 | 파우더/음료 OEM/ODM | 파우더류 HACCP, FSSC22000, ISO22000 인증과 OEM/ODM 메뉴 공개 | 미확인 | A | 파우더류 인증·B2B 생산 가능 범위 확인 | https://www.cellplus.kr/certification |
| F069 | (주)디알푸드솔루션 | 수산물 HMR/OEM | 수산물 HMR/OEM 및 클라이언트 맞춤형 제품생산 공개 | 미확인 | C | 수산 HMR은 MVP 후순위로 보관 | https://www.factory-platform.com/index.html?locale=ko&return_url=%2Fmanufacturer%3Ftpf%3Dproduct%2Fview%26category_code%3D10%2C14%26code%3D161 |
| F070 | 프로틴컴퍼니 | 프로틴/건강분말 OEM/ODM | 헬스보충제, 보조식품, 다이어트식품, 선식 등 건강분말 제조 공개 | 미확인 | A | 저당·고단백 Case 001/002 후보 확인 | https://www.factory-platform.com/index.html?locale=ko&return_url=%2Fmanufacturer%3Ftpf%3Dproduct%2Fview%26category_code%3D17%26code%3D214 |
| F071 | 픽테이블 | HMR/밀키트 기획·공급 | HACCP 인증 제조시설 협력 기반 HMR·밀키트 공급 공개 | 미확인 | B | HMR 브랜드/플랫폼 협력 후보로 확인 | https://biz.megashow.co.kr/shop/new_detail.php?uid=53280 |
| F072 | 주식회사 힐링 | 건강기능식품/건강식품 OEM/ODM | 건강식품 위탁생산, OEM/ODM, 분말스틱·타블렛, GMP/HACCP/FSSC22000 공개 | 미확인 | A | 분말스틱·타블렛 Case 002 최우선 상담 | https://www.healingu.net/ |
| F073 | 케이지랩 주식회사 | 건강기능식품 OEM/ODM | GMP/HACCP/FSSC22000 기반 다양한 제형 생산 및 OEM/ODM 공개 | 경기 양평 | B | 스틱젤리·분말·음료 제형 범위 확인 | https://kglab.co.kr/77 |
| F074 | 주식회사 셀타디움 | 건강기능식품/기타가공품 ODM/OEM | GMP/HACCP 보유 건강기능식품·기타가공품 ODM/OEM 전문회사 공개 | 미확인 | B | 대량 납품형 건기식 후보로 분리 | https://celtadium.com/%EC%9D%B8%EC%82%AC%EB%A7%90/ |
| F075 | 주식회사 이수바이오 | 건강기능식품/일반식품 OEM/ODM | 건강기능식품 및 일반식품 OEM/ODM, GMP/HACCP 기업정보 공개 | 경기 이천 | B | 건기식 원료·완제품 생산 범위 확인 | https://www.jobploy.kr/ko/company/isu-bio-co-ltd |
| F076 | 유니크바이오텍 | 프로폴리스/건강기능식품 OEM/ODM | OEM/ODM 파트너 역량, GMP/HACCP/FSSC22000/할랄 인증 공개 | 미확인 | B | 프로폴리스 소재·수출 대응 후보로 분리 | https://uniquebiotech.co.kr/certification |
| F077 | 렉스바이오 | 건강기능식품 OEM/ODM | 건강기능식품 사업, OEM/ODM, GMP/HACCP/ISO22000 공개 | 미확인 | B | 건기식 ODM 후보로 제형 확인 | https://www.rexbio.co.kr/kr/biz01.php |
| F078 | 바이오피던스 | 건강기능식품 OEM/ODM | 환 제형 제조, GMP/HACCP, OEM/ODM 서비스 기업정보 공개 | 경기 남양주 | B | 환 제형 전문 후보로 분리 | https://app.rndcircle.io/company/6480f28d-598b-5ce5-8483-9bc155be21f5 |
| F079 | 명인양념육 | 양념육/HMR OEM/ODM | 팩토리플랫폼 상세 기준 양념육 OEM/ODM 개발과 HACCP 시설 공개 | 미확인 | C | 축산/HMR 확장 후보로 보관 | https://factory-platform.com/manufacturer?category_code=11&code=588&tpf=product%2Fview |
| F080 | (주)이노프레시 | 종합 식품 제조 | HACCP 인증 종합 식품 제조업체 공개 | 미확인 | C | 종합식품 OEM 가능 여부 확인 | https://factory-platform.com/manufacturer?category_code=11&tpf=product%2Flist |
| F081 | (주)삼아푸드 | 소스 제조 | HACCP 인증 소스업체 공개 | 미확인 | B | 프랜차이즈 소스 OEM 가능 여부 확인 | https://www.factory-platform.com/manufacturer?category_code=12&is_sub=y&nature_url=manufacturer&orderBy=3&page=2&status=y&tpf=product%2Flist&url=manufacturer |
| F082 | (주)다고내푸드 | 소스 제조 | HACCP 인증 소스 제조업체 공개 | 미확인 | B | 소스 샘플 개발 가능 여부 확인 | https://www.factory-platform.com/manufacturer?category_code=12&is_sub=y&nature_url=manufacturer&orderBy=3&page=2&status=y&tpf=product%2Flist&url=manufacturer |
| F083 | (주)신성티엔에프 | 축산농축액/소스 제조 | 첨가물 없는 축산농축액 전문 제조 공개 | 미확인 | B | 육수·엑기스 소스 후보로 상담 | https://www.factory-platform.com/manufacturer?category_code=12&is_sub=y&nature_url=manufacturer&orderBy=3&page=2&status=y&tpf=product%2Flist&url=manufacturer |
| F084 | (주)데어리랜드 | 분말치즈 제조 | 분말치즈 전문 제조업체 공개 | 미확인 | B | 시즈닝·분말치즈 원료 후보 확인 | https://www.factory-platform.com/manufacturer?category_code=12&is_sub=y&nature_url=manufacturer&orderBy=3&page=2&status=y&tpf=product%2Flist&url=manufacturer |
| F085 | 하주푸드 | 소스 제조 | HACCP 기반 소스 전문 제조업체 공개 | 미확인 | B | 프랜차이즈 소스 생산 가능 범위 확인 | https://www.factory-platform.com/manufacturer?category_code=12&is_sub=y&nature_url=manufacturer&orderBy=3&page=2&status=y&tpf=product%2Flist&url=manufacturer |
| F086 | (주)정이푸드빌 | B2B 간편식 OEM/ODM | 20년 노하우의 B2B 간편식 OEM/ODM 제조, HACCP 공개 | 미확인 | B | 간편식·소스 복합 후보로 검증 | https://www.jungefood.com/ |
| F087 | 하남소스 | 프랜차이즈 소스 OEM/ODM | 프랜차이즈 OEM/ODM 파트너, 액상·분말소스, 소량/대량 제작 공개 | 미확인 | A | 소스 Case 003 소량/대량 제작 조건 확인 | https://hanamsc.com/ |
| F088 | 더밥 | 분말소스 OEM/ODM | 분말소스 OEM/ODM/임가공, 소량 생산, HACCP 공개 | 미확인 | A | 비건 분말소스와 소량 생산 조건 확인 | https://thebab.kr/page/index?tpl=etc%2Fb2b_info.html |
| F089 | 에스팩토리 | 소스 OEM/ODM | 소스 OEM/ODM 전문, 수출용 K-소스, HACCP 기반 공정 공개 | 경북 경산 | A | 수출용 K-소스 Case 003 후보 상담 | https://s-factory.kr/business/business_01.php |
| F090 | 주식회사 유명식품 | 소스 OEM/ODM | 브랜드용 소스 개발, PB상품, HACCP/스마트해썹 공개 | 미확인 | A | PB 소스 개발 및 샘플 프로세스 확인 | https://yumyeongfood.com/ |
| F091 | 소스토랑 | 소스 OEM/ODM | 소스 OEM/ODM 진행 절차와 샘플 제작 프로세스 공개 | 미확인 | B | 샘플비·MOQ·레시피 보안 조건 확인 | https://saucetaurant.com/article/%EA%B3%B5%EC%A7%80%EC%82%AC%ED%95%AD/1/3/ |
| F092 | 주식회사 한국에프에스 | 소스 원료/개발 | 푸드이음 기준 짜장·짬뽕소스, 튀김가루, 고객 맞춤 소스 개발 가능성 공개 | 미확인 | B | 소스 개발실과 OEM 가능 여부 확인 | https://www.foodpolis.kr/fbip/co/mat/info/srch/list.do |
| F093 | 원일그룹 | 식품 원료/소스 OEM/ODM | 브로슈어 기준 식품 OEM/ODM 회사, 중식·양식 소스군 공개 | 미확인 | B | 소스 원료·완제품 생산 범위 확인 | https://www.wonilfood.com/data/bbsData/17060801051.pdf |
| F094 | (주)예우당에프에스 | 프랜차이즈 소스 OEM/ODM | 프랜차이즈 전용 소스 OEM/ODM 제조 및 HACCP 기업정보 공개 | 미확인 | B | 프랜차이즈 전용 소스 후보로 상담 | https://www.jobploy.kr/ko/company/yewoodang-fs-co-ltd |
| F095 | 팡마니 | 베이커리/HMR/밀키트 제조 | HACCP 시설 기반 베이커리, 식사대용 HMR, 밀키트 생산 공개 | 미확인 | C | 베이커리·식사대용 HMR 후보 확인 | https://pangmani.com/Company-Introduction-1 |
| F096 | 마고푸드랩 | 디저트 OEM/ODM | HACCP 자체 제조시설 기반 디저트 OEM/ODM 공개 | 미확인 | A | 카페·프랜차이즈 디저트 OEM 후보 상담 | https://margofoodlab.com/oem.html |
| F097 | 골든브라운 | 베이커리/디저트 주문생산 | HACCP 인증 및 카페 디저트 주문생산 전문 회사 공개 | 미확인 | B | 카페 디저트 대량생산 조건 확인 | https://www.goldenbrown.co.kr/oem/ |
| F098 | 율성푸드랩 | 견과스프레드/김/과자 제조 | 자체 공장과 OEM/ODM 기반 상품 개발 공개 | 미확인 | A | 견과 스프레드·스낵 Case 001 후보 확인 | https://yulsungfoodlab.com/Foodmanufacturing |
| F099 | 튤립인터내셔널 | 음료 OEM/ODM | 음료 OEM/ODM, 탄산·비탄산, HACCP/FSSC22000/ISO22000 공개 | 미확인 | B | 음료 카테고리 확장 후보로 분리 | https://www.tulipint.com/%EB%B3%B5%EC%A0%9C-technology-facility?lang=ko |
| F100 | 진태식품 | 김스낵 OEM/ODM | 김스낵 제품 개발 OEM/ODM 공개 | 미확인 | B | 김스낵 PB/OEM 가능 범위 확인 | https://www.jintaefood.com/blank-3 |
| F101 | 자연과사람들 | 음료 OEM/ODM | 원스톱 음료 OEM/ODM 전문 기업, HACCP/FSSC22000/ISO 공개 | 미확인 | B | 음료 대형 OEM/ODM 후보로 분리 | https://www.innp.co.kr/about/ceo/ |
| F102 | 서울F&B | 음료 OEM/ODM | OEM/ODM Beverage Manufacturer 공개 | 강원 원주/횡성 | B | 음료·건기식 음료 대형 후보로 분리 | https://www.seoulfnb.com/ko |
| F103 | 삼양패키징 | 아셉틱 음료 OEM/ODM | Aseptic Filling OEM/ODM 프로세스 공개 | 충북 광혜원 | B | 아셉틱 음료 대형 생산 후보로 분리 | https://www.samyangpackaging.co.kr/kr/business/aseptic-filling |
| F104 | 씨알푸드 | 시리얼/시리얼바 OEM/ODM | ODM/OEM, 시리얼바·곡물가공 제품군, HACCP/GMP 공개 | 미확인 | A | 프로틴바·시리얼바 Case 001 후보 상담 | https://www.crfood.kr/page/22 |
| F105 | 스포츠바이오텍 | 단백질식품 OEM | 건강기능식품·일반식품 OEM 생산 공개 | 미확인 | A | 프로틴 쉐이크·건강분말 후보 확인 | https://sportsbiotec.com/ |
| F106 | 삼아인터내셔날 | 과자/시리얼 제조 | 과자류 OEM 생산 및 HACCP 이력 공개 | 미확인 | B | 시리얼·과자 OEM 가능 범위 확인 | https://www.samah.co.kr/develop/cms/?m_mode=view&pds_no=2022122609181007914 |
| F107 | 네추럴웨이 | 건강기능식품 OEM/ODM | OEM/ODM 상담, HACCP/GMP 음료라인 이력 공개 | 경기 포천 | B | 액상·음료형 건기식 후보 확인 | https://www.naturalway.co.kr/kr/company/history.php |
| F108 | 다원바이오텍 | 건강기능식품/일반식품 OEM/ODM | 건강기능식품·일반식품 OEM/ODM 공개 | 미확인 | B | 분말·환 제형 후보로 상담 | https://wellfiber.com/oem-odm/ |
| F109 | 큐어드 | 식품원료/제품개발 OEM/ODM | 식품원료 및 제품 개발 OEM/ODM 공개 | 미확인 | B | 원료 소재와 제형·포장 파트너 가능성 확인 | https://www.cured.co.kr/oem%C2%B7odm/ |
| F110 | 에스디에스코리아 | 김/김스낵 OEM/ODM | K-Food 김 제품 OEM/ODM 커스터마이징 공개 | 미확인 | B | 김스낵 수출형 후보 확인 | https://sdskorea.co.kr/business/kfood.php |
| F111 | 비에이치앤바이오 | 소스 OEM/ODM | 프랜차이즈 소스 OEM/ODM 생산과 FSSC22000/HACCP/ISO22000 보도 | 충북 진천 | B | 대형 프랜차이즈 소스 후보로 분리 | https://www.youthdaily.co.kr/news/article.html?no=187448 |
| F112 | 네오팜 | 음료 OEM/ODM | 팩토리플랫폼 음료 OEM/ODM 전문 제조업체 등재 | 미확인 | B | 음료 OEM/ODM 품목과 설비 확인 | https://factory-platform.com/manufacturer?category_code=&is_sub=y&nature_url=manufacturer&orderBy=1&page=2&status=y&tpf=&url=manufacturer |
| F113 | 농업회사법인 꼬숨식품(주) | 오일 OEM/ODM | HACCP 인증 오일 OEM/ODM 전문 제조업체 공개 | 미확인 | B | 오일 원료·소스 소재 후보 확인 | https://factory-platform.com/manufacturer?category_code=10&tpf=product%2Flist |
| F114 | (주)로열푸드코리아 | 김치/절임/반찬 제조 | HACCP 인증 김치·절임류·반찬류 제조 공개 | 미확인 | C | 반찬·절임류 HMR 확장 후보로 보관 | https://factory-platform.com/manufacturer?category_code=10&tpf=product%2Flist |
| F115 | 에이치앤티(HnT) | 누룽지/현미스낵 제조 | 유기농 현미 스낵 누룽지 제조 공개 | 미확인 | A | 저당·건강스낵 Case 001 후보 확인 | https://factory-platform.com/manufacturer?category_code=&is_sub=y&nature_url=manufacturer&orderBy=1&page=2&status=y&tpf=&url=manufacturer |
| F116 | (주)제이브이디저트 | 디저트 제조 | 디저트 전문 제조업체 등재 | 미확인 | B | 디저트 OEM/ODM 가능 여부 확인 | https://factory-platform.com/manufacturer?category_code=&is_sub=y&nature_url=manufacturer&orderBy=3&page=18&status=y&tpf=&url=manufacturer |
| F117 | (주)미트코리아 | HMR/원팩 OEM/ODM | HMR·원팩 제품 OEM/ODM 전문 제조업체 공개 | 미확인 | C | 축산 원팩 HMR 후보로 보관 | https://factory-platform.com/manufacturer?category_code=19&tpf=product%2Flist |
| F118 | 코어그린 | 분말육수/조미식품 OEM/ODM | 분말 조미식품 OEM/ODM, HACCP/FSSC22000/비건 공개 | 미확인 | A | 클린라벨 시즈닝·분말육수 후보 상담 | https://factory-platform.com/manufacturer?category_code=16&tpf=product%2Flist |
| F119 | 휴오스케이 | 바닐라 시럽 제조 | 바닐라 시럽 전문 제조회사 공개 | 미확인 | B | 카페 시럽·소스 후보 확인 | https://factory-platform.com/manufacturer?category_code=16&is_sub=y&nature_url=manufacturer&orderBy=1&page=2&status=y&tpf=product%2Flist&url=manufacturer |
| F120 | (주)푸드야 | 냉동과일/냉동야채 제조 | 냉동과일/냉동야채 전문 제조업체 공개 | 미확인 | C | 원료·토핑 후보로 보관 | https://factory-platform.com/manufacturer?category_code=16&is_sub=y&nature_url=manufacturer&orderBy=1&page=2&status=y&tpf=product%2Flist&url=manufacturer |
| F121 | (주)레인보우에프에스 | 소스 제조 | 소스 전문 제조업체 등재 | 미확인 | B | 프랜차이즈 소스 가능 여부 확인 | https://www.factory-platform.com/manufacturer?category_code=&is_sub=y&nature_url=manufacturer&orderBy=3&page=18&status=y&tpf=product%2Flist&url=manufacturer |
| F122 | (주)춘천장에프앤비 | 육개장 밀키트 제조 | 육개장 밀키트 전문 제조업체 공개 | 미확인 | C | 한식 밀키트 HMR 후보로 보관 | https://www.factory-platform.com/manufacturer?category_code=&is_sub=y&nature_url=manufacturer&orderBy=3&page=18&status=y&tpf=product%2Flist&url=manufacturer |
| F123 | (주)선도식품 | 한식/일식 소스 OEM/ODM | 한식/일식 소스 OEM/ODM 전문 제조업체 공개 | 미확인 | A | 소스 Case 003 후보 상담 | https://www.factory-platform.com/manufacturer?category_code=&is_sub=y&nature_url=manufacturer&orderBy=3&page=18&status=y&tpf=product%2Flist&url=manufacturer |
| F124 | (주)엠제이글로벌 | 커피 OEM/ODM | 원두·드립백·더치커피 OEM/ODM 제조업체 공개 | 미확인 | B | 커피/음료 확장 후보 확인 | https://www.factory-platform.com/manufacturer?category_code=13&tpf=product%2Flist |
| F125 | (주)하우스원푸드 | 제과제빵 제조 | HACCP 제과제빵/커피 제조업체 공개 | 미확인 | B | 베이커리 OEM 가능 범위 확인 | https://www.factory-platform.com/manufacturer?category_code=13&tpf=product%2Flist |
| F126 | 파우더컴퍼니 | 음료 파우더 제조 | 음료 파우더 전문 제조업체 공개 | 미확인 | A | 분말 음료 Case 002 후보 확인 | https://www.factory-platform.com/manufacturer?category_code=13&tpf=product%2Flist |
| F127 | (주)푸드코아 | 제과제빵/커피 제조 | 제과제빵/커피 제조사 등재 | 미확인 | B | 제과제빵 OEM 가능 여부 확인 | https://www.factory-platform.com/manufacturer?category_code=&field=content&is_sub=y&keyword=&nature_url=manufacturer&orderBy=3&page=17&s_area=&status=y&tpf=&url=manufacturer |
| F128 | 보은푸드 | 탕류 제조 | 탕류 전문 제조기업 공개 | 미확인 | C | 탕류 HMR 후보로 보관 | https://www.factory-platform.com/manufacturer?category_code=&field=content&is_sub=y&keyword=&nature_url=manufacturer&orderBy=3&page=17&s_area=&status=y&tpf=&url=manufacturer |
| F129 | 해돈계푸드 | 직화 원팩 제조 | 숯불 직화 원팩 전문 제조업체 공개 | 미확인 | C | 직화 원팩 HMR 후보로 보관 | https://www.factory-platform.com/manufacturer?category_code=&field=content&is_sub=y&keyword=&nature_url=manufacturer&orderBy=3&page=17&s_area=&status=y&tpf=&url=manufacturer |
| F130 | (주)라움푸드 | 갈비찜/찜닭 제조 | 갈비찜·찜닭 전문 제조업체 공개 | 미확인 | C | 축산 HMR 후보로 보관 | https://www.factory-platform.com/manufacturer?category_code=&field=content&is_sub=y&keyword=&nature_url=manufacturer&orderBy=3&page=17&s_area=&status=y&tpf=&url=manufacturer |
| F131 | (주)진성바이오 | 소스/향신료 제조 | 소스·향신료 전문 제조업체 공개 | 미확인 | B | 소스·시즈닝 Case 003 후보 확인 | https://www.factory-platform.com/manufacturer?category_code=&field=content&is_sub=y&keyword=&nature_url=manufacturer&orderBy=3&page=17&s_area=&status=y&tpf=&url=manufacturer |
| F132 | 영흥식품(주) | 소스/가공/원료 제조 | 소스·가공·원료 제조사 등재 | 미확인 | B | 소스·원료 후보로 세부 품목 확인 | https://www.factory-platform.com/manufacturer?category_code=&field=content&is_sub=y&keyword=&nature_url=manufacturer&orderBy=3&page=17&s_area=&status=y&tpf=&url=manufacturer |
| F133 | 브레드107 | 빵/냉동생지 제조 | HACCP 빵·냉동생지 제조 게시글 공개 | 미확인 | B | 냉동생지 OEM 가능 범위 확인 | https://factory-platform.com/community?category=N0tDYzZyTzg3S0NjNjdtMUwreTdwTzJVdkE9PQ%3D%3D |
| F134 | 델리베이 | 냉동생지 제조 | HACCP 냉동생지 전문 제조 게시글 공개 | 미확인 | B | 냉동생지 제조 조건 확인 | https://factory-platform.com/community?category=N0tDYzZyTzg3S0NjNjdtMUwreTdwTzJVdkE9PQ%3D%3D |
| F135 | (주)장생도라지 | 젤리스틱/레토르트 OEM/ODM | 젤리스틱 전문 생산과 HACCP 생산환경 공개 | 경남 하동 | B | 젤리스틱·건강식품 스틱 제형 후보 확인 | https://jangsaeng.clickn.co.kr/pages/oemodm |
| F136 | 에스디푸드 | 기능성 구미/젤리 OEM/ODM | 기능성 구미 OEM/ODM 전문기업, HACCP/GMP/FSSC22000 등 인증 공개 | 미확인 | A | 기능성 구미·스틱젤리 Case 002 후보 상담 | https://sdfoods.co.kr/index.php |
| F137 | 다이식품 | 캔디/젤리 OEM/ODM | 60년 전통 캔디·젤리 OEM/ODM 전문 제조업체 공개 | 미확인 | A | 캔디·젤리 소량/대량 OEM 조건 확인 | https://daifood.co.kr/ |
| F138 | 웰팜 | 건강즙/음료 OEM/ODM | 생산/OEM 및 OEM(ODM) 업무 공개 | 충북 음성 | B | 건강즙·액상 음료 OEM 후보 확인 | https://www.well-farm.co.kr/%EB%B3%B5%EC%A0%9C-%EC%83%9D%EC%82%B0-%EC%84%A4%EB%B9%84 |
| F139 | 제이와이네추럴 | 식품 OEM/ODM | 식품 OEM/ODM 전문생산기업, 콤부차·효소·스틱포장, HACCP 이력 공개 | 미확인 | A | 콤부차·효소·스틱포장 Case 002 후보 확인 | https://jynatural.co.kr/jynatural/company/history |
| F140 | 맑은내일 | 건강즙/음료/발효식품 OEM/ODM | OEM/ODM 문의와 액상차·과채주스 HACCP 인증 공개 | 경남 창원 | B | 액상차·과채주스 OEM/ODM 가능 범위 확인 | https://www.malgeunaeil.co.kr/22 |
| F141 | (유)신우S&F | 식품 OEM/ODM | OEM/ODM 전문기업 및 HACCP 품질관리시스템 공개 | 미확인 | B | 주력 품목과 생산 가능 범위 확인 | https://www.sinwoosnf.co.kr/factory/systems |
| F142 | (주)더젓갈 | 젓갈 OEM/ODM | 젓갈 제조 및 수출 OEM/ODM 전문기업 공지 공개 | 미확인 | C | 젓갈·수산가공 수출형 후보로 보관 | https://www.bjfood.co.kr/mobile/design/subpage/customer.php?id=454&mode=view&page=1&table=UT1418210665 |
| F143 | 그린푸드 | 냉동 가공식품 OEM/ODM | OEM/ODM 맞춤형 냉동식품 제품 개발 공개 | 미확인 | B | 냉동 HMR·튀김류 후보 상담 | https://greenfd.co.kr/ |
| F144 | 델리후레쉬 | 직화소스 OEM/ODM | 소스 OEM/ODM 생산과 HACCP 공정 공개 | 미확인 | A | 프랜차이즈 직화소스 Case 003 후보 확인 | https://www.delyfresh.co.kr/ |
| F145 | (주)니드플러스 | 식품 OEM/ODM | OEM/ODM 및 HACCP 인증 메뉴 공개 | 미확인 | B | 제품군·설비·MOQ 확인 | https://addneed.co.kr/page/oemodm.php |
| F146 | 팜텍코리아 | 건강기능식품/일반식품 OEM/ODM | OEM/ODM 기반 건강기능식품 및 일반식품 제조 보도 | 강원 원주 | B | 건강식품 OEM/ODM 후보로 공식 페이지 추가 확인 | https://www.todaypeople.co.kr/news/articleView.html?idxno=4000 |
| F147 | 웰츄럴바이오 | 건강식품 OEM | 대기업 OEM 제조 전문기업 및 HACCP/ISO/할랄 인증 보도 | 미확인 | B | 건강식품 대기업 OEM 후보로 분리 | https://www.todaytimes.co.kr/news/463806 |
| F148 | (주)케이지이 | 홍삼/액상 OEM/ODM | 홍삼·액상 제품 OEM/ODM 집중 보도 | 미확인 | B | 홍삼 액상 제형 후보로 확인 | https://www.kfdn.co.kr/72449 |
| F149 | 자연그대로(주) | 식품/건기식 OEM/ODM | 풀릭스 기준 OEM/ODM 및 HACCP 정보 공개 | 미확인 | B | 콤부차·건강식품 후보로 공식 출처 추가 확인 | https://www.poolix.io/company/120319 |
| F150 | (주)휴온스엔 | 건강기능식품/홍삼 OEM/ODM | 회사개요 기준 OEM·ODM 제품 및 주요 제형 공개 | 미확인 | B | 홍삼·액상·정제 제형 후보로 분리 | https://huonsfoodience.com/layout/kor/home.php?go=page0.0&mid=00 |
| F151 | 에치와이 hyLabs | 기능성 원료/OEM/ODM | hyLabs B2B에서 OEM/ODM 생산과 완제품 생산지원 공개 | 미확인 | B | 기능성 원료와 완제품 생산지원 범위 확인 | https://www.hy.co.kr/business/research-development/b2b/hylabs |
| F152 | (주)진화에프아이 | 식품 원료/가공 OEM 후보 | 식품 개발·제조·가공 및 HACCP 인증 공개 | 미확인 | C | 원료소재 OEM 가능 여부 확인 | https://www.jinhwagroup.com/default/business/business_1.php?sub=01&tit=02 |
| F153 | 주식회사 내츄럴코어 | 건강식품 OEM/ODM | 건강식품 OEM·ODM 전문업체 및 HACCP 공개 | 미확인 | B | 건강식품 소량/대량 생산 조건 확인 | https://www.naturalcore.ai/ |
| F154 | 엔피케이(주) | 건강기능식품/일반식품 OEM/ODM | OEM/ODM 문의 폼 기준 일반식품원료 및 다양한 제형 공개 | 미확인 | B | 제형별 생산 가능 범위와 인증 확인 | https://npkor.co.kr/issues |
| F155 | 농성원푸드 | 고춧가루/전통식품 제조 | HACCP과 전통식품 품질인증 공개 | 미확인 | C | 고춧가루 원료·B2B 납품 가능 범위 확인 | https://nswfood.co.kr/features |
| F156 | 약목참 | 액젓/식품소재 제조 | HACCP 시설 제조와 김치용 소재 메시지 공개 | 미확인 | C | 김치·소스 소재 원료 후보로 확인 | https://www.ymf.co.kr/ |
| F157 | 푸드트리 | 영유아/HMR 식품 제조 | 공시 기준 냉동식품 OEM/ODM 메뉴 개발 및 HACCP 공장 공개 | 경기 성남 | C | 케어푸드/HMR 후보로 보관 | https://kind.krx.co.kr/external/2025/05/15/000553/20250515001243/11013.htm |
| F158 | 성신비엔에프 | 만두/붕어빵/고로케 제조 | RnDcircle 기준 HACCP 생산시설과 만두·붕어빵·고로케 공개 | 미확인 | C | 냉동식품 OEM 가능 여부 확인 | https://app.rndcircle.io/company/36ce3cae-ebc2-5f2d-a018-89bdd8db3210 |
| F159 | 맥널티바이오 | 건강기능식품 OEM/ODM | OEM/ODM 메뉴 및 GMP/HACCP 인증 공개 | 미확인 | B | 건기식 제형과 MOQ 확인 | https://www.mcnultybio.co.kr/default/01/03.php |
| F160 | 빵터지는집 | 제과제빵 OEM/ODM | 제과제빵 OEM/ODM 및 HACCP 기반 위생관리 공개 | 미확인 | B | 편의점·프랜차이즈 베이커리 후보 확인 | https://bbtjbakery.com/ |
| F161 | 산들푸드 | 소스 OEM/ODM | 소스 제조·OEM/ODM·레시피 개발 전문기업과 HACCP 공개 | 미확인 | A | 소스 Case 003 후보 상담 | https://sandeulfood.com/haccp |
| F162 | (주)오그래농업회사법인 | 그래놀라/시리얼 OEM/ODM | OEM/ODM 및 ISO/HACCP 생산 설비 공개 | 미확인 | A | 저당·고단백 그래놀라 Case 001 후보 확인 | https://ograe.co.kr/oem-odm/ |
| F163 | 도우앤코/와이엔비컴퍼니 | 베이커리 B2B 제조 | HACCP 기반 베이커리 제조 시스템 및 B2B 솔루션 공개 | 미확인 | B | 베이커리 OEM/ODM 가능 여부 확인 | https://mirukku.com/bakery-factory/ |
| F164 | 나눔베이커리 | 쿠키/베이커리 제조 | HACCP 인증 쿠키·베이커리 제조공장 공개 | 미확인 | B | 카페 디저트 OEM 가능 여부 확인 | https://www.nanumbakery.co.kr/%EB%B3%B5%EC%A0%9C-%EB%B9%B5%EC%83%9D%EC%A7%80 |
| F165 | 베이커스팀 | 카페디저트 OEM/ODM | OEM/ODM 포트폴리오와 HACCP·ISO 제과제빵 공장 공개 | 미확인 | A | 카페 디저트 OEM/ODM 후보 상담 | https://www.bakers-team.kr/386 |
| F166 | (주)푸드웨어 | 만두 OEM/ODM | 국내 최대 만두 단일 품목 OEM/ODM 생산기업 공개 | 미확인 | B | 냉동 만두 대형 OEM/ODM 후보 확인 | https://www.foodware.co.kr/ |
| F167 | 네이처앤컬처 | 냉동식품 OEM/ODM | HACCP 인증 보유와 냉동식품 R&D 역량 공개 | 미확인 | B | 냉동식품·HMR OEM/ODM 후보 확인 | https://natureculturefoods.com/%ED%95%B5%EC%8B%AC%EC%97%AD%EB%9F%89/ |
| F168 | 아이진푸드 | 소스 OEM/ODM | 소스 제조 공정에서 OEM/ODM 방식 공개 | 미확인 | A | 소스 Case 003 후보 상담 | https://ijinfood.co.kr/sub/sub02_02.php |
| F169 | ANFL | 중화요리 소스 OEM/ODM | 소스 납품/OEM/ODM 및 파트너 제조 공개 | 미확인 | B | 중식 소스·프랜차이즈 납품 후보 확인 | https://www.anfl.co.kr/oem |
| F170 | (주)오뚜기 | B2B 종합식품 제조 후보 | 팩토리플랫폼 기준 다양한 B2B 고객 맞춤 제품·서비스 공개 | 미확인 | C | 대형 B2B 원료·완제품 후보로 분리 | https://factory-platform.com/manufacturer?category_code=19&tpf=product%2Flist |
| F171 | 서양푸드주식회사 | 냉동만두 제조 | 소비자24 기준 냉동식품 중 만두 HACCP 인증 사업자 공개 | 미확인 | C | OEM/ODM 가능 여부 확인 | https://www.consumer.go.kr/user/ftc/consumer/crtfc/1022/selectCrtfcInfo.do%3Bjsessionid%3D2dCCEYFpy2uJ5ey5ZcGqDsyC.ftc11?crtfcSn=HACP_000000000038830 |
| F172 | 한푸드코리아 | 냉동만두 제조 | 소비자24 기준 냉동식품 중 만두 HACCP 인증 사업자 공개 | 미확인 | C | OEM/ODM 가능 여부 확인 | https://www.consumer.go.kr/user/ftc/consumer/crtfc/1022/selectCrtfcInfo.do%3Bjsessionid%3DB1XxMoFiRUFjJ4A0hBM1cdh9.ftc21?beginDe=&brno=&certInstNmS=&certSttusNmS=&crtfcCdS=10&crtfcCnS=&crtfcInsttCdS=&crtfcNoS=&crtfcSn=HACP_000000000000079&crtfcSttusS=&crtfcTypeCdS=&delYnS=N&endDe=&entrpsAdresS=&entrpsNmS=&firstCrtfcNoS=&imgFlag=&insttId=&mnfacrS=&modlNmS=&page=1632&productNmS=&row=25 |
| F173 | 대장경식품 | 떡/농식품 OEM | 식품 제조 및 OEM 생산, HACCP 인증 공개 | 경남 합천 | B | 떡·쌀가공 Case 확장 후보 확인 | https://djgfood.co.kr/layout/basic/html/company.html |
| F174 | 미도식품 | 식품 OEM/ODM | OEM/ODM과 HACCP 기반 위생관리 공개 | 미확인 | B | 주력 품목과 생산 가능 범위 확인 | https://www.midofd.co.kr/ |
| F175 | (주)디에스푸드웰 | 육수/당류가공품 OEM/ODM | OEM/ODM 메뉴와 HACCP 인증서 공개 | 미확인 | A | 육수·코인육수·분말류 Case 003 후보 확인 | https://dsfoodwell.co.kr/ |
| F176 | (주)우복당식품 | 한식 HMR OEM/ODM | HACCP 기반 공장 운영과 OEM/ODM 경쟁력 보도 | 미확인 | B | 한식 HMR·레토르트 후보로 확인 | https://www.mssnews.com/news/articleView.html?idxno=586 |
| F177 | 원스그룹 한닢쿡 | 코인육수/동결건조 제조 | 동결건조·타정 설비와 FSSC22000·HACCP 인증 공개 | 미확인 | A | 코인육수·분말육수 Case 003 후보 확인 | https://onesgroup.co.kr/27 |
| F178 | (주)한미양행 | 건강기능식품 OEM/ODM | 카탈로그 기준 GMP/HACCP 제조관리 공개 | 미확인 | B | 대형 건기식 후보로 제형·MOQ 확인 | https://hanmiyh.mycafe24.com/wp-content/uploads/2024/08/catalog_ko.pdf |
| F179 | 대원헬스케어 | 건강기능식품 OEM/ODM | Global OEM & ODM 전문기업 비전과 GMP 공개 | 미확인 | B | 건기식 제형과 인증 상세 확인 | https://daewonhealthcare.com/ |
| F180 | (주)진성에프엠 | 식품원료/HMR OEM/ODM | RnDcircle 기준 식품 원료 OEM/ODM 및 HACCP/FSSC22000 공개 | 경기 화성 | A | 식품 원료·HMR B2B 후보로 상담 | https://app.rndcircle.io/company/4b0a2100-e8a7-5ae2-9eb3-93d7ea245ed8 |
| F181 | 사임당푸드 | 전통떡/디저트떡 제조 | 전통떡·디저트떡 제품군 공개 | 미확인 | B | 떡 OEM/ODM 가능 여부 확인 | https://saimdangfood.co.kr/ |
| F182 | 서비푸드 | 단백질식품 OEM/ODM/OBM | 단백질 식품 OEM/ODM/OBM 제조사 매칭 파트너 공개 | 미확인 | A | 단백질 식품 Case 001/002 후보 확인 | https://seobifood.com/company |
| F183 | 주식회사 연 | 레토르트/HMR OEM/ODM | 식품 OEM/ODM 서비스와 레토르트·소스·즉석조리식품 HACCP 공개 | 미확인 | A | 레토르트·HMR Case 확장 후보 확인 | https://yeon2008.com/ |
| F184 | 한양제너럴푸드 | 육가공/편의점 OEM/ODM | 기업정보 기준 HACCP·OEM/ODM·편의점 유통 공개 | 미확인 | B | 육가공·닭가슴살 후보로 확인 | https://www.jobploy.kr/ko/company/hanyang-general-food |
| F185 | JMJ푸드 떡불킹 | 분말소스 OEM/ODM | HACCP 직영 소스 생산 공장과 분말 소스 OEM/ODM 공개 | 미확인 | A | 떡볶이 분말소스 Case 003 후보 확인 | https://jmjfood.co.kr/ |
| F186 | (주)산마을 | 동결건조/절임식품 OEM/ODM | 기업정보 기준 OEM/ODM 생산 및 기술 지원 공개 | 미확인 | B | 동결건조 원료·스낵 후보 확인 | https://www.jobploy.kr/ko/company/C0000009101 |
| F187 | (유)삼각에프엠씨 | 음료 OEM/ODM | OEM/ODM 음료 생산 능력과 HACCP/FSSC22000/ISO22000 공개 | 미확인 | B | 음료·파우치 OEM/ODM 후보 확인 | https://www.komachine.com/ko/companies/samgak-fmc |
| F188 | 건우에프피 | 건강기능성 원료/식품소재 OEM/ODM | 스마트공장 사례 기준 식품 소재 OEM/ODM 제조기업 공개 | 미확인 | C | 식품소재 후보로 공식 출처 추가 확인 | https://smhaccp-blog.com/21 |
| F189 | 파머스에프앤에스 | 김치/절임배추 제조 | 스마트공장 사례 기준 김치 제품 생산 기업 공개 | 미확인 | C | 김치·절임류 후보로 공식 출처 추가 확인 | https://smhaccp-blog.com/21 |
| F190 | 흥신식품 | 면류 제조 | 스마트공장 사례 기준 면류 생산 식품가공기업 공개 | 미확인 | C | 면류 OEM 가능 여부 확인 | https://smhaccp-blog.com/21 |
| F191 | 아름터 | 액상/분말 OEM/ODM | 식품 제조기업 OEM/ODM 전문 제조 시스템과 HACCP 공개 | 미확인 | B | 액상·분말 제조 후보로 공식 출처 추가 확인 | https://buza.biz/bbs/board.php?bo_table=changup_news&sca=%EC%B0%BD%EC%97%85%EA%B2%BD%EC%98%81%EC%8B%A4%EB%AC%B4&wr_id=8331 |
| F192 | 산정푸드 | 절임식품 OEM/ODM | 팩토리플랫폼 기준 OEM/ODM 서비스 및 절임식품 공개 | 미확인 | B | 김밥 단무지·절임류 후보 확인 | https://www.factory-platform.com/member/login?category_code=&nature_url=manufacturer%2Fai-recommended-manufacturers&orderBy=rand&page=744&return_url=%2Fmanufacturer%2Fai-recommended-manufacturers%3Ftpf%3Dproduct%2Flist_ai&tpf=&url=manufacturer%2Fai-recommended-manufacturers |
| F193 | (주)웰파인 | 가공/음료/제과제빵 후보 | 팩토리플랫폼 기준 HACCP 가공·제과제빵·음료 제조사 공개 | 강원 횡성 | C | 주력 품목과 OEM/ODM 가능 여부 확인 | https://www.factory-platform.com/member/login?category_code=&nature_url=manufacturer%2Fai-recommended-manufacturers&orderBy=rand&page=744&return_url=%2Fmanufacturer%2Fai-recommended-manufacturers%3Ftpf%3Dproduct%2Flist_ai&tpf=&url=manufacturer%2Fai-recommended-manufacturers |
| F194 | 서림농원 | 절임식품 제조 | 팩토리플랫폼 기준 절임 제품 전문 제조업체 공개 | 강원 정선 | C | 절임식품 OEM 가능 여부 확인 | https://www.factory-platform.com/member/login?category_code=&nature_url=manufacturer%2Fai-recommended-manufacturers&orderBy=rand&page=744&return_url=%2Fmanufacturer%2Fai-recommended-manufacturers%3Ftpf%3Dproduct%2Flist_ai&tpf=&url=manufacturer%2Fai-recommended-manufacturers |
| F195 | 가나식품 | 파우더/분말소스 OEM/ODM | 공개 SNS 기준 OEM/ODM 생산과 파우더·분말소스 품목 확인 | 미확인 | B | 공식 홈페이지 또는 사업자 출처 추가 확인 | https://www.instagram.com/p/C8vxqyGvUli/ |
| F196 | 제이케이글로벌 | 김/해조류 제조 | 공식 페이지 기준 김·해조류 제조 사업 확인 | 미확인 | C | 조미김·해조 스낵 OEM 가능 여부 확인 | https://www.jkginc.co.kr/page/?pid=about_01 |
| F197 | (주)주스템 | 식음료 OEM/ODM | 팩토리플랫폼 기준 식음료 OEM/ODM 제조사 공개 | 미확인 | B | 과채주스·액상차·건강즙 후보 확인 | https://factory-platform.com/manufacturer?category_code=15&code=601&tpf=product%2Fview |
| F198 | (주)신영푸드 / 그루버드 | 음료 OEM | 팩토리플랫폼 기준 음료 제조 후보 공개 | 미확인 | C | 음료 OEM 범위와 MOQ 확인 | https://factory-platform.com/manufacturer?category_code=&is_sub=y&nature_url=manufacturer&orderBy=1&page=3&status=y&tpf=&url=manufacturer |
| F199 | 대양식품(주) | 음료/환/분말 OEM/ODM | 팩토리플랫폼 기준 음료·환·분말 OEM/ODM 후보 공개 | 미확인 | B | 건강즙·분말·환 Case 002 후보 확인 | https://factory-platform.com/manufacturer?category_code=15&is_sub=y&nature_url=manufacturer&orderBy=1&page=4&status=y&tpf=product%2Flist&url=manufacturer |
| F200 | (주)신영허브 | 분말/타정 제조 | 팩토리플랫폼 기준 분말·타정 제조 후보 공개 | 미확인 | B | 분말·정제 제형 가능 범위 확인 | https://factory-platform.com/manufacturer?category_code=15&is_sub=y&nature_url=manufacturer&orderBy=3&page=1&status=y&tpf=product%2Flist&url=manufacturer |
| F201 | (주)놀이터 팩토리D1 | 과채주스/액상차 OEM/ODM | 팩토리플랫폼 기준 과채주스·액상차 OEM/ODM 후보 공개 | 미확인 | B | 음료 샘플 제작과 소량 MOQ 확인 | https://factory-platform.com/manufacturer?category_code=15&is_sub=y&nature_url=manufacturer&orderBy=3&page=1&status=y&tpf=product%2Flist&url=manufacturer |
| F202 | (주)JC대경 | 커피/베이커리 OEM | 팩토리플랫폼 기준 커피·베이커리 제조 후보 공개 | 미확인 | C | 카페 디저트·원두 OEM 가능 여부 확인 | https://factory-platform.com/manufacturer?category_code=&is_sub=y&nature_url=manufacturer&orderBy=1&page=3&status=y&tpf=&url=manufacturer |
| F203 | (주)뉴지코리아 | 드립백/커피백 제조 | 팩토리플랫폼 기준 드립백·커피백 제조 후보 공개 | 미확인 | C | 카페 PB 드립백 MOQ 확인 | https://factory-platform.com/manufacturer?category_code=&is_sub=y&nature_url=manufacturer&orderBy=1&page=3&status=y&tpf=&url=manufacturer |
| F204 | 농업회사법인 (주)대경햄 | 수제햄 제조 | 팩토리플랫폼 기준 수제햄 제조 후보 공개 | 미확인 | C | 육가공 OEM 가능 여부 확인 | https://factory-platform.com/manufacturer?category_code=14&tpf=product%2Flist |
| F205 | (주)에프원에프앤비 | 냉동수산/유탕류 제조 | 팩토리플랫폼 기준 냉동수산·유탕류 제조 후보 공개 | 미확인 | C | 냉동 수산 HMR 후보 확인 | https://www.factory-platform.com/manufacturer?category_code=10&is_sub=y&nature_url=manufacturer&orderBy=1&page=4&status=y&tpf=product%2Flist&url=manufacturer |
| F206 | 밥순삭 꽃게야 | 순살 꽃게장 제조 | 팩토리플랫폼 기준 순살 꽃게장 제조 후보 공개 | 미확인 | C | 양념게장·수산 반찬 OEM 가능 여부 확인 | https://www.factory-platform.com/manufacturer?category_code=10&is_sub=y&nature_url=manufacturer&orderBy=1&page=4&status=y&tpf=product%2Flist&url=manufacturer |
| F207 | 두리푸드 | 짠지/절임식품 제조 | 팩토리플랫폼 기준 짠지·절임식품 제조 후보 공개 | 미확인 | C | 절임 반찬 OEM 가능 여부 확인 | https://www.factory-platform.com/manufacturer?category_code=10&is_sub=y&nature_url=manufacturer&orderBy=1&page=4&status=y&tpf=product%2Flist&url=manufacturer |
| F208 | 해나라수산 | 수산물 가공 | 팩토리플랫폼 기준 수산물 가공 후보 공개 | 미확인 | C | 수산 가공품 OEM 가능 여부 확인 | https://www.factory-platform.com/manufacturer?category_code=10&is_sub=y&nature_url=manufacturer&orderBy=1&page=4&status=y&tpf=product%2Flist&url=manufacturer |
| F209 | (주)형돈유통 | 새우장/전복장 제조 | 팩토리플랫폼 기준 새우장·전복장 제조 후보 공개 | 미확인 | C | 수산 장류 반찬 OEM 가능 여부 확인 | https://www.factory-platform.com/manufacturer?category_code=10&is_sub=y&nature_url=manufacturer&orderBy=1&page=4&status=y&tpf=product%2Flist&url=manufacturer |
| F210 | (주)빅쭌식품 | 김치 제조 | 팩토리플랫폼 기준 김치 제조 후보 공개 | 미확인 | C | 김치 OEM·수출 포장 가능 여부 확인 | https://www.factory-platform.com/manufacturer?category_code=10&is_sub=y&nature_url=manufacturer&orderBy=1&page=4&status=y&tpf=product%2Flist&url=manufacturer |
| F211 | (주)옳은 | 샐러드/샌드위치 제조 | 팩토리플랫폼 기준 샐러드·샌드위치 제조 후보 공개 | 미확인 | C | 신선편의식품 B2B 납품 가능 여부 확인 | https://www.factory-platform.com/manufacturer?category_code=10&is_sub=y&nature_url=manufacturer&orderBy=1&page=4&status=y&tpf=product%2Flist&url=manufacturer |
| F212 | 주식회사 동방푸드마스타 | 소스/조미식품 제조 | 풀릭스 기준 소스·조미식품 제조 기업 공개 | 미확인 | A | 소스·시즈닝 대형 B2B 후보 확인 | https://www.poolix.io/company/167685 |
| F213 | 농심태경 | 식품소재/소스/시즈닝 제조 | 공식 페이지 기준 식품소재·소스·시즈닝 사업 확인 | 미확인 | A | 시즈닝·소스·식품소재 후보 확인 | https://www.nongshimtk.com/ |
| F214 | BSF KOREA | 식품 OEM/ODM | 공식 페이지 기준 식품 OEM/ODM 서비스 공개 | 미확인 | B | 제조 품목·인증·MOQ 확인 | https://bsfkorea.co.kr/en/oem-odm/oem-odm/ |
| F215 | (주)엔푸드 | 건강식품 OEM/ODM | 보도 기준 건강식품 OEM/ODM 기업 공개 | 미확인 | B | 건강식품 제형과 인증 범위 확인 | https://www.job-post.co.kr/news/articleView.html?idxno=43188 |
| F216 | 아모제산업 | HMR/소스/농수축산가공 제조 | 보도 기준 HMR·소스·농수축산가공 제조 역량 공개 | 미확인 | B | HMR·소스 B2B 후보 확인 | https://foodbank.co.kr/news/articleView.html?idxno=29491 |
| F217 | 인산가 | 죽염/건강식품 OEM/ODM | 공시 기준 죽염·건강식품 OEM/ODM 사업 확인 | 미확인 | B | 죽염 기반 소재·건강식품 후보 확인 | https://kind.krx.co.kr/external/2021/11/08/000169/20211108000401/11013.htm |
| F218 | 거북이달린다 | 수산물가공 OEM/ODM | 셀러나우 기준 수산물가공 OEM/ODM 후보 공개 | 미확인 | C | 수산 가공품 소량 OEM 여부 확인 | https://www.sellernow.co.kr/?categoryId=474&menuId=61 |
| F219 | (주)다원 | 식음료 OEM/ODM | 사람인 기업정보 기준 식음료 OEM/ODM 후보 확인 | 미확인 | C | 공식 홈페이지와 품목 범위 추가 확인 | https://m.saramin.co.kr/job-search/company-info-view?csn=TVRaTUVrdFdabm5GelN5NUFyN25iUT09 |
| F220 | (주)오투바이오 | 건강식품/음료베이스 제조 | 공식 자료 기준 건강식품·음료베이스 제조 품목 확인 | 미확인 | B | 음료베이스·과채가공품 후보 확인 | https://o2bio.co.kr/wp-content/uploads/O2bio-catalog_Korea.pdf |
| F221 | 아이엠김치 | 김치 제조/수출 후보 | 협력 소식 기준 김치 제조·수출 후보 확인 | 미확인 | C | 김치 OEM 가능 여부와 수출 조건 확인 | https://sdskorea.co.kr/business/kfood.php |
| F222 | 삼육식품 | 조미김/종합식품 후보 | 보도 기준 조미김 등 종합식품 후보 확인 | 미확인 | C | 조미김·PB 생산 가능 여부 확인 | https://www.thinkfood.co.kr/news/articleView.html?idxno=100551 |
| F223 | 국애찬푸드 R&D | 즉석조리/HMR 제조 | 팩토리플랫폼 기준 즉석조리·HMR 제조 후보 공개 | 미확인 | C | HMR 반찬 OEM 가능 여부 확인 | https://factory-platform.com/manufacturer/ai-recommended-manufacturers?category_code=%EA%B0%80%EA%B3%B5&nature_url=manufacturer%2Fai-recommended-manufacturers&orderBy=rand&page=172&tpf=product%2Flist_ai&url=manufacturer%2Fai-recommended-manufacturers |
| F224 | 덕양식품 | 절임/조림/소스 제조 | 팩토리플랫폼 기준 절임·조림·소스 제조 후보 공개 | 미확인 | C | 반찬·소스 OEM 가능 여부 확인 | https://factory-platform.com/manufacturer/ai-recommended-manufacturers?category_code=%EA%B0%80%EA%B3%B5&nature_url=manufacturer%2Fai-recommended-manufacturers&orderBy=rand&page=172&tpf=product%2Flist_ai&url=manufacturer%2Fai-recommended-manufacturers |
| F225 | (주)비앤비코리아 | 식물성 오일 제조 | 팩토리플랫폼 기준 식물성 오일 제조 후보 공개 | 미확인 | C | 식물성 오일 원료·완제품 공급 가능 여부 확인 | https://factory-platform.com/manufacturer/ai-recommended-manufacturers?category_code=%EC%86%8C%EC%8A%A4&nature_url=manufacturer%2Fai-recommended-manufacturers&orderBy=rand&page=115&tpf=product%2Flist_ai&url=manufacturer%2Fai-recommended-manufacturers |
| F226 | 농업법인 (주)옻가네 | 건강식품 OEM/ODM | 공식 홈페이지 기준 건강기능식품·건강보조식품 OEM/ODM 제조 공개 | 미확인 | B | 건강식품 제형·MOQ·인증 범위 확인 | https://www.okannae.com/ |
| F227 | (주)원일바이오 | 건강식품 OEM/ODM | 공식 식품부 페이지 기준 OEM/ODM 가능 및 GMP/HACCP/ISO 인증 공개 | 충북 제천 | A | 분말·액상스틱 Case 002 후보 확인 | https://food.wonilbio.com/ |
| F228 | (주)정풍 | 소스/HMR/식품소재 제조 | 공식 홈페이지 기준 맞춤형 소스 OEM/ODM과 분말·HMR 제품 공개 | 미확인 | A | 소스·HMR·분말 소재 대형 B2B 후보 확인 | https://jeongpoong.com/ |
| F229 | (주)상일 | 음료 OEM/ODM | 공식 홈페이지 기준 PB 음료 개발·생산·납품 공개 | 경남 거창 | B | 캔·병 음료 PB/OEM 가능 조건 확인 | https://isangil.com/kr/ |
| F230 | (주)소스플러스 | 조미식품/소스 OEM/ODM | 공식 홈페이지 기준 비즈니스 OEM/ODM 메뉴와 조미식품 제조·HACCP 설비 공개 | 미확인 | B | 소스 OEM/ODM 개발 범위와 MOQ 확인 | https://xn--vl2b19o9xaba276u.kr/ |
| F231 | (주)서해식품 | 맞춤형 소스 OEM/ODM | 공식 홈페이지 기준 맞춤형 소스 OEM/ODM 개발과 HACCP 인증 공개 | 경기 부천 | B | 소량 레시피·대량 생산 대응 범위 확인 | https://seohaefoods.com/ |
| F232 | (주)우리식품 | 소스 OEM | 공식 페이지 기준 대용량 업소용 제품 OEM 생산 및 HACCP 공개 | 미확인 | B | 참소스·업소용 소스 OEM 후보 확인 | https://chamsauce.com/bbs/pro04.php |
| F233 | (주)제이푸드서비스 | 분말/소스 제조 | 팩토리플랫폼 기준 HACCP 분말 전문 제조업체 공개 | 미확인 | C | 분말 전문 제조 품목과 OEM 가능 여부 확인 | https://www.factory-platform.com/manufacturer?category_code=12&is_sub=y&nature_url=manufacturer&orderBy=3&page=2&status=y&tpf=product%2Flist&url=manufacturer |
| F234 | (주)토담 / 브랜드 푸드담 | 축산물/소스/가공 제조 | 팩토리플랫폼 기준 축산물·소스·가공 제조 후보 공개 | 미확인 | C | 소스·가공식품 OEM 가능 여부 확인 | https://www.factory-platform.com/manufacturer?category_code=12&is_sub=y&nature_url=manufacturer&orderBy=3&page=2&status=y&tpf=product%2Flist&url=manufacturer |
| F235 | 바이오디피씨(주) | 건강기능식품 OEM/ODM | 팩토리플랫폼 상세 기준 건강기능식품 OEM/ODM 및 GMP/HACCP 공개 | 미확인 | B | 환·분말·정제 Case 002 후보 확인 | https://www.factory-platform.com/manufacturer?category_code=15&code=140&tpf=product%2Fview |
| F236 | 조리쿡 | 소스 OEM/ODM | 공식 홈페이지 기준 주문자제작 OEM 방식과 소스 제조 공개 | 경기 파주 | B | 소포장 소스 OEM과 레시피 개발 조건 확인 | https://www.joricook.co.kr/ |
| F237 | 선학FS | 소스 제조 | 팩토리플랫폼 기준 소스 제조 후보 공개 | 미확인 | C | 소스 OEM/ODM 가능 여부 확인 | https://www.factory-platform.com/manufacturer?category_code=12&is_sub=y&nature_url=manufacturer&orderBy=3&page=2&status=y&tpf=product%2Flist&url=manufacturer |
| F238 | 농업회사법인 케이푸드원 주식회사 | 소스 제조 | 팩토리플랫폼 신규 파트너 기준 소스 제조 후보 공개 | 미확인 | C | 농산물 기반 소스 OEM 가능 여부 확인 | https://www.factory-platform.com/manufacturer?category_code=12&is_sub=y&nature_url=manufacturer&orderBy=3&page=2&status=y&tpf=product%2Flist&url=manufacturer |
| F239 | (주)케이알푸드 | 외식/HMR 제조 | 팩토리플랫폼 기준 외식 종합 전문 식품기업 공개 | 미확인 | C | 외식형 HMR·축산물 가공 가능 여부 확인 | https://factory-platform.com/manufacturer?category_code=11&tpf=product%2Flist |
| F240 | (주)드림바이오 | 건강기능/일반식품 제조 | 팩토리플랫폼 기준 건강기능식품·일반식품 전문 제조업체 공개 | 미확인 | C | 건강식품 제조 품목과 OEM 가능 여부 확인 | https://factory-platform.com/manufacturer?category_code=15&is_sub=y&nature_url=manufacturer&orderBy=3&page=1&status=y&tpf=product%2Flist&url=manufacturer |
| F241 | (주)농업회사법인 웨일즈 / 브랜드 즙문가 | 과채주스 제조 | 팩토리플랫폼 기준 HACCP 과채주스 전문 제조업체 공개 | 미확인 | B | 과채주스 OEM/ODM 가능 여부 확인 | https://factory-platform.com/manufacturer?category_code=15&is_sub=y&nature_url=manufacturer&orderBy=3&page=1&status=y&tpf=product%2Flist&url=manufacturer |
| F242 | (주)푸른들 | 건강기능식품 제조 | 팩토리플랫폼 기준 GMP/HACCP 건강기능식품 제조사 공개 | 제주 | C | 제주 원료 기반 건강식품 후보 확인 | https://factory-platform.com/manufacturer?category_code=15&is_sub=y&nature_url=manufacturer&orderBy=3&page=1&status=y&tpf=product%2Flist&url=manufacturer |
| F243 | 자연농장 | 과채/홍삼음료 OEM/ODM | 팩토리플랫폼 기준 과채·홍삼 음료 및 분말 배합 OEM/ODM 공개 | 미확인 | B | 과채·홍삼음료·분말 배합 후보 확인 | https://factory-platform.com/manufacturer?category_code=15&is_sub=y&nature_url=manufacturer&orderBy=3&page=1&status=y&tpf=product%2Flist&url=manufacturer |
| F244 | 해오름에프앤비(F&B) | 수제청/착즙주스 제조 | 팩토리플랫폼 기준 HACCP 수제청·착즙주스 전문 제조업체 공개 | 미확인 | B | 수제청·착즙주스 소량 생산 가능 여부 확인 | https://factory-platform.com/manufacturer?category_code=15&is_sub=y&nature_url=manufacturer&orderBy=3&page=2&status=y&tpf=product%2Flist&url=manufacturer |
| F245 | (주)푸른나무 | 음료베이스 제조 | 팩토리플랫폼 기준 HACCP 음료베이스 전문 제조업체 공개 | 미확인 | B | 카페·음료베이스 B2B 후보 확인 | https://factory-platform.com/manufacturer?category_code=15&is_sub=y&nature_url=manufacturer&orderBy=3&page=2&status=y&tpf=product%2Flist&url=manufacturer |
| F246 | (주)고려원인삼 | 홍삼/인삼 제품 제조 | 팩토리플랫폼 기준 HACCP/GMP 홍삼·인삼 제품 전문 제조업체 공개 | 미확인 | B | 홍삼·인삼 건강식품 후보 확인 | https://factory-platform.com/manufacturer?category_code=15&is_sub=y&nature_url=manufacturer&orderBy=3&page=2&status=y&tpf=product%2Flist&url=manufacturer |
| F247 | (주)고철남 | 액상건강식품 제조 | 팩토리플랫폼 기준 HACCP/GMP 액상건강식품 전문 제조업체 공개 | 미확인 | B | 액상 건강식품 파우치 후보 확인 | https://factory-platform.com/manufacturer?category_code=15&is_sub=y&nature_url=manufacturer&orderBy=3&page=2&status=y&tpf=product%2Flist&url=manufacturer |
| F248 | (주)스위트컵 | 음료베이스 제조 | 팩토리플랫폼 기준 HACCP 음료베이스 전문 제조업체 공개 | 미확인 | B | 카페 음료 베이스 OEM 가능 여부 확인 | https://factory-platform.com/manufacturer?category_code=15&is_sub=y&nature_url=manufacturer&orderBy=3&page=2&status=y&tpf=product%2Flist&url=manufacturer |
| F249 | (주)핀코퍼레이션 | 과채주스 제조 | 팩토리플랫폼 기준 특허기술 과채주스 제조사 공개 | 미확인 | B | 과채주스 기술·생산 조건 확인 | https://factory-platform.com/manufacturer?category_code=15&is_sub=y&nature_url=manufacturer&orderBy=3&page=2&status=y&tpf=product%2Flist&url=manufacturer |
| F250 | (유)강산농원 | 전통발효식품 제조 | 팩토리플랫폼 기준 보성 전통발효식품 제조기업 공개 | 전남 보성 | C | 발효식품·음료형 제품 후보 확인 | https://factory-platform.com/manufacturer?category_code=15&is_sub=y&nature_url=manufacturer&orderBy=3&page=2&status=y&tpf=product%2Flist&url=manufacturer |
| F251 | (주)리빙라이프 | 단백질/그래놀라 제조 | 팩토리플랫폼 기준 단백질 쉐이크·시리얼·그래놀라 전문 제조업체 공개 | 미확인 | B | 단백질·그래놀라 Case 001 후보 확인 | https://www.factory-platform.com/manufacturer?category_code=13&tpf=product%2Flist |
| F252 | (주)베노프하우스 | 프로틴바/프로틴스낵 OEM | 팩토리플랫폼 기준 최소 MOQ 프로틴바·프로틴스낵 OEM 제조업체 공개 | 미확인 | A | 저당·고단백 스낵 Case 001 우선 후보 확인 | https://www.factory-platform.com/manufacturer?category_code=13&tpf=product%2Flist |
| F253 | (주)BC2000 | 베이커리 제조 | 팩토리플랫폼 기준 HACCP 베이커리 전문 제조업체 공개 | 미확인 | C | 베이커리 OEM 가능 여부 확인 | https://www.factory-platform.com/manufacturer?category_code=13&tpf=product%2Flist |
| F254 | (주)베리랜드 | 원두 제조 | 팩토리플랫폼 기준 원두 제조업체 공개 | 미확인 | C | 원두 B2B·OEM 가능 여부 확인 | https://www.factory-platform.com/manufacturer?NaPm=ct%3Dmdoxahg7%7Cci%3DER37f17f0b-6cb1-11f0-8482-821da0f47b5f%7Ctr%3Dsa%7Chk%3Dab9c3ee8a02dc6875bc1d77870fc562baaeadc4e%7Cnacn%3D1VfECYhKf08ZD&category_code=13&is_sub=y&nature_url=manufacturer&orderBy=1&page=4&status=y&tpf=product%2Flist&url=manufacturer |
| F255 | (유)새만금에프앤비 | 즉석조리/제빵/과자류 제조 | 팩토리플랫폼 기준 HACCP 즉석조리식품·제빵·과자류 제조업체 공개 | 미확인 | C | 즉석조리·제빵 복합 후보 확인 | https://www.factory-platform.com/manufacturer?NaPm=ct%3Dmdoxahg7%7Cci%3DER37f17f0b-6cb1-11f0-8482-821da0f47b5f%7Ctr%3Dsa%7Chk%3Dab9c3ee8a02dc6875bc1d77870fc562baaeadc4e%7Cnacn%3D1VfECYhKf08ZD&category_code=13&is_sub=y&nature_url=manufacturer&orderBy=1&page=4&status=y&tpf=product%2Flist&url=manufacturer |
| F256 | 화이트도우 | 빵류 제조 | 팩토리플랫폼 기준 HACCP 빵류 전문 제조업체 공개 | 미확인 | C | 빵류 OEM 가능 여부 확인 | https://www.factory-platform.com/manufacturer?NaPm=ct%3Dmdoxahg7%7Cci%3DER37f17f0b-6cb1-11f0-8482-821da0f47b5f%7Ctr%3Dsa%7Chk%3Dab9c3ee8a02dc6875bc1d77870fc562baaeadc4e%7Cnacn%3D1VfECYhKf08ZD&category_code=13&is_sub=y&nature_url=manufacturer&orderBy=1&page=4&status=y&tpf=product%2Flist&url=manufacturer |
| F257 | (주)넥타홀딩스 / 브랜드 모건커피 | 드립백/원두 OEM/ODM | 팩토리플랫폼 기준 드립백·티백·원두 OEM/ODM 제조업체 공개 | 미확인 | B | 드립백·원두 PB 후보 확인 | https://www.factory-platform.com/manufacturer?NaPm=ct%3Dmdoxahg7%7Cci%3DER37f17f0b-6cb1-11f0-8482-821da0f47b5f%7Ctr%3Dsa%7Chk%3Dab9c3ee8a02dc6875bc1d77870fc562baaeadc4e%7Cnacn%3D1VfECYhKf08ZD&category_code=13&is_sub=y&nature_url=manufacturer&orderBy=1&page=4&status=y&tpf=product%2Flist&url=manufacturer |
| F258 | 서바나도나쓰 | 츄러스 제조 | 팩토리플랫폼 기준 HACCP 츄러스 전문 제조업체 공개 | 미확인 | C | 츄러스·냉동 디저트 후보 확인 | https://www.factory-platform.com/manufacturer?NaPm=ct%3Dmdoxahg7%7Cci%3DER37f17f0b-6cb1-11f0-8482-821da0f47b5f%7Ctr%3Dsa%7Chk%3Dab9c3ee8a02dc6875bc1d77870fc562baaeadc4e%7Cnacn%3D1VfECYhKf08ZD&category_code=13&is_sub=y&nature_url=manufacturer&orderBy=1&page=4&status=y&tpf=product%2Flist&url=manufacturer |
| F259 | (주)쿱 | 액상커피 제조 | 팩토리플랫폼 기준 액상커피 전문 제조업체 공개 | 미확인 | C | 액상커피 B2B 공급 가능 여부 확인 | https://www.factory-platform.com/manufacturer?NaPm=ct%3Dmdoxahg7%7Cci%3DER37f17f0b-6cb1-11f0-8482-821da0f47b5f%7Ctr%3Dsa%7Chk%3Dab9c3ee8a02dc6875bc1d77870fc562baaeadc4e%7Cnacn%3D1VfECYhKf08ZD&category_code=13&is_sub=y&nature_url=manufacturer&orderBy=1&page=4&status=y&tpf=product%2Flist&url=manufacturer |
| F260 | (주)에프엠프렌즈 | 랩샌드 제조 | 팩토리플랫폼 기준 HACCP 랩샌드 전문 제조업체 공개 | 미확인 | C | 신선 샌드위치·랩샌드 B2B 후보 확인 | https://www.factory-platform.com/manufacturer?NaPm=ct%3Dmdoxahg7%7Cci%3DER37f17f0b-6cb1-11f0-8482-821da0f47b5f%7Ctr%3Dsa%7Chk%3Dab9c3ee8a02dc6875bc1d77870fc562baaeadc4e%7Cnacn%3D1VfECYhKf08ZD&category_code=13&is_sub=y&nature_url=manufacturer&orderBy=1&page=4&status=y&tpf=product%2Flist&url=manufacturer |
| F261 | (주)프레스네이처 | 가공/건강기능음료 제조 | 팩토리플랫폼 기준 HACCP 가공·건강기능/음료 제조 후보 공개 | 미확인 | B | 건강기능음료 제조 품목과 OEM 가능 여부 확인 | https://www.factory-platform.com/manufacturer?category_code=&is_sub=y&nature_url=manufacturer&orderBy=3&page=15&status=y&tpf=product%2Flist&url=manufacturer |
| F262 | 제천인삼약초영농조합법인 천수인 | 인삼/건강음료 제조 | 팩토리플랫폼 상세 기준 제천인삼약초영농조합법인 천수인 공개 | 미확인 | B | 인삼·약초 건강음료 후보 확인 | https://www.factory-platform.com/index.html?locale=ko&return_url=%2Fmanufacturer%3Ftpf%3Dproduct%2Fview%26category_code%3D15%26code%3D455 |
| F263 | (주)경주생약 | 건강기능/음료 제조 | 팩토리플랫폼 기준 HACCP 건강기능/음료 제조사 공개 | 미확인 | B | 생약 기반 건강식품·음료 후보 확인 | https://factory-platform.com/manufacturer?category_code=15&is_sub=y&nature_url=manufacturer&orderBy=1&page=4&status=y&tpf=product%2Flist&url=manufacturer |
| F264 | (주)엠에스씨 | 식품첨가물/음료 OEM/ODM | 팩토리플랫폼 기준 다양한 식품 전문 ODM/OEM 및 일반식품·건강기능식품 생산 가능 공개 | 미확인 | A | 음료·젤리·스틱 ODM/OEM 대형 후보 확인 | https://www.factory-platform.com/manufacturer?category_code=12&nature_url=manufacturer&orderBy=3&page=3&status=y&tpf=product%2Flist&url=manufacturer |
| F265 | (주)에르코스 농업회사법인 | 비건/제과제빵 제조 | 팩토리플랫폼 기준 HACCP 비건 제품 전문 제조업체 공개 | 미확인 | B | 비건 디저트·제과 후보 확인 | https://www.factory-platform.com/manufacturer?NaPm=ct%3Dmd3suhpl%7Cci%3DER610b51b2-6113-11f0-92f0-0aca1d163bde%7Ctr%3Dsa%7Chk%3D63c24212dca7f76ab049a066e24f22bb5d7efa0f%7Cnacn%3DSoXQBsQSuk5K&category_code=13&is_sub=y&nature_url=manufacturer&orderBy=3&status=y&tpf=product%2Flist&url=manufacturer |
| F266 | (주)넥스푸드 | 견과류/디저트 제조 | 팩토리플랫폼 기준 HACCP 견과류 및 디저트 전문 제조업체 공개 | 미확인 | B | 견과류·디저트 Case 001 후보 확인 | https://www.factory-platform.com/manufacturer?NaPm=ct%3Dmd3suhpl%7Cci%3DER610b51b2-6113-11f0-92f0-0aca1d163bde%7Ctr%3Dsa%7Chk%3D63c24212dca7f76ab049a066e24f22bb5d7efa0f%7Cnacn%3DSoXQBsQSuk5K&category_code=13&nature_url=manufacturer&orderBy=3&page=2&status=y&tpf=product%2Flist&url=manufacturer |
| F267 | 필배치 | 원두 로스팅 OEM/ODM | 팩토리플랫폼 기준 맞춤형 로스팅 원두 OEM/ODM 전문 제조업체 공개 | 미확인 | B | 원두 로스팅 PB/OEM 후보 확인 | https://www.factory-platform.com/manufacturer?NaPm=ct%3Dmd3suhpl%7Cci%3DER610b51b2-6113-11f0-92f0-0aca1d163bde%7Ctr%3Dsa%7Chk%3D63c24212dca7f76ab049a066e24f22bb5d7efa0f%7Cnacn%3DSoXQBsQSuk5K&category_code=13&nature_url=manufacturer&orderBy=3&page=2&status=y&tpf=product%2Flist&url=manufacturer |
| F268 | 스위티 | 수제 캔디 제조 | 팩토리플랫폼 기준 HACCP 수제 캔디 전문 제조업체 공개 | 미확인 | C | 수제 캔디 제조 후보 확인 | https://www.factory-platform.com/manufacturer?category_code=14&nature_url=manufacturer&orderBy=3&page=2&status=y&tpf=product%2Flist&url=manufacturer |
| F269 | 부라보식품 | 수제꼬치 제조 | 팩토리플랫폼 기준 HACCP 수제꼬치 전문 제조업체 공개 | 미확인 | C | 수제꼬치·축산가공 후보 확인 | https://www.factory-platform.com/manufacturer?category_code=14&nature_url=manufacturer&orderBy=3&page=2&status=y&tpf=product%2Flist&url=manufacturer |
| F270 | 횡성하동식품 | 유탕/수산물/양념육 제조 | 팩토리플랫폼 기준 HACCP 유탕·수산물·양념육 전문 제조업체 공개 | 미확인 | C | 유탕·수산물·양념육 후보 확인 | https://www.factory-platform.com/manufacturer?category_code=14&nature_url=manufacturer&orderBy=3&page=2&status=y&tpf=product%2Flist&url=manufacturer |
| F271 | 딩동쿡 | 양념 쭈꾸미 제조 | 팩토리플랫폼 기준 HACCP 양념 쭈꾸미 전문 제조업체 공개 | 미확인 | C | 양념 수산 HMR 후보 확인 | https://www.factory-platform.com/manufacturer?category_code=14&nature_url=manufacturer&orderBy=3&page=2&status=y&tpf=product%2Flist&url=manufacturer |
| F272 | (주)신양식품 | 떡류 제조 | 팩토리플랫폼 기준 HACCP 떡류 전문 제조업체 공개 | 미확인 | C | 떡류 OEM 가능 여부 확인 | https://www.factory-platform.com/manufacturer?category_code=14&nature_url=manufacturer&orderBy=3&page=2&status=y&tpf=product%2Flist&url=manufacturer |
| F273 | 농업회사법인 (주)에쓰와이푸드 | 종합 식품 가공 | 팩토리플랫폼 기준 HACCP 종합 식품 가공 업체 공개 | 미확인 | C | 종합 식품가공 품목과 OEM 가능 여부 확인 | https://www.factory-platform.com/manufacturer?category_code=14&nature_url=manufacturer&orderBy=3&page=2&status=y&tpf=product%2Flist&url=manufacturer |
| F274 | (주)하랑커뮤니티 | 냉동피자/식빵 제조 | 팩토리플랫폼 기준 HACCP 냉동피자·식빵 전문 제조업체 공개 | 미확인 | B | 냉동피자·식빵 B2B 후보 확인 | https://www.factory-platform.com/manufacturer?NaPm=ct%3Dmd3suhpl%7Cci%3DER610b51b2-6113-11f0-92f0-0aca1d163bde%7Ctr%3Dsa%7Chk%3D63c24212dca7f76ab049a066e24f22bb5d7efa0f%7Cnacn%3DSoXQBsQSuk5K&category_code=13&is_sub=y&nature_url=manufacturer&orderBy=3&status=y&tpf=product%2Flist&url=manufacturer |
| F275 | 스윗드림 / 브랜드 나나스캔디 | 수제캔디 제조 | 팩토리플랫폼 기준 HACCP 수제캔디 전문 제조업체 공개 | 미확인 | C | 캔디류 소량 제조 후보 확인 | https://www.factory-platform.com/manufacturer?NaPm=ct%3Dmd3suhpl%7Cci%3DER610b51b2-6113-11f0-92f0-0aca1d163bde%7Ctr%3Dsa%7Chk%3D63c24212dca7f76ab049a066e24f22bb5d7efa0f%7Cnacn%3DSoXQBsQSuk5K&category_code=13&is_sub=y&nature_url=manufacturer&orderBy=3&status=y&tpf=product%2Flist&url=manufacturer |
| F276 | MISS LEE | 디저트 제조 | 팩토리플랫폼 기준 HACCP 디저트 전문 제조업체 공개 | 미확인 | C | 디저트 OEM 가능 여부 확인 | https://www.factory-platform.com/manufacturer?NaPm=ct%3Dmd3suhpl%7Cci%3DER610b51b2-6113-11f0-92f0-0aca1d163bde%7Ctr%3Dsa%7Chk%3D63c24212dca7f76ab049a066e24f22bb5d7efa0f%7Cnacn%3DSoXQBsQSuk5K&category_code=13&is_sub=y&nature_url=manufacturer&orderBy=3&status=y&tpf=product%2Flist&url=manufacturer |
| F277 | 포와 | 수제 디저트 제조 | 팩토리플랫폼 기준 생초콜릿·휘낭시에·르뱅쿠키 수제 디저트 제조업체 공개 | 미확인 | C | 수제 디저트 제조 후보 확인 | https://www.factory-platform.com/manufacturer?NaPm=ct%3Dmd3suhpl%7Cci%3DER610b51b2-6113-11f0-92f0-0aca1d163bde%7Ctr%3Dsa%7Chk%3D63c24212dca7f76ab049a066e24f22bb5d7efa0f%7Cnacn%3DSoXQBsQSuk5K&category_code=13&is_sub=y&nature_url=manufacturer&orderBy=3&status=y&tpf=product%2Flist&url=manufacturer |
| F278 | (주)키토라푸드 | 제과제빵/커피 제조 | 팩토리플랫폼 신규 파트너 기준 HACCP 제과제빵/커피 제조 후보 공개 | 미확인 | C | 제과제빵 제조 품목 확인 | https://www.factory-platform.com/manufacturer?NaPm=ct%3Dmd3suhpl%7Cci%3DER610b51b2-6113-11f0-92f0-0aca1d163bde%7Ctr%3Dsa%7Chk%3D63c24212dca7f76ab049a066e24f22bb5d7efa0f%7Cnacn%3DSoXQBsQSuk5K&category_code=13&nature_url=manufacturer&orderBy=3&page=2&status=y&tpf=product%2Flist&url=manufacturer |
| F279 | 헷지 허그 딜레마 | 제과제빵/커피 제조 | 팩토리플랫폼 신규 파트너 기준 HACCP 제과제빵/커피 제조 후보 공개 | 미확인 | C | 제과제빵 제조 품목 확인 | https://www.factory-platform.com/manufacturer?NaPm=ct%3Dmd3suhpl%7Cci%3DER610b51b2-6113-11f0-92f0-0aca1d163bde%7Ctr%3Dsa%7Chk%3D63c24212dca7f76ab049a066e24f22bb5d7efa0f%7Cnacn%3DSoXQBsQSuk5K&category_code=13&nature_url=manufacturer&orderBy=3&page=2&status=y&tpf=product%2Flist&url=manufacturer |
| F280 | (주)엠스푸드 | 제과제빵/커피 제조 | 팩토리플랫폼 신규 파트너 기준 HACCP 제과제빵/커피 제조 후보 공개 | 미확인 | C | 제과제빵 제조 품목 확인 | https://www.factory-platform.com/manufacturer?NaPm=ct%3Dmd3suhpl%7Cci%3DER610b51b2-6113-11f0-92f0-0aca1d163bde%7Ctr%3Dsa%7Chk%3D63c24212dca7f76ab049a066e24f22bb5d7efa0f%7Cnacn%3DSoXQBsQSuk5K&category_code=13&nature_url=manufacturer&orderBy=3&page=2&status=y&tpf=product%2Flist&url=manufacturer |
| F281 | (주)유라에프에스 | 육가공/냉동식품 제조 | 팩토리플랫폼 상세 기준 육가공 냉동식품 생산라인 및 HACCP 공개 | 충북 음성 | B | 육가공 냉동식품 B2B 후보 확인 | https://www.factory-platform.com/manufacturer?code=284&tpf=product%2Fview |
| F282 | (주)주원 | 축산물 가공 | 팩토리플랫폼 기준 HACCP 축산물 가공 후보 공개 | 미확인 | C | 축산물 가공 후보 확인 | https://www.factory-platform.com/manufacturer?category_code=11&nature_url=manufacturer&orderBy=3&page=2&status=y&tpf=product%2Flist&url=manufacturer |
| F283 | (주)맥우드림육가공 | 축산물 가공 | 팩토리플랫폼 기준 HACCP 축산물 가공 후보 공개 | 미확인 | C | 육가공 OEM 가능 여부 확인 | https://www.factory-platform.com/manufacturer?category_code=11&nature_url=manufacturer&orderBy=3&page=2&status=y&tpf=product%2Flist&url=manufacturer |
| F284 | (주)씨엔에스테크 / 브랜드 찬솔 | 분쇄가공육/양념육 OEM/ODM | 팩토리플랫폼 기준 분쇄가공육·양념육·기타수산물 OEM/ODM 전문 제조업체 공개 | 미확인 | B | 양념육·수산물 OEM/ODM 후보 확인 | https://www.factory-platform.com/manufacturer?category_code=14&nature_url=manufacturer&orderBy=3&page=2&status=y&tpf=product%2Flist&url=manufacturer |
| F285 | (주)푸디노에프앤디 | 가공식품 제조 | 팩토리플랫폼 AI 추천 기준 가공식품 제조 후보 공개 | 미확인 | C | 가공식품 제조 품목과 OEM 가능 여부 확인 | https://factory-platform.com/manufacturer/ai-recommended-manufacturers?category_code=%EA%B0%80%EA%B3%B5&nature_url=manufacturer%2Fai-recommended-manufacturers&orderBy=rand&page=318&tpf=product%2Flist_ai&url=manufacturer%2Fai-recommended-manufacturers |
| F286 | 다솜식품 | 가공식품 제조 | 팩토리플랫폼 AI 추천 기준 가공식품 제조 후보 공개 | 미확인 | C | 가공식품 제조 품목과 OEM 가능 여부 확인 | https://factory-platform.com/manufacturer/ai-recommended-manufacturers?category_code=%EA%B0%80%EA%B3%B5&nature_url=manufacturer%2Fai-recommended-manufacturers&orderBy=rand&page=318&tpf=product%2Flist_ai&url=manufacturer%2Fai-recommended-manufacturers |
| F287 | GSE푸드 | 가공식품 제조 | 팩토리플랫폼 AI 추천 기준 가공식품 제조 후보 공개 | 미확인 | C | 가공식품 제조 품목과 OEM 가능 여부 확인 | https://factory-platform.com/manufacturer/ai-recommended-manufacturers?category_code=%EA%B0%80%EA%B3%B5&nature_url=manufacturer%2Fai-recommended-manufacturers&orderBy=rand&page=318&tpf=product%2Flist_ai&url=manufacturer%2Fai-recommended-manufacturers |
| F288 | 타이런트 커피 컴퍼니 | 원두 로스팅 OEM/ODM | 팩토리플랫폼 상세 기준 원두 로스팅 OEM/ODM 전문 업체 공개 | 인천 | B | 원두 로스팅 PB/OEM 후보 확인 | https://www.factory-platform.com/index.html?locale=ko&return_url=%2Fmanufacturer%3Ftpf%3Dproduct%2Fview%26category_code%3D13%26code%3D320 |
| F289 | (주)꼬루인터내셔널 | 한식 디저트/스낵 OEM | 팩토리플랫폼 게시글 기준 유통·납품·OEM 가능 HACCP 공장 및 제품 라인업 공개 | 미확인 | B | 한식 디저트·안주류 OEM 후보 확인 | https://www.factory-platform.com/member/login?board_code=11&code=595&tpf=board%2Fview |
| F290 | 코라커피 | 원두 B2B OEM/ODM | 팩토리플랫폼 상세 기준 원두 B2B OEM/ODM 전문 제조업체 공개 | 경기 포천 | B | 원두 B2B OEM/ODM 후보 확인 | https://www.factory-platform.com/index.html?locale=ko&return_url=%2Fmanufacturer%3Ftpf%3Dproduct%2Fview%26category_code%3D13%26code%3D456 |
| F291 | (주)태양E&S | 파운드케익 제조 | 팩토리플랫폼 상세 기준 파운드케익 전문 제조업체 공개 | 미확인 | C | 파운드케익 제조 후보 확인 | https://www.factory-platform.com/index.html?locale=ko&return_url=%2Fmanufacturer%3Ftpf%3Dproduct%2Fview%26category_code%3D13%26code%3D125 |
| F292 | 다원F&S / 브랜드 장수천 | 축산물 제조 | 팩토리플랫폼 신규 파트너 기준 축산물 제조 후보 공개 | 미확인 | C | 축산물 가공 후보 확인 | https://factory-platform.com/manufacturer?category_code=11&tpf=product%2Flist |
| F293 | 주식회사 비젼식품 | 축산물/가공 제조 | 팩토리플랫폼 신규 파트너 기준 축산물·가공 제조 후보 공개 | 미확인 | C | 축산물·가공 제조 후보 확인 | https://factory-platform.com/manufacturer?category_code=11&tpf=product%2Flist |
| F294 | 삼초에프앤비 | 축산물 제조 | 팩토리플랫폼 신규 파트너 기준 축산물 제조 후보 공개 | 미확인 | C | 축산물 제조 후보 확인 | https://factory-platform.com/manufacturer?category_code=11&tpf=product%2Flist |
| F295 | 이지쿡(주) | 축산물/소스/가공 제조 | 팩토리플랫폼 신규 파트너 기준 축산물·소스·가공 제조 후보 공개 | 미확인 | B | 축산물 소스 HMR 후보 확인 | https://factory-platform.com/manufacturer?category_code=11&tpf=product%2Flist |
| F296 | 퍼플랜드 | 커피 로스팅/파우더 제조 | 팩토리플랫폼 기준 HACCP 커피 로스팅·파우더 전문 제조업체 공개 | 미확인 | B | 커피 파우더·로스팅 후보 확인 | https://www.factory-platform.com/manufacturer?NaPm=ct%3Dmd3suhpl%7Cci%3DER610b51b2-6113-11f0-92f0-0aca1d163bde%7Ctr%3Dsa%7Chk%3D63c24212dca7f76ab049a066e24f22bb5d7efa0f%7Cnacn%3DSoXQBsQSuk5K&category_code=13&nature_url=manufacturer&orderBy=3&page=2&status=y&tpf=product%2Flist&url=manufacturer |
| F297 | (주)디저트스토리 | 프리미엄 디저트 제조 | 팩토리플랫폼 기준 HACCP 수제 프리미엄 디저트 전문 제조업체 공개 | 미확인 | C | 수제 디저트 OEM 가능 여부 확인 | https://www.factory-platform.com/manufacturer?NaPm=ct%3Dmd3suhpl%7Cci%3DER610b51b2-6113-11f0-92f0-0aca1d163bde%7Ctr%3Dsa%7Chk%3D63c24212dca7f76ab049a066e24f22bb5d7efa0f%7Cnacn%3DSoXQBsQSuk5K&category_code=13&nature_url=manufacturer&orderBy=3&page=2&status=y&tpf=product%2Flist&url=manufacturer |
| F298 | (주)ABP홀딩스 | 베이커리 제조 | 팩토리플랫폼 기준 베이커리 전문 제조업체 공개 | 미확인 | C | 베이커리 제조 후보 확인 | https://www.factory-platform.com/manufacturer?NaPm=ct%3Dmd3suhpl%7Cci%3DER610b51b2-6113-11f0-92f0-0aca1d163bde%7Ctr%3Dsa%7Chk%3D63c24212dca7f76ab049a066e24f22bb5d7efa0f%7Cnacn%3DSoXQBsQSuk5K&category_code=13&nature_url=manufacturer&orderBy=3&page=2&status=y&tpf=product%2Flist&url=manufacturer |
| F299 | (주)굿투베이크 | 베이커리 제조 | 팩토리플랫폼 기준 HACCP 베이커리 전문 제조업체 공개 | 미확인 | C | 베이커리 OEM 가능 여부 확인 | https://www.factory-platform.com/manufacturer?NaPm=ct%3Dmd3suhpl%7Cci%3DER610b51b2-6113-11f0-92f0-0aca1d163bde%7Ctr%3Dsa%7Chk%3D63c24212dca7f76ab049a066e24f22bb5d7efa0f%7Cnacn%3DSoXQBsQSuk5K&category_code=13&nature_url=manufacturer&orderBy=3&page=2&status=y&tpf=product%2Flist&url=manufacturer |
| F300 | (주)스마트푸드 / 브랜드 김가네 영웅갈비 | 양념육 OEM/ODM | 팩토리플랫폼 기준 HACCP 양념육 OEM/ODM 전문 제조업체 공개 | 미확인 | B | 양념육 OEM/ODM 후보 확인 | https://www.factory-platform.com/manufacturer?category_code=11&nature_url=manufacturer&orderBy=3&page=2&status=y&tpf=product%2Flist&url=manufacturer |
| F301 | (주)예길식품 | 김치 제조 | 팩토리플랫폼 기준 HACCP 김치 전문 제조업체 공개 | 미확인 | C | 김치 OEM 가능 여부 확인 | https://www.factory-platform.com/manufacturer?category_code=10&is_sub=y&nature_url=manufacturer&orderBy=1&page=4&status=y&tpf=product%2Flist&url=manufacturer |
| F302 | (주)웰빙라이프 | 농산물 임가공 | 팩토리플랫폼 기준 농산물 세척·건조·분쇄 전문 임가공업체 공개 | 미확인 | C | 농산물 세척·건조·분쇄 임가공 후보 확인 | https://www.factory-platform.com/manufacturer?category_code=10&is_sub=y&nature_url=manufacturer&orderBy=1&page=4&status=y&tpf=product%2Flist&url=manufacturer |
| F303 | 심플리 | 고형화 소스 제조 | 팩토리플랫폼 기준 고추장·액상·분말 소스를 슬라이스 고형화 상품으로 제조·납품 가능 업체 공개 | 미확인 | B | 고형화 소스·분말소스 후보 확인 | https://www.factory-platform.com/manufacturer?category_code=14&is_sub=y&nature_url=manufacturer&orderBy=3&page=6&status=y&tpf=product%2Flist&url=manufacturer |
| F304 | (주)이랜드이츠 부평공장 | 밀키트/소스 OEM/ODM | 팩토리플랫폼 기준 밀키트 및 소스 OEM/ODM 전문 제조업체 공개 | 미확인 | A | 밀키트·소스 OEM/ODM 우선 후보 확인 | https://www.factory-platform.com/manufacturer?category_code=14&is_sub=y&nature_url=manufacturer&orderBy=3&page=6&status=y&tpf=product%2Flist&url=manufacturer |
| F305 | 주식회사 뉴밀 | 건강식품 OEM | 팩토리플랫폼 기준 건강식품·건강기능식품 OEM 전문 기업 공개 | 미확인 | B | 건강식품 OEM 제형·MOQ 확인 | https://factory-platform.com/manufacturer?category_code=19&is_sub=y&nature_url=manufacturer&orderBy=3&page=2&status=y&tpf=product%2Flist&url=manufacturer |
| F306 | 농업회사 법인 아람뜰 주식회사 | 곡물소재/OEM 제조 | 팩토리플랫폼 기준 곡물 원료 가공 및 다품종 소량 맞춤 OEM 대응 가능 공개 | 미확인 | A | 곡물 소재·다품종 소량 OEM 후보 확인 | https://factory-platform.com/manufacturer?category_code=19&is_sub=y&nature_url=manufacturer&orderBy=3&page=2&status=y&tpf=product%2Flist&url=manufacturer |
| F307 | (주)서림원 | 냉동 밀키트 OEM | 팩토리플랫폼 기준 냉동 밀키트 OEM 전문 제조공장 공개 | 미확인 | A | 냉동 밀키트 OEM 우선 후보 확인 | https://www.factory-platform.com/manufacturer?category_code=14&is_sub=y&nature_url=manufacturer&orderBy=3&page=5&status=y&tpf=product%2Flist&url=manufacturer |
| F308 | 삼제이김치 | 김치 제조 | 팩토리플랫폼 충남 제조사 페이지 기준 HACCP 김치 전문 제조업체 공개 | 충남 | C | 김치 OEM 가능 여부 확인 | https://www.factory-platform.com/manufacturer?category_code=&field=content&is_sub=y&keyword=&nature_url=manufacturer&orderBy=1&page=1&s_area=%EC%B6%A9%EB%82%A8&status=y&tpf=&url=manufacturer |
| F309 | (주)디엠코리아 | 건강기능/가공/소스 제조 | 팩토리플랫폼 AI 추천 기준 건강기능/음료·가공·농수산물·소스 제조 후보 공개 | 충북 음성 | B | 건강기능·소스 복합 제조 후보 확인 | https://factory-platform.com/manufacturer/ai-recommended-manufacturers?category_code=%EA%B0%80%EA%B3%B5&nature_url=manufacturer%2Fai-recommended-manufacturers&orderBy=rand&page=1140&tpf=product%2Flist_ai&url=manufacturer%2Fai-recommended-manufacturers |
| F310 | 주식회사 한교 | 냉동면/숙면 제조 | 팩토리플랫폼 AI 추천 기준 냉동식품 중 면류·숙면·당면 생산 및 HACCP 공개 | 전북 부안 | C | 냉동면·숙면 제조 후보 확인 | https://factory-platform.com/manufacturer/ai-recommended-manufacturers?category_code=%EA%B0%80%EA%B3%B5&nature_url=manufacturer%2Fai-recommended-manufacturers&orderBy=rand&page=1140&tpf=product%2Flist_ai&url=manufacturer%2Fai-recommended-manufacturers |
| F311 | 정우김치 | 절임식품/김치 제조 | 팩토리플랫폼 AI 추천 기준 HACCP 절임식품 제조업체 공개 | 충남 공주 | C | 절임식품·김치 후보 확인 | https://factory-platform.com/manufacturer/ai-recommended-manufacturers?category_code=%EB%86%8D%2F%EC%88%98%EC%82%B0%EB%AC%BC&nature_url=manufacturer%2Fai-recommended-manufacturers&orderBy=rand&page=82&tpf=product%2Flist_ai&url=manufacturer%2Fai-recommended-manufacturers |
| F312 | 주식회사24에스이에이 | 수산물 가공 | 팩토리플랫폼 AI 추천 기준 해산물 가공 전문 식품제조업체 공개 | 대구 | C | 수산물 전처리·가공 후보 확인 | https://factory-platform.com/manufacturer/ai-recommended-manufacturers?category_code=%EB%86%8D%2F%EC%88%98%EC%82%B0%EB%AC%BC&nature_url=manufacturer%2Fai-recommended-manufacturers&orderBy=rand&page=82&tpf=product%2Flist_ai&url=manufacturer%2Fai-recommended-manufacturers |
| F313 | 대성에프에스 | 수산물 가공 | 팩토리플랫폼 AI 추천 기준 냉동연체류 제조업체 공개 | 충북 청주 | C | 냉동 수산물 가공 후보 확인 | https://factory-platform.com/manufacturer/ai-recommended-manufacturers?category_code=%EB%86%8D%2F%EC%88%98%EC%82%B0%EB%AC%BC&nature_url=manufacturer%2Fai-recommended-manufacturers&orderBy=rand&page=82&tpf=product%2Flist_ai&url=manufacturer%2Fai-recommended-manufacturers |
| F314 | 닥터케이바이오 | 소량 OEM 제조 | 팩토리플랫폼 AI 추천 기준 소량 생산 가능 OEM 전문 제조기업 공개 | 미확인 | B | 소규모 업체용 소량 OEM 후보 확인 | https://factory-platform.com/manufacturer/ai-recommended-manufacturers?category_code=%EA%B0%80%EA%B3%B5&nature_url=manufacturer%2Fai-recommended-manufacturers&orderBy=rand&page=417&tpf=product%2Flist_ai&url=manufacturer%2Fai-recommended-manufacturers |
| F315 | SL&C센트럴키친 | 냉동식품 제조 | 팩토리플랫폼 AI 추천 기준 냉동식품 전문 제조업체 및 HACCP 공개 | 서울 서초 | C | 냉동식품 센트럴키친 후보 확인 | https://factory-platform.com/manufacturer/ai-recommended-manufacturers?category_code=%EA%B0%80%EA%B3%B5&nature_url=manufacturer%2Fai-recommended-manufacturers&orderBy=rand&page=465&tpf=product%2Flist_ai&url=manufacturer%2Fai-recommended-manufacturers |
| F316 | (주)요리비 | 수제돈까스 제조 | 팩토리플랫폼 기준 HACCP 프리미엄 수제돈까스 제조업체 공개 | 미확인 | C | 돈까스 HMR 후보 확인 | https://www.factory-platform.com/manufacturer?category_code=14&is_sub=y&nature_url=manufacturer&orderBy=3&page=5&status=y&tpf=product%2Flist&url=manufacturer |
| F317 | 주식회사 아이두비 | 쌀눈/현미밥 가공 | 팩토리플랫폼 기준 쌀눈을 활용한 현미밥 가공 업체 공개 | 미확인 | C | 곡물 기반 스낵·밥류 후보 확인 | https://www.factory-platform.com/manufacturer?category_code=14&is_sub=y&nature_url=manufacturer&orderBy=3&page=5&status=y&tpf=product%2Flist&url=manufacturer |
| F318 | (주)세움바이오텍 | 건강기능/분말 제형 제조 | 팩토리플랫폼 기준 건강기능/음료 제형과 스틱포·파우치 포장 공개 | 미확인 | B | 환·과립·분말·캡슐 제형 후보 확인 | https://www.factory-platform.com/manufacturer?category_code=&field=content&is_sub=y&keyword=&nature_url=manufacturer&orderBy=3&page=17&s_area=&status=y&tpf=&url=manufacturer |
| F319 | 채움에프앤비 농업회사법인(주) | 건강기능/음료 제조 | 팩토리플랫폼 신규 파트너 기준 건강기능/음료 제조 후보 공개 | 미확인 | C | 건강기능/음료 품목 확인 | https://factory-platform.com/manufacturer?category_code=15&is_sub=y&nature_url=manufacturer&orderBy=1&page=4&status=y&tpf=product%2Flist&url=manufacturer |
| F320 | 농업회사법인 한신식품 | 농수산물 제조 | 팩토리플랫폼 신규 파트너 기준 농수산물 제조 후보 공개 | 미확인 | C | 농수산물 가공 품목 확인 | https://www.factory-platform.com/manufacturer?category_code=&is_sub=y&nature_url=manufacturer&orderBy=3&page=16&status=y&tpf=product%2Flist&url=manufacturer |
| F321 | (주)진어전가마보꼬 | 어묵/수산가공 제조 | 팩토리플랫폼 신규 파트너 기준 농수산물·가공 제조 후보 공개 | 미확인 | C | 어묵·수산가공 후보 확인 | https://www.factory-platform.com/manufacturer?category_code=14&nature_url=manufacturer&orderBy=3&page=2&status=y&tpf=product%2Flist&url=manufacturer |
| F322 | (주)자연애 | 농수산물 가공 | 팩토리플랫폼 신규 파트너 기준 농수산물·가공 제조 후보 공개 | 미확인 | C | 농수산물 가공 후보 확인 | https://www.factory-platform.com/manufacturer?category_code=14&nature_url=manufacturer&orderBy=3&page=2&status=y&tpf=product%2Flist&url=manufacturer |
| F323 | (주)다인팩토리 | 떡볶이/양념육 제조 | 팩토리플랫폼 기준 HACCP 떡볶이 및 양념육 전문 제조업체 공개 | 미확인 | B | 떡볶이·양념육 HMR 후보 확인 | https://www.factory-platform.com/manufacturer?category_code=14&nature_url=manufacturer&orderBy=3&page=2&status=y&tpf=product%2Flist&url=manufacturer |
| F324 | (주)다담 | 식육추출/소스 가공 | 팩토리플랫폼 기준 HACCP 식육 추출 전문 가공업체 공개 | 미확인 | B | 식육추출 소스·육수 후보 확인 | https://www.factory-platform.com/manufacturer?category_code=14&nature_url=manufacturer&orderBy=3&page=2&status=y&tpf=product%2Flist&url=manufacturer |
| F325 | 비비드 이츠 | 쭈꾸미볶음 밀키트 제조 | 팩토리플랫폼 기준 HACCP 쭈꾸미볶음 밀키트 전문 제조업체 공개 | 미확인 | B | 수산 밀키트 후보 확인 | https://www.factory-platform.com/manufacturer?category_code=14&nature_url=manufacturer&orderBy=3&page=2&status=y&tpf=product%2Flist&url=manufacturer |
| F326 | (주)청안푸드 / 브랜드 무친놈 | 수산물 무침/젓갈 제조 | 팩토리플랫폼 기준 HACCP 수산물 무침 및 젓갈류 전문 제조업체 공개 | 미확인 | B | 젓갈·수산물 무침 후보 확인 | https://www.factory-platform.com/manufacturer?category_code=14&nature_url=manufacturer&orderBy=3&page=2&status=y&tpf=product%2Flist&url=manufacturer |
| F327 | (주)잇마플 | 질환자 도시락 제조 | 팩토리플랫폼 기준 HACCP 질환자 도시락 전문 제조업체 공개 | 미확인 | C | 특수식·도시락 제조 후보 확인 | https://www.factory-platform.com/manufacturer?category_code=14&nature_url=manufacturer&orderBy=3&page=2&status=y&tpf=product%2Flist&url=manufacturer |
| F328 | (주)담다식품 | 수산물 훈제/김치 제조 | 팩토리플랫폼 기준 HACCP 수산물 훈제 및 김치 전문 제조업체 공개 | 미확인 | C | 수산물 훈제·김치 후보 확인 | https://www.factory-platform.com/manufacturer?category_code=14&nature_url=manufacturer&orderBy=3&page=2&status=y&tpf=product%2Flist&url=manufacturer |
| F329 | (주)러블리강정 | 견과류 강정/에너지바 제조 | 팩토리플랫폼 기준 HACCP 견과류 강정 및 에너지바 전문 제조업체 공개 | 미확인 | A | 저당·고단백 바 Case 001 후보 확인 | https://www.factory-platform.com/manufacturer?NaPm=ct%3Dmd3suhpl%7Cci%3DER610b51b2-6113-11f0-92f0-0aca1d163bde%7Ctr%3Dsa%7Chk%3D63c24212dca7f76ab049a066e24f22bb5d7efa0f%7Cnacn%3DSoXQBsQSuk5K&category_code=13&nature_url=manufacturer&orderBy=3&page=2&status=y&tpf=product%2Flist&url=manufacturer |
| F330 | (주)개미식품 | 곡물과자 제조 | 팩토리플랫폼 기준 HACCP 크리스피롤 곡물과자 제조업체 공개 | 미확인 | A | 곡물 스낵 Case 001 후보 확인 | https://www.factory-platform.com/manufacturer?NaPm=ct%3Dmd3suhpl%7Cci%3DER610b51b2-6113-11f0-92f0-0aca1d163bde%7Ctr%3Dsa%7Chk%3D63c24212dca7f76ab049a066e24f22bb5d7efa0f%7Cnacn%3DSoXQBsQSuk5K&category_code=13&nature_url=manufacturer&orderBy=3&page=2&status=y&tpf=product%2Flist&url=manufacturer |
| F331 | 선진제과(주) / 브랜드 추억의 옛날 손 꽈배기 | 꽈배기 과자 제조 | 팩토리플랫폼 기준 HACCP 꽈배기 과자 전문 제조업체 공개 | 미확인 | C | 꽈배기 과자 제조 후보 확인 | https://www.factory-platform.com/manufacturer?NaPm=ct%3Dmd3suhpl%7Cci%3DER610b51b2-6113-11f0-92f0-0aca1d163bde%7Ctr%3Dsa%7Chk%3D63c24212dca7f76ab049a066e24f22bb5d7efa0f%7Cnacn%3DSoXQBsQSuk5K&category_code=13&nature_url=manufacturer&orderBy=3&page=2&status=y&tpf=product%2Flist&url=manufacturer |
| F332 | (주)마나에프앤비 / 브랜드 로카·풀바·안단잼 | 커피/잼 제조 | 팩토리플랫폼 기준 HACCP 커피·잼 전문 제조업체 공개 | 미확인 | B | 커피·잼 제조 후보 확인 | https://www.factory-platform.com/manufacturer?NaPm=ct%3Dmd3suhpl%7Cci%3DER610b51b2-6113-11f0-92f0-0aca1d163bde%7Ctr%3Dsa%7Chk%3D63c24212dca7f76ab049a066e24f22bb5d7efa0f%7Cnacn%3DSoXQBsQSuk5K&category_code=13&nature_url=manufacturer&orderBy=3&page=2&status=y&tpf=product%2Flist&url=manufacturer |
| F333 | (주)플랜에스인터내셔널 | 타르트/디저트 제조 | 팩토리플랫폼 기준 타르트·까눌레·마카롱 생산 제과 제조기업 공개 | 미확인 | C | 타르트·마카롱 디저트 후보 확인 | https://www.factory-platform.com/manufacturer?NaPm=ct%3Dmd3suhpl%7Cci%3DER610b51b2-6113-11f0-92f0-0aca1d163bde%7Ctr%3Dsa%7Chk%3D63c24212dca7f76ab049a066e24f22bb5d7efa0f%7Cnacn%3DSoXQBsQSuk5K&category_code=13&nature_url=manufacturer&orderBy=3&page=2&status=y&tpf=product%2Flist&url=manufacturer |
| F334 | (주)대하 | 디저트 제조 | 팩토리플랫폼 기준 디저트 전문 제조업체 공개 | 미확인 | C | 디저트 OEM 가능 여부 확인 | https://www.factory-platform.com/manufacturer?NaPm=ct%3Dmd3suhpl%7Cci%3DER610b51b2-6113-11f0-92f0-0aca1d163bde%7Ctr%3Dsa%7Chk%3D63c24212dca7f76ab049a066e24f22bb5d7efa0f%7Cnacn%3DSoXQBsQSuk5K&category_code=13&nature_url=manufacturer&orderBy=3&page=2&status=y&tpf=product%2Flist&url=manufacturer |
| F335 | 브레몬 | 제과/제빵 제조 | 팩토리플랫폼 기준 제과·제빵 전문업체 공개 | 미확인 | C | 제과·제빵 후보 확인 | https://www.factory-platform.com/manufacturer?NaPm=ct%3Dmd3suhpl%7Cci%3DER610b51b2-6113-11f0-92f0-0aca1d163bde%7Ctr%3Dsa%7Chk%3D63c24212dca7f76ab049a066e24f22bb5d7efa0f%7Cnacn%3DSoXQBsQSuk5K&category_code=13&nature_url=manufacturer&orderBy=3&page=2&status=y&tpf=product%2Flist&url=manufacturer |
| F336 | (주)케이엔씨푸드 | 바베큐 폭립 제조 | 팩토리플랫폼 상세 기준 바베큐 폭립 제조 전문기업 공개 | 경기 파주 | B | 폭립·육가공 HMR 후보 확인 | https://www.factory-platform.com/index.html?locale=ko&return_url=%2Fmanufacturer%3Ftpf%3Dproduct%2Fview%26category_code%3D11%2C14%26code%3D420 |
| F337 | (주)선일에프에스 | 축산물 가공 | 팩토리플랫폼 상세 기준 축산물 전문업체 및 신선 선육 공개 | 경기 안산 | C | 축산물 가공·납품 후보 확인 | https://www.factory-platform.com/index.html?locale=ko&return_url=%2Fmanufacturer%3Ftpf%3Dproduct%2Fview%26category_code%3D11%2C14%26code%3D430 |
| F338 | (주)동아푸드 | 수산물 수입/가공 제조 | 팩토리플랫폼 상세 기준 수산물 전문 제조업체 공개 | 부산 | C | 수산물 가공 B2B 후보 확인 | https://www.factory-platform.com/index.html?locale=ko&return_url=%2Fmanufacturer%3Ftpf%3Dproduct%2Fview%26category_code%3D10%26code%3D429 |
| F339 | 문푸드 | 순대 제조 | 팩토리플랫폼 AI 추천 기준 순대 제조 및 HACCP 공개 | 미확인 | C | 순대 HMR 제조 후보 확인 | https://factory-platform.com/manufacturer/ai-recommended-manufacturers?category_code=%EA%B0%80%EA%B3%B5&nature_url=manufacturer%2Fai-recommended-manufacturers&orderBy=rand&page=318&tpf=product%2Flist_ai&url=manufacturer%2Fai-recommended-manufacturers |
| F340 | (주)재원에프앤에스 중앙 조리센터 | 즉석섭취식품 제조 | 팩토리플랫폼 AI 추천 기준 즉석섭취식품 전문 식품제조가공업체 및 HACCP 공개 | 경기 하남 | C | 즉석섭취식품 센트럴키친 후보 확인 | https://factory-platform.com/manufacturer/ai-recommended-manufacturers?category_code=%EA%B0%80%EA%B3%B5&nature_url=manufacturer%2Fai-recommended-manufacturers&orderBy=rand&page=318&tpf=product%2Flist_ai&url=manufacturer%2Fai-recommended-manufacturers |
| F341 | 향미김치 | 김치/절임식품 제조 | 팩토리플랫폼 AI 추천 기준 김치 및 절임식품 전문 제조업체 공개 | 충북 옥천 | C | 김치·절임식품 후보 확인 | https://factory-platform.com/manufacturer/ai-recommended-manufacturers?category_code=%EA%B0%80%EA%B3%B5&nature_url=manufacturer%2Fai-recommended-manufacturers&orderBy=rand&page=318&tpf=product%2Flist_ai&url=manufacturer%2Fai-recommended-manufacturers |
| F342 | (주)호텔리어쿡 | 김치/절임식품 제조 | 팩토리플랫폼 AI 추천 기준 김치·절임식품 및 HACCP 공개 | 경기 김포 | C | 김치·김칫속 제조 후보 확인 | https://factory-platform.com/manufacturer/ai-recommended-manufacturers?category_code=%EA%B0%80%EA%B3%B5&nature_url=manufacturer%2Fai-recommended-manufacturers&orderBy=rand&page=318&tpf=product%2Flist_ai&url=manufacturer%2Fai-recommended-manufacturers |
| F343 | 청원생명농협쌀조합공동사업법인 식품소재가공센터 | 곡류가공/떡/과자 제조 | 팩토리플랫폼 AI 추천 기준 곡류가공품·떡류·과자 HACCP 공개 | 충북 청주 | B | 곡물소재·쌀가공 후보 확인 | https://factory-platform.com/manufacturer/ai-recommended-manufacturers?category_code=%EA%B0%80%EA%B3%B5&nature_url=manufacturer%2Fai-recommended-manufacturers&orderBy=rand&page=318&tpf=product%2Flist_ai&url=manufacturer%2Fai-recommended-manufacturers |
| F344 | (주)이킴 | 김치/절임식품 제조 | 팩토리플랫폼 AI 추천 기준 김치 및 절임식품 주력 제조업체 공개 | 충북 보은 | C | 김치·절임식품 후보 확인 | https://factory-platform.com/manufacturer/ai-recommended-manufacturers?category_code=%EA%B0%80%EA%B3%B5&nature_url=manufacturer%2Fai-recommended-manufacturers&orderBy=rand&page=318&tpf=product%2Flist_ai&url=manufacturer%2Fai-recommended-manufacturers |
| F345 | 농업회사법인 코네이처(주) | 건강식품 원료/가공 제조 | 팩토리플랫폼 AI 추천 기준 자연 원료 기반 식품 가공 전문업체 공개 | 충남 공주 | C | 건강식품 원료 가공 후보 확인 | https://factory-platform.com/manufacturer/ai-recommended-manufacturers?category_code=%EA%B0%80%EA%B3%B5&nature_url=manufacturer%2Fai-recommended-manufacturers&orderBy=rand&page=318&tpf=product%2Flist_ai&url=manufacturer%2Fai-recommended-manufacturers |
| F346 | 동산영농조합 | 과채가공품 제조 | 팩토리플랫폼 AI 추천 기준 과채가공품 생산 업체 공개 | 경북 청도 | C | 과채가공품 후보 확인 | https://factory-platform.com/manufacturer/ai-recommended-manufacturers?category_code=%EA%B0%80%EA%B3%B5&nature_url=manufacturer%2Fai-recommended-manufacturers&orderBy=rand&page=318&tpf=product%2Flist_ai&url=manufacturer%2Fai-recommended-manufacturers |
| F347 | 주식회사 고려인삼제품공사 | 침출차/음료베이스 제조 | 팩토리플랫폼 AI 추천 기준 침출차·음료베이스·커피 등 생산 및 HACCP 공개 | 충남 천안 | B | 차·음료베이스 후보 확인 | https://factory-platform.com/manufacturer/ai-recommended-manufacturers?category_code=%EA%B0%80%EA%B3%B5&nature_url=manufacturer%2Fai-recommended-manufacturers&orderBy=rand&page=318&tpf=product%2Flist_ai&url=manufacturer%2Fai-recommended-manufacturers |
| F348 | (주)삼진 지.에프 | 소스/농수산물 가공 제조 | 팩토리플랫폼 AI 추천 기준 소스·가공·농수산물 제조 후보 공개 | 전남 나주 | C | 소스·농수산물 가공 후보 확인 | https://factory-platform.com/manufacturer/ai-recommended-manufacturers?category_code=%EA%B0%80%EA%B3%B5&nature_url=manufacturer%2Fai-recommended-manufacturers&orderBy=rand&page=318&tpf=product%2Flist_ai&url=manufacturer%2Fai-recommended-manufacturers |
| F349 | (주)네츄럴굿띵스 | 효모/효소/전분가공 제조 | 팩토리플랫폼 AI 추천 기준 효모식품·효소식품·전분가공품 생산 및 HACCP 공개 | 충북 청주 | C | 기능성 소재·분말 후보 확인 | https://factory-platform.com/manufacturer/ai-recommended-manufacturers?category_code=%EA%B0%80%EA%B3%B5&nature_url=manufacturer%2Fai-recommended-manufacturers&orderBy=rand&page=318&tpf=product%2Flist_ai&url=manufacturer%2Fai-recommended-manufacturers |
| F350 | 나라식품 | 홍어무침/수산가공 제조 | 팩토리플랫폼 AI 추천 기준 홍어무침·회무침 제조업체 공개 | 경기 안양 | C | 수산 무침 가공 후보 확인 | https://factory-platform.com/manufacturer/ai-recommended-manufacturers?category_code=%EA%B0%80%EA%B3%B5&nature_url=manufacturer%2Fai-recommended-manufacturers&orderBy=rand&page=338&tpf=product%2Flist_ai&url=manufacturer%2Fai-recommended-manufacturers |
| F351 | 다오미식품 | 소스/절임식품 제조 | 팩토리플랫폼 AI 추천 기준 소스·절임식품 제조 후보 공개 | 경남 양산 | C | 냉면 소스·절임식품 후보 확인 | https://factory-platform.com/manufacturer/ai-recommended-manufacturers?category_code=%EA%B0%80%EA%B3%B5&nature_url=manufacturer%2Fai-recommended-manufacturers&orderBy=rand&page=338&tpf=product%2Flist_ai&url=manufacturer%2Fai-recommended-manufacturers |
| F352 | 안면도해송고구마말랭이 | 고구마 가공 제조 | 팩토리플랫폼 AI 추천 기준 고구마 가공 제조업체 공개 | 충남 태안 | C | 고구마 말랭이 스낵 후보 확인 | https://factory-platform.com/manufacturer/ai-recommended-manufacturers?category_code=%EA%B0%80%EA%B3%B5&nature_url=manufacturer%2Fai-recommended-manufacturers&orderBy=rand&page=338&tpf=product%2Flist_ai&url=manufacturer%2Fai-recommended-manufacturers |
| F353 | 우리축산물유통 | 식육추출/도가니곰국 제조 | 팩토리플랫폼 AI 추천 기준 상주 가마솥 도가니 곰국 생산 공개 | 경북 상주 | C | 곰국·탕류 HMR 후보 확인 | https://factory-platform.com/manufacturer/ai-recommended-manufacturers?category_code=%EA%B0%80%EA%B3%B5&nature_url=manufacturer%2Fai-recommended-manufacturers&orderBy=rand&page=338&tpf=product%2Flist_ai&url=manufacturer%2Fai-recommended-manufacturers |
| F354 | 콩뜨는집 | 전통 발효식품 제조 | 팩토리플랫폼 AI 추천 기준 수제청국장·고추장·간장·된장 제조업체 공개 | 제주 | C | 전통 발효식품 후보 확인 | https://factory-platform.com/manufacturer/ai-recommended-manufacturers?category_code=%EB%86%8D%2F%EC%88%98%EC%82%B0%EB%AC%BC&tpf=product%2Flist_ai |
| F355 | 이거어때 | 곡류가공품 제조 | 팩토리플랫폼 AI 추천 기준 깜밥누룽지 등 곡류가공품 제조 후보 공개 | 충북 괴산 | C | 누룽지·곡류 스낵 후보 확인 | https://www.factory-platform.com/main/member/login?category_code=&nature_url=member%2Flogin&orderBy=rand&page=3&tpf=product%2Flist_ai&url=member%2Flogin |
| F356 | 도들샘 | 즉석조리/견과류 가공 제조 | 팩토리플랫폼 AI 추천 기준 즉석조리식품과 땅콩·견과류 가공품 제조 공개 | 경북 경산 | B | 즉석조리·견과류 반찬 후보 확인 | https://factory-platform.com/index.html?locale=ko&return_url=%2Fmember%2Flogin%3Ftpf%3D%26url%3Dmanufacturer%2Fai-recommended-manufacturers%26return_url%3D%2Fmanufacturer%2Fai-recommended-manufacturers%3Ftpf%3Dproduct%2Flist_ai%26category_code%3D%26nature_url%3Dmanufacturer%2Fai-recommended-manufacturers%26orderBy%3Drand%26page%3D662 |
| F357 | 대박마을 | 가공식품 제조 | 팩토리플랫폼 AI 추천 기준 HACCP 가공식품 제조 후보 공개 | 충남 보령 | C | 가공식품 품목 확인 | https://factory-platform.com/manufacturer/ai-recommended-manufacturers?category_code=%EA%B0%80%EA%B3%B5&nature_url=manufacturer%2Fai-recommended-manufacturers&orderBy=rand&page=450&tpf=product%2Flist_ai&url=manufacturer%2Fai-recommended-manufacturers |
| F358 | 삼진식품 | 농수산물 가공 제조 | 팩토리플랫폼 AI 추천 기준 농수산물·가공 제조 후보 공개 | 경북 예천 | C | 농수산물 가공 후보 확인 | https://factory-platform.com/manufacturer/ai-recommended-manufacturers?category_code=%EA%B0%80%EA%B3%B5&nature_url=manufacturer%2Fai-recommended-manufacturers&orderBy=rand&page=317&tpf=product%2Flist_ai&url=manufacturer%2Fai-recommended-manufacturers |
| F359 | (주)지산푸드시스템 | 떡 제조 | 팩토리플랫폼 기준 HACCP 떡 전문 제조업체 공개 | 미확인 | C | 떡류 제조 후보 확인 | https://www.factory-platform.com/manufacturer?category_code=14&nature_url=manufacturer&orderBy=3&page=2&status=y&tpf=product%2Flist&url=manufacturer |
| F360 | 해바라기식품 | 식품 제조 후보 | 팩토리플랫폼 제조사 목록 기준 식품 제조 후보 공개 | 미확인 | C | 주력 품목과 OEM 가능 여부 확인 | https://factory-platform.com/index.html?locale=ko&return_url=%2Fmember%2Flogin%3Ftpf%3D%26url%3Dmanufacturer%26return_url%3D%2Fmanufacturer%3Ftpf%3D%26nature_url%3Dmanufacturer%26category_code%3D%26status%3Dy%26is_sub%3Dy%26orderBy%3D1%26page%3D32 |
| F361 | (주)BDP | 베이커리 냉동생지/완제품 제조 | 팩토리플랫폼 기준 베이커리류 냉동 생지와 냉동 완제품 제조 HACCP 회사 공개 | 미확인 | B | 냉동 베이커리 후보 확인 | https://factory-platform.com/index.html?locale=ko&return_url=%2Fmember%2Flogin%3Freturn_url%3D%2Fmanufacturer%3Ftpf%3D%26url%3Dmanufacturer%26nature_url%3Dmanufacturer%26category_code%3D%26status%3Dy%26page%3D28 |
| F362 | 캔버스에프앤비(F&B) | 과일/채소칩 제조 | 팩토리플랫폼 상세 기준 HACCP 과일칩·채소칩·건강 간식류 제조 후보 공개 | 경기 수원 | B | 건강 간식·건조 원료 후보 확인 | https://factory-platform.com/manufacturer?category_code=10%2C13%2C14%2C19&code=602&tpf=product%2Fview |
| F363 | 애쉬애쉬웍스/ASH ASH WORKS | 스페셜티 커피 제조 | 팩토리플랫폼 기준 스페셜티 커피 기반 제조 회사 공개 | 미확인 | C | 스페셜티 커피 제조 후보 확인 | https://www.factory-platform.com/index.html?locale=ko&return_url=%2Fmain%2Fmember%2Flogin%3Ftpf%3D%26url%3Dmanufacturer%26return_url%3D%252Fmanufacturer%253Ftpf%253D%26nature_url%3Dmanufacturer%26category_code%3D%26status%3Dy%26print_data_count%3D5%26is_sub%3Dy%26orderBy%3D1%26page%3D67 |
| F364 | 리바이프로덕트 | 제과제빵 OEM/ODM | 팩토리플랫폼 상세 기준 제과제빵 OEM/ODM과 HACCP 인증시설 공개 | 미확인 | A | 제과제빵 OEM/ODM 우선 후보 확인 | https://www.factory-platform.com/manufacturer?category_code=13&code=574&tpf=product%2Fview |
| F365 | (주)맘메이크 | 곡물/즉석섭취/체중조절식 제조 | 팩토리플랫폼 AI 추천 기준 곡물 가공품·즉석섭취식품·체중조절용 조제식품 생산 공개 | 경기 파주 | B | 곡물·체중조절식 후보 확인 | https://www.factory-platform.com/main/member/login?category_code=&nature_url=member%2Flogin&orderBy=rand&page=3&tpf=product%2Flist_ai&url=member%2Flogin |
| F366 | 농업회사법인(주)꼬로베이 | 잼/혼합간장 제조 | 팩토리플랫폼 AI 추천 기준 사과잼과 만능간장 농산물 가공 제품 제조 공개 | 강원 평창 | C | 잼·간장 소스 후보 확인 | https://factory-platform.com/member/login?category_code=%EC%86%8C%EC%8A%A4&tpf=product%2Flist_ai |
| F367 | 혜원식품 | 조미료/고춧가루 제조 | 팩토리플랫폼 AI 추천 기준 조미료 및 양념 가공 전문 기업 공개 | 경남 창녕 | C | 조미료·고춧가루 원료 후보 확인 | https://www.factory-platform.com/main/member/login?category_code=&nature_url=member%2Flogin&orderBy=rand&page=3&tpf=product%2Flist_ai&url=member%2Flogin |
| F368 | 서울향료(주)진천공장 | 향료/소스/원료 제조 | 팩토리플랫폼 AI 추천 기준 HACCP 가공·제과제빵·원료·소스 제조 후보 공개 | 충북 진천 | B | 향료·소스 원료 후보 확인 | https://factory-platform.com/member/login?category_code=%EC%86%8C%EC%8A%A4&tpf=product%2Flist_ai |
| F369 | 필넛로스터스 | 드립백/블렌드 커피 제조 | 팩토리플랫폼 AI 추천 기준 드립백 및 블렌드 커피 전문 제조업체 공개 | 경기 구리 | C | 드립백 커피 후보 확인 | https://www.factory-platform.com/main/member/login?category_code=&nature_url=member%2Flogin&orderBy=rand&page=3&tpf=product%2Flist_ai&url=member%2Flogin |
| F370 | 농민식품 | 만두/냉면/소스 제조 | 공식 홈페이지 기준 만두·냉면사리·냉면육수·소스 제품군 공개 | 미확인 | B | 만두·냉면·소스 B2B/OEM 가능 여부 확인 | https://www.nongminfood.co.kr/ |
| F371 | 리파이커피컴퍼니 | 원두 OEM/ODM | 팩토리플랫폼 기준 원두 OEM/ODM 전문 제조업체 공개 | 미확인 | B | 원두 OEM/ODM 후보 확인 | https://www.factory-platform.com/manufacturer?NaPm=ct%3Dmdoxahg7%7Cci%3DER37f17f0b-6cb1-11f0-8482-821da0f47b5f%7Ctr%3Dsa%7Chk%3Dab9c3ee8a02dc6875bc1d77870fc562baaeadc4e%7Cnacn%3D1VfECYhKf08ZD&category_code=13&is_sub=y&nature_url=manufacturer&orderBy=1&page=2&status=y&tpf=product%2Flist&url=manufacturer |
| F372 | (주)도우팩토리 | 도우 제조 | 팩토리플랫폼 기준 도우 전문 제조업체 공개 | 미확인 | C | 피자·베이커리 도우 후보 확인 | https://www.factory-platform.com/manufacturer?NaPm=ct%3Dmdoxahg7%7Cci%3DER37f17f0b-6cb1-11f0-8482-821da0f47b5f%7Ctr%3Dsa%7Chk%3Dab9c3ee8a02dc6875bc1d77870fc562baaeadc4e%7Cnacn%3D1VfECYhKf08ZD&category_code=13&is_sub=y&nature_url=manufacturer&orderBy=1&page=2&status=y&tpf=product%2Flist&url=manufacturer |
| F373 | (주)천마하나로 | 캡슐커피/드립백 OEM/ODM | 팩토리플랫폼 기준 캡슐커피·드립백·원두 OEM/ODM 전문 제조업체 공개 | 미확인 | B | 캡슐커피·드립백 OEM/ODM 후보 확인 | https://www.factory-platform.com/manufacturer?NaPm=ct%3Dmdoxahg7%7Cci%3DER37f17f0b-6cb1-11f0-8482-821da0f47b5f%7Ctr%3Dsa%7Chk%3Dab9c3ee8a02dc6875bc1d77870fc562baaeadc4e%7Cnacn%3D1VfECYhKf08ZD&category_code=13&is_sub=y&nature_url=manufacturer&orderBy=1&page=2&status=y&tpf=product%2Flist&url=manufacturer |
| F374 | (주)브라우니웍스 | 케이크 제조 | 팩토리플랫폼 기준 케이크 전문 제조공장 공개 | 미확인 | C | 케이크 제조 후보 확인 | https://www.factory-platform.com/manufacturer?category_code=&is_sub=y&nature_url=manufacturer&orderBy=3&page=31&status=y&tpf=product%2Flist&url=manufacturer |
| F375 | (주)소울 | 소스/분말/드레싱 제조 | 팩토리플랫폼 상세 기준 소스·분말류 제조 및 300여종 소스 레시피 공개 | 경기 용인 | A | 소스·분말·드레싱 대형 후보 확인 | https://www.factory-platform.com/manufacturer?category_code=13&code=119&tpf=product%2Fview |
| F376 | 가람에프엔비 | 디저트 제조 | 팩토리플랫폼 기준 디저트 전문 제조 후보 공개 | 미확인 | C | 디저트 제조 후보 확인 | https://www.factory-platform.com/manufacturer?category_code=13&is_sub=y&nature_url=manufacturer&orderBy=3&page=5&status=y&tpf=product%2Flist&url=manufacturer |
| F377 | (주)소울네이처푸드 | 복합조미/음료/커피 제조 | 팩토리플랫폼 AI 추천 기준 복합조미식품과 음료·커피 제조업체 공개 | 충남 천안 | C | 복합조미·음료 후보 확인 | https://factory-platform.com/manufacturer/ai-recommended-manufacturers?category_code=%EA%B0%80%EA%B3%B5&nature_url=manufacturer%2Fai-recommended-manufacturers&orderBy=rand&page=285&tpf=product%2Flist_ai&url=manufacturer%2Fai-recommended-manufacturers |
| F378 | 정인바이오 | 과채/당류/캔디 제조 | 팩토리플랫폼 AI 추천 기준 과채가공품·당류가공품·캔디 제조 및 HACCP 공개 | 경기 이천 | C | 환·캔디·과채가공 후보 확인 | https://factory-platform.com/manufacturer/ai-recommended-manufacturers?category_code=%EA%B0%80%EA%B3%B5&nature_url=manufacturer%2Fai-recommended-manufacturers&orderBy=rand&page=285&tpf=product%2Flist_ai&url=manufacturer%2Fai-recommended-manufacturers |
| F379 | (주)아로마에프아이 | 캔디/건강기능음료 제조 | 팩토리플랫폼 AI 추천 기준 HACCP 캔디류 및 건강기능/음료 제조 후보 공개 | 충북 음성 | C | 캔디·건강음료 후보 확인 | https://factory-platform.com/manufacturer/ai-recommended-manufacturers?category_code=%EA%B0%80%EA%B3%B5&nature_url=manufacturer%2Fai-recommended-manufacturers&orderBy=rand&page=285&tpf=product%2Flist_ai&url=manufacturer%2Fai-recommended-manufacturers |
| F380 | (주)더본코리아 예산공장 | 소스/커피/복합조미 제조 | 팩토리플랫폼 AI 추천 기준 커피·기타가공품·복합조미식품·소스·혼합장 제조 및 HACCP 공개 | 충남 예산 | B | 소스·복합조미 B2B 후보 확인 | https://factory-platform.com/manufacturer/ai-recommended-manufacturers?category_code=&nature_url=manufacturer%2Fai-recommended-manufacturers&orderBy=rand&page=2&tpf=&url=manufacturer%2Fai-recommended-manufacturers |
| F381 | 순정원 에프에스 | 어육살 제조 | 팩토리플랫폼 AI 추천 기준 어육살 제조 후보 공개 | 경기 남양주 | C | 어육살·수산 원료 후보 확인 | https://factory-platform.com/manufacturer/ai-recommended-manufacturers?category_code=&nature_url=manufacturer%2Fai-recommended-manufacturers&orderBy=rand&page=2&tpf=&url=manufacturer%2Fai-recommended-manufacturers |
| F382 | 베비에르에프앤비 | 빵류 제조 | 팩토리플랫폼 AI 추천 기준 빵류 제조 및 HACCP 공개 | 광주 | C | 페스츄리·빵류 후보 확인 | https://factory-platform.com/manufacturer/ai-recommended-manufacturers?category_code=&nature_url=manufacturer%2Fai-recommended-manufacturers&orderBy=rand&page=2&tpf=&url=manufacturer%2Fai-recommended-manufacturers |
| F383 | 영진얼음 | 식용얼음 제조 | 팩토리플랫폼 AI 추천 기준 식용얼음 제조 후보 공개 | 인천 | C | 식용얼음 B2B 후보 확인 | https://factory-platform.com/manufacturer/ai-recommended-manufacturers?category_code=&nature_url=manufacturer%2Fai-recommended-manufacturers&orderBy=rand&page=2&tpf=&url=manufacturer%2Fai-recommended-manufacturers |
| F384 | (주)대현상회 | 참기름/들기름 제조 | 팩토리플랫폼 AI 추천 기준 기타농산가공품·들기름·참기름 제조 및 HACCP 공개 | 부산 | C | 참기름·들기름 원료 후보 확인 | https://factory-platform.com/manufacturer/ai-recommended-manufacturers?category_code=%EB%86%8D%2F%EC%88%98%EC%82%B0%EB%AC%BC&tpf=product%2Flist_ai |
| F385 | 토음바이오 주식회사 | 과채음료 제조 | 팩토리플랫폼 AI 추천 기준 HACCP 과채음료 제조 후보 공개 | 경기 광주 | B | 과채음료 후보 확인 | https://factory-platform.com/manufacturer/ai-recommended-manufacturers?category_code=%EA%B0%80%EA%B3%B5&nature_url=manufacturer%2Fai-recommended-manufacturers&orderBy=rand&page=246&tpf=product%2Flist_ai&url=manufacturer%2Fai-recommended-manufacturers |
| F386 | 주식회사 채움들 | 곡류가공품 제조 | 팩토리플랫폼 AI 추천 기준 곡류가공품 제조 후보 공개 | 충북 제천 | C | 곡류가공품 후보 확인 | https://factory-platform.com/manufacturer/ai-recommended-manufacturers?category_code=%EA%B0%80%EA%B3%B5&nature_url=manufacturer%2Fai-recommended-manufacturers&orderBy=rand&page=246&tpf=product%2Flist_ai&url=manufacturer%2Fai-recommended-manufacturers |
| F387 | (주)서울에프엔비 횡성지점 | 특수영양/주스/콜드브루 제조 | 팩토리플랫폼 AI 추천 기준 암환자용·당뇨환자용 영양조제식품과 주스 제조 공개 | 강원 횡성 | B | 특수영양·주스 후보 확인 | https://factory-platform.com/manufacturer/ai-recommended-manufacturers?category_code=%EA%B0%80%EA%B3%B5&nature_url=manufacturer%2Fai-recommended-manufacturers&orderBy=rand&page=246&tpf=product%2Flist_ai&url=manufacturer%2Fai-recommended-manufacturers |
| F388 | 주식회사 태산알엔디 | 농수산물/가공 제조 | 팩토리플랫폼 AI 추천 기준 농수산물·가공 제조 후보 공개 | 경기 안양 | C | 농수산물 가공 후보 확인 | https://factory-platform.com/manufacturer/ai-recommended-manufacturers?category_code=%EA%B0%80%EA%B3%B5&nature_url=manufacturer%2Fai-recommended-manufacturers&orderBy=rand&page=246&tpf=product%2Flist_ai&url=manufacturer%2Fai-recommended-manufacturers |
| F389 | 하늘누리 | 절임배추 제조 | 팩토리플랫폼 AI 추천 기준 해남 하늘누리 절임배추 및 HACCP 공개 | 전남 해남 | C | 절임배추 후보 확인 | https://factory-platform.com/manufacturer/ai-recommended-manufacturers?category_code=%EA%B0%80%EA%B3%B5&nature_url=manufacturer%2Fai-recommended-manufacturers&orderBy=rand&page=246&tpf=product%2Flist_ai&url=manufacturer%2Fai-recommended-manufacturers |
| F390 | (주)유맥 | 식용유 제조 | 팩토리플랫폼 AI 추천 기준 해바라기유·혼합식용유·콩기름 생산 및 HACCP 공개 | 전남 해남 | C | 식용유 원료 후보 확인 | https://factory-platform.com/manufacturer/ai-recommended-manufacturers?category_code=%EA%B0%80%EA%B3%B5&nature_url=manufacturer%2Fai-recommended-manufacturers&orderBy=rand&page=222&tpf=product%2Flist_ai&url=manufacturer%2Fai-recommended-manufacturers |
| F391 | (주)우포라이스텍 | 발아현미/건강기능식품 제조 | 팩토리플랫폼 AI 추천 기준 발아현미 및 건강기능식품 전문 제조 공개 | 경남 창녕 | B | 발아현미·특수영양 후보 확인 | https://factory-platform.com/manufacturer/ai-recommended-manufacturers?category_code=%EA%B0%80%EA%B3%B5&nature_url=manufacturer%2Fai-recommended-manufacturers&orderBy=rand&page=222&tpf=product%2Flist_ai&url=manufacturer%2Fai-recommended-manufacturers |
| F392 | 주식회사 엔제이에프앤비 | 해조추출물/효소식품 제조 | 팩토리플랫폼 AI 추천 기준 해조추출물·패각발효칼슘 등 건강 지향 제품 생산 및 HACCP 공개 | 부산 기장 | C | 해조·효소식품 소재 후보 확인 | https://factory-platform.com/manufacturer/ai-recommended-manufacturers?category_code=%EA%B0%80%EA%B3%B5&nature_url=manufacturer%2Fai-recommended-manufacturers&orderBy=rand&page=222&tpf=product%2Flist_ai&url=manufacturer%2Fai-recommended-manufacturers |
| F393 | 주식회사 케어푸드 | 누룽칩/곡류가공품 제조 | 팩토리플랫폼 AI 추천 기준 곡류가공품 주력 누룽칩 제조 및 HACCP 공개 | 인천 부평 | B | 누룽칩 스낵 후보 확인 | https://factory-platform.com/manufacturer/ai-recommended-manufacturers?category_code=%EA%B0%80%EA%B3%B5&nature_url=manufacturer%2Fai-recommended-manufacturers&orderBy=rand&page=222&tpf=product%2Flist_ai&url=manufacturer%2Fai-recommended-manufacturers |
| F394 | (주)태림에프웰 | 레토르트/소스/즉석조리 제조 | 팩토리플랫폼 AI 추천 기준 즉석조리식품·카레·소스·레토르트식품 제조 및 HACCP 공개 | 경기 파주 | B | 레토르트·소스 HMR 후보 확인 | https://factory-platform.com/manufacturer/ai-recommended-manufacturers?category_code=%EA%B0%80%EA%B3%B5&nature_url=manufacturer%2Fai-recommended-manufacturers&orderBy=rand&page=222&tpf=product%2Flist_ai&url=manufacturer%2Fai-recommended-manufacturers |
| F395 | 씨제이제일제당(주) 안산공장 | 원료/소스/가공 제조 | 팩토리플랫폼 AI 추천 기준 덱스트린·곡류가공품·전분 및 다양한 파우더·시럽 제조 공개 | 경기 안산 | B | 원료·파우더·시럽 대형 후보 확인 | https://factory-platform.com/manufacturer/ai-recommended-manufacturers?category_code=%EA%B0%80%EA%B3%B5&nature_url=manufacturer%2Fai-recommended-manufacturers&orderBy=rand&page=222&tpf=product%2Flist_ai&url=manufacturer%2Fai-recommended-manufacturers |
| F396 | (주)도타 | 빵류 제조 | 팩토리플랫폼 AI 추천 기준 HACCP 빵류 제조 후보 공개 | 경기 남양주 | C | 빵류 제조 후보 확인 | https://factory-platform.com/manufacturer/ai-recommended-manufacturers?category_code=%EA%B0%80%EA%B3%B5&nature_url=manufacturer%2Fai-recommended-manufacturers&orderBy=rand&page=222&tpf=product%2Flist_ai&url=manufacturer%2Fai-recommended-manufacturers |
| F397 | 주식회사디아이 | 레토르트/소스/어묵 제조 | 팩토리플랫폼 AI 추천 기준 레토르트식품·소스·어묵 등 다양한 식품 제조 및 HACCP 공개 | 강원 강릉 | B | 레토르트·소스·어묵 복합 후보 확인 | https://factory-platform.com/manufacturer/ai-recommended-manufacturers?category_code=%EA%B0%80%EA%B3%B5&nature_url=manufacturer%2Fai-recommended-manufacturers&orderBy=rand&page=222&tpf=product%2Flist_ai&url=manufacturer%2Fai-recommended-manufacturers |
| F398 | 샘표식품(주) 이천공장 | 간장/소스/복합조미 제조 | 팩토리플랫폼 AI 추천 기준 혼합간장·한식간장·소스·복합조미식품 제조 및 HACCP 공개 | 경기 이천 | B | 간장·소스 B2B 후보 확인 | https://factory-platform.com/manufacturer/ai-recommended-manufacturers?category_code=%EC%86%8C%EC%8A%A4&nature_url=manufacturer%2Fai-recommended-manufacturers&orderBy=rand&page=69&tpf=product%2Flist_ai&url=manufacturer%2Fai-recommended-manufacturers |
| F399 | (주)아인츠푸드 | 과자 제조 | 팩토리플랫폼 AI 추천 기준 HACCP 과자 제조 후보 공개 | 경기 이천 | C | 과자 제조 후보 확인 | https://factory-platform.com/manufacturer/ai-recommended-manufacturers?category_code=%EA%B0%80%EA%B3%B5&nature_url=manufacturer%2Fai-recommended-manufacturers&orderBy=rand&page=222&tpf=product%2Flist_ai&url=manufacturer%2Fai-recommended-manufacturers |
| F400 | 주식회사 선정원푸드시스템 | 소스/복합조미 제조 | 팩토리플랫폼 AI 추천 기준 복합조미식품·소스·기타가공품 제조 및 HACCP 공개 | 경기 양주 | B | 소스·복합조미 후보 확인 | https://factory-platform.com/manufacturer/ai-recommended-manufacturers?category_code=%EC%86%8C%EC%8A%A4&nature_url=manufacturer%2Fai-recommended-manufacturers&orderBy=rand&page=69&tpf=product%2Flist_ai&url=manufacturer%2Fai-recommended-manufacturers |
| F401 | 농업회사법인 늘만나식품(주) | 김치/김칫속 제조 | 팩토리플랫폼 AI 추천 기준 김치 및 김칫속 제조와 HACCP 공개 | 경기 이천 | C | 김치·김칫속 제조 후보 확인 | https://factory-platform.com/manufacturer/ai-recommended-manufacturers?category_code=%EB%86%8D%2F%EC%88%98%EC%82%B0%EB%AC%BC&nature_url=manufacturer%2Fai-recommended-manufacturers&orderBy=rand&page=91&tpf=product%2Flist_ai&url=manufacturer%2Fai-recommended-manufacturers |
| F402 | 화가장가평발효과학 | 전통 발효식품 제조 | 팩토리플랫폼 AI 추천 기준 한식된장·한식간장·김치·청국장 전문 제조와 HACCP 공개 | 경기 가평 | C | 된장·간장·김치 발효식품 후보 확인 | https://factory-platform.com/manufacturer/ai-recommended-manufacturers?category_code=%EB%86%8D%2F%EC%88%98%EC%82%B0%EB%AC%BC&nature_url=manufacturer%2Fai-recommended-manufacturers&orderBy=rand&page=91&tpf=product%2Flist_ai&url=manufacturer%2Fai-recommended-manufacturers |
| F403 | 서신식품(주) | 두부 제조 | 팩토리플랫폼 AI 추천 기준 가공두부 및 두부 생산과 HACCP 공개 | 충북 음성 | C | 두부·고단백 식품 후보 확인 | https://factory-platform.com/manufacturer/ai-recommended-manufacturers?category_code=%EB%86%8D%2F%EC%88%98%EC%82%B0%EB%AC%BC&nature_url=manufacturer%2Fai-recommended-manufacturers&orderBy=rand&page=91&tpf=product%2Flist_ai&url=manufacturer%2Fai-recommended-manufacturers |
| F404 | 농업회사법인 주식회사 진양푸드 | 어묵 제조 | 팩토리플랫폼 AI 추천 기준 어묵 제조 및 HACCP 공개 | 경남 김해 | B | 어묵·핫바 HMR 후보 확인 | https://factory-platform.com/manufacturer/ai-recommended-manufacturers?category_code=%EB%86%8D%2F%EC%88%98%EC%82%B0%EB%AC%BC&nature_url=manufacturer%2Fai-recommended-manufacturers&orderBy=rand&page=91&tpf=product%2Flist_ai&url=manufacturer%2Fai-recommended-manufacturers |
| F405 | 남동푸드 | 수산물/절임 제조 | 팩토리플랫폼 AI 추천 기준 냉동연체류·냉동어류 제조와 HACCP 공개 | 인천 | C | 수산물·절임 반찬 후보 확인 | https://factory-platform.com/manufacturer/ai-recommended-manufacturers?category_code=%EB%86%8D%2F%EC%88%98%EC%82%B0%EB%AC%BC&nature_url=manufacturer%2Fai-recommended-manufacturers&orderBy=rand&page=91&tpf=product%2Flist_ai&url=manufacturer%2Fai-recommended-manufacturers |
| F406 | 착한어부 | 젓갈 제조 | 팩토리플랫폼 AI 추천 기준 새우젓 가공 생산 후보 공개 | 전남 신안 | C | 새우젓·젓갈 후보 확인 | https://factory-platform.com/manufacturer/ai-recommended-manufacturers?category_code=%EB%86%8D%2F%EC%88%98%EC%82%B0%EB%AC%BC&nature_url=manufacturer%2Fai-recommended-manufacturers&orderBy=rand&page=91&tpf=product%2Flist_ai&url=manufacturer%2Fai-recommended-manufacturers |
| F407 | (주)바다로 | 수산물/김 가공 제조 | 팩토리플랫폼 AI 추천 기준 김과 냉동수산물 가공 및 HACCP 공개 | 인천 | B | 김·수산물 가공 B2B 후보 확인 | https://factory-platform.com/manufacturer/ai-recommended-manufacturers?category_code=%EB%86%8D%2F%EC%88%98%EC%82%B0%EB%AC%BC&nature_url=manufacturer%2Fai-recommended-manufacturers&orderBy=rand&page=91&tpf=product%2Flist_ai&url=manufacturer%2Fai-recommended-manufacturers |
| F408 | 이삭식품(주) | 김치/절임식품 제조 | 팩토리플랫폼 AI 추천 기준 김칫속·절임식품·김치 생산 및 HACCP 공개 | 충북 음성 | B | 김치·비건김치 후보 확인 | https://factory-platform.com/manufacturer/ai-recommended-manufacturers?category_code=%EB%86%8D%2F%EC%88%98%EC%82%B0%EB%AC%BC&nature_url=manufacturer%2Fai-recommended-manufacturers&orderBy=rand&page=91&tpf=product%2Flist_ai&url=manufacturer%2Fai-recommended-manufacturers |
| F409 | 주식회사 코리아수산 | 수산물 가공 | 팩토리플랫폼 AI 추천 기준 냉동연체류 등 수산물 가공 및 HACCP 공개 | 경남 사천 | C | 오징어 전처리·수산가공 후보 확인 | https://factory-platform.com/manufacturer/ai-recommended-manufacturers?category_code=%EB%86%8D%2F%EC%88%98%EC%82%B0%EB%AC%BC&nature_url=manufacturer%2Fai-recommended-manufacturers&orderBy=rand&page=91&tpf=product%2Flist_ai&url=manufacturer%2Fai-recommended-manufacturers |
| F410 | 이천현암 무지개식품 | 유지/장류 제조 | 팩토리플랫폼 AI 추천 기준 들기름·고추장·된장·참기름 제조 후보 공개 | 경기 이천 | C | 참기름·고추장·조청 후보 확인 | https://factory-platform.com/manufacturer/ai-recommended-manufacturers?category_code=%EB%86%8D%2F%EC%88%98%EC%82%B0%EB%AC%BC&nature_url=manufacturer%2Fai-recommended-manufacturers&orderBy=rand&page=91&tpf=product%2Flist_ai&url=manufacturer%2Fai-recommended-manufacturers |
| F411 | 푸른푸드팩토리 | 수산물 가공 | 팩토리플랫폼 AI 추천 기준 냉동연체류 및 기타 수산물 가공품 제조와 HACCP 공개 | 대구 | C | 냉동 수산물 가공 후보 확인 | https://factory-platform.com/manufacturer/ai-recommended-manufacturers?category_code=%EB%86%8D%2F%EC%88%98%EC%82%B0%EB%AC%BC&nature_url=manufacturer%2Fai-recommended-manufacturers&orderBy=rand&page=91&tpf=product%2Flist_ai&url=manufacturer%2Fai-recommended-manufacturers |
| F412 | 대자연식품 제2공장 | 떡류 제조 | 팩토리플랫폼 AI 추천 기준 쌀떡국·쌀떡볶이 등 떡류 제조 및 HACCP 공개 | 대구 | C | 떡류 HMR 후보 확인 | https://factory-platform.com/manufacturer/ai-recommended-manufacturers?category_code=%EB%86%8D%2F%EC%88%98%EC%82%B0%EB%AC%BC&nature_url=manufacturer%2Fai-recommended-manufacturers&orderBy=rand&page=91&tpf=product%2Flist_ai&url=manufacturer%2Fai-recommended-manufacturers |
| F413 | 두리산업(주) | 건어포 제조 | 팩토리플랫폼 AI 추천 기준 건어포 제조 후보 공개 | 경기 광주 | C | 건어포 후보 확인 | https://factory-platform.com/manufacturer/ai-recommended-manufacturers?category_code=%EB%86%8D%2F%EC%88%98%EC%82%B0%EB%AC%BC&nature_url=manufacturer%2Fai-recommended-manufacturers&orderBy=rand&page=91&tpf=product%2Flist_ai&url=manufacturer%2Fai-recommended-manufacturers |
| F414 | 금강물산 | 수산물 가공 | 팩토리플랫폼 AI 추천 기준 기타 수산물 가공품 및 HACCP 공개 | 부산 | C | 수산 가공 HMR 후보 확인 | https://factory-platform.com/manufacturer/ai-recommended-manufacturers?category_code=%EB%86%8D%2F%EC%88%98%EC%82%B0%EB%AC%BC&nature_url=manufacturer%2Fai-recommended-manufacturers&orderBy=rand&page=91&tpf=product%2Flist_ai&url=manufacturer%2Fai-recommended-manufacturers |
| F415 | (주)해저마켓 | 수산물/소스 가공 | 팩토리플랫폼 AI 추천 기준 농수산물·가공·소스 제조 후보 공개 | 부산 | C | 수산물·소스 가공 후보 확인 | https://factory-platform.com/manufacturer/ai-recommended-manufacturers?category_code=%EB%86%8D%2F%EC%88%98%EC%82%B0%EB%AC%BC&nature_url=manufacturer%2Fai-recommended-manufacturers&orderBy=rand&page=91&tpf=product%2Flist_ai&url=manufacturer%2Fai-recommended-manufacturers |
| F416 | 일광푸드 | 시즈닝 제조 | 팩토리플랫폼 AI 추천 기준 다양한 시즈닝 제품 전문 제조 공개 | 세종 | C | 시즈닝·향신료 후보 확인 | https://factory-platform.com/manufacturer/ai-recommended-manufacturers?category_code=%EC%86%8C%EC%8A%A4&nature_url=manufacturer%2Fai-recommended-manufacturers&orderBy=rand&page=122&tpf=product%2Flist_ai&url=manufacturer%2Fai-recommended-manufacturers |
| F417 | 주식회사 해나눔 | 마라/중식 소스 제조 | 팩토리플랫폼 AI 추천 기준 라유·마파두부소스·마라 육수소스 등 소스 제조 공개 | 경기 양평 | B | 마라·중식 소스 후보 확인 | https://factory-platform.com/manufacturer/ai-recommended-manufacturers?category_code=%EC%86%8C%EC%8A%A4&nature_url=manufacturer%2Fai-recommended-manufacturers&orderBy=rand&page=122&tpf=product%2Flist_ai&url=manufacturer%2Fai-recommended-manufacturers |
| F418 | 마라신(마라푸드) | 고추기름/마라소스 제조 | 팩토리플랫폼 AI 추천 기준 고추기름과 마라 양념 소스 전문 제조 후보 공개 | 대구 | C | 마라 소스 후보 확인 | https://factory-platform.com/manufacturer/ai-recommended-manufacturers?category_code=%EC%86%8C%EC%8A%A4&nature_url=manufacturer%2Fai-recommended-manufacturers&orderBy=rand&page=122&tpf=product%2Flist_ai&url=manufacturer%2Fai-recommended-manufacturers |
| F419 | 사조산업(주) 순창공장 | 장류/소스 제조 | 팩토리플랫폼 AI 추천 기준 춘장·고추장·된장·혼합장 제조 및 HACCP 공개 | 전북 순창 | B | 장류·춘장 소스 후보 확인 | https://factory-platform.com/manufacturer/ai-recommended-manufacturers?category_code=%EC%86%8C%EC%8A%A4&nature_url=manufacturer%2Fai-recommended-manufacturers&orderBy=rand&page=122&tpf=product%2Flist_ai&url=manufacturer%2Fai-recommended-manufacturers |
| F420 | 제일유업(주) | 소스/유함유가공품 제조 | 팩토리플랫폼 AI 추천 기준 기타가공품·소스·유함유가공품 제조 및 HACCP 공개 | 경기 화성 | B | 유제품 베이스·소스 후보 확인 | https://factory-platform.com/manufacturer/ai-recommended-manufacturers?category_code=%EC%86%8C%EC%8A%A4&nature_url=manufacturer%2Fai-recommended-manufacturers&orderBy=rand&page=122&tpf=product%2Flist_ai&url=manufacturer%2Fai-recommended-manufacturers |
| F421 | 농업회사법인(유)신가네 | 국밥/소스/간편조리 제조 | 팩토리플랫폼 AI 추천 기준 들기름·간편조리세트·소스·복합조미식품 제조 후보 공개 | 전북 정읍 | C | 국밥 HMR·전골소스 후보 확인 | https://factory-platform.com/manufacturer/ai-recommended-manufacturers?category_code=%EC%86%8C%EC%8A%A4&nature_url=manufacturer%2Fai-recommended-manufacturers&orderBy=rand&page=122&tpf=product%2Flist_ai&url=manufacturer%2Fai-recommended-manufacturers |
| F422 | 수일농산 | 유지/조미료 제조 | 팩토리플랫폼 AI 추천 기준 들기름·참기름·고춧가루 제조 후보 공개 | 경기 화성 | C | 참기름·고춧가루 원료 후보 확인 | https://factory-platform.com/manufacturer/ai-recommended-manufacturers?category_code=%EC%86%8C%EC%8A%A4&nature_url=manufacturer%2Fai-recommended-manufacturers&orderBy=rand&page=122&tpf=product%2Flist_ai&url=manufacturer%2Fai-recommended-manufacturers |
| F423 | (주)청우F&B | 조미액젓/젓갈 제조 | 팩토리플랫폼 AI 추천 기준 조미액젓·양념젓갈·절임식품 제조 및 HACCP 공개 | 전남 화순 | C | 액젓·젓갈·절임식품 후보 확인 | https://factory-platform.com/manufacturer/ai-recommended-manufacturers?category_code=%EC%86%8C%EC%8A%A4&nature_url=manufacturer%2Fai-recommended-manufacturers&orderBy=rand&page=122&tpf=product%2Flist_ai&url=manufacturer%2Fai-recommended-manufacturers |
| F424 | 디앤비푸드(D&B Food) | 소스/식육수산가공 제조 | 팩토리플랫폼 AI 추천 기준 소스·식육함유가공품·수산물가공품 제조 후보 공개 | 대구 | C | 드레싱·조리소스 후보 확인 | https://factory-platform.com/manufacturer/ai-recommended-manufacturers?category_code=%EC%86%8C%EC%8A%A4&nature_url=manufacturer%2Fai-recommended-manufacturers&orderBy=rand&page=122&tpf=product%2Flist_ai&url=manufacturer%2Fai-recommended-manufacturers |
| F425 | (주)다우푸드 | 소스 제조 | 팩토리플랫폼 AI 추천 기준 HACCP 소스 제조 후보 공개 | 경기 광주 | C | 소스 제조 후보 확인 | https://factory-platform.com/manufacturer/ai-recommended-manufacturers?category_code=%EC%86%8C%EC%8A%A4&nature_url=manufacturer%2Fai-recommended-manufacturers&orderBy=rand&page=122&tpf=product%2Flist_ai&url=manufacturer%2Fai-recommended-manufacturers |
| F426 | (주)그린위치 | 복합조미식품 제조 | 팩토리플랫폼 AI 추천 기준 HACCP 복합조미식품 제조 후보 공개 | 충북 증평 | C | 복합조미식품 후보 확인 | https://factory-platform.com/manufacturer/ai-recommended-manufacturers?category_code=%EC%86%8C%EC%8A%A4&nature_url=manufacturer%2Fai-recommended-manufacturers&orderBy=rand&page=69&tpf=product%2Flist_ai&url=manufacturer%2Fai-recommended-manufacturers |
| F427 | (주)파리크라상 성남제2공장 | 빵류/즉석조리/소스 제조 | 팩토리플랫폼 AI 추천 기준 유함유가공품·빵류·즉석조리식품 제조 및 HACCP 공개 | 경기 성남 | B | 빵류·드레싱 B2B 후보 확인 | https://factory-platform.com/manufacturer/ai-recommended-manufacturers?category_code=%EC%86%8C%EC%8A%A4&nature_url=manufacturer%2Fai-recommended-manufacturers&orderBy=rand&page=69&tpf=product%2Flist_ai&url=manufacturer%2Fai-recommended-manufacturers |
| F428 | (주)신세계푸드 음성공장 | 소스/잼/건강기능음료 제조 | 팩토리플랫폼 AI 추천 기준 소스·가공·건강기능/음료 제조 및 HACCP 공개 | 충북 음성 | B | 소스·잼·음료 대형 후보 확인 | https://factory-platform.com/manufacturer/ai-recommended-manufacturers?category_code=%EC%86%8C%EC%8A%A4&nature_url=manufacturer%2Fai-recommended-manufacturers&orderBy=rand&page=69&tpf=product%2Flist_ai&url=manufacturer%2Fai-recommended-manufacturers |
| F429 | 커피노리 | 커피 제조 | 팩토리플랫폼 AI 추천 기준 커피 제품 제조 전문 기업 공개 | 대전 | C | 커피 제조 후보 확인 | https://factory-platform.com/manufacturer/ai-recommended-manufacturers |
| F430 | 청오건강 농업회사법인주식회사 4공장 | 침출차 제조 | 팩토리플랫폼 AI 추천 기준 침출차 생산 및 HACCP 공개 | 경기 광주 | B | 침출차·티백 후보 확인 | https://factory-platform.com/manufacturer/ai-recommended-manufacturers |
| F431 | 담아본 영농조합법인 | 과채주스/액상차 제조 | 팩토리플랫폼 AI 추천 기준 과채주스·액상차 제조 및 HACCP 공개 | 경북 의성 | B | 과채주스·액상차 후보 확인 | https://factory-platform.com/manufacturer/ai-recommended-manufacturers?category_code=%EA%B1%B4%EA%B0%95%EA%B8%B0%EB%8A%A5%2F%EC%9D%8C%EB%A3%8C&tpf=product%2Flist_ai |
| F432 | ㈜혜진수산 | 냉동조미수산물 제조 | 팩토리플랫폼 AI 추천 기준 기타수산물가공품 중 냉동조미가공품 제조 공개 | 인천 | C | 냉동수산물 B2B 후보 확인 | https://factory-platform.com/manufacturer/ai-recommended-manufacturers?category_code=%EB%86%8D%2F%EC%88%98%EC%82%B0%EB%AC%BC&tpf=product%2Flist_ai |
| F433 | (주)무궁화식품 | 조청/당절임/건강식품 제조 | 팩토리플랫폼 AI 추천 기준 조청·당절임·건강식품 제조 후보 공개 | 충북 청주 | C | 당류·전통가공 후보 확인 | https://factory-platform.com/manufacturer/ai-recommended-manufacturers?category_code=%EA%B0%80%EA%B3%B5&nature_url=manufacturer%2Fai-recommended-manufacturers&orderBy=rand&page=300&tpf=product%2Flist_ai&url=manufacturer%2Fai-recommended-manufacturers |
| F434 | 디엠티씨티(주) | 게장/수산가공 제조 | 팩토리플랫폼 AI 추천 기준 간장게장·양념게장 제조 후보 공개 | 충남 태안 | C | 게장·수산가공 후보 확인 | https://factory-platform.com/manufacturer/ai-recommended-manufacturers?category_code=%EA%B0%80%EA%B3%B5&nature_url=manufacturer%2Fai-recommended-manufacturers&orderBy=rand&page=300&tpf=product%2Flist_ai&url=manufacturer%2Fai-recommended-manufacturers |
| F435 | (주)쿠엔즈버킷 | 참기름/들기름 제조 | 팩토리플랫폼 AI 추천 및 공개 기사 기준 참기름·들기름 제조 후보 공개 | 서울/익산 | B | 프리미엄 오일 원료 후보 확인 | https://factory-platform.com/manufacturer/ai-recommended-manufacturers?category_code=%EA%B0%80%EA%B3%B5&nature_url=manufacturer%2Fai-recommended-manufacturers&orderBy=rand&page=300&tpf=product%2Flist_ai&url=manufacturer%2Fai-recommended-manufacturers |
| F436 | 한국농업융복합조합 | 즉석조리/발효식초 제조 | 팩토리플랫폼 AI 추천 기준 즉석조리식품·발효식초 제조 후보 공개 | 경기 남양주 | C | 즉석조리·발효식초 후보 확인 | https://factory-platform.com/manufacturer/ai-recommended-manufacturers?category_code=%EA%B0%80%EA%B3%B5&nature_url=manufacturer%2Fai-recommended-manufacturers&orderBy=rand&page=300&tpf=product%2Flist_ai&url=manufacturer%2Fai-recommended-manufacturers |
| F437 | 라노션 | 원두커피/드립커피 제조 | 팩토리플랫폼 AI 추천 기준 원두커피·드립커피 제조 후보 공개 | 경남 창원 | C | 커피 PB 후보 확인 | https://factory-platform.com/manufacturer/ai-recommended-manufacturers?category_code=%EA%B0%80%EA%B3%B5&nature_url=manufacturer%2Fai-recommended-manufacturers&orderBy=rand&page=300&tpf=product%2Flist_ai&url=manufacturer%2Fai-recommended-manufacturers |
| F438 | (주)대호양행 | 코코아/당류가공 제조 | 팩토리플랫폼 AI 추천 기준 코코아·당류 가공 및 HACCP 공개 | 경기 화성 | B | 코코아·음료 소재 후보 확인 | https://factory-platform.com/manufacturer/ai-recommended-manufacturers?category_code=%EA%B0%80%EA%B3%B5&nature_url=manufacturer%2Fai-recommended-manufacturers&orderBy=rand&page=300&tpf=product%2Flist_ai&url=manufacturer%2Fai-recommended-manufacturers |
| F439 | 농업회사법인힘찬한우(주) | 한우 HMR 제조 | 팩토리플랫폼 AI 추천 기준 한우곰탕·한우국밥·한우육개장 제조 후보 공개 | 경기 시흥 | C | 한우 국탕류 HMR 후보 확인 | https://factory-platform.com/manufacturer/ai-recommended-manufacturers?category_code=%EA%B0%80%EA%B3%B5&nature_url=manufacturer%2Fai-recommended-manufacturers&orderBy=rand&page=300&tpf=product%2Flist_ai&url=manufacturer%2Fai-recommended-manufacturers |
| F440 | 남문식품 | 냉동면/떡류 제조 | 팩토리플랫폼 AI 추천 기준 숙면·생면·떡류 제조 및 HACCP 공개 | 대구 | C | 냉동면·떡류 후보 확인 | https://factory-platform.com/manufacturer/ai-recommended-manufacturers?category_code=%EA%B0%80%EA%B3%B5&nature_url=manufacturer%2Fai-recommended-manufacturers&orderBy=rand&page=300&tpf=product%2Flist_ai&url=manufacturer%2Fai-recommended-manufacturers |
| F441 | 주식회사콩밭뜰 | 두부/콩가공 제조 | 팩토리플랫폼 AI 추천 기준 두부·두부떡갈비 제조 및 HACCP 공개 | 경기 파주 | B | 두부·고단백 식품 후보 확인 | https://factory-platform.com/manufacturer/ai-recommended-manufacturers?category_code=%EA%B0%80%EA%B3%B5&nature_url=manufacturer%2Fai-recommended-manufacturers&orderBy=rand&page=300&tpf=product%2Flist_ai&url=manufacturer%2Fai-recommended-manufacturers |
| F442 | (주)백천제면 | 생면/건면 제조 | 팩토리플랫폼 AI 추천 기준 생면·건면 제조 후보 공개 | 경북 경산 | C | 면류 OEM 후보 확인 | https://factory-platform.com/manufacturer/ai-recommended-manufacturers?category_code=%EA%B0%80%EA%B3%B5&nature_url=manufacturer%2Fai-recommended-manufacturers&orderBy=rand&page=300&tpf=product%2Flist_ai&url=manufacturer%2Fai-recommended-manufacturers |
| F443 | 원복송어 | 송어/수산물가공 제조 | 팩토리플랫폼 AI 추천 기준 송어 및 수산물 가공 후보 공개 | 강원 평창 | C | 송어 수산가공 후보 확인 | https://factory-platform.com/manufacturer/ai-recommended-manufacturers |
| F444 | 청주골김치 | 김치/절임식품 제조 | 팩토리플랫폼 AI 추천 기준 김치·절임식품 제조 및 HACCP 공개 | 충북 청주 | C | 김치·절임식품 후보 확인 | https://factory-platform.com/manufacturer/ai-recommended-manufacturers?category_code=%EB%86%8D%2F%EC%88%98%EC%82%B0%EB%AC%BC&tpf=product%2Flist_ai |
| F445 | 디엠지레클리스협동조합 | 커피/음료 제조 | 팩토리플랫폼 AI 추천 기준 드립커피·물쑥차 제조 후보 공개 | 경기 연천 | C | 커피·차류 지역가공 후보 확인 | https://www.factory-platform.com/index.html?locale=ko&return_url=%2Fmain%2Fmain%2Fmember%2Flogin%3Ftpf%3D%26url%3Dmanufacturer%252Fai-recommended-manufacturers%26return_url%3D%252Fmember%252Flogin%253Freturn_url%253D%252Fmember%252Flogin%253Freturn_url%253D%252Fmain%252Fmember%252Flogin%253Freturn_url%253D%252Fmain%252Fmain%252Fmanufacturer%252Fai-recommended-manufacturers%253Ftpf%253Dproduct%252Flist_ai%26category_code%3D%26nature_url%3Dmanufacturer%252Fai-recommended-manufacturers%26orderBy%3Drand%26page%3D5 |
| F446 | 태안농산물가공영농조합법인 | 과채주스/농산물가공 제조 | 팩토리플랫폼 AI 추천 기준 과채주스·농산물가공 및 HACCP 공개 | 충남 태안 | C | 과채주스 농산가공 후보 확인 | https://factory-platform.com/manufacturer/ai-recommended-manufacturers?category_code=%EA%B1%B4%EA%B0%95%EA%B8%B0%EB%8A%A5%2F%EC%9D%8C%EB%A3%8C&tpf=product%2Flist_ai |
| F447 | (주)해여름 | 천일염/조미료 제조 | 팩토리플랫폼 AI 추천 기준 천일염·조미료 제조 후보 공개 | 전남 신안 | C | 소금·조미 원료 후보 확인 | https://factory-platform.com/manufacturer/ai-recommended-manufacturers?category_code=%EA%B0%80%EA%B3%B5&nature_url=manufacturer%2Fai-recommended-manufacturers&orderBy=rand&page=300&tpf=product%2Flist_ai&url=manufacturer%2Fai-recommended-manufacturers |
| F448 | 농업회사법인 주식회사 비건아이 | 식물성 분말 제조 | 팩토리플랫폼 AI 추천 기준 식물성 분말 및 ABC주스분말 제조 후보 공개 | 경기 이천 | B | 분말 원료·스틱 후보 확인 | https://factory-platform.com/manufacturer/ai-recommended-manufacturers?category_code=%EC%9B%90%EB%A3%8C&tpf=product%2Flist_ai |
| F449 | 아하플래닛(주)진천점 | 가공식품 제조 | 팩토리플랫폼 AI 추천 기준 진천 식품 제조 및 HACCP 후보 공개 | 충북 진천 | C | 가공식품 HACCP 후보 확인 | https://factory-platform.com/manufacturer/ai-recommended-manufacturers?category_code=%EA%B0%80%EA%B3%B5&nature_url=manufacturer%2Fai-recommended-manufacturers&orderBy=rand&page=172&tpf=product%2Flist_ai&url=manufacturer%2Fai-recommended-manufacturers |
| F450 | 우일수산㈜ | 어묵/수산가공 제조 | 팩토리플랫폼 AI 추천 기준 어묵 제조 및 HACCP 공개 | 충남 서천 | C | 어묵·수산가공 후보 확인 | https://factory-platform.com/manufacturer/ai-recommended-manufacturers?category_code=%EA%B0%80%EA%B3%B5&nature_url=manufacturer%2Fai-recommended-manufacturers&orderBy=rand&page=285&tpf=product%2Flist_ai&url=manufacturer%2Fai-recommended-manufacturers |
| F451 | (주)한풍네이처팜 | 과채가공/액상차 제조 | 팩토리플랫폼 AI 추천 기준 과채가공품·고형차·액상차 제조 및 HACCP 공개 | 전북 완주 | B | 콜라겐·액상차 후보 확인 | https://factory-platform.com/manufacturer/ai-recommended-manufacturers?category_code=%EA%B0%80%EA%B3%B5&nature_url=manufacturer%2Fai-recommended-manufacturers&orderBy=rand&page=285&tpf=product%2Flist_ai&url=manufacturer%2Fai-recommended-manufacturers |
| F452 | 천하식품 | 과채가공/전처리 제조 | 팩토리플랫폼 AI 추천 기준 과채가공품·전처리 채소 제조 및 HACCP 공개 | 인천 | C | 전처리 채소·반찬 후보 확인 | https://factory-platform.com/manufacturer/ai-recommended-manufacturers?category_code=%EA%B0%80%EA%B3%B5&nature_url=manufacturer%2Fai-recommended-manufacturers&orderBy=rand&page=285&tpf=product%2Flist_ai&url=manufacturer%2Fai-recommended-manufacturers |
| F453 | 농업회사법인 한조주식회사 2공장 | 곡류가공/청류 제조 | 팩토리플랫폼 AI 추천 기준 곡류가공품·생강청·유자청 제조 후보 공개 | 경북 영천 | C | 청류·차류·염지소재 후보 확인 | https://factory-platform.com/manufacturer/ai-recommended-manufacturers?category_code=%EA%B0%80%EA%B3%B5&nature_url=manufacturer%2Fai-recommended-manufacturers&orderBy=rand&page=285&tpf=product%2Flist_ai&url=manufacturer%2Fai-recommended-manufacturers |
| F454 | 서림식품 | 콩가루/곡물분말 제조 | 팩토리플랫폼 AI 추천 기준 대두·콩가루·미숫가루 제조 후보 공개 | 경기 화성 | B | 곡물·두류 분말 후보 확인 | https://factory-platform.com/manufacturer/ai-recommended-manufacturers?category_code=%EA%B0%80%EA%B3%B5&nature_url=manufacturer%2Fai-recommended-manufacturers&orderBy=rand&page=279&tpf=product%2Flist_ai&url=manufacturer%2Fai-recommended-manufacturers |
| F455 | 한우리음식 | 생면 제조 | 팩토리플랫폼 AI 추천 기준 국수 생면 제조 및 HACCP 공개 | 서울 | C | 생면·국수 후보 확인 | https://factory-platform.com/manufacturer/ai-recommended-manufacturers?category_code=%EA%B0%80%EA%B3%B5&nature_url=manufacturer%2Fai-recommended-manufacturers&orderBy=rand&page=279&tpf=product%2Flist_ai&url=manufacturer%2Fai-recommended-manufacturers |
| F456 | ㈜메디오젠 | 유산균/기타가공품 제조 | 팩토리플랫폼 AI 추천 기준 기타가공품·유산균 원료 및 HACCP 공개 | 충북 제천 | B | 유산균 분말 후보 확인 | https://factory-platform.com/manufacturer/ai-recommended-manufacturers?category_code=%EA%B0%80%EA%B3%B5&nature_url=manufacturer%2Fai-recommended-manufacturers&orderBy=rand&page=279&tpf=product%2Flist_ai&url=manufacturer%2Fai-recommended-manufacturers |
| F457 | 순창군귀농귀촌인영농조합법인 | 여주/울금 건강가공 제조 | 팩토리플랫폼 AI 추천 기준 여주·울금·표고버섯 분말 및 차류 제조 후보 공개 | 전북 순창 | C | 지역 건강분말·차류 후보 확인 | https://factory-platform.com/manufacturer/ai-recommended-manufacturers?category_code=%EA%B0%80%EA%B3%B5&nature_url=manufacturer%2Fai-recommended-manufacturers&orderBy=rand&page=279&tpf=product%2Flist_ai&url=manufacturer%2Fai-recommended-manufacturers |
| F458 | (주)지앤씨에프에스 | 과채가공/소스/음료베이스 제조 | 팩토리플랫폼 AI 추천 기준 과채가공품·복합조미식품·소스·음료베이스 제조 및 HACCP 공개 | 충북 제천 | B | 소스·음료베이스·분말소재 후보 확인 | https://factory-platform.com/manufacturer/ai-recommended-manufacturers?category_code=%EA%B0%80%EA%B3%B5&nature_url=manufacturer%2Fai-recommended-manufacturers&orderBy=rand&page=279&tpf=product%2Flist_ai&url=manufacturer%2Fai-recommended-manufacturers |
| F459 | 황제식품 | 순대/즉석조리 제조 | 팩토리플랫폼 AI 추천 기준 즉석조리식품 순대 제조 및 HACCP 공개 | 서울 | C | 순대·즉석조리 후보 확인 | https://factory-platform.com/manufacturer/ai-recommended-manufacturers?category_code=%EA%B0%80%EA%B3%B5&nature_url=manufacturer%2Fai-recommended-manufacturers&orderBy=rand&page=279&tpf=product%2Flist_ai&url=manufacturer%2Fai-recommended-manufacturers |
| F460 | (주)엔트리 | 과채음료/건강음료 제조 | 팩토리플랫폼 AI 추천 기준 과채음료·건강음료 제조 및 HACCP 공개 | 경남 양산 | B | 건강음료·스틱 후보 확인 | https://factory-platform.com/manufacturer/ai-recommended-manufacturers?category_code=%EA%B0%80%EA%B3%B5&nature_url=manufacturer%2Fai-recommended-manufacturers&orderBy=rand&page=317&tpf=product%2Flist_ai&url=manufacturer%2Fai-recommended-manufacturers |

## MVP 우선 컨택 리스트

1. 에스와이솔루션: 저당·고단백 곡물스낵 Case 001 검증
2. 채움바이오: 분말·스틱 소량 생산 Case 002 검증
3. 데이앤바이오: 분말·환·정제·캡슐 제형 Case 002 검증
4. 한국네츄럴팜: GMP/HACCP 건강기능식품 생산 조건 확인
5. 제이스: 소스 OEM/ODM Case 003 검증
6. 소담푸드: 소스 소량 테스트와 샘플 프로세스 검증
7. 비티씨: 푸드이음 기반 분말 OEM/ODM 후보 확인
8. 성진바이오: 환·분말 후보 확인
9. 신비바이오: 소량 다품종 건기식/일반식품 분말·스틱 후보 확인
10. 상상바이오/QOEM: 스타트업 소량 건기식 ODM 후보 확인
11. 관주식품: 분말·분말스틱·동결건조 Case 002 후보 확인
12. 이앤에스: 유동층 과립 기반 분말 스틱 후보 확인
13. 삼진푸드: 소스·분말·농축 대형 B2B Case 003 후보 확인
14. 매일식품: 밀키트/HMR 소스 OEM 후보 확인
15. 미쓰리: 떡볶이·요리 분말소스 OEM/ODM 후보 확인
16. 크레이지피넛: 저당·클린라벨 견과 스프레드 후보 확인
17. 소스나라: 프랜차이즈 맞춤형 소스 소량 샘플 후보 확인
18. 쿠커페이스: MVP 샘플 제작/소분 가능성 확인
19. 대호식품: 카페 파우더·분말 OEM/ODM 후보 확인
20. RASA F&B: 분말 음료·카페 파우더 ODM 후보 확인
21. 힐링: 분말스틱·타블렛 건강식품 후보 확인
22. 프로틴컴퍼니: 프로틴/건강분말 Case 001·002 후보 확인
23. 셀플러스: 파우더류 HACCP/FSSC22000 인증 후보 확인
24. 하남소스: 액상·분말 프랜차이즈 소스 후보 확인
25. 더밥: 비건·분말소스 소량 생산 후보 확인
26. 에스팩토리: 수출용 K-소스 후보 확인
27. 유명식품: PB 소스 개발 후보 확인
28. 원일그룹: 소스 원료·완제품 OEM/ODM 범위 확인
29. 마고푸드랩: 카페·프랜차이즈 디저트 OEM/ODM 후보 확인
30. 율성푸드랩: 견과 스프레드·스낵 Case 001 후보 확인
31. 씨알푸드: 시리얼바·프로틴바 Case 001 후보 확인
32. 스포츠바이오텍: 프로틴 쉐이크·건강분말 Case 002 후보 확인
33. 파우더컴퍼니: 음료 파우더 Case 002 후보 확인
34. 코어그린: 클린라벨 시즈닝·분말육수 Case 003 후보 확인
35. 선도식품: 한식/일식 소스 OEM/ODM 후보 확인
36. 에스디푸드: 기능성 구미·스틱젤리 Case 002 후보 확인
37. 다이식품: 캔디·젤리 OEM/ODM 후보 확인
38. 제이와이네추럴: 콤부차·효소·스틱포장 Case 002 후보 확인
39. 델리후레쉬: 직화소스 Case 003 후보 확인
40. 산들푸드: 소스 OEM/ODM·레시피 개발 후보 확인
41. 오그래: 저당·고단백 그래놀라 Case 001 후보 확인
42. 아이진푸드: 소스 OEM/ODM 공정 후보 확인
43. 베이커스팀: 카페 디저트 OEM/ODM 후보 확인
44. 디에스푸드웰: 육수·코인육수·분말류 Case 003 후보 확인
45. 원스그룹 한닢쿡: 코인육수·분말육수 후보 확인
46. 진성에프엠: 식품 원료·HMR B2B 후보 확인
47. 서비푸드: 닭가슴살 파우더 기반 단백질식품 후보 확인
48. 주식회사 연: 레토르트·즉석조리식품 HMR 후보 확인
49. JMJ푸드 떡불킹: 떡볶이 분말소스 후보 확인
50. 새한그레인: 곡물 기반 건강 스낵 Case 001 후보 재확인
51. 주스템: 과채주스·액상차·건강즙 음료 후보 확인
52. 놀이터 팩토리D1: 과채주스·액상차 OEM/ODM 후보 확인
53. 동방푸드마스타: 소스·시즈닝 대형 B2B 후보 확인
54. 농심태경: 시즈닝·소스·식품소재 후보 확인
55. 오투바이오: 음료베이스·과채가공품 후보 확인
56. 원일바이오: 분말·액상스틱·건강식품 Case 002 후보 확인
57. 정풍: 소스·HMR·분말 소재 대형 B2B 후보 확인
58. 서해식품: 맞춤형 소스 소량 개발 후보 확인
59. 베노프하우스: 프로틴바·프로틴스낵 Case 001 우선 후보 확인
60. 자연농장: 과채·홍삼음료 및 분말 배합 후보 확인
61. 엠에스씨: 음료·젤리·스틱 ODM/OEM 대형 후보 확인
62. 필배치: 원두 로스팅 PB/OEM 후보 확인
63. 씨엔에스테크/찬솔: 양념육·수산물 OEM/ODM 후보 확인
64. 꼬루인터내셔널: 한식 디저트·안주류 OEM 후보 확인
65. 스마트푸드/김가네 영웅갈비: 양념육 OEM/ODM 후보 확인
66. 이랜드이츠 부평공장: 밀키트·소스 OEM/ODM 우선 후보 확인
67. 아람뜰: 곡물 소재·다품종 소량 OEM 후보 확인
68. 서림원: 냉동 밀키트 OEM 우선 후보 확인
69. 러블리강정: 견과류 강정·에너지바 Case 001 후보 확인
70. 개미식품: 곡물과자 Case 001 후보 확인
71. 케이엔씨푸드: 폭립·육가공 HMR 후보 확인
72. 리바이프로덕트: 제과제빵 OEM/ODM 우선 후보 확인
73. 캔버스에프앤비: 과일칩·채소칩 건강 간식 후보 확인
74. 청원생명농협 식품소재가공센터: 쌀가공·곡물소재 후보 확인
75. 농민식품: 만두·냉면·소스 B2B/OEM 가능 여부 확인
76. 소울: 소스·분말·드레싱 대형 B2B 후보 확인
77. 천마하나로: 캡슐커피·드립백 OEM/ODM 후보 확인
78. 서울에프엔비 횡성지점: 특수영양·주스 후보 확인
79. 태림에프웰: 레토르트·소스 HMR 후보 확인
80. 케어푸드: 누룽칩 스낵 후보 확인
81. 바다로: 김·냉동수산물 가공 B2B 후보 확인
82. 이삭식품: 김치·비건김치 후보 확인
83. 해나눔: 마라·중식 소스 후보 확인
84. 사조산업 순창공장: 춘장·장류 소스 후보 확인
85. 진양푸드: 어묵·핫바 HMR 후보 확인
86. 담아본: 과채주스·액상차 Case 002 후보 확인
87. 쿠엔즈버킷: 프리미엄 참기름·들기름 원료 후보 확인
88. 콩밭뜰: 두부·두부떡갈비 고단백 식품 후보 확인
89. 비건아이: 식물성 분말·ABC주스분말 원료 후보 확인
90. 한풍네이처팜: 콜라겐·액상차·과채가공 후보 확인
91. 메디오젠: 유산균 분말·기타가공품 후보 확인
92. 지앤씨에프에스: 소스·음료베이스·분말소재 후보 확인
93. 엔트리: 과채음료·홍삼스틱 후보 확인

## 공통 확인 질문

1. 최소 생산 수량과 샘플 제작 가능 수량은 얼마인가?
2. OEM만 가능한가, ODM 레시피 개발도 가능한가?
3. 저당, 고단백, 식이섬유, 비건, 할랄 같은 클레임 검토가 가능한가?
4. 원재료 BOM을 받으면 대체 원료와 원가 피드백이 가능한가?
5. HACCP/GMP/ISO/비건/할랄 등 인증서 사본 제공 범위는 어디까지인가?
6. 원료 발주를 공장이 대행하는가, 발주자가 지정 원료를 공급해야 하는가?
7. 샘플 개발 리드타임과 본생산 리드타임은 각각 얼마인가?
8. D2C용 소포장, 공동구매용 라벨, B2B 벌크 포장 중 어떤 포장이 가능한가?

## 출처 메모

- 푸드이음은 한국식품산업클러스터진흥원의 OEM/ODM 업체 검색에서 `검색결과 61건`과 인증/주문생산 방식 필터를 제공한다.
- 팩토리플랫폼 공개 제조사 페이지는 일부 업체의 품목, 인증, 등록일, 진행 프로젝트 정보를 제공하지만 실제 계약 조건은 플랫폼 또는 업체 상담으로 재확인해야 한다.
- 업체 공식 페이지는 OEM/ODM 가능 범위와 프로세스 설명을 우선 근거로 사용했다.
- 전시/비즈니스 매칭 페이지는 공개 기업소개와 인증·품목 확인용으로만 쓰고, 계약 가능성은 직접 컨택으로 재검증한다.

## 다음 리서치 라운드

1. `단백질바/프로틴 스낵`: 저당·고단백 Case 001에 바로 붙일 수 있는 바, 쿠키, 곡물칩 제조사 보강
2. `스틱 파우더`: 일반식품 분말과 건강기능식품 분말을 분리해 MOQ/제형/포장 단가를 비교
3. `프랜차이즈 소스`: 냉장/냉동/상온/레토르트 소스 가능 범위와 살균 조건 분리
4. `수출 대응`: FSSC22000, 할랄, 비건, FDA 등록 신호가 있는 후보 별도 태깅
5. `원료소재`: 완제품 생산 전 단계의 원료 OEM/ODM 후보를 BOM 대체 원료 DB와 연결
