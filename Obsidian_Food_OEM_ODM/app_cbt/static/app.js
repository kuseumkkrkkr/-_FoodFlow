const state = {
  selectedRequestId: null,
  detail: null,
  vibeOptions: null,
  agentReport: null,
};

const $ = (selector) => document.querySelector(selector);
const $$ = (selector) => [...document.querySelectorAll(selector)];

async function api(path, options = {}) {
  const response = await fetch(path, {
    headers: { "Content-Type": "application/json", ...(options.headers || {}) },
    ...options,
  });
  if (!response.ok) {
    const text = await response.text();
    throw new Error(text || response.statusText);
  }
  return response.json();
}

function formatNumber(value) {
  return Number(value || 0).toLocaleString("ko-KR");
}

function formatMoney(value) {
  return `${formatNumber(Math.round(Number(value || 0)))}원`;
}

function escapeHtml(value) {
  return String(value ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function badge(value) {
  return `<span class="badge ${value}">${value}</span>`;
}

function card(title, body) {
  return `<div class="data-card"><h3>${title}</h3>${body}</div>`;
}

function renderKeyValues(obj) {
  return `<dl class="kv">${Object.entries(obj || {})
    .map(([key, value]) => `<dt>${key}</dt><dd>${Array.isArray(value) || typeof value === "object" ? JSON.stringify(value) : value}</dd>`)
    .join("")}</dl>`;
}

function renderPills(items) {
  return `<div class="pill-row">${(items || []).map((item) => `<span class="pill">${item}</span>`).join("")}</div>`;
}

function splitList(value) {
  return (value || "").split(",").map((item) => item.trim()).filter(Boolean);
}

function fillSelect(selector, items) {
  const element = $(selector);
  if (!element) return;
  element.innerHTML = (items || []).map((item) => `<option value="${escapeHtml(item.value)}">${escapeHtml(item.label)}</option>`).join("");
}

async function loadHealth() {
  const health = await api("/api/health");
  $("#healthBox").innerHTML = `상태: ${health.status}<br />공장 ${formatNumber(health.factories)}개 · 규칙 ${formatNumber(health.rules)}개`;
}

async function loadVibeOptions() {
  state.vibeOptions = await api("/api/vibe-cooking/options");
  fillSelect("#vibeTarget", state.vibeOptions.targets);
  fillSelect("#vibeScene", state.vibeOptions.scenes);
  fillSelect("#vibeTexture", state.vibeOptions.textures);
  fillSelect("#vibeProcess", state.vibeOptions.process_modes);
}

async function loadSummary() {
  const summary = await api("/api/summary");
  const status = Object.entries(summary.status_counts || {})
    .map(([key, value]) => `<div class="summary-item"><strong>${key}</strong><br /><span class="mini">${formatNumber(value)}건</span></div>`)
    .join("");
  $("#summaryBox").innerHTML = `${status}<div class="summary-item"><strong>공장 DB</strong><br /><span class="mini">${formatNumber(summary.factory_count)}개 활성</span></div>`;
}

async function loadRequests() {
  const data = await api("/api/product-requests?include_dummy=true&limit=30");
  $("#requestList").innerHTML = data.items
    .map(
      (item) => `
        <article class="request-item" data-id="${item.id}">
          <strong>${item.product_case_label} · ${badge(item.status)}</strong>
          <span>${item.raw_prompt}</span><br />
          <span>${formatNumber(item.target_qty)}${item.qty_unit} · ${item.sales_type} · ${item.package_type}</span>
        </article>
      `,
    )
    .join("");
  $$(".request-item").forEach((el) => el.addEventListener("click", () => selectRequest(Number(el.dataset.id))));
}

async function selectRequest(id) {
  state.selectedRequestId = id;
  state.agentReport = null;
  state.detail = await api(`/api/product-requests/${id}`);
  renderDetail();
}

function renderDetail() {
  const detail = state.detail;
  $("#emptyState").classList.add("hidden");
  $("#detailView").classList.remove("hidden");
  $("#statusBadge").className = `badge ${detail.status}`;
  $("#statusBadge").textContent = detail.status;
  $("#detailTitle").textContent = `${detail.product_case_label} 요청 #${detail.id}`;
  $("#detailMeta").textContent = `${formatNumber(detail.target_qty)}${detail.qty_unit} · ${detail.sales_type} · ${detail.package_type}`;
  renderSpec(detail);
  renderAgent(detail);
  renderRisk(detail);
  renderMatches(detail);
  renderPurchaseOrders(detail);
  renderDocs(detail);
  renderCost(detail.cost_calculation);
}

function renderSpec(detail) {
  const spec = detail.spec || {};
  const recipe = detail.recipe || {};
  $("#tab-spec").innerHTML = [
    card("제품 컨셉", renderKeyValues(spec.concept)),
    card("제조 공정", renderPills(spec.process_list)),
    card("원재료/BOM 초안", `<div class="data-table">${(recipe.ingredients || [])
      .map((line) => `<div class="finding"><strong>${line.role}</strong><br />${line.name}<br /><span class="mini">${line.ratio_range} · 알레르기: ${line.allergen_flag || "없음"} · 대체: ${line.substitute_allowed}</span></div>`)
      .join("")}</div>`),
    card("검증 질문", renderPills(spec.validation_questions)),
  ].join("");
}

function renderAgent(detail) {
  const report = state.agentReport;
  const reportHtml = report
    ? [
        card("기획 적합도", renderKeyValues({
          판단: report.decision,
          점수: `${report.readiness_score}점`,
          목표: report.planning_goal,
          수량: report.fit_summary?.target_qty || "",
          포장: report.fit_summary?.package_type || "",
        })),
        card("강점", renderPills(report.strengths)),
        card("리스크", renderPills(report.risks)),
        card("다음 액션", renderPills(report.recommended_actions)),
        report.revision_prompt ? card("수정 프롬프트", `<p class="copy-box">${escapeHtml(report.revision_prompt)}</p>`) : "",
      ].join("")
    : `<div class="empty compact-empty">에이전트를 실행하면 현재 사양, BOM, 규제, 공장 후보 기준으로 기획 적합도를 판단합니다.</div>`;
  $("#tab-agent").innerHTML = `
    <div class="agent-runner">
      <label>기획 목표 <input id="agentGoal" value="샘플 발주 가능한 제품 기획으로 정리" /></label>
      <button class="primary" id="agentRunBtn">에이전트 실행</button>
    </div>
    ${reportHtml}
  `;
  $("#agentRunBtn").addEventListener("click", runVibeAgent);
}

function renderRisk(detail) {
  const screening = detail.screening || { findings: [] };
  $("#tab-risk").innerHTML = [
    card("전체 상태", `${badge(screening.overall_status)}<p class="mini">법률 판단이 아니라 출시 전 확인 플래그입니다.</p>`),
    ...(screening.findings || []).map(
      (finding) => `
        <div class="finding ${finding.severity}">
          <strong>${finding.severity} · ${finding.rule_id}</strong><br />
          ${finding.message}<br />
          <span class="mini">필요 증빙: ${finding.required_evidence}</span><br />
          <a class="mini" href="${finding.source_url}" target="_blank" rel="noreferrer">출처 열기</a>
        </div>
      `,
    ),
  ].join("");
}

function renderMatches(detail) {
  $("#tab-matches").innerHTML = (detail.matches || [])
    .map((match) => {
      const factory = match.factory || {};
      return `
        <article class="match-card">
          <div class="list-head">
            <h3>${factory.company_name || "공장"}</h3>
            <strong>${match.score}점</strong>
          </div>
          <p>${match.reason}</p>
          <p class="mini">${factory.primary_category || ""} · ${factory.certification_signal || "인증 미확인"} · ${factory.verification_status || ""}</p>
          <div class="pill-row">${match.confirm_questions.map((q) => `<span class="pill">${q}</span>`).join("")}</div>
        </article>
      `;
    })
    .join("") || `<div class="empty">공장 후보가 없습니다. 조건을 완화하거나 공장 DB를 보강하세요.</div>`;
}

function renderDocs(detail) {
  const plan = detail.product_plan?.body || {};
  const brief = detail.sample_brief?.body || {};
  $("#tab-docs").innerHTML = [
    card("제품 기획안", renderKeyValues({ 상태: detail.product_plan?.status || "없음", 제목: plan.title || "" })),
    card("샘플 발주안", renderKeyValues({ 상태: detail.sample_brief?.status || "없음", 제목: brief.title || "", 용도: brief.disclaimer || "" })),
    `<div class="doc-actions">
      <button class="primary" id="planPdfBtn">기획안 PDF 생성</button>
      <button class="primary" id="briefPdfBtn">발주안 PDF 생성</button>
      <a class="ghost" href="/api/export/product-requests/${detail.id}.json" target="_blank">JSON 내보내기</a>
    </div>`,
    card("툴 실행 로그", (detail.tool_runs || []).map((run) => `<div class="finding"><strong>${run.tool_name}</strong><br /><span class="mini">${run.status} · ${run.summary}</span></div>`).join("")),
  ].join("");
  $("#planPdfBtn").addEventListener("click", () => createPdf("product_plan"));
  $("#briefPdfBtn").addEventListener("click", () => createPdf("sample_brief"));
}

function defaultPoFormValues(detail) {
  const topMatch = (detail.matches || [])[0]?.factory || {};
  const cost = detail.cost_calculation || {};
  return {
    supplier_company: topMatch.company_name || "",
    product_name: `${detail.product_case_label} ${detail.package_type} 생산`,
    specification: detail.raw_prompt,
    quantity: detail.target_qty,
    unit: detail.qty_unit,
    unit_price: Math.round(Number(cost.supply_price || 0)),
  };
}

function renderPurchaseOrderCard(order) {
  const rows = (order.line_items || [])
    .map(
      (line) => `
        <tr>
          <td>${escapeHtml(line.item_name)}</td>
          <td>${escapeHtml(line.specification)}</td>
          <td>${formatNumber(line.quantity)}${escapeHtml(line.unit)}</td>
          <td>${formatMoney(line.unit_price)}</td>
          <td>${formatMoney(line.amount)}</td>
        </tr>
      `,
    )
    .join("");
  return `
    <article class="po-card">
      <div class="list-head">
        <div>
          <strong>발주요청 #${order.id} · ${badge(order.status)}</strong>
          <p class="mini">${escapeHtml(order.buyer_company)} → ${escapeHtml(order.supplier_company || "공급처 미정")} · ${escapeHtml(order.order_date)}</p>
        </div>
        <button class="ghost po-pdf-btn" data-order-id="${order.id}">PDF</button>
      </div>
      <div class="table-wrap">
        <table class="po-table">
          <thead><tr><th>품목</th><th>규격</th><th>수량</th><th>단가</th><th>금액</th></tr></thead>
          <tbody>${rows}</tbody>
        </table>
      </div>
      <dl class="kv compact">
        <dt>납품장소</dt><dd>${escapeHtml(order.delivery_place || "미입력")}</dd>
        <dt>결제조건</dt><dd>${escapeHtml(order.payment_terms || "미입력")}</dd>
        <dt>총액</dt><dd>${formatMoney(order.total_amount)} <span class="mini">(${escapeHtml(order.vat_type)})</span></dd>
      </dl>
      ${(order.risk_flags || []).length ? `<div class="finding YELLOW"><strong>확인 필요</strong><br />${order.risk_flags.map(escapeHtml).join("<br />")}</div>` : ""}
    </article>
  `;
}

function renderPurchaseOrders(detail) {
  const values = defaultPoFormValues(detail);
  const orders = detail.purchase_orders || [];
  $("#tab-po").innerHTML = `
    <div class="po-layout">
      <form id="purchaseOrderForm" class="po-form">
        <h3>실제 발주 양식 입력</h3>
        <label>받은 발주 양식 원문/메모 <textarea name="raw_order_form" rows="4" placeholder="공급사 또는 내부 양식의 핵심 내용을 그대로 붙여 넣으세요."></textarea></label>
        <button type="button" class="ghost" id="parsePoFormBtn">양식 자동 반영</button>
        <div class="two-col">
          <label>발주처 <input name="buyer_company" value="CBT 운영사" /></label>
          <label>담당자 <input name="buyer_contact" value="브랜드 담당자" /></label>
        </div>
        <div class="two-col">
          <label>공급처 <input name="supplier_company" value="${escapeHtml(values.supplier_company)}" /></label>
          <label>공급 담당자 <input name="supplier_contact" placeholder="이름/연락처" /></label>
        </div>
        <div class="three-col">
          <label>발주일 <input name="order_date" type="date" /></label>
          <label>납기일 <input name="due_date" type="date" /></label>
          <label>VAT <select name="vat_type"><option>VAT 별도</option><option>VAT 포함</option></select></label>
        </div>
        <div class="po-line-box">
          <h3>품목</h3>
          <label>품목명 <input name="item_name" value="${escapeHtml(values.product_name)}" /></label>
          <label>규격/사양 <textarea name="specification" rows="3">${escapeHtml(values.specification)}</textarea></label>
          <div class="three-col">
            <label>수량 <input name="quantity" type="number" min="1" value="${escapeHtml(values.quantity)}" /></label>
            <label>단위 <input name="unit" value="${escapeHtml(values.unit)}" /></label>
            <label>단가 <input name="unit_price" type="number" min="0" value="${escapeHtml(values.unit_price)}" /></label>
          </div>
          <label>품목 메모 <input name="line_notes" value="최종 단가는 공급사 견적서로 확정" /></label>
        </div>
        <label>납품장소 <input name="delivery_place" placeholder="예: 서울시 성동구 물류센터" /></label>
        <label>납품조건 <input name="delivery_terms" value="납품 전 일정 확정, 운송비 포함 여부 별도 확인" /></label>
        <label>결제조건 <input name="payment_terms" value="세금계산서 발행 후 30일 이내 지급" /></label>
        <label>검수조건 <input name="inspection_terms" value="입고 수량, 외관, 표시사항, 시험성적서 확인 후 검수" /></label>
        <div class="two-col">
          <label>품질 조건 <textarea name="quality_terms" rows="3">입고 수량/외관 검수
표시사항 초안 확인
알레르기 및 원산지 증빙 확인</textarea></label>
          <label>필수 서류 <textarea name="required_documents" rows="3">견적서
사업자등록증
HACCP 등 인증서
시험성적서 또는 원료 규격서</textarea></label>
        </div>
        <label class="checkline">
          <input type="checkbox" name="is_dummy" checked />
          더미 검증 발주로 생성
        </label>
        <button type="submit" class="primary">발주요청 저장</button>
      </form>
      <div class="po-list">
        <h3>발주요청 이력</h3>
        ${orders.length ? orders.map(renderPurchaseOrderCard).join("") : `<div class="empty compact-empty">아직 발주요청이 없습니다.</div>`}
      </div>
    </div>
  `;
  $("#purchaseOrderForm").addEventListener("submit", createPurchaseOrder);
  $("#parsePoFormBtn").addEventListener("click", parsePurchaseOrderForm);
  $$(".po-pdf-btn").forEach((btn) => btn.addEventListener("click", () => createPurchaseOrderPdf(Number(btn.dataset.orderId))));
}

function renderCost(cost) {
  if (!cost) {
    $("#costResult").innerHTML = "";
    return;
  }
  $("#costResult").innerHTML = `
    <div><strong>1식당 원가</strong><br />${formatNumber(cost.unit_cost)}원</div>
    <div><strong>공급가 제안</strong><br />${formatNumber(cost.supply_price)}원</div>
    <div><strong>VAT 포함 총액</strong><br />${formatNumber(cost.vat_included_total)}원</div>
  `;
}

async function createPdf(docType) {
  if (!state.selectedRequestId) return;
  const result = await api(`/api/product-requests/${state.selectedRequestId}/documents/${docType}/pdf`, { method: "POST" });
  window.open(result.download_url, "_blank");
  await selectRequest(state.selectedRequestId);
}

async function createPurchaseOrder(event) {
  event.preventDefault();
  if (!state.selectedRequestId) return;
  const data = formDataObject(event.currentTarget);
  const payload = {
    buyer_company: data.buyer_company,
    buyer_contact: data.buyer_contact,
    supplier_company: data.supplier_company,
    supplier_contact: data.supplier_contact,
    order_date: data.order_date,
    due_date: data.due_date,
    delivery_place: data.delivery_place,
    delivery_terms: data.delivery_terms,
    payment_terms: data.payment_terms,
    inspection_terms: data.inspection_terms,
    vat_type: data.vat_type,
    raw_order_form: data.raw_order_form,
    quality_terms: (data.quality_terms || "").split(/\r?\n/).map((item) => item.trim()).filter(Boolean),
    required_documents: (data.required_documents || "").split(/\r?\n/).map((item) => item.trim()).filter(Boolean),
    line_items: [
      {
        item_name: data.item_name,
        specification: data.specification,
        quantity: Number(data.quantity),
        unit: data.unit,
        unit_price: Number(data.unit_price),
        notes: data.line_notes,
      },
    ],
    is_dummy: Boolean(data.is_dummy),
  };
  await api(`/api/product-requests/${state.selectedRequestId}/purchase-orders`, {
    method: "POST",
    body: JSON.stringify(payload),
  });
  await selectRequest(state.selectedRequestId);
}

function setFormValue(form, name, value) {
  if (value === undefined || value === null || value === "" || !form.elements[name]) return;
  form.elements[name].value = value;
}

async function parsePurchaseOrderForm() {
  if (!state.selectedRequestId) return;
  const form = $("#purchaseOrderForm");
  const raw = form.elements.raw_order_form.value.trim();
  if (!raw) return;
  const result = await api(`/api/product-requests/${state.selectedRequestId}/purchase-orders/parse-form`, {
    method: "POST",
    body: JSON.stringify({ raw_order_form: raw }),
  });
  const parsed = result.parsed || {};
  setFormValue(form, "buyer_company", parsed.buyer_company);
  setFormValue(form, "supplier_company", parsed.supplier_company);
  setFormValue(form, "order_date", parsed.order_date);
  setFormValue(form, "due_date", parsed.due_date);
  setFormValue(form, "delivery_place", parsed.delivery_place);
  setFormValue(form, "delivery_terms", parsed.delivery_terms);
  setFormValue(form, "payment_terms", parsed.payment_terms);
  setFormValue(form, "inspection_terms", parsed.inspection_terms);
  setFormValue(form, "vat_type", parsed.vat_type);
  if ((parsed.quality_terms || []).length) setFormValue(form, "quality_terms", parsed.quality_terms.join("\n"));
  if ((parsed.required_documents || []).length) setFormValue(form, "required_documents", parsed.required_documents.join("\n"));
  const line = (parsed.line_items || [])[0];
  if (line) {
    setFormValue(form, "item_name", line.item_name);
    setFormValue(form, "specification", line.specification);
    setFormValue(form, "quantity", line.quantity);
    setFormValue(form, "unit", line.unit);
    setFormValue(form, "unit_price", line.unit_price);
    setFormValue(form, "line_notes", line.notes);
  }
}

async function createPurchaseOrderPdf(orderId) {
  const result = await api(`/api/purchase-orders/${orderId}/documents/pdf`, { method: "POST" });
  window.open(result.download_url, "_blank");
  await selectRequest(state.selectedRequestId);
}

function bindTabs() {
  $$(".tab").forEach((tab) => {
    tab.addEventListener("click", () => {
      $$(".tab").forEach((item) => item.classList.remove("active"));
      tab.classList.add("active");
      $$(".tab-panel").forEach((panel) => panel.classList.add("hidden"));
      $(`#tab-${tab.dataset.tab}`).classList.remove("hidden");
    });
  });
}

function bindNav() {
  $$(".nav-btn").forEach((btn) => {
    btn.addEventListener("click", () => {
      $$(".nav-btn").forEach((item) => item.classList.remove("active"));
      btn.classList.add("active");
      $$(".view").forEach((view) => view.classList.add("hidden"));
      $(`#${btn.dataset.view}View`).classList.remove("hidden");
      if (btn.dataset.view === "admin") loadFactories();
    });
  });
}

function formDataObject(form) {
  return Object.fromEntries(new FormData(form).entries());
}

function applyRequestPayload(payload) {
  const form = $("#requestForm");
  form.elements.product_case.value = payload.product_case;
  form.elements.raw_prompt.value = payload.raw_prompt;
  form.elements.sales_type.value = payload.sales_type;
  form.elements.target_qty_text.value = payload.target_qty_text;
  form.elements.package_type.value = payload.package_type;
  form.elements.claim_list.value = (payload.claim_list || []).join(",");
  form.elements.target_price.value = payload.target_price || "";
}

async function composeVibeCooking(runAfterCompose = false) {
  const vibe = formDataObject($("#vibeForm"));
  const request = formDataObject($("#requestForm"));
  const payload = {
    base_idea: vibe.base_idea,
    product_case: request.product_case,
    target_customer: vibe.target_customer,
    eating_scene: vibe.eating_scene,
    texture: vibe.texture,
    process_mode: vibe.process_mode,
    key_ingredients: splitList(vibe.key_ingredients),
    avoid_ingredients: splitList(vibe.avoid_ingredients),
    claim_list: splitList(request.claim_list),
    sales_type: request.sales_type,
    package_type: request.package_type,
    target_qty_text: request.target_qty_text,
    target_price: request.target_price,
  };
  const composed = await api("/api/vibe-cooking/compose", { method: "POST", body: JSON.stringify(payload) });
  applyRequestPayload(composed.request_payload);
  $("#vibePreview").classList.remove("empty-small");
  $("#vibePreview").innerHTML = `
    <strong>${escapeHtml(composed.vibe_card.product_case)} · ${escapeHtml(composed.vibe_card.process_mode)}</strong>
    <p class="mini">${escapeHtml(composed.preview_prompt)}</p>
    ${renderPills(composed.vibe_card.claims)}
  `;
  if (runAfterCompose) {
    await createRequestFromCurrentForm();
  }
}

async function createRequestFromCurrentForm() {
  const data = formDataObject($("#requestForm"));
  const payload = {
    raw_prompt: data.raw_prompt,
    product_case: data.product_case,
    sales_type: data.sales_type,
    target_qty_text: data.target_qty_text,
    package_type: data.package_type,
    claim_list: splitList(data.claim_list),
    target_price: data.target_price,
    is_dummy: Boolean(data.is_dummy),
    run_full: true,
  };
  const created = await api("/api/product-requests", { method: "POST", body: JSON.stringify(payload) });
  await loadRequests();
  await loadSummary();
  state.selectedRequestId = created.id;
  state.agentReport = null;
  state.detail = created;
  renderDetail();
}

async function runVibeAgent() {
  if (!state.selectedRequestId) return;
  const report = await api(`/api/product-requests/${state.selectedRequestId}/vibe-agent`, {
    method: "POST",
    body: JSON.stringify({ planning_goal: $("#agentGoal").value, include_revision_prompt: true }),
  });
  state.agentReport = report;
  state.detail = await api(`/api/product-requests/${state.selectedRequestId}`);
  renderDetail();
}

function bindForms() {
  $("#requestForm").addEventListener("submit", async (event) => {
    event.preventDefault();
    await createRequestFromCurrentForm();
  });

  $("#composeBtn").addEventListener("click", () => composeVibeCooking(false));
  $("#composeRunBtn").addEventListener("click", () => composeVibeCooking(true));

  $("#costForm").addEventListener("submit", async (event) => {
    event.preventDefault();
    if (!state.selectedRequestId) return;
    const raw = formDataObject(event.currentTarget);
    const payload = Object.fromEntries(Object.entries(raw).map(([key, value]) => [key, Number(value)]));
    const result = await api(`/api/product-requests/${state.selectedRequestId}/cost-calculations`, {
      method: "POST",
      body: JSON.stringify(payload),
    });
    renderCost(result);
    await selectRequest(state.selectedRequestId);
  });

  $("#factoryForm").addEventListener("submit", async (event) => {
    event.preventDefault();
    const payload = formDataObject(event.currentTarget);
    await api("/api/admin/factories", { method: "POST", body: JSON.stringify(payload) });
    event.currentTarget.reset();
    await loadFactories();
    await loadHealth();
  });
}

async function loadFactories() {
  const q = encodeURIComponent($("#factoryQuery").value || "");
  const data = await api(`/api/admin/factories?q=${q}&limit=50`);
  $("#factoryList").innerHTML = data.items
    .map(
      (factory) => `
        <article class="factory-item">
          <strong>${factory.company_name}</strong>
          <span>${factory.primary_category} · ${factory.certification_signal || "인증 미확인"} · ${factory.verification_status}</span><br />
          <span>${factory.product_keywords}</span>
        </article>
      `,
    )
    .join("");
}

async function init() {
  bindTabs();
  bindNav();
  bindForms();
  $("#refreshBtn").addEventListener("click", loadRequests);
  $("#factoryRefreshBtn").addEventListener("click", loadFactories);
  $("#rerunBtn").addEventListener("click", async () => {
    if (!state.selectedRequestId) return;
    state.detail = await api(`/api/product-requests/${state.selectedRequestId}/tool-runs/full`, { method: "POST" });
    renderDetail();
    await loadSummary();
  });
  $("#cleanupBtn").addEventListener("click", async () => {
    await api("/api/dummy-data", { method: "DELETE" });
    state.selectedRequestId = null;
    state.detail = null;
    $("#detailView").classList.add("hidden");
    $("#emptyState").classList.remove("hidden");
    await loadRequests();
    await loadSummary();
  });
  await loadVibeOptions();
  await loadHealth();
  await loadSummary();
  await loadRequests();
}

init().catch((error) => {
  console.error(error);
  $("#healthBox").textContent = `오류: ${error.message}`;
});
