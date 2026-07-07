import fs from "node:fs/promises";
import path from "node:path";
import { SpreadsheetFile, Workbook } from "@oai/artifact-tool";

const threadId = "019f3a37-c85a-7600-bf57-c29b18f14967";
const rootDir = path.resolve("..");
const outputDir = path.resolve("..");
const outputPath = path.join(outputDir, "2026_대한민국_식품트렌드_딥서치.xlsx");

const generatedAt = "2026-07-07";

const sources = [
  {
    id: "S01",
    name: "KREI 식품외식정보 웹진: 2026 식품외식산업 7대 이슈",
    type: "공공/연구",
    date: "2026-04-23",
    url: "https://www.krei.re.kr/foodInfo/page/306?cmd=view&pst=505043",
    use: "식품외식산업 7대 이슈, 간편식, 온라인 식품, 푸드테크, 규제, K-푸드 세계화",
  },
  {
    id: "S02",
    name: "KREI PDF: 2026 식품외식산업 7대 이슈",
    type: "공공/연구 PDF",
    date: "2026-04-23",
    url: "https://www.krei.re.kr/foodInfo/board/atchDown.do?no=113520",
    use: "정량 데이터: 식품제조업/외식산업 전망, HMR, 온라인 식품, 푸드테크 시장",
  },
  {
    id: "S03",
    name: "KATI: 글로벌 2025년 식품시장 트렌드 및 2026 전망",
    type: "공공/수출정보",
    date: "2025-12-17",
    url: "https://www.kati.net/board/reportORpubilcationView.do?board_seq=104476&menu_dept2=49",
    use: "2026 전망: AI 초개인화 식생활, 아시아 식품 글로벌화, 소용량/친환경 포장",
  },
  {
    id: "S04",
    name: "농림축산식품부: 2026년 식품산업진흥 시행계획",
    type: "정부 PDF",
    date: "2026-03",
    url: "https://www.mafra.go.kr/bbs/home/795/594785/download.do",
    use: "푸드테크 기본계획, 연구지원센터, 스마트제조/간편식 정책",
  },
  {
    id: "S05",
    name: "농림축산식품부: RICE SHOW 2026 보도자료",
    type: "정부 보도자료",
    date: "2026-06-07",
    url: "https://www.mafra.go.kr/bbs/home/792/578111/artclView.do?layout=unknown",
    use: "쌀가공식품, 글루텐프리, 식물성 기반 식품, 전통 가공 트렌드",
  },
  {
    id: "S06",
    name: "농림축산식품부: 서울푸드 2026 개막 보도자료",
    type: "정부 보도자료",
    date: "2026-06-09",
    url: "https://www.mafra.go.kr/bbs/home/792/578122/artclView.do",
    use: "49개국 1,800개 기업, AI/로봇 푸드 컨버전스, 대체육/기호식품/푸드테크",
  },
  {
    id: "S07",
    name: "MFDS/정책브리핑: 2026년부터 가공식품 영양표시 확대",
    type: "정부 정책뉴스",
    date: "2024-08-09",
    url: "https://www.korea.kr/news/policyNewsView.do?newsId=148932450",
    use: "2026~2028 영양표시 단계 의무화, 고카페인/당알코올 표시 강화",
  },
  {
    id: "S08",
    name: "식품의약품안전처: 2026년 영양표시제도 주요 변경사항",
    type: "정부 공지",
    date: "2025-02-28",
    url: "https://www.mfds.go.kr/brd/m_1105/view.do?seq=33773",
    use: "2026년 1월 1일부터 시행되는 영양표시 주요 변경 안내",
  },
  {
    id: "S09",
    name: "ListeningMind: 2026 푸드 트렌드 분석",
    type: "검색 데이터 리포트",
    date: "2026-04-14",
    url: "https://kr.listeningmind.com/2026-health-functional-food-market-trends-2/",
    use: "푸드 논브랜드 키워드 검색 규모, 최근 6개월 급증 키워드, 연령별 검색 관심",
  },
  {
    id: "S10",
    name: "국가데이터처: 2025 통계로 보는 1인가구",
    type: "정부 통계",
    date: "2025-12-09",
    url: "https://mods.go.kr/board.es?act=view&bid=10820&list_no=442130&mainXml=Y&mid=a10301010000",
    use: "2024년 1인가구 804.5만 가구, 전체 가구 36.1%",
  },
  {
    id: "S11",
    name: "식품음료신문: 2026 한국인의 식탁, 건강·편리미엄",
    type: "업계 뉴스",
    date: "2025-11-03",
    url: "https://www.thinkfood.co.kr/news/articleView.html?idxno=103743",
    use: "한 그릇 음식, 샐러드/비빔밥/덮밥 증가, 단백질 시장 진화",
  },
  {
    id: "S12",
    name: "식품음료신문: 고령친화우수식품 시장 성장",
    type: "업계 뉴스",
    date: "2026-04-03",
    url: "https://www.thinkfood.co.kr/news/articleView.html?idxno=105029",
    use: "늘편푸드 2025년 매출 127.87억 원, 제품 수 268개",
  },
  {
    id: "S13",
    name: "푸드아이콘: 장건강·단백질·멀티 기능성",
    type: "업계 뉴스",
    date: "2026-05",
    url: "https://www.foodicon.co.kr/news/articleView.html?idxno=33540",
    use: "단백질과 장건강, 식이섬유, 멀티 기능성 제품 동향",
  },
  {
    id: "S14",
    name: "농림축산식품부: K-푸드+ 2025년 수출 136억 달러",
    type: "정부 보도자료",
    date: "2026-01-12",
    url: "https://www.mafra.go.kr/bbs/home/792/576527/artclView.do",
    use: "K-푸드+ 2025년 수출 136.2억 달러, 2026년 목표 160억 달러",
  },
  {
    id: "S15",
    name: "FIS 식품산업통계정보: 2026 트렌드 Pick 목록",
    type: "공공/시장분석",
    date: "2026-06-05",
    url: "https://www.atfis.or.kr/home/board/FB0002.do",
    use: "2026년 간편식, 체중조절식품, 당류 저감, 고령친화식품 트렌드 Pick 주제 확인",
  },
];

const trendRows = [
  {
    rank: 1,
    keyword: "혼웰식·한그릇 건강식",
    category: "웰니스+편의",
    signal: "1인 가구 증가와 건강지향이 결합해 덮밥, 비빔밥, 샐러드, 샌드위치 등 원보울·원디쉬 포맷이 성장.",
    searchRank: "검색 직접 순위 없음; 검색 데이터상 건강식/식사 카테고리 분산 성장",
    data: "2024년 1인가구 804.5만 가구, 전체 36.1%; 2022~2025 덮밥 +8.2%, 비빔밥 +13.7%, 샐러드 +22.2%",
    fact: "확인",
    sourceIds: "S10, S11, S01",
    opportunity: "1인분 영양 균형 도시락, 고단백 샐러드, 원보울 HMR, 직장인 식단 구독",
    caveat: "혼웰식 자체는 트렌드 명칭이므로 실제 제품화는 세부 메뉴/채널 데이터로 재검증 필요",
    searchScore: 4,
    marketScore: 5,
    newsScore: 5,
    commercialScore: 5,
    confidenceScore: 4,
  },
  {
    rank: 2,
    keyword: "저당·혈당관리·로우스펙",
    category: "건강/규제",
    signal: "당류 저감과 혈당관리 관심이 정책, 검색, 제품 출시로 동시에 확인됨.",
    searchRank: "ListeningMind 최근 6개월 급증 건강 키워드 예시: 저당 팝콘",
    data: "2026~2028 영양표시 259개 품목 확대; 2026년 설탕 부담금 논의와 가공식품 표시 규제 확대",
    fact: "확인",
    sourceIds: "S07, S08, S09, S01, S15",
    opportunity: "저당 간식, 알룰로스/대체당 소스, 혈당관리형 곡물·음료, 영양표시 대응 패키지",
    caveat: "설탕 부담금은 2026년 7월 현재 도입 확정이 아닌 논의/발의 단계",
    searchScore: 5,
    marketScore: 4,
    newsScore: 5,
    commercialScore: 5,
    confidenceScore: 5,
  },
  {
    rank: 3,
    keyword: "간편식 HMR·냉동 프리미엄",
    category: "편의/프리미엄",
    signal: "간편식 시장은 성숙기에 들어섰지만 가성비 즉석섭취식과 건강·미식형 RMR/프리미엄 냉동이 함께 성장.",
    searchRank: "검색 직접 순위 없음; 식사/건강식 탐색 증가와 연계",
    data: "2024년 간편식 국내 판매액 7조 2,606억 원, 2026년 7조 5천억 원 전망; 즉석조리 40.7%, 즉석섭취 38.3%",
    fact: "확인",
    sourceIds: "S01, S02, S15, S11",
    opportunity: "냉동 국·탕·찌개, 건강 도시락, 유명 맛집 RMR, 단백질 강화 간편식",
    caveat: "밀키트/간편조리세트는 일부 하락 신호가 있어 냉동·즉석섭취 중심으로 구분 필요",
    searchScore: 3,
    marketScore: 5,
    newsScore: 5,
    commercialScore: 5,
    confidenceScore: 5,
  },
  {
    rank: 4,
    keyword: "단백질·식이섬유·장건강",
    category: "기능성 식품",
    signal: "단백질이 기본 옵션화되고, 식이섬유/프로바이오틱스/프리바이오틱스가 포만감·장건강·체중관리와 결합.",
    searchRank: "검색 직접 순위 없음; 건강식/저당 검색 구조와 결합",
    data: "글로벌 소비자 63%가 식이섬유 섭취를 늘린다는 보도; 2026 트렌드에서 장건강+단백질 결합 강조",
    fact: "보조 확인",
    sourceIds: "S13, S11, S09",
    opportunity: "고단백 디저트, 식이섬유 음료, 장건강 스낵, 포스트바이오틱스 국물 간편식",
    caveat: "국내 개별 시장규모는 추가 유료/전문 데이터 확인 필요",
    searchScore: 3,
    marketScore: 4,
    newsScore: 4,
    commercialScore: 5,
    confidenceScore: 4,
  },
  {
    rank: 5,
    keyword: "AI 맞춤영양·푸드테크 제조",
    category: "푸드테크",
    signal: "푸드테크산업육성법 시행 이후 2026년은 데이터 표준화, 스마트제조, AI 맞춤식단, 로봇/외식 혁신의 제도화 원년.",
    searchRank: "검색 직접 순위 없음; B2AI/AI 식단은 외식 트렌드 자료에서 반복 등장",
    data: "국내 푸드테크 시장규모 2020년 50조 1,553억 원 -> 2024년 96조 2,332억 원, 연평균 17.7%",
    fact: "확인",
    sourceIds: "S01, S02, S03, S04, S06",
    opportunity: "공장 역량 DB, AI 레시피/원가 산출, 스마트제조 매칭, 개인맞춤 식단 서비스",
    caveat: "AI 키워드는 기술 가능성 대비 실제 식품 구매 전환 검증이 필요",
    searchScore: 3,
    marketScore: 5,
    newsScore: 5,
    commercialScore: 4,
    confidenceScore: 5,
  },
  {
    rank: 6,
    keyword: "K-푸드 수출·라면·쌀가공",
    category: "수출/글로벌",
    signal: "K-푸드 수출이 기록 경신 국면에서 시장 다변화와 수출 구조 고도화 단계로 이동.",
    searchRank: "검색 직접 순위 없음; K-푸드 검색/관광 수요와 별도 검증 필요",
    data: "2025년 K-푸드+ 수출 136.2억 달러, 농식품 104.1억 달러; 2026년 목표 160억 달러. RICE SHOW 2026은 글루텐프리·식물성·전통 가공 조명.",
    fact: "확인",
    sourceIds: "S14, S05, S06, S01",
    opportunity: "라면/소스/쌀가공 수출형 제품, 글루텐프리 떡·면, 할랄/현지 인증 대응",
    caveat: "수출 실적은 2025년 확정/잠정치, 2026년 수치는 목표 또는 1분기 일부 실적",
    searchScore: 3,
    marketScore: 5,
    newsScore: 5,
    commercialScore: 5,
    confidenceScore: 5,
  },
  {
    rank: 7,
    keyword: "온라인 식품·D2C·퀵커머스",
    category: "유통",
    signal: "온라인 식품시장은 코로나 이후 회귀하지 않고 신선식품·간편식까지 구조적으로 확대.",
    searchRank: "검색 직접 순위 없음; 소비 접근성/구매채널 데이터로 보완",
    data: "식품 온라인 거래액 비중 2019년 12.6% -> 2025년 19.1%; 2025년 온라인 전체 시장 275조 원",
    fact: "확인",
    sourceIds: "S01, S02",
    opportunity: "D2C몰, 구독형 식단, 신선/냉동 배송, 리뷰 기반 상품개선",
    caveat: "플랫폼 수수료, 정산, 품질/진위 확인 리스크 관리 필요",
    searchScore: 2,
    marketScore: 5,
    newsScore: 4,
    commercialScore: 4,
    confidenceScore: 5,
  },
  {
    rank: 8,
    keyword: "고령친화식품·케어푸드",
    category: "시니어/헬스케어",
    signal: "초고령사회 진입과 시설/B2B 수요 증가로 고령친화식품이 식품산업의 새 성장축으로 부상.",
    searchRank: "검색 직접 순위 없음; FIS 2026년 4월 트렌드 Pick 주제",
    data: "늘편푸드 매출 2021년 2.3억 원 -> 2025년 127.87억 원; 제품 수 27개 -> 268개 누적",
    fact: "확인",
    sourceIds: "S12, S15",
    opportunity: "연화식, 단백질 강화 반찬, 구독형 케어푸드, 돌봄기관 B2B 납품",
    caveat: "전체 케어푸드 시장과 고령친화우수식품 지정 시장은 범위가 다름",
    searchScore: 2,
    marketScore: 4,
    newsScore: 5,
    commercialScore: 4,
    confidenceScore: 5,
  },
  {
    rank: 9,
    keyword: "피스타치오·두바이쫀득쿠키·비주얼 디저트",
    category: "마이크로 트렌드",
    signal: "SNS형 디저트와 재료 검색이 결합해 메뉴명, 재료, 만들기/레시피, 브랜드 검색으로 확산.",
    searchRank: "ListeningMind 최근 6개월 급증 키워드 예시: 두바이쫀득쿠키, 피스타치오",
    data: "푸드 논브랜드 키워드 100개 기준 연간 약 19억 회, 월평균 약 1.5억 회 검색 규모 안에서 급증 키워드로 공개 언급",
    fact: "확인",
    sourceIds: "S09",
    opportunity: "피스타치오 디저트, 쿠키/베이커리 한정판, 편의점 협업 상품",
    caveat: "급상승 마이크로 트렌드는 수명 짧을 수 있어 재고/생산량 보수적 설계 필요",
    searchScore: 5,
    marketScore: 3,
    newsScore: 4,
    commercialScore: 4,
    confidenceScore: 4,
  },
  {
    rank: 10,
    keyword: "봄동비빔밥·굴무침·제철 한식",
    category: "로컬/제철",
    signal: "한식 및 제철 식재료 검색이 건강식·집밥·레시피 수요와 함께 상승.",
    searchRank: "ListeningMind 최근 6개월 급증 키워드 예시: 봄동비빔밥, 굴무침",
    data: "30대는 레시피/반찬/가정식, 50대 이상은 전통식/건강식 중심 검색 패턴",
    fact: "확인",
    sourceIds: "S09, S11",
    opportunity: "제철 반찬 HMR, 지역 식재료 비빔밥, 로컬 소스/양념 키트",
    caveat: "제철성 강해 시즌 캘린더와 원물 수급 리스크 반영 필요",
    searchScore: 5,
    marketScore: 3,
    newsScore: 4,
    commercialScore: 3,
    confidenceScore: 4,
  },
  {
    rank: 11,
    keyword: "클린라벨·영양표시·GMO/카페인 표시",
    category: "규제/투명성",
    signal: "소비자 알권리 강화와 건강/안전 중심 정책 전환으로 라벨링, 원료 이력, 표시 대응이 상품 경쟁력에 포함.",
    searchRank: "검색 직접 순위 없음; 정책 리스크 기반 트렌드",
    data: "영양표시 259개 품목 확대, 과라나 함유 고체식품 고카페인 주의문구 확대, 당알코올 표시 강화",
    fact: "확인",
    sourceIds: "S07, S08, S01",
    opportunity: "영양성분 자동 산출, 클린라벨 원료, 표시 검수 서비스, 제조 이력 관리",
    caveat: "GMO 완전표시제 등 일부 세부 시행은 하위 규정 확인 필요",
    searchScore: 2,
    marketScore: 4,
    newsScore: 5,
    commercialScore: 4,
    confidenceScore: 5,
  },
  {
    rank: 12,
    keyword: "소용량·가성비·PB 프리미엄",
    category: "가격/패키징",
    signal: "고물가 대응 소비와 1인/소가구 증가가 소용량 포장, 가성비 즉석식, PB 프리미엄화를 밀어올림.",
    searchRank: "검색 직접 순위 없음; KATI/KREI 이슈로 보완",
    data: "KATI 2026 전망에 소용량 포장 및 친환경 혁신 포함; KREI는 고물가와 간편식 양극화 지적",
    fact: "확인",
    sourceIds: "S03, S01, S02",
    opportunity: "소용량 냉동식, 1인용 소스/조미료, PB 건강 간편식, 친환경 패키징",
    caveat: "가성비와 친환경 포장은 원가 상승과 충돌할 수 있어 가격 민감도 테스트 필요",
    searchScore: 2,
    marketScore: 4,
    newsScore: 4,
    commercialScore: 4,
    confidenceScore: 4,
  },
];

const searchRows = [
  ["지표", "값", "범위/기간", "출처", "해석", "한계"],
  ["푸드(식음료) 논브랜드 키워드 검색량", "연간 약 19억 회 이상", "2026 리포트 공개 기준", "S09", "푸드 카테고리가 일상 탐색의 큰 축으로 자리 잡음", "키워드 100개 묶음 기준으로 개별 키워드 절대 검색량은 비공개"],
  ["월평균 검색량", "약 1억 5천만 회 이상", "2026 리포트 공개 기준", "S09", "식품 소비 관심이 상시적으로 발생", "개별 검색엔진/플랫폼 구성은 공개 텍스트만으로 확인 제한"],
  ["연관 키워드", "약 166만 개 이상", "2026 리포트 공개 기준", "S09", "디저트, 식사, 건강식 등 다층적 관심 구조", "중복/유사어 정제 기준은 출처 리포트 기준"],
  ["최근 6개월 급증 키워드", "두바이쫀득쿠키, 피스타치오", "디저트", "S09", "비주얼 디저트와 재료 검색 확산", "공개 본문은 순위표 전체가 아닌 예시 키워드 중심"],
  ["최근 6개월 급증 키워드", "봄동비빔밥, 굴무침", "한식/제철", "S09", "제철 한식과 집밥/레시피 니즈 부상", "계절성 영향 큼"],
  ["최근 6개월 급증 키워드", "저당 팝콘", "건강", "S09", "저당/건강 간식 수요 확인", "절대 검색량 미공개"],
  ["검색량 직접 수집 시도", "Google Trends 공개 API 접근 제한(HTTP 429)", "2026-07-07 확인", "직접 검증", "절대 검색량 재현 불가로 공개 리포트 기반 대체", "워크북의 키워드 순위는 검색량 단독 순위가 아니라 검색+뉴스+시장 데이터 종합순위"],
];

const marketRows = [
  ["항목", "값", "연도/기간", "출처", "관련 키워드", "팩트체크 메모"],
  ["국내 식품제조업 시장 전망", 202.9, "2026 전망, 조 원", "S01/S02", "산업 전체", "KREI 전망치"],
  ["외식산업 시장 전망", 221.5, "2026 전망, 조 원", "S01/S02", "외식/간편식", "KREI 전망치"],
  ["간편식 국내 판매액", 7.2606, "2024, 조 원", "S02", "간편식 HMR", "KREI: 7조 2,606억 원"],
  ["간편식 시장 전망", 7.5, "2026 전망, 조 원", "S02", "간편식 HMR", "KREI 전망치"],
  ["즉석조리식품 비중", 40.7, "2024, %", "S02", "간편식 HMR", "KREI 유형별 비중"],
  ["즉석섭취식품 비중", 38.3, "2024, %", "S02", "간편식 HMR", "KREI 유형별 비중"],
  ["온라인 전체 시장규모", 275, "2025, 조 원", "S02", "온라인 식품", "KREI 인용 온라인 시장규모"],
  ["식품 온라인 거래액 비중", 19.1, "2025, %", "S02", "온라인 식품", "2019년 12.6%에서 상승"],
  ["푸드테크 시장규모", 50.1553, "2020, 조 원", "S02", "푸드테크", "KREI 추정"],
  ["푸드테크 시장규모", 96.2332, "2024, 조 원", "S02", "푸드테크", "KREI 추정"],
  ["푸드테크 연평균 성장률", 17.7, "2020~2024, %", "S02", "푸드테크", "KREI 제시"],
  ["K-푸드+ 수출액", 136.2, "2025, 억 달러", "S14", "K-푸드 수출", "농식품 104.1억, 농산업 32.2억 달러"],
  ["K-푸드+ 수출 목표", 160, "2026 목표, 억 달러", "S14", "K-푸드 수출", "목표치이지 실적 아님"],
  ["RICE SHOW 쌀가공식품 1분기 수출", 7089, "2026 1분기, 만 달러", "S05", "쌀가공/K-푸드", "전년동기 대비 9.6% 증가"],
  ["서울푸드 참가국/기업", 1800, "2026, 개 기업", "S06", "K-푸드/푸드테크", "49개국, 1,800개 기업"],
  ["1인 가구 수", 804.5, "2024, 만 가구", "S10", "혼웰식", "전체 가구의 36.1%"],
  ["고령친화우수식품 매출", 127.87, "2025, 억 원", "S12", "케어푸드", "전년 대비 약 34% 증가"],
  ["고령친화우수식품 제품 수", 268, "2025, 누적 개", "S12", "케어푸드", "2021년 27개에서 확대"],
];

const factRows = [
  ["검증 항목", "판정", "근거 출처", "검증 내용", "주의/한계"],
  ["2026년 식품외식산업 7대 이슈 존재", "확인", "S01/S02", "기후·물가, 푸드테크, 규제, 간편식, 온라인 플랫폼, 외식 비용, K-푸드 세계화가 제시됨", "PDF 공공누리 4유형: 변경금지 조건"],
  ["간편식 2026년 7.5조 원 전망", "확인", "S02", "KREI PDF에서 간편식 시장이 2026년 7조 5천억 원 규모에 달할 것으로 전망", "전망치이며 실제 연간 실적 아님"],
  ["온라인 식품 거래 확대", "확인", "S02", "식품 온라인 거래액 비중이 2019년 12.6%에서 2025년 19.1%까지 증가", "자료 기준과 상품군 정의 확인 필요"],
  ["영양표시 2026~2028 확대", "확인", "S07/S08", "182개 품목에서 77개 추가, 총 259개 품목 적용. 매출 규모별 단계 시행", "세부 적용 품목은 최신 고시 확인 필요"],
  ["검색량 절대 순위 산출", "부분 확인", "S09/직접 검증", "ListeningMind는 검색 규모와 급증 키워드를 공개했으나 개별 키워드 절대 검색량은 공개 본문에 없음", "종합순위는 검색량 단독 순위가 아님"],
  ["두바이쫀득쿠키·피스타치오·저당 팝콘 급증", "확인", "S09", "최근 6개월 검색량 급증 키워드 예시로 공개", "순위표 전체와 수치 원본은 비공개/다운로드 필요"],
  ["K-푸드+ 2025년 수출 136.2억 달러", "확인", "S14", "농식품부 보도자료 기준 잠정치", "2026년 목표 160억 달러는 목표치"],
  ["쌀가공식품 글루텐프리·식물성·전통 가공 트렌드", "확인", "S05", "RICE SHOW 2026 주제관이 해당 트렌드를 집중 조명", "전시회 큐레이션이므로 시장 전체 점유율과는 다름"],
  ["고령친화우수식품 성장", "확인", "S12", "2025년 늘편푸드 매출 127.87억 원, 제품 수 268개 누적", "고령친화우수식품 지정 시장과 전체 케어푸드 시장 구분 필요"],
  ["푸드테크 시장 2024년 96.2조 원", "확인", "S02", "KREI 추정: 2020년 50.1553조 원에서 2024년 96.2332조 원", "푸드테크 범위가 넓어 세부 카테고리별 재분류 필요"],
];

const methodologyRows = [
  ["구분", "내용"],
  ["작성일", generatedAt],
  ["검색 범위", "2026년 대한민국 식품 트렌드를 중심으로 한국어 뉴스, 정부/공공자료, 식품산업 리포트, 검색 데이터 공개 리포트를 확인"],
  ["우선순위", "1차: 정부/공공/연구기관 자료, 2차: 식품 전문지/업계 뉴스, 3차: 브랜드/마케팅 리포트"],
  ["종합순위 산정", "검색/인텐트 점수 + 시장/정책 데이터 점수 + 뉴스 신선도 + 상업화 가능성 + 팩트체크 신뢰도 합산"],
  ["검색량 순위 처리", "개별 키워드의 절대 검색량 원자료가 공개되어 있지 않아, ListeningMind 공개 검색 리포트의 집계 검색량과 급증 키워드를 사용하고, 종합순위에는 시장 데이터와 출처 강도를 함께 반영"],
  ["팩트체크 기준", "숫자·정책·날짜는 원문 출처가 확인되는 경우 '확인', 업계 기사 중심이거나 글로벌 자료를 국내 적용한 경우 '보조 확인'으로 표기"],
  ["주의", "2026년 7월 7일 현재 확인 가능한 자료 기준이며, 2026년 연간 실적은 대부분 전망/목표/1분기 일부 실적임"],
];

function a1(row, col) {
  let s = "";
  let n = col;
  while (n > 0) {
    const m = (n - 1) % 26;
    s = String.fromCharCode(65 + m) + s;
    n = Math.floor((n - 1) / 26);
  }
  return `${s}${row}`;
}

function writeMatrix(sheet, startRow, startCol, matrix) {
  const rows = matrix.length;
  const cols = matrix[0].length;
  const start = a1(startRow, startCol);
  const end = a1(startRow + rows - 1, startCol + cols - 1);
  sheet.getRange(`${start}:${end}`).values = matrix;
}

function styleHeader(range) {
  range.format = {
    fill: "#14532D",
    font: { bold: true, color: "#FFFFFF" },
    wrapText: true,
  };
}

function styleTitle(range) {
  range.format = {
    fill: "#0F172A",
    font: { bold: true, color: "#FFFFFF", size: 14 },
  };
}

function finishSheet(sheet, usedRange, freezeRows = 1) {
  sheet.showGridLines = false;
  if (freezeRows > 0) sheet.freezePanes.freezeRows(freezeRows);
  sheet.getRange(usedRange).format.wrapText = true;
  sheet.getRange(usedRange).format.autofitRows();
}

const workbook = Workbook.create();
workbook.comments.setSelf({ displayName: "User" });

const summary = workbook.worksheets.add("요약");
summary.getRange("A1:L1").merge();
summary.getRange("A1").values = [["2026 대한민국 식품 트렌드 딥서치"]];
styleTitle(summary.getRange("A1:L1"));
summary.getRange("A2:L2").merge();
summary.getRange("A2").values = [[`작성 기준일: ${generatedAt} | 검색량 원자료 한계: 개별 키워드 절대 검색량은 공개 출처로 확인 불가, 공개 검색 리포트와 시장 데이터를 결합한 종합순위입니다.`]];
summary.getRange("A2:L2").format = { fill: "#E2E8F0", font: { color: "#0F172A" }, wrapText: true };
const summaryHeaders = ["종합순위", "트렌드 키워드", "분류", "핵심 신호", "검색량/인텐트 근거", "핵심 데이터", "팩트체크", "출처ID", "상품/사업 기회", "주의점", "종합점수", "우선 액션"];
const summaryValues = trendRows.map((r) => [
  r.rank,
  r.keyword,
  r.category,
  r.signal,
  r.searchRank,
  r.data,
  r.fact,
  r.sourceIds,
  r.opportunity,
  r.caveat,
  null,
  r.rank <= 4 ? "즉시 검증" : r.rank <= 8 ? "파일럿" : "관찰",
]);
writeMatrix(summary, 4, 1, [summaryHeaders, ...summaryValues]);
styleHeader(summary.getRange("A4:L4"));
for (let i = 0; i < trendRows.length; i += 1) {
  const row = 5 + i;
  summary.getRange(`K${row}`).formulas = [[`='키워드_딥서치'!N${row}`]];
}
summary.tables.add(`A4:L${4 + trendRows.length}`, true, "SummaryTable");
summary.getRange("A:A").format.columnWidth = 9;
summary.getRange("B:B").format.columnWidth = 24;
summary.getRange("C:C").format.columnWidth = 14;
summary.getRange("D:F").format.columnWidth = 34;
summary.getRange("G:H").format.columnWidth = 12;
summary.getRange("I:J").format.columnWidth = 36;
summary.getRange("K:L").format.columnWidth = 12;
summary.getRange(`A5:A${4 + trendRows.length}`).format.numberFormat = "#,##0";
summary.getRange(`K5:K${4 + trendRows.length}`).format.numberFormat = "#,##0";
summary.getRange(`G5:G${4 + trendRows.length}`).conditionalFormats.add("containsText", {
  text: "확인",
  format: { fill: "#DCFCE7", font: { color: "#14532D", bold: true } },
});
summary.getRange(`G5:G${4 + trendRows.length}`).conditionalFormats.add("containsText", {
  text: "보조",
  format: { fill: "#FEF3C7", font: { color: "#92400E", bold: true } },
});
summary.getRange("N4:O16").values = [
  ["트렌드", "점수"],
  ...trendRows.map((r) => [r.keyword, null]),
];
for (let i = 0; i < trendRows.length; i += 1) {
  summary.getRange(`O${5 + i}`).formulas = [[`=K${5 + i}`]];
}
const chart = summary.charts.add("bar", summary.getRange("N4:O16"));
chart.title = "2026 식품 트렌드 종합점수";
chart.hasLegend = false;
chart.setPosition("N1", "U20");
finishSheet(summary, "A1:U20", 4);

const deep = workbook.worksheets.add("키워드_딥서치");
const deepHeaders = [
  "종합순위", "트렌드 키워드", "분류", "핵심 신호", "검색량/인텐트 근거", "핵심 데이터", "팩트체크",
  "출처ID", "상품/사업 기회", "주의점", "검색점수", "시장점수", "뉴스점수", "종합점수", "신뢰도점수", "상업화점수"
];
const deepValues = trendRows.map((r) => [
  r.rank, r.keyword, r.category, r.signal, r.searchRank, r.data, r.fact, r.sourceIds,
  r.opportunity, r.caveat, r.searchScore, r.marketScore, r.newsScore, null, r.confidenceScore, r.commercialScore,
]);
writeMatrix(deep, 4, 1, [deepHeaders, ...deepValues]);
deep.getRange("A1:P1").merge();
deep.getRange("A1").values = [["키워드별 딥서치: 검색 신호, 시장 데이터, 출처, 상품화 관점"]];
styleTitle(deep.getRange("A1:P1"));
styleHeader(deep.getRange("A4:P4"));
for (let i = 0; i < trendRows.length; i += 1) {
  const row = 5 + i;
  deep.getRange(`N${row}`).formulas = [[`=K${row}+L${row}+M${row}+O${row}+P${row}`]];
}
deep.tables.add(`A4:P${4 + trendRows.length}`, true, "DeepDiveTable");
deep.getRange("A:A").format.columnWidth = 9;
deep.getRange("B:B").format.columnWidth = 24;
deep.getRange("C:C").format.columnWidth = 14;
deep.getRange("D:J").format.columnWidth = 32;
deep.getRange("K:P").format.columnWidth = 11;
deep.getRange(`K5:P${4 + trendRows.length}`).format.numberFormat = "#,##0";
finishSheet(deep, `A1:P${4 + trendRows.length}`, 4);

const search = workbook.worksheets.add("검색량_근거");
search.getRange("A1:F1").merge();
search.getRange("A1").values = [["검색량/검색 관심도 근거 및 한계"]];
styleTitle(search.getRange("A1:F1"));
writeMatrix(search, 3, 1, searchRows);
styleHeader(search.getRange("A3:F3"));
search.tables.add(`A3:F${2 + searchRows.length}`, true, "SearchEvidenceTable");
search.getRange("A:F").format.columnWidth = 24;
search.getRange("E:F").format.columnWidth = 42;
finishSheet(search, `A1:F${2 + searchRows.length}`, 3);

const market = workbook.worksheets.add("시장데이터");
market.getRange("A1:F1").merge();
market.getRange("A1").values = [["시장·정책·인구 데이터"]];
styleTitle(market.getRange("A1:F1"));
writeMatrix(market, 3, 1, marketRows);
styleHeader(market.getRange("A3:F3"));
market.tables.add(`A3:F${2 + marketRows.length}`, true, "MarketDataTable");
market.getRange("A:A").format.columnWidth = 28;
market.getRange("B:B").format.columnWidth = 13;
market.getRange("C:C").format.columnWidth = 20;
market.getRange("D:F").format.columnWidth = 28;
market.getRange(`B4:B${2 + marketRows.length}`).format.numberFormat = "#,##0.0";
finishSheet(market, `A1:F${2 + marketRows.length}`, 3);

const fact = workbook.worksheets.add("팩트체크_출처");
fact.getRange("A1:E1").merge();
fact.getRange("A1").values = [["팩트체크 기록"]];
styleTitle(fact.getRange("A1:E1"));
writeMatrix(fact, 3, 1, factRows);
styleHeader(fact.getRange("A3:E3"));
fact.tables.add(`A3:E${2 + factRows.length}`, true, "FactCheckTable");
fact.getRange("A:A").format.columnWidth = 30;
fact.getRange("B:B").format.columnWidth = 12;
fact.getRange("C:C").format.columnWidth = 16;
fact.getRange("D:E").format.columnWidth = 48;
fact.getRange(`B4:B${2 + factRows.length}`).conditionalFormats.add("containsText", {
  text: "확인",
  format: { fill: "#DCFCE7", font: { color: "#14532D", bold: true } },
});
fact.getRange(`B4:B${2 + factRows.length}`).conditionalFormats.add("containsText", {
  text: "부분",
  format: { fill: "#FEF3C7", font: { color: "#92400E", bold: true } },
});
finishSheet(fact, `A1:E${2 + factRows.length}`, 3);

const sourceSheet = workbook.worksheets.add("출처_URL");
sourceSheet.getRange("A1:F1").merge();
sourceSheet.getRange("A1").values = [["출처 URL 목록"]];
styleTitle(sourceSheet.getRange("A1:F1"));
const sourceRows = [["ID", "출처명", "유형", "일자", "URL", "사용 목적"], ...sources.map((s) => [s.id, s.name, s.type, s.date, s.url, s.use])];
writeMatrix(sourceSheet, 3, 1, sourceRows);
styleHeader(sourceSheet.getRange("A3:F3"));
sourceSheet.tables.add(`A3:F${2 + sourceRows.length}`, true, "SourceUrlTable");
sourceSheet.getRange("A:A").format.columnWidth = 8;
sourceSheet.getRange("B:B").format.columnWidth = 42;
sourceSheet.getRange("C:D").format.columnWidth = 16;
sourceSheet.getRange("E:E").format.columnWidth = 68;
sourceSheet.getRange("F:F").format.columnWidth = 42;
finishSheet(sourceSheet, `A1:F${2 + sourceRows.length}`, 3);

const method = workbook.worksheets.add("방법론");
method.getRange("A1:B1").merge();
method.getRange("A1").values = [["방법론 및 해석 주의사항"]];
styleTitle(method.getRange("A1:B1"));
writeMatrix(method, 3, 1, methodologyRows);
styleHeader(method.getRange("A3:B3"));
method.tables.add(`A3:B${2 + methodologyRows.length}`, true, "MethodologyTable");
method.getRange("A:A").format.columnWidth = 22;
method.getRange("B:B").format.columnWidth = 95;
finishSheet(method, `A1:B${2 + methodologyRows.length}`, 3);

// Add source comments to key header cells for auditability.
workbook.comments.addThread({ cell: summary.getRange("E4") }, "검색량은 개별 키워드 절대량이 아니라 ListeningMind 공개 검색 리포트와 공개 급증 키워드에 기반한 대체 지표입니다.");
workbook.comments.addThread({ cell: summary.getRange("K4") }, "종합점수 = 검색점수 + 시장점수 + 뉴스점수 + 신뢰도점수 + 상업화점수. 세부 점수는 키워드_딥서치 시트에서 확인하세요.");

const errorScan = await workbook.inspect({
  kind: "match",
  searchTerm: "#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A",
  options: { useRegex: true, maxResults: 300 },
  summary: "formula error scan before export",
});
console.log(errorScan.ndjson);

await fs.mkdir(outputDir, { recursive: true });

for (const sheetName of ["요약", "키워드_딥서치", "검색량_근거", "시장데이터", "팩트체크_출처", "출처_URL", "방법론"]) {
  const preview = await workbook.render({ sheetName, autoCrop: "all", scale: 1, format: "png" });
  await fs.writeFile(path.join(outputDir, `preview_${sheetName}.png`), new Uint8Array(await preview.arrayBuffer()));
}

const output = await SpreadsheetFile.exportXlsx(workbook);
await output.save(outputPath);

const inspectSummary = await workbook.inspect({
  kind: "table",
  range: "요약!A1:L16",
  include: "values,formulas",
  tableMaxRows: 16,
  tableMaxCols: 12,
  maxChars: 4000,
});
console.log(inspectSummary.ndjson);
console.log(JSON.stringify({ outputPath, threadId }, null, 2));
