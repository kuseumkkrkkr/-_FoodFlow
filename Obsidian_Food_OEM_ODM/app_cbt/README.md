# Food OEM/ODM CBT App

Obsidian 기획 문서를 기준으로 만든 닫힌 베타 테스트용 앱입니다. 자연어 제품 요청을 저장하고 사양화, 규제 스크리닝, 공장 매칭, 원가 계산, 제품 기획안, 샘플 발주안, PDF 생성까지 한 흐름으로 검증합니다.

## 백엔드 실행

```powershell
cd C:\Users\82102\Desktop\dev_main\Obsidian_Food_OEM_ODM\app_cbt
$env:SAM_API_KEY="sam_xxx"
$env:SAM_MODEL="az-deepseek-v4-flash"
python main.py
```

`SAM_API_KEY`가 없으면 규칙 기반 폴백으로 CBT 흐름은 계속 동작합니다. DeepSeek 계열 기본 모델은 `az-deepseek-v4-flash`이고, 선택 후보는 `az-deepseek-v4-flash`, `az-deepseek-v4-pro`입니다.

## 가격 데이터 동기화

기본값은 별도 키 없이 World Bank Commodity Markets의 Pink Sheet 월별 원자재 가격 엑셀을 다운로드해 파싱합니다. 최근 5년 월별 관측치를 저장하고, 원본 가격 단위가 `$/kg` 또는 `$/mt`이면 `normalized_price_kg`를 원/kg로 환산합니다.

```powershell
$env:PRICE_SYNC_ENABLED="true"
$env:PRICE_SYNC_INTERVAL_HOURS="24"
$env:PRICE_SYNC_HISTORY_YEARS="5"
$env:WORLD_BANK_USD_KRW="1380"
python main.py
```

수동 실행:

```powershell
Invoke-RestMethod -Method Post "http://127.0.0.1:8010/api/admin/price-sync-runs?source=worldbank_pink_sheet&history_years=5"
```

수집 품목을 바꾸려면 World Bank 원본 컬럼명과 앱 표시명을 `WORLD_BANK_COMMODITIES_JSON`에 넣습니다.

```powershell
$env:WORLD_BANK_COMMODITIES_JSON='{"Soybeans":"대두","Wheat, US HRW":"밀","Sugar, world":"설탕","Palm oil":"팜유"}'
```

KAMIS 공식 가격 Open API도 선택적으로 사용할 수 있습니다. KAMIS는 인증키가 필요하며 기간 API가 최대 1년 단위라서 5년 히스토리는 서버가 1년 단위로 나눠 받습니다.

```powershell
$env:KAMIS_CERT_KEY="발급받은 인증Key"
$env:KAMIS_CERT_ID="요청자id"
$env:KAMIS_PRICE_ITEMS_JSON='[{"ingredient_name":"쌀","itemcategorycode":"100","itemcode":"111","kindcode":"01","productrankcode":"04","countrycode":"1101","price_type":"wholesale","market":"KAMIS 서울 도매","grade":"상품"}]'
Invoke-RestMethod -Method Post "http://127.0.0.1:8010/api/admin/price-sync-runs?source=kamis_api&history_years=5"
```

## Flutter 실행

```powershell
cd C:\Users\82102\Desktop\dev_main\Obsidian_Food_OEM_ODM\app_flutter
flutter run -d chrome --dart-define=API_BASE_URL=http://127.0.0.1:8010
```

정적 빌드:

```powershell
flutter build web --dart-define=API_BASE_URL=http://127.0.0.1:8010
```

## 주요 기능

- 바이브 쿠킹 GUI 조합: 타깃, 섭취 장면, 식감, 제조 방향, 핵심/제외 원료를 조합해 발주 요청서 초안을 생성
- 바이브 쿠킹 에이전트: 생성된 사양, BOM, 규제 플래그, 공장 후보, 원가를 기준으로 기획 적합도와 다음 액션 제안
- 제품 요청 생성: 건강간식, 분말스틱, 소스
- 사양화: SAM API의 DeepSeek 모델 기반 제품 콘셉트, 제조 공정, BOM 초안, 검증 질문
- 규제 스크리닝: RED/YELLOW/GREEN 플래그와 공식 출처 URL
- 공장 매칭: CSV 시드 기반 상위 후보 3~5개 추천
- 공장 검색: 전체 목록 직접 노출 없이 제품군, 인증, 포장, 검증상태, 적합도 필터로 조회
- 레시피 평가: 제조성, 영양 추정, 표현 가능성, 알레르기, 공정, 원가 점수
- 가격/환율 기준 데이터: 원재료 가격 인덱스, 환율, 가격 동기화 로그
- 원가 계산: 직접원가, 부대비, 1식당 원가, 공급가, MOQ 시나리오
- 문서 생성: 제품 기획안, 샘플 발주안, PDF 다운로드
- 관리자: 공장 검색, 수동 등록, 검증 상태 수정 API
- 더미 검증: 더미 생성 후 `/api/dummy-data`로 삭제

## 검증

서버가 켜진 상태에서 실행합니다.

```powershell
python .\tests\verify_cbt.py
```

검증 스크립트는 바이브 쿠킹 조합, 건강간식, 분말스틱, 소스 더미 요청을 만들고 상세 조회, 에이전트 판단, 매칭, 원가, PDF 생성, 발주요청 생성, 더미 삭제를 확인합니다.

## 바이브 쿠킹 API

- 옵션 조회: `GET /api/vibe-cooking/options`
- 조합 결과 생성: `POST /api/vibe-cooking/compose`
- 기획 에이전트 실행: `POST /api/product-requests/{id}/vibe-agent`

`/api/vibe-cooking/compose`는 GUI 조합값을 기존 `POST /api/product-requests`에 넣을 수 있는 `request_payload`로 변환합니다. 별도 조합 테이블을 만들지 않아 대량 요청 목록과 상세 조회 쿼리는 기존 구조를 유지합니다.

## 데이터

- DB: `data/cbt_app.db`
- 공장 시드: `../database/korea_oem_odm_seed.csv`
- 규제 룰 시드: `../database/regulatory_screening_rules_seed.csv`
- 생성 PDF: `generated/`

모든 파일 입출력은 UTF-8 기준으로 작성했습니다.
