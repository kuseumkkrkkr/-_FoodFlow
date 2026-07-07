# Food OEM/ODM Flutter CBT

Flutter 기반 CBT 클라이언트입니다. Flask 백엔드(`../app_cbt`)에 연결해 제품 요청 생성, DeepSeek 모델 선택, 규제 플래그, 공장 후보, 원가 계산, PDF 생성 액션을 제공합니다.

## 화면 범위

- 요청 워크룸: 제품 요청, DeepSeek 모델 선택, 사양/규제/공장 후보/문서 탭
- 레시피 평가: 제조성, 표현 가능성, 알레르기, 원가 점수 확인
- 운영 기준 데이터: 원재료 참고 가격, 환율 기준 표시
- 공장 DB: 전체 목록 직접 노출 없이 검색어, 제품군, 인증, 포장, 검증상태, 적합도 필터로만 조회

## 실행

백엔드를 먼저 실행합니다.

```powershell
cd C:\Users\82102\Desktop\dev_main\Obsidian_Food_OEM_ODM\app_cbt
$env:SAM_API_KEY="sam_xxx"
python main.py
```

Flutter 앱을 실행합니다.

```powershell
cd C:\Users\82102\Desktop\dev_main\Obsidian_Food_OEM_ODM\app_flutter
flutter run -d chrome --dart-define=API_BASE_URL=http://127.0.0.1:8010
```

웹 빌드:

```powershell
flutter build web --dart-define=API_BASE_URL=http://127.0.0.1:8010
```

## 검증

```powershell
flutter analyze
flutter test
```
