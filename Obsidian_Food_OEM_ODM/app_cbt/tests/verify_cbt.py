from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import Request, urlopen


BASE_URL = os.getenv("BASE_URL", "http://127.0.0.1:8010")


def request_json(method: str, path: str, payload: dict | None = None) -> dict:
    body = json.dumps(payload, ensure_ascii=False).encode("utf-8") if payload is not None else None
    req = Request(
        f"{BASE_URL}{path}",
        data=body,
        method=method,
        headers={"Content-Type": "application/json; charset=utf-8"},
    )
    try:
        with urlopen(req, timeout=20) as response:
            return json.loads(response.read().decode("utf-8"))
    except HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"{method} {path} failed: {exc.code} {detail}") from exc


def assert_true(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> None:
    health = request_json("GET", "/api/health")
    assert_true(health["status"] == "ok", "health check failed")
    assert_true(health["factories"] >= 100, "factory seed was not loaded")
    assert_true(health["rules"] >= 10, "regulatory rule seed was not loaded")
    prices = request_json("GET", "/api/ingredient-prices")
    assert_true(len(prices["items"]) >= 3, "ingredient price seed was not loaded")
    fx_rates = request_json("GET", "/api/fx-rates")
    assert_true(len(fx_rates["items"]) >= 1, "fx rate seed was not loaded")
    sync_run = request_json("POST", "/api/admin/price-sync-runs?source=manual_reference")
    assert_true(sync_run["status"] == "succeeded", "price sync run failed")
    public_sync = request_json("POST", "/api/admin/price-sync-runs?source=worldbank_pink_sheet&history_years=5")
    assert_true(public_sync["status"] == "succeeded", "public price crawl failed")
    sync_runs = request_json("GET", "/api/admin/price-sync-runs?limit=3")
    assert_true(len(sync_runs["items"]) >= 1, "price sync runs missing")
    crawled_prices = request_json("GET", "/api/ingredient-prices?source=worldbank_pink_sheet&limit=5")
    assert_true(len(crawled_prices["items"]) >= 1, "public crawled prices missing")
    filter_options = request_json("GET", "/api/admin/factory-filter-options")
    assert_true(len(filter_options["product_cases"]) >= 3, "factory filter options missing")
    filtered_factories = request_json("GET", "/api/admin/factories?product_case=sauce&cert=HACCP&mvp_fit=A&active=true&limit=5")
    assert_true(filtered_factories["total"] >= 1, "filtered factory search returned no result")
    vibe_options = request_json("GET", "/api/vibe-cooking/options")
    assert_true(len(vibe_options["targets"]) >= 3, "vibe cooking target options missing")
    composed = request_json(
        "POST",
        "/api/vibe-cooking/compose",
        {
            "product_case": "health_snack",
            "base_idea": "저당 고단백 그래놀라바를 만들고 싶다.",
            "target_customer": "office",
            "eating_scene": "snack",
            "texture": "chewy",
            "process_mode": "high_protein",
            "key_ingredients": ["귀리", "분리대두단백", "알룰로스"],
            "avoid_ingredients": ["설탕", "물엿"],
            "claim_list": ["저당"],
            "sales_type": "공동구매",
            "package_type": "개별포장",
            "target_qty_text": "1,000개",
            "target_price": "소비자가 2,900원 이하",
        },
    )
    assert_true("request_payload" in composed, "vibe cooking compose payload missing")
    assert_true("고단백" in composed["request_payload"]["claim_list"], "vibe cooking claim merge failed")

    scenarios = [
        composed["request_payload"],
        {
            "raw_prompt": "저당 고단백 그래놀라바를 온라인 공동구매로 1,000개 테스트 생산하고 싶다. 개별포장과 단백질 강조가 필요하다.",
            "product_case": "health_snack",
            "sales_type": "공동구매",
            "target_qty_text": "1,000개",
            "package_type": "개별포장",
            "claim_list": ["저당", "고단백"],
        },
        {
            "raw_prompt": "식이섬유 분말을 5,000포 스틱포로 만들고 싶다. 장건강 표현은 위험한지 확인이 필요하다.",
            "product_case": "powder_stick",
            "sales_type": "D2C",
            "target_qty_text": "5,000포",
            "package_type": "스틱",
            "claim_list": ["식이섬유", "장건강"],
        },
        {
            "raw_prompt": "프랜차이즈용 저당 매운 소스를 1톤 파우치로 만들고 싶다. 살균 조건과 나트륨 확인이 필요하다.",
            "product_case": "sauce",
            "sales_type": "프랜차이즈",
            "target_qty_text": "1톤",
            "package_type": "파우치",
            "claim_list": ["저당", "나트륨 감소"],
        },
    ]

    created_ids: list[int] = []
    for scenario in scenarios:
        payload = {**scenario, "is_dummy": True, "run_full": True}
        detail = request_json("POST", "/api/product-requests", payload)
        created_ids.append(detail["id"])
        assert_true(detail["status"] in {"brief_ready", "needs_review"}, f"unexpected status: {detail['status']}")
        assert_true(detail["spec"] is not None, "spec missing")
        assert_true(len(detail["recipe"]["ingredients"]) >= 3, "recipe ingredients missing")
        assert_true(detail["screening"]["overall_status"] in {"RED", "YELLOW", "GREEN"}, "screening missing")
        assert_true(len(detail["matches"]) >= 1, "factory match missing")
        assert_true(detail["product_plan"] is not None, "product plan missing")
        assert_true(detail["sample_brief"] is not None, "sample brief missing")
        assert_true(detail["cost_calculation"]["unit_cost"] > 0, "cost calculation missing")
        agent = request_json(
            "POST",
            f"/api/product-requests/{detail['id']}/vibe-agent",
            {"planning_goal": "기획 의도에 맞는 샘플 발주 가능 상태로 정리", "include_revision_prompt": True},
        )
        assert_true(agent["readiness_score"] > 0, "vibe agent score missing")
        assert_true(agent["decision"] in {"send_brief", "revise", "hold"}, "vibe agent decision invalid")
        assert_true(len(agent["recommended_actions"]) >= 1, "vibe agent actions missing")
        recipe_id = detail["recipe"]["id"]
        evaluation = request_json("POST", f"/api/recipes/{recipe_id}/evaluations", {"include_cost": True})
        assert_true(evaluation["manufacturability_score"] > 0, "recipe evaluation missing")
        evaluations = request_json("GET", f"/api/product-requests/{detail['id']}/recipe-evaluations")
        assert_true(len(evaluations["items"]) >= 1, "request recipe evaluations missing")
        pdf = request_json("POST", f"/api/product-requests/{detail['id']}/documents/product_plan/pdf")
        assert_true(pdf["file_uid"], "pdf file uid missing")
        with urlopen(f"{BASE_URL}{pdf['download_url']}", timeout=20) as response:
            assert_true(response.status == 200, "pdf download failed")
            assert_true(response.read(4) == b"%PDF", "download is not a pdf")
        raw_order_form = "\n".join(
            [
                "발주처: CBT 더미 발주처",
                "공급처: 더미 공급사",
                "발주일: 2026-07-07",
                "납기일: 2026-08-31",
                "납품장소: 서울시 성동구 더미 물류센터",
                "결제조건: 세금계산서 발행 후 30일 이내 지급",
                "품목명: 더미 제품 생산",
                f"수량: {detail['target_qty']}{detail['qty_unit']}",
                f"단가: {detail['cost_calculation']['supply_price']}",
                "VAT: 별도",
            ]
        )
        parsed_po = request_json("POST", f"/api/product-requests/{detail['id']}/purchase-orders/parse-form", {"raw_order_form": raw_order_form})
        assert_true(parsed_po["parsed"]["supplier_company"] == "더미 공급사", "purchase order supplier parse failed")
        assert_true(parsed_po["parsed"]["due_date"] == "2026-08-31", "purchase order due date parse failed")
        po = request_json(
            "POST",
            f"/api/product-requests/{detail['id']}/purchase-orders",
            {
                "buyer_company": "CBT 더미 발주처",
                "buyer_contact": "검증 담당자",
                "supplier_company": "더미 공급사",
                "supplier_contact": "공급 담당자",
                "due_date": "2026-08-31",
                "delivery_place": "서울시 성동구 더미 물류센터",
                "payment_terms": "세금계산서 발행 후 30일 이내 지급",
                "delivery_terms": "지정 장소 납품, 운송비 포함 여부 확인",
                "inspection_terms": "입고 수량, 외관, 표시사항, 시험성적서 확인 후 검수",
                "raw_order_form": raw_order_form,
                "line_items": [
                    {
                        "item_name": f"{detail['product_case_label']} 생산",
                        "specification": detail["raw_prompt"],
                        "quantity": detail["target_qty"],
                        "unit": detail["qty_unit"],
                        "unit_price": detail["cost_calculation"]["supply_price"],
                        "notes": "검증용 더미 품목",
                    }
                ],
                "quality_terms": ["입고 검수", "표시사항 확인"],
                "required_documents": ["견적서", "사업자등록증", "인증서"],
                "is_dummy": True,
            },
        )
        assert_true(po["status"] == "ready_to_send", f"purchase order not ready: {po['status']}")
        assert_true(po["total_amount"] > 0, "purchase order amount missing")
        po_list = request_json("GET", f"/api/product-requests/{detail['id']}/purchase-orders")
        assert_true(len(po_list["items"]) >= 1, "purchase order list missing")
        po_pdf = request_json("POST", f"/api/purchase-orders/{po['id']}/documents/pdf")
        assert_true(po_pdf["file_uid"], "purchase order pdf file uid missing")
        with urlopen(f"{BASE_URL}{po_pdf['download_url']}", timeout=20) as response:
            assert_true(response.status == 200, "purchase order pdf download failed")
            assert_true(response.read(4) == b"%PDF", "purchase order download is not a pdf")

    cleanup = request_json("DELETE", "/api/dummy-data")
    assert_true(set(created_ids).issubset(set(cleanup["deleted"])), "dummy cleanup did not delete created requests")
    assert_true(len(cleanup.get("deleted_purchase_orders", [])) >= len(created_ids), "dummy purchase orders were not deleted")
    print(json.dumps({"ok": True, "created_ids": created_ids, "deleted": cleanup["deleted"]}, ensure_ascii=False))


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"CBT verification failed: {exc}", file=sys.stderr)
        sys.exit(1)
