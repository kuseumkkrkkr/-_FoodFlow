from __future__ import annotations

import json
import os
from datetime import date, datetime
from typing import Any

import requests
from pydantic import BaseModel, Field
from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, String, Text, and_, func, select
from sqlalchemy.orm import Mapped, Session, mapped_column

from .core import (
    Base,
    CostCalculation,
    GeneratedFile,
    IngredientLine,
    ProductRequest,
    RecipeDraft,
    ScreeningFinding,
    ToolRun,
    api_error,
    as_json,
    db_session,
    engine,
    from_json,
    json_payload,
    make_hash,
    now_utc,
    query_int,
    record_tool_run,
)
from .price_crawler import (
    PriceObservation,
    PriceSyncError,
    TrendSnapshot,
    collect_public_crawl_prices,
    collect_kamis_prices,
    env_int,
    start_periodic_price_sync,
)


PRICE_SYNC_SCHEDULER_STARTED = False


class DocumentTemplate(Base):
    __tablename__ = "document_templates"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    doc_type: Mapped[str] = mapped_column(String(40), index=True)
    version: Mapped[int] = mapped_column(Integer, default=1)
    template_name: Mapped[str] = mapped_column(String(120))
    active: Mapped[bool] = mapped_column(Boolean, default=True, index=True)


class DocumentRenderJob(Base):
    __tablename__ = "document_render_jobs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    doc_type: Mapped[str] = mapped_column(String(40), index=True)
    source_id: Mapped[int] = mapped_column(Integer, index=True)
    template_id: Mapped[int | None] = mapped_column(ForeignKey("document_templates.id"), nullable=True)
    status: Mapped[str] = mapped_column(String(40), index=True, default="queued")
    file_id: Mapped[int | None] = mapped_column(ForeignKey("generated_files.id"), nullable=True)
    error_code: Mapped[str] = mapped_column(String(80), default="")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: now_utc())


class DocumentAuditLog(Base):
    __tablename__ = "document_audit_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    file_id: Mapped[int] = mapped_column(ForeignKey("generated_files.id"), index=True)
    user_id: Mapped[int] = mapped_column(Integer, index=True, default=1)
    action: Mapped[str] = mapped_column(String(40), index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: now_utc())


class RecipeEvaluation(Base):
    __tablename__ = "recipe_evaluations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    recipe_id: Mapped[int] = mapped_column(ForeignKey("recipe_drafts.id"), index=True)
    request_id: Mapped[int] = mapped_column(ForeignKey("product_requests.id"), index=True)
    manufacturability_score: Mapped[float] = mapped_column(Float)
    nutrition_estimate: Mapped[str] = mapped_column(Text)
    claim_feasibility: Mapped[str] = mapped_column(String(40))
    allergen_risk: Mapped[str] = mapped_column(String(40))
    process_risk: Mapped[str] = mapped_column(String(40))
    cost_score: Mapped[float] = mapped_column(Float)
    required_tests: Mapped[str] = mapped_column(Text)
    revision_suggestions: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: now_utc())


class NutritionReference(Base):
    __tablename__ = "nutrition_references"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    food_name: Mapped[str] = mapped_column(String(160), index=True)
    category: Mapped[str] = mapped_column(String(80), index=True)
    calories_kcal: Mapped[float] = mapped_column(Float)
    protein_g: Mapped[float] = mapped_column(Float)
    sugar_g: Mapped[float] = mapped_column(Float)
    sodium_mg: Mapped[float] = mapped_column(Float)
    source: Mapped[str] = mapped_column(String(80), default="manual_reference")
    checked_at: Mapped[str] = mapped_column(String(20), default="")


class IngredientPriceIndex(Base):
    __tablename__ = "ingredient_price_indexes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    ingredient_name: Mapped[str] = mapped_column(String(120), index=True)
    source: Mapped[str] = mapped_column(String(60), index=True)
    price: Mapped[float] = mapped_column(Float)
    unit: Mapped[str] = mapped_column(String(30))
    normalized_price_kg: Mapped[float] = mapped_column(Float)
    market: Mapped[str] = mapped_column(String(80), default="")
    grade: Mapped[str] = mapped_column(String(80), default="")
    observed_at: Mapped[str] = mapped_column(String(20), index=True)
    status: Mapped[str] = mapped_column(String(40), index=True, default="manual_input")
    stale: Mapped[bool] = mapped_column(Boolean, default=False, index=True)
    source_url: Mapped[str] = mapped_column(Text, default="")
    trend_5y_change_pct: Mapped[float | None] = mapped_column(Float, nullable=True)
    trend_5y_low_price: Mapped[float | None] = mapped_column(Float, nullable=True)
    trend_5y_high_price: Mapped[float | None] = mapped_column(Float, nullable=True)
    trend_5y_points: Mapped[int] = mapped_column(Integer, default=0)


class FxRate(Base):
    __tablename__ = "fx_rates"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    currency: Mapped[str] = mapped_column(String(10), index=True)
    base_currency: Mapped[str] = mapped_column(String(10), default="KRW")
    rate: Mapped[float] = mapped_column(Float)
    source: Mapped[str] = mapped_column(String(40), default="manual")
    rate_date: Mapped[str] = mapped_column(String(20), index=True)
    stale_flag: Mapped[bool] = mapped_column(Boolean, default=False, index=True)
    fx_buffer_rate: Mapped[float] = mapped_column(Float, default=0.03)


class PriceSyncRun(Base):
    __tablename__ = "price_sync_runs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    source: Mapped[str] = mapped_column(String(60), index=True)
    status: Mapped[str] = mapped_column(String(40), index=True)
    started_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: now_utc())
    finished_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    error_code: Mapped[str] = mapped_column(String(80), default="")
    summary: Mapped[str] = mapped_column(Text, default="")


class RecipeEvaluationCreate(BaseModel):
    include_cost: bool = True


class PriceCreate(BaseModel):
    ingredient_name: str
    price: float = Field(..., ge=0)
    unit: str = "kg"
    normalized_price_kg: float = Field(..., ge=0)
    source: str = "manual_input"
    market: str = ""
    grade: str = ""
    observed_at: str | None = None
    status: str = "manual_input"
    source_url: str = ""


class FxRateCreate(BaseModel):
    currency: str = "USD"
    rate: float = Field(..., gt=0)
    source: str = "manual"
    rate_date: str | None = None
    stale_flag: bool = False
    fx_buffer_rate: float = 0.03


def seed_extra_data(db: Session) -> None:
    if not db.scalar(select(func.count(DocumentTemplate.id))):
        db.add_all(
            [
                DocumentTemplate(doc_type="product_plan", template_name="CBT 제품 기획안 기본", active=True),
                DocumentTemplate(doc_type="sample_brief", template_name="CBT 샘플 발주안 기본", active=True),
            ]
        )

    if not db.scalar(select(func.count(NutritionReference.id))):
        db.add_all(
            [
                NutritionReference(food_name="곡물 단백질바 참고", category="건강간식", calories_kcal=380, protein_g=18, sugar_g=6, sodium_mg=180, checked_at=str(date.today())),
                NutritionReference(food_name="식이섬유 분말 참고", category="분말스틱", calories_kcal=220, protein_g=5, sugar_g=3, sodium_mg=90, checked_at=str(date.today())),
                NutritionReference(food_name="저당 매운 소스 참고", category="소스", calories_kcal=90, protein_g=2, sugar_g=5, sodium_mg=780, checked_at=str(date.today())),
            ]
        )

    if not db.scalar(select(func.count(IngredientPriceIndex.id))):
        today = str(date.today())
        db.add_all(
            [
                IngredientPriceIndex(ingredient_name="현미", source="manual_reference", price=4200, unit="kg", normalized_price_kg=4200, market="내부 참고", grade="일반", observed_at=today, status="manual_input"),
                IngredientPriceIndex(ingredient_name="대두단백", source="supplier_quote", price=9800, unit="kg", normalized_price_kg=9800, market="내부 견적", grade="식품용", observed_at=today, status="confirmed_quote"),
                IngredientPriceIndex(ingredient_name="알룰로스", source="supplier_quote", price=6200, unit="kg", normalized_price_kg=6200, market="내부 견적", grade="시럽/분말 후보", observed_at=today, status="confirmed_quote"),
                IngredientPriceIndex(ingredient_name="계란", source="public_reference", price=5800, unit="kg", normalized_price_kg=5800, market="공공 참고", grade="가공용 환산", observed_at=today, status="public_reference"),
                IngredientPriceIndex(ingredient_name="스틱필름", source="manual_input", price=32, unit="매", normalized_price_kg=0, market="포장재", grade="식품용 확인 필요", observed_at=today, status="manual_input"),
            ]
        )

    if not db.scalar(select(func.count(FxRate.id))):
        db.add_all(
            [
                FxRate(currency="USD", rate=1380.0, source="manual", rate_date=str(date.today()), stale_flag=True, fx_buffer_rate=0.03),
                FxRate(currency="EUR", rate=1500.0, source="manual", rate_date=str(date.today()), stale_flag=True, fx_buffer_rate=0.03),
            ]
        )


def ensure_extra_schema_columns() -> None:
    with engine.begin() as conn:
        rows = conn.exec_driver_sql("PRAGMA table_info(ingredient_price_indexes)").fetchall()
        existing = {row[1] for row in rows}
        additions = {
            "source_url": "TEXT DEFAULT ''",
            "trend_5y_change_pct": "FLOAT",
            "trend_5y_low_price": "FLOAT",
            "trend_5y_high_price": "FLOAT",
            "trend_5y_points": "INTEGER DEFAULT 0",
        }
        for name, ddl in additions.items():
            if name not in existing:
                conn.exec_driver_sql(f"ALTER TABLE ingredient_price_indexes ADD COLUMN {name} {ddl}")


def serialize_price(row: IngredientPriceIndex) -> dict[str, Any]:
    return {
        "id": row.id,
        "ingredient_name": row.ingredient_name,
        "source": row.source,
        "price": row.price,
        "unit": row.unit,
        "normalized_price_kg": row.normalized_price_kg,
        "market": row.market,
        "grade": row.grade,
        "observed_at": row.observed_at,
        "status": row.status,
        "stale": row.stale,
        "source_url": row.source_url,
        "trend_5y_change_pct": row.trend_5y_change_pct,
        "trend_5y_low_price": row.trend_5y_low_price,
        "trend_5y_high_price": row.trend_5y_high_price,
        "trend_5y_points": row.trend_5y_points,
    }


def serialize_fx(row: FxRate) -> dict[str, Any]:
    return {
        "id": row.id,
        "currency": row.currency,
        "base_currency": row.base_currency,
        "rate": row.rate,
        "source": row.source,
        "rate_date": row.rate_date,
        "stale_flag": row.stale_flag,
        "fx_buffer_rate": row.fx_buffer_rate,
    }


def price_identity(row: PriceObservation) -> tuple[str, str, str, str, str]:
    return (row.ingredient_name, row.source, row.market, row.grade, row.observed_at)


def apply_trend(row: IngredientPriceIndex, trend: TrendSnapshot | None) -> None:
    if trend is None:
        return
    row.trend_5y_change_pct = trend.change_pct
    row.trend_5y_low_price = trend.low_price
    row.trend_5y_high_price = trend.high_price
    row.trend_5y_points = trend.points


def upsert_price_observations(
    db: Session,
    observations: list[PriceObservation],
    trends: dict[str, TrendSnapshot],
) -> int:
    if not observations:
        return 0

    names = sorted({row.ingredient_name for row in observations})
    dates = sorted({row.observed_at for row in observations})
    sources = sorted({row.source for row in observations})
    rows = db.scalars(
        select(IngredientPriceIndex).where(
            IngredientPriceIndex.source.in_(sources),
            IngredientPriceIndex.ingredient_name.in_(names),
            IngredientPriceIndex.observed_at >= dates[0],
            IngredientPriceIndex.observed_at <= dates[-1],
        )
    ).all()
    existing = {
        (row.ingredient_name, row.source, row.market, row.grade, row.observed_at): row
        for row in rows
    }

    changed = 0
    for item in observations:
        key = price_identity(item)
        row = existing.get(key)
        if row is None:
            row = IngredientPriceIndex(
                ingredient_name=item.ingredient_name,
                source=item.source,
                price=item.price,
                unit=item.unit,
                normalized_price_kg=item.normalized_price_kg,
                market=item.market,
                grade=item.grade,
                observed_at=item.observed_at,
                status=item.status,
                source_url=item.source_url,
                stale=False,
            )
            existing[key] = row
            db.add(row)
            changed += 1
        else:
            row.price = item.price
            row.unit = item.unit
            row.normalized_price_kg = item.normalized_price_kg
            row.status = item.status
            row.source_url = item.source_url
            row.stale = False
            changed += 1
        apply_trend(row, trends.get(item.ingredient_name))
    return changed


def run_public_price_sync(db: Session, history_years: int) -> PriceSyncRun:
    run = PriceSyncRun(source="worldbank_pink_sheet", status="running")
    db.add(run)
    db.flush()
    try:
        observations, trends, summary = collect_public_crawl_prices(years=history_years)
        changed = upsert_price_observations(db, observations, trends)
        run.status = "succeeded" if observations else "skipped"
        run.summary = f"{summary}; DB 반영 {changed}건"
        run.finished_at = now_utc()
    except (PriceSyncError, requests.RequestException, ValueError, OSError) as exc:
        run.status = "failed"
        run.error_code = exc.__class__.__name__
        run.summary = str(exc)
        run.finished_at = now_utc()
    return run


def run_kamis_price_sync(db: Session, history_years: int) -> PriceSyncRun:
    run = PriceSyncRun(source="kamis_api", status="running")
    db.add(run)
    db.flush()
    try:
        observations, trends, summary = collect_kamis_prices(years=history_years)
        changed = upsert_price_observations(db, observations, trends)
        run.status = "succeeded" if observations else "skipped"
        run.summary = f"{summary}; DB 반영 {changed}건"
        run.finished_at = now_utc()
    except (PriceSyncError, requests.RequestException) as exc:
        run.status = "failed"
        run.error_code = exc.__class__.__name__
        run.summary = str(exc)
        run.finished_at = now_utc()
    return run


def run_periodic_public_sync_once() -> None:
    history_years = env_int("PRICE_SYNC_HISTORY_YEARS", 5, 1, 5)
    with db_session() as db:
        run_public_price_sync(db, history_years)


def ensure_price_sync_scheduler_started() -> None:
    global PRICE_SYNC_SCHEDULER_STARTED
    if PRICE_SYNC_SCHEDULER_STARTED:
        return
    PRICE_SYNC_SCHEDULER_STARTED = True
    start_periodic_price_sync(run_periodic_public_sync_once)


def evaluate_recipe(db: Session, recipe: RecipeDraft, include_cost: bool = True) -> RecipeEvaluation:
    findings = list(db.scalars(select(ScreeningFinding).where(ScreeningFinding.request_id == recipe.request_id)))
    ingredients = list(db.scalars(select(IngredientLine).where(IngredientLine.request_id == recipe.request_id)))
    cost = db.scalar(select(CostCalculation).where(CostCalculation.request_id == recipe.request_id).order_by(CostCalculation.id.desc()))
    red_count = sum(1 for finding in findings if finding.severity == "RED")
    yellow_count = sum(1 for finding in findings if finding.severity == "YELLOW")
    allergen_count = sum(1 for line in ingredients if line.allergen_flag)
    manufacturability = max(45, 88 - red_count * 12 - yellow_count * 3 - allergen_count * 2)
    cost_score = 80.0
    if include_cost and cost:
        cost_score = max(35, min(95, 95 - max(0, cost.unit_cost - 900) / 40))
    nutrition = {
        "calories_kcal": "유사 식품 참고 추정",
        "protein": "고단백/단백질 문구는 분석값 필요",
        "sugar": "저당/무당 문구는 영양성분 분석값 필요",
        "sodium": "소스류는 나트륨 강조표시 기준 확인",
    }
    required_tests = ["영양성분 분석", "알레르기 교차오염 확인", "라벨 검수"]
    if red_count:
        required_tests.insert(0, "표시광고 전문가 검토")
    suggestions = ["공장 샘플 3종으로 맛/식감 비교", "원료 대체 가능 여부와 MOQ 동시 확인"]
    if cost_score < 65:
        suggestions.append("포장비 또는 샘플비를 분리 견적해 목표 원가를 재검토")
    evaluation = RecipeEvaluation(
        recipe_id=recipe.id,
        request_id=recipe.request_id,
        manufacturability_score=round(float(manufacturability), 1),
        nutrition_estimate=as_json(nutrition),
        claim_feasibility="위험" if red_count else "주의" if yellow_count else "좋음",
        allergen_risk="주의" if allergen_count else "낮음",
        process_risk="주의" if manufacturability < 70 else "좋음",
        cost_score=round(float(cost_score), 1),
        required_tests=as_json(required_tests),
        revision_suggestions=as_json(suggestions),
    )
    db.add(evaluation)
    record_tool_run(db, recipe.request_id, "recipe_evaluator", {"recipe_id": recipe.id}, f"레시피 평가 {evaluation.claim_feasibility}")
    return evaluation


def serialize_evaluation(row: RecipeEvaluation) -> dict[str, Any]:
    return {
        "id": row.id,
        "recipe_id": row.recipe_id,
        "request_id": row.request_id,
        "manufacturability_score": row.manufacturability_score,
        "nutrition_estimate": from_json(row.nutrition_estimate, {}),
        "claim_feasibility": row.claim_feasibility,
        "allergen_risk": row.allergen_risk,
        "process_risk": row.process_risk,
        "cost_score": row.cost_score,
        "required_tests": from_json(row.required_tests, []),
        "revision_suggestions": from_json(row.revision_suggestions, []),
        "created_at": row.created_at.isoformat(),
    }


def register_extra_routes(app) -> None:
    Base.metadata.create_all(bind=engine)
    ensure_extra_schema_columns()
    with db_session() as db:
        seed_extra_data(db)
    ensure_price_sync_scheduler_started()

    @app.get("/api/ingredient-prices")
    def list_ingredient_prices() -> dict[str, Any]:
        from flask import request

        q = request.args.get("q")
        source = request.args.get("source")
        history = request.args.get("history", "").lower() in {"1", "true", "yes", "y"}
        limit = query_int("limit", 30, 1, 100)
        offset = query_int("offset", 0, 0)
        with db_session() as db:
            filters = []
            if q:
                filters.append(IngredientPriceIndex.ingredient_name.like(f"%{q}%"))
            if source:
                filters.append(IngredientPriceIndex.source == source)
            if history:
                total = db.scalar(select(func.count(IngredientPriceIndex.id)).where(*filters))
                rows = db.scalars(
                    select(IngredientPriceIndex)
                    .where(*filters)
                    .order_by(IngredientPriceIndex.observed_at.desc(), IngredientPriceIndex.ingredient_name)
                    .limit(limit)
                    .offset(offset)
                ).all()
                return {"total": total, "items": [serialize_price(row) for row in rows]}

            latest = (
                select(
                    IngredientPriceIndex.ingredient_name.label("ingredient_name"),
                    IngredientPriceIndex.source.label("source"),
                    IngredientPriceIndex.market.label("market"),
                    IngredientPriceIndex.grade.label("grade"),
                    func.max(IngredientPriceIndex.observed_at).label("observed_at"),
                )
                .where(*filters)
                .group_by(
                    IngredientPriceIndex.ingredient_name,
                    IngredientPriceIndex.source,
                    IngredientPriceIndex.market,
                    IngredientPriceIndex.grade,
                )
                .subquery()
            )
            total = db.scalar(select(func.count()).select_from(latest))
            rows = db.scalars(
                select(IngredientPriceIndex)
                .join(
                    latest,
                    and_(
                        IngredientPriceIndex.ingredient_name == latest.c.ingredient_name,
                        IngredientPriceIndex.source == latest.c.source,
                        IngredientPriceIndex.market == latest.c.market,
                        IngredientPriceIndex.grade == latest.c.grade,
                        IngredientPriceIndex.observed_at == latest.c.observed_at,
                    ),
                )
                .order_by(IngredientPriceIndex.observed_at.desc(), IngredientPriceIndex.ingredient_name)
                .limit(limit)
                .offset(offset)
            ).all()
            return {"total": total, "items": [serialize_price(row) for row in rows]}

    @app.post("/api/admin/ingredient-prices")
    def create_ingredient_price() -> dict[str, Any]:
        payload = json_payload(PriceCreate)
        with db_session() as db:
            row = IngredientPriceIndex(
                ingredient_name=payload.ingredient_name,
                source=payload.source,
                price=payload.price,
                unit=payload.unit,
                normalized_price_kg=payload.normalized_price_kg,
                market=payload.market,
                grade=payload.grade,
                observed_at=payload.observed_at or str(date.today()),
                status=payload.status,
                source_url=payload.source_url,
            )
            db.add(row)
            db.flush()
            return serialize_price(row)

    @app.get("/api/fx-rates")
    def list_fx_rates() -> dict[str, Any]:
        from flask import request

        currency = request.args.get("currency")
        with db_session() as db:
            filters = []
            if currency:
                filters.append(FxRate.currency == currency.upper())
            rows = db.scalars(select(FxRate).where(*filters).order_by(FxRate.currency, FxRate.rate_date.desc())).all()
            return {"items": [serialize_fx(row) for row in rows]}

    @app.post("/api/admin/fx-rates")
    def create_fx_rate() -> dict[str, Any]:
        payload = json_payload(FxRateCreate)
        with db_session() as db:
            row = FxRate(
                currency=payload.currency.upper(),
                rate=payload.rate,
                source=payload.source,
                rate_date=payload.rate_date or str(date.today()),
                stale_flag=payload.stale_flag,
                fx_buffer_rate=payload.fx_buffer_rate,
            )
            db.add(row)
            db.flush()
            return serialize_fx(row)

    @app.post("/api/admin/price-sync-runs")
    def create_price_sync_run() -> dict[str, Any]:
        from flask import request

        source = request.args.get("source", "worldbank_pink_sheet")
        history_years = query_int("history_years", env_int("PRICE_SYNC_HISTORY_YEARS", 5, 1, 5), 1, 5)
        with db_session() as db:
            if source in {"kamis", "kamis_api"}:
                row = run_kamis_price_sync(db, history_years)
            elif source in {"crawl", "public_crawl", "worldbank", "worldbank_pink_sheet"}:
                row = run_public_price_sync(db, history_years)
            else:
                row = PriceSyncRun(source=source, status="succeeded", finished_at=now_utc(), summary="CBT 수동 기준 데이터 확인")
                db.add(row)
            db.flush()
            return {"id": row.id, "source": row.source, "status": row.status, "summary": row.summary, "error_code": row.error_code}

    @app.get("/api/admin/price-sync-runs")
    def list_price_sync_runs() -> dict[str, Any]:
        limit = query_int("limit", 10, 1, 50)
        with db_session() as db:
            rows = db.scalars(select(PriceSyncRun).order_by(PriceSyncRun.started_at.desc()).limit(limit)).all()
            return {
                "configured": True,
                "public_crawl_source": "worldbank_pink_sheet",
                "kamis_configured": bool(os.getenv("KAMIS_CERT_KEY") and os.getenv("KAMIS_CERT_ID")),
                "items": [
                    {
                        "id": row.id,
                        "source": row.source,
                        "status": row.status,
                        "started_at": row.started_at.isoformat(),
                        "finished_at": row.finished_at.isoformat() if row.finished_at else None,
                        "error_code": row.error_code,
                        "summary": row.summary,
                    }
                    for row in rows
                ],
            }

    @app.get("/api/admin/price-sync-runs/<int:run_id>")
    def get_price_sync_run(run_id: int) -> dict[str, Any]:
        with db_session() as db:
            row = db.get(PriceSyncRun, run_id)
            if not row:
                api_error(404, "price_sync_run_not_found")
            return {"id": row.id, "source": row.source, "status": row.status, "started_at": row.started_at.isoformat(), "finished_at": row.finished_at.isoformat() if row.finished_at else None, "error_code": row.error_code, "summary": row.summary}

    @app.post("/api/recipes/<int:recipe_id>/evaluations")
    def create_recipe_evaluation(recipe_id: int) -> dict[str, Any]:
        payload = json_payload(RecipeEvaluationCreate)
        with db_session() as db:
            recipe = db.get(RecipeDraft, recipe_id)
            if not recipe:
                api_error(404, "recipe_not_found")
            row = evaluate_recipe(db, recipe, include_cost=payload.include_cost)
            db.flush()
            return serialize_evaluation(row)

    @app.get("/api/recipes/<int:recipe_id>/evaluations/<int:evaluation_id>")
    def get_recipe_evaluation(recipe_id: int, evaluation_id: int) -> dict[str, Any]:
        with db_session() as db:
            row = db.get(RecipeEvaluation, evaluation_id)
            if not row or row.recipe_id != recipe_id:
                api_error(404, "recipe_evaluation_not_found")
            return serialize_evaluation(row)

    @app.get("/api/product-requests/<int:request_id>/recipe-evaluations")
    def list_request_recipe_evaluations(request_id: int) -> dict[str, Any]:
        with db_session() as db:
            rows = db.scalars(select(RecipeEvaluation).where(RecipeEvaluation.request_id == request_id).order_by(RecipeEvaluation.id.desc())).all()
            return {"items": [serialize_evaluation(row) for row in rows]}

    @app.get("/api/nutrition-references")
    def list_nutrition_references() -> dict[str, Any]:
        from flask import request

        q = request.args.get("q")
        with db_session() as db:
            filters = []
            if q:
                filters.append(NutritionReference.food_name.like(f"%{q}%"))
            rows = db.scalars(select(NutritionReference).where(*filters).order_by(NutritionReference.food_name).limit(30)).all()
            return {
                "items": [
                    {
                        "id": row.id,
                        "food_name": row.food_name,
                        "category": row.category,
                        "calories_kcal": row.calories_kcal,
                        "protein_g": row.protein_g,
                        "sugar_g": row.sugar_g,
                        "sodium_mg": row.sodium_mg,
                        "source": row.source,
                        "checked_at": row.checked_at,
                    }
                    for row in rows
                ]
            }

    @app.get("/api/document-audit-logs")
    def list_document_audit_logs() -> dict[str, Any]:
        limit = query_int("limit", 30, 1, 100)
        with db_session() as db:
            rows = db.scalars(select(DocumentAuditLog).order_by(DocumentAuditLog.created_at.desc()).limit(limit)).all()
            return {"items": [{"id": row.id, "file_id": row.file_id, "user_id": row.user_id, "action": row.action, "created_at": row.created_at.isoformat()} for row in rows]}

    @app.post("/api/files/<file_uid>/audit")
    def create_document_audit(file_uid: str) -> dict[str, Any]:
        from flask import request

        action = request.args.get("action", "download")
        with db_session() as db:
            file_row = db.scalar(select(GeneratedFile).where(GeneratedFile.file_uid == file_uid))
            if not file_row:
                api_error(404, "file_not_found")
            audit = DocumentAuditLog(file_id=file_row.id, action=action)
            db.add(audit)
            db.flush()
            return {"id": audit.id, "file_id": audit.file_id, "action": audit.action}
