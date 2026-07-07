import 'package:flutter/material.dart';
import 'package:url_launcher/url_launcher.dart';

import '../api/api_client.dart';
import '../widgets/common.dart';

class CbtShell extends StatefulWidget {
  const CbtShell({super.key});

  @override
  State<CbtShell> createState() => _CbtShellState();
}

class _CbtShellState extends State<CbtShell> {
  final api = const ApiClient(apiBaseUrl);
  final factoryKeyword = TextEditingController();

  int navIndex = 0;
  bool loading = false;
  String? error;

  Map<String, dynamic>? health;
  Map<String, dynamic>? summary;
  Map<String, dynamic>? selected;
  Map<String, dynamic> factoryFilterOptions = {};

  List<dynamic> requests = [];
  List<dynamic> models = [];
  List<dynamic> factories = [];
  List<dynamic> ingredientPrices = [];
  List<dynamic> fxRates = [];
  List<dynamic> priceSyncRuns = [];
  List<dynamic> recipeEvaluations = [];

  String factoryProductCase = '';
  String factoryCertification = '';
  String factoryMvpFit = '';
  String factoryVerificationStatus = '';
  String factoryPackageType = '';

  @override
  void initState() {
    super.initState();
    refreshAll();
  }

  Future<void> refreshAll() async {
    await runBusy(() async {
      health = await api.getJson('/api/health');
      summary = await api.getJson('/api/summary');
      final requestResult = await api.getJson(
        '/api/product-requests?include_dummy=true&limit=30',
      );
      requests = requestResult['items'] as List<dynamic>;
      final modelResult = await api.getJson('/api/llm/models');
      models = modelResult['models'] as List<dynamic>;
      factoryFilterOptions = await api.getJson(
        '/api/admin/factory-filter-options',
      );
      final priceResult = await api.getJson('/api/ingredient-prices?limit=8');
      ingredientPrices = priceResult['items'] as List<dynamic>;
      final fxResult = await api.getJson('/api/fx-rates');
      fxRates = fxResult['items'] as List<dynamic>;
      final syncResult = await api.getJson(
        '/api/admin/price-sync-runs?limit=3',
      );
      priceSyncRuns = syncResult['items'] as List<dynamic>;
    });
  }

  Future<void> runBusy(Future<void> Function() action) async {
    setState(() {
      loading = true;
      error = null;
    });
    try {
      await action();
    } catch (e) {
      error = e.toString();
    } finally {
      if (mounted) {
        setState(() => loading = false);
      }
    }
  }

  Future<void> selectRequest(int id, {bool openRequestTab = true}) async {
    await runBusy(() async {
      selected = await api.getJson('/api/product-requests/$id');
      final evaluationResult = await api.getJson(
        '/api/product-requests/$id/recipe-evaluations',
      );
      recipeEvaluations = evaluationResult['items'] as List<dynamic>;
      if (openRequestTab) {
        navIndex = 1;
      }
    });
  }

  Future<void> cleanupDummy() async {
    await runBusy(() async {
      await api.deleteJson('/api/dummy-data');
      selected = null;
      recipeEvaluations = [];
      final requestResult = await api.getJson(
        '/api/product-requests?include_dummy=true&limit=30',
      );
      requests = requestResult['items'] as List<dynamic>;
      summary = await api.getJson('/api/summary');
    });
  }

  Future<void> onCreated(Map<String, dynamic> payload) async {
    await runBusy(() async {
      selected = await api.postJson('/api/product-requests', payload);
      final evaluationResult = await api.getJson(
        '/api/product-requests/${selected!['id']}/recipe-evaluations',
      );
      recipeEvaluations = evaluationResult['items'] as List<dynamic>;
      final requestResult = await api.getJson(
        '/api/product-requests?include_dummy=true&limit=30',
      );
      requests = requestResult['items'] as List<dynamic>;
      summary = await api.getJson('/api/summary');
    });
  }

  Future<void> searchFactories() async {
    final params = <String, String>{'limit': '60', 'active': 'true'};
    if (factoryKeyword.text.trim().isNotEmpty) {
      params['q'] = factoryKeyword.text.trim();
    }
    if (factoryProductCase.isNotEmpty) {
      params['product_case'] = factoryProductCase;
    }
    if (factoryCertification.isNotEmpty) params['cert'] = factoryCertification;
    if (factoryMvpFit.isNotEmpty) params['mvp_fit'] = factoryMvpFit;
    if (factoryVerificationStatus.isNotEmpty) {
      params['verification_status'] = factoryVerificationStatus;
    }
    if (factoryPackageType.isNotEmpty) {
      params['package_type'] = factoryPackageType;
    }
    if (params.length == 2) {
      setState(() {
        factories = [];
        error = '검색어 또는 필터를 하나 이상 선택하세요.';
      });
      return;
    }
    await runBusy(() async {
      final uri = Uri(path: '/api/admin/factories', queryParameters: params);
      final result = await api.getJson(uri.toString());
      factories = result['items'] as List<dynamic>;
    });
  }

  Future<void> createPdf(String docType) async {
    if (selected == null) return;
    await runBusy(() async {
      final result = await api.postJson(
        '/api/product-requests/${selected!['id']}/documents/$docType/pdf',
      );
      final uri = Uri.parse('$apiBaseUrl${result['download_url']}');
      await launchUrl(uri, mode: LaunchMode.externalApplication);
      selected = await api.getJson('/api/product-requests/${selected!['id']}');
    });
  }

  Future<void> evaluateRecipe() async {
    if (selected == null) return;
    final recipe = selected!['recipe'] as Map<String, dynamic>?;
    final recipeId = recipe?['id'];
    if (recipeId == null) return;
    await runBusy(() async {
      await api.postJson('/api/recipes/$recipeId/evaluations', {
        'include_cost': true,
      });
      final evaluationResult = await api.getJson(
        '/api/product-requests/${selected!['id']}/recipe-evaluations',
      );
      recipeEvaluations = evaluationResult['items'] as List<dynamic>;
      selected = await api.getJson('/api/product-requests/${selected!['id']}');
    });
  }

  Future<void> syncPublicPrices() async {
    await runBusy(() async {
      await api.postJson(
        '/api/admin/price-sync-runs?source=worldbank_pink_sheet&history_years=5',
      );
      final priceResult = await api.getJson('/api/ingredient-prices?limit=8');
      ingredientPrices = priceResult['items'] as List<dynamic>;
      final syncResult = await api.getJson(
        '/api/admin/price-sync-runs?limit=3',
      );
      priceSyncRuns = syncResult['items'] as List<dynamic>;
    });
  }

  Future<void> recalculateCost(Map<String, dynamic> payload) async {
    if (selected == null) return;
    await runBusy(() async {
      await api.postJson(
        '/api/product-requests/${selected!['id']}/cost-calculations',
        payload,
      );
      selected = await api.getJson('/api/product-requests/${selected!['id']}');
    });
  }

  @override
  Widget build(BuildContext context) {
    final titles = ['제품 만들기 요청', '새 요청', '공장 검색', '운영 데이터'];
    return Scaffold(
      appBar: AppBar(
        title: Text(titles[navIndex]),
        centerTitle: false,
        actions: [
          IconButton(onPressed: refreshAll, icon: const Icon(Icons.refresh)),
          PopupMenuButton<String>(
            onSelected: (value) {
              if (value == 'cleanup') cleanupDummy();
            },
            itemBuilder: (context) => const [
              PopupMenuItem(value: 'cleanup', child: Text('더미 삭제')),
            ],
          ),
        ],
      ),
      body: Stack(
        children: [
          SafeArea(
            child: RefreshIndicator(
              onRefresh: refreshAll,
              child: IndexedStack(
                index: navIndex,
                children: [
                  buildHomeScreen(),
                  buildRequestScreen(),
                  buildFactoryScreen(),
                  buildDataScreen(),
                ],
              ),
            ),
          ),
          if (loading) const LinearProgressIndicator(minHeight: 3),
        ],
      ),
      bottomNavigationBar: NavigationBar(
        selectedIndex: navIndex,
        onDestinationSelected: (value) => setState(() => navIndex = value),
        destinations: const [
          NavigationDestination(
            icon: Icon(Icons.home_outlined),
            selectedIcon: Icon(Icons.home),
            label: '홈',
          ),
          NavigationDestination(
            icon: Icon(Icons.add_box_outlined),
            selectedIcon: Icon(Icons.add_box),
            label: '요청',
          ),
          NavigationDestination(
            icon: Icon(Icons.manage_search),
            selectedIcon: Icon(Icons.factory),
            label: '공장',
          ),
          NavigationDestination(
            icon: Icon(Icons.data_usage_outlined),
            selectedIcon: Icon(Icons.data_usage),
            label: '데이터',
          ),
        ],
      ),
    );
  }

  Widget buildHomeScreen() {
    final counts = (summary?['status_counts'] as Map<String, dynamic>?) ?? {};
    return MobileList(
      children: [
        if (error != null) ErrorBanner(error: error!),
        AppCard(
          title: '진행 현황',
          child: Wrap(
            spacing: 8,
            runSpacing: 8,
            children: [
              StatusChip(
                label: health?['sam_configured'] == true ? 'SAM 연결' : 'SAM 폴백',
                tone: health?['sam_configured'] == true
                    ? ChipTone.green
                    : ChipTone.yellow,
              ),
              ...counts.entries.map(
                (entry) => StatusChip(label: '${entry.key} ${entry.value}'),
              ),
            ],
          ),
        ),
        FilledButton.icon(
          onPressed: () => setState(() => navIndex = 1),
          icon: const Icon(Icons.add),
          label: const Text('새 제품 요청'),
        ),
        AppCard(
          title: '최근 요청',
          child: requests.isEmpty
              ? const Text('아직 저장된 요청이 없습니다.')
              : Column(
                  children: requests
                      .take(6)
                      .map((item) => requestTile(item as Map<String, dynamic>))
                      .toList(),
                ),
        ),
        AppCard(
          title: '기준 데이터',
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              ...ingredientPrices.take(3).map((item) {
                final row = item as Map<String, dynamic>;
                return Text(
                  '${row['ingredient_name']} ${row['normalized_price_kg']}원/kg',
                  style: const TextStyle(fontSize: 13),
                );
              }),
              const SizedBox(height: 8),
              Wrap(
                spacing: 6,
                runSpacing: 6,
                children: fxRates.map((item) {
                  final row = item as Map<String, dynamic>;
                  return StatusChip(label: '${row['currency']} ${row['rate']}');
                }).toList(),
              ),
            ],
          ),
        ),
      ],
    );
  }

  Widget buildRequestScreen() {
    return MobileList(
      children: [
        if (error != null) ErrorBanner(error: error!),
        MobileRequestComposer(models: models, onCreated: onCreated),
        RequestDetailCard(
          detail: selected,
          evaluations: recipeEvaluations,
          onRefresh: selected == null
              ? null
              : () => selectRequest(
                  selected!['id'] as int,
                  openRequestTab: false,
                ),
          onCreatePdf: createPdf,
          onEvaluateRecipe: evaluateRecipe,
          onRecalculateCost: recalculateCost,
        ),
        if (requests.isNotEmpty)
          AppCard(
            title: '내 요청',
            child: Column(
              children: requests
                  .take(8)
                  .map((item) => requestTile(item as Map<String, dynamic>))
                  .toList(),
            ),
          ),
      ],
    );
  }

  Widget buildFactoryScreen() {
    final productCases =
        (factoryFilterOptions['product_cases'] as List<dynamic>?) ?? [];
    final certifications =
        (factoryFilterOptions['certifications'] as List<dynamic>?) ?? [];
    final packageTypes =
        (factoryFilterOptions['package_types'] as List<dynamic>?) ?? [];
    final statuses =
        (factoryFilterOptions['verification_statuses'] as List<dynamic>?) ?? [];
    final mvpFits = (factoryFilterOptions['mvp_fits'] as List<dynamic>?) ?? [];
    return MobileList(
      children: [
        if (error != null) ErrorBanner(error: error!),
        AppCard(
          title: '검색 조건',
          child: Column(
            children: [
              TextField(
                controller: factoryKeyword,
                decoration: const InputDecoration(
                  labelText: '검색어',
                  hintText: '예: 소스, 분말, HACCP',
                  prefixIcon: Icon(Icons.search),
                ),
                onSubmitted: (_) => searchFactories(),
              ),
              const SizedBox(height: 10),
              Wrap(
                spacing: 8,
                runSpacing: 8,
                children: [
                  FilterMenu(
                    label: '제품군',
                    value: factoryProductCase,
                    entries: {
                      for (final item in productCases)
                        (item as Map<String, dynamic>)['value'] as String:
                            item['label'] as String,
                    },
                    onChanged: (value) =>
                        setState(() => factoryProductCase = value),
                  ),
                  FilterMenu(
                    label: '인증',
                    value: factoryCertification,
                    entries: {
                      for (final item in certifications) '$item': '$item',
                    },
                    onChanged: (value) =>
                        setState(() => factoryCertification = value),
                  ),
                  FilterMenu(
                    label: '포장',
                    value: factoryPackageType,
                    entries: {
                      for (final item in packageTypes) '$item': '$item',
                    },
                    onChanged: (value) =>
                        setState(() => factoryPackageType = value),
                  ),
                  FilterMenu(
                    label: '검증',
                    value: factoryVerificationStatus,
                    entries: {for (final item in statuses) '$item': '$item'},
                    onChanged: (value) =>
                        setState(() => factoryVerificationStatus = value),
                  ),
                  FilterMenu(
                    label: '적합도',
                    value: factoryMvpFit,
                    entries: {for (final item in mvpFits) '$item': '$item'},
                    onChanged: (value) => setState(() => factoryMvpFit = value),
                  ),
                ],
              ),
              const SizedBox(height: 12),
              Row(
                children: [
                  Expanded(
                    child: FilledButton.icon(
                      onPressed: searchFactories,
                      icon: const Icon(Icons.search),
                      label: const Text('검색'),
                    ),
                  ),
                  const SizedBox(width: 8),
                  IconButton.outlined(
                    onPressed: () {
                      setState(() {
                        factoryKeyword.clear();
                        factoryProductCase = '';
                        factoryCertification = '';
                        factoryMvpFit = '';
                        factoryVerificationStatus = '';
                        factoryPackageType = '';
                        factories = [];
                        error = null;
                      });
                    },
                    icon: const Icon(Icons.filter_alt_off),
                  ),
                ],
              ),
            ],
          ),
        ),
        if (factories.isEmpty)
          const AppCard(
            title: '검색 결과',
            child: Text('필터를 선택하고 검색하면 공장 후보가 표시됩니다.'),
          )
        else
          ...factories.map((item) => factoryCard(item as Map<String, dynamic>)),
      ],
    );
  }

  Widget buildDataScreen() {
    return MobileList(
      children: [
        if (error != null) ErrorBanner(error: error!),
        AppCard(
          title: '서버',
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(apiBaseUrl),
              const SizedBox(height: 8),
              StatusChip(
                label: health?['sam_configured'] == true
                    ? 'SAM API 사용'
                    : '규칙 기반 폴백',
                tone: health?['sam_configured'] == true
                    ? ChipTone.green
                    : ChipTone.yellow,
              ),
              const SizedBox(height: 6),
              Text('모델: ${health?['default_llm_model'] ?? '-'}'),
            ],
          ),
        ),
        AppCard(
          title: '가격 동기화',
          trailing: IconButton(
            onPressed: syncPublicPrices,
            icon: const Icon(Icons.cloud_sync_outlined),
          ),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              if (priceSyncRuns.isEmpty)
                const Text('아직 동기화 이력이 없습니다.')
              else
                ...priceSyncRuns.map((item) {
                  final row = item as Map<String, dynamic>;
                  return ListTile(
                    dense: true,
                    contentPadding: EdgeInsets.zero,
                    title: Text('${row['source']} · ${row['status']}'),
                    subtitle: Text(row['summary'] as String? ?? ''),
                  );
                }),
            ],
          ),
        ),
        AppCard(
          title: '원재료 가격',
          child: Column(
            children: ingredientPrices.map((item) {
              final row = item as Map<String, dynamic>;
              final trend = row['trend_5y_change_pct'];
              final trendText = trend == null ? '' : ' · 5년 $trend%';
              return ListTile(
                dense: true,
                contentPadding: EdgeInsets.zero,
                title: Text(row['ingredient_name'] as String),
                subtitle: Text(
                  '${row['source']} · ${row['status']} · ${row['observed_at']}$trendText',
                ),
                trailing: Text('${row['normalized_price_kg']}원/kg'),
              );
            }).toList(),
          ),
        ),
        AppCard(
          title: '환율',
          child: Column(
            children: fxRates.map((item) {
              final row = item as Map<String, dynamic>;
              return ListTile(
                dense: true,
                contentPadding: EdgeInsets.zero,
                title: Text('${row['currency']} / ${row['base_currency']}'),
                subtitle: Text('${row['source']} · ${row['rate_date']}'),
                trailing: Text('${row['rate']}'),
              );
            }).toList(),
          ),
        ),
      ],
    );
  }

  Widget requestTile(Map<String, dynamic> row) {
    return ListTile(
      contentPadding: EdgeInsets.zero,
      title: Text(
        '${row['product_case_label']} #${row['id']}',
        maxLines: 1,
        overflow: TextOverflow.ellipsis,
      ),
      subtitle: Text(
        '${row['status']} · ${row['target_qty']}${row['qty_unit']} · ${row['package_type']}',
        maxLines: 1,
        overflow: TextOverflow.ellipsis,
      ),
      trailing: const Icon(Icons.chevron_right),
      onTap: () => selectRequest(row['id'] as int),
    );
  }

  Widget factoryCard(Map<String, dynamic> factory) {
    return AppCard(
      title: factory['company_name'] as String,
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(factory['primary_category'] as String),
          const SizedBox(height: 8),
          Wrap(
            spacing: 6,
            runSpacing: 6,
            children: [
              StatusChip(label: factory['mvp_fit'] as String),
              StatusChip(label: factory['verification_status'] as String),
              if ((factory['certification_signal'] as String).isNotEmpty)
                StatusChip(label: factory['certification_signal'] as String),
            ],
          ),
          const SizedBox(height: 8),
          Text(
            factory['product_keywords'] as String,
            maxLines: 2,
            overflow: TextOverflow.ellipsis,
          ),
        ],
      ),
    );
  }
}

class MobileList extends StatelessWidget {
  const MobileList({super.key, required this.children});

  final List<Widget> children;

  @override
  Widget build(BuildContext context) {
    return ListView(
      physics: const AlwaysScrollableScrollPhysics(),
      padding: const EdgeInsets.fromLTRB(14, 12, 14, 24),
      children: separated(children, 12),
    );
  }
}

class MobileRequestComposer extends StatefulWidget {
  const MobileRequestComposer({
    super.key,
    required this.models,
    required this.onCreated,
  });

  final List<dynamic> models;
  final Future<void> Function(Map<String, dynamic> payload) onCreated;

  @override
  State<MobileRequestComposer> createState() => _MobileRequestComposerState();
}

class _MobileRequestComposerState extends State<MobileRequestComposer> {
  final prompt = TextEditingController(
    text: '저당 고단백 그래놀라바를 온라인 공동구매로 1,000개 테스트 생산하고 싶다. 개별포장과 단백질 강조가 필요하다.',
  );
  final qty = TextEditingController(text: '1,000개');
  final claims = TextEditingController(text: '저당,고단백');
  String productCase = 'health_snack';
  String salesType = '공동구매';
  String packageType = '개별포장';
  String llmModel = 'az-deepseek-v4-flash';
  bool dummy = true;
  int step = 0;

  @override
  void didUpdateWidget(covariant MobileRequestComposer oldWidget) {
    super.didUpdateWidget(oldWidget);
    final aliases = widget.models
        .map((model) => (model as Map<String, dynamic>)['alias'])
        .whereType<String>()
        .toList();
    if (aliases.isNotEmpty && !aliases.contains(llmModel)) {
      llmModel = aliases.first;
    }
  }

  @override
  Widget build(BuildContext context) {
    final modelAliases = widget.models
        .map((model) => (model as Map<String, dynamic>)['alias'])
        .whereType<String>()
        .toList();
    final modelItems =
        (modelAliases.isEmpty
                ? ['az-deepseek-v4-flash', 'az-deepseek-v4-pro']
                : modelAliases)
            .toSet()
            .toList();
    return AppCard(
      title: '새 요청',
      child: Stepper(
        currentStep: step,
        physics: const NeverScrollableScrollPhysics(),
        controlsBuilder: (context, details) {
          final last = step == 2;
          return Padding(
            padding: const EdgeInsets.only(top: 12),
            child: Row(
              children: [
                Expanded(
                  child: FilledButton(
                    onPressed: last ? submit : details.onStepContinue,
                    child: Text(last ? '요청 생성' : '다음'),
                  ),
                ),
                if (step > 0) ...[
                  const SizedBox(width: 8),
                  TextButton(
                    onPressed: details.onStepCancel,
                    child: const Text('이전'),
                  ),
                ],
              ],
            ),
          );
        },
        onStepContinue: () => setState(() => step = (step + 1).clamp(0, 2)),
        onStepCancel: () => setState(() => step = (step - 1).clamp(0, 2)),
        onStepTapped: (value) => setState(() => step = value),
        steps: [
          Step(
            title: const Text('제품군'),
            isActive: step >= 0,
            content: DropdownButtonFormField<String>(
              initialValue: productCase,
              decoration: const InputDecoration(labelText: '제품군'),
              items: const [
                DropdownMenuItem(value: 'health_snack', child: Text('건강간식')),
                DropdownMenuItem(value: 'powder_stick', child: Text('분말스틱')),
                DropdownMenuItem(value: 'sauce', child: Text('소스')),
              ],
              onChanged: (value) =>
                  setState(() => productCase = value ?? productCase),
            ),
          ),
          Step(
            title: const Text('아이디어'),
            isActive: step >= 1,
            content: Column(
              children: [
                TextField(
                  controller: prompt,
                  minLines: 5,
                  maxLines: 7,
                  decoration: const InputDecoration(labelText: '만들고 싶은 제품'),
                ),
                const SizedBox(height: 10),
                DropdownButtonFormField<String>(
                  initialValue: llmModel,
                  decoration: const InputDecoration(labelText: 'DeepSeek 모델'),
                  items: modelItems
                      .map(
                        (item) =>
                            DropdownMenuItem(value: item, child: Text(item)),
                      )
                      .toList(),
                  onChanged: (value) =>
                      setState(() => llmModel = value ?? llmModel),
                ),
              ],
            ),
          ),
          Step(
            title: const Text('조건'),
            isActive: step >= 2,
            content: Column(
              children: [
                DropdownButtonFormField<String>(
                  initialValue: salesType,
                  decoration: const InputDecoration(labelText: '판매 방식'),
                  items: ['D2C', '공동구매', '프랜차이즈', 'PB', 'B2B']
                      .map(
                        (item) =>
                            DropdownMenuItem(value: item, child: Text(item)),
                      )
                      .toList(),
                  onChanged: (value) =>
                      setState(() => salesType = value ?? salesType),
                ),
                const SizedBox(height: 10),
                TextField(
                  controller: qty,
                  decoration: const InputDecoration(labelText: '목표 수량'),
                ),
                const SizedBox(height: 10),
                DropdownButtonFormField<String>(
                  initialValue: packageType,
                  decoration: const InputDecoration(labelText: '포장'),
                  items: ['개별포장', '스틱', '파우치', '병']
                      .map(
                        (item) =>
                            DropdownMenuItem(value: item, child: Text(item)),
                      )
                      .toList(),
                  onChanged: (value) =>
                      setState(() => packageType = value ?? packageType),
                ),
                const SizedBox(height: 10),
                TextField(
                  controller: claims,
                  decoration: const InputDecoration(labelText: '강조 문구'),
                ),
                SwitchListTile(
                  contentPadding: EdgeInsets.zero,
                  value: dummy,
                  title: const Text('더미 검증 데이터'),
                  onChanged: (value) => setState(() => dummy = value),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }

  Future<void> submit() {
    return widget.onCreated({
      'raw_prompt': prompt.text,
      'product_case': productCase,
      'sales_type': salesType,
      'target_qty_text': qty.text,
      'package_type': packageType,
      'claim_list': claims.text
          .split(',')
          .map((e) => e.trim())
          .where((e) => e.isNotEmpty)
          .toList(),
      'llm_model': llmModel,
      'is_dummy': dummy,
      'run_full': true,
    });
  }
}

class RequestDetailCard extends StatefulWidget {
  const RequestDetailCard({
    super.key,
    required this.detail,
    required this.evaluations,
    required this.onRefresh,
    required this.onCreatePdf,
    required this.onEvaluateRecipe,
    required this.onRecalculateCost,
  });

  final Map<String, dynamic>? detail;
  final List<dynamic> evaluations;
  final Future<void> Function()? onRefresh;
  final Future<void> Function(String docType) onCreatePdf;
  final Future<void> Function() onEvaluateRecipe;
  final Future<void> Function(Map<String, dynamic> payload) onRecalculateCost;

  @override
  State<RequestDetailCard> createState() => _RequestDetailCardState();
}

class _RequestDetailCardState extends State<RequestDetailCard> {
  final ingredient = TextEditingController(text: '450');
  final packaging = TextEditingController(text: '120');
  final manufacturing = TextEditingController(text: '250');

  @override
  Widget build(BuildContext context) {
    final detail = widget.detail;
    if (detail == null) {
      return const AppCard(
        title: '결과',
        child: Text('요청을 생성하거나 홈에서 요청을 선택하세요.'),
      );
    }
    final spec = (detail['spec'] as Map<String, dynamic>?) ?? {};
    final recipe = (detail['recipe'] as Map<String, dynamic>?) ?? {};
    final screening = (detail['screening'] as Map<String, dynamic>?) ?? {};
    final matches = (detail['matches'] as List<dynamic>?) ?? [];
    final cost = (detail['cost_calculation'] as Map<String, dynamic>?) ?? {};
    final concept = (spec['concept'] as Map<String, dynamic>?) ?? {};
    final ingredients = (recipe['ingredients'] as List<dynamic>?) ?? [];
    final findings = (screening['findings'] as List<dynamic>?) ?? [];
    return AppCard(
      title: '${detail['product_case_label']} #${detail['id']}',
      trailing: Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          StatusChip(label: detail['status'] as String),
          IconButton(
            onPressed: widget.onRefresh,
            icon: const Icon(Icons.refresh),
          ),
        ],
      ),
      child: Column(
        children: [
          Align(
            alignment: Alignment.centerLeft,
            child: Text(
              '${detail['target_qty']}${detail['qty_unit']} · ${detail['sales_type']} · ${detail['package_type']}',
            ),
          ),
          ExpansionTile(
            tilePadding: EdgeInsets.zero,
            title: const Text('사양'),
            initiallyExpanded: true,
            children: [
              InfoBlock(
                title: '제품 컨셉',
                lines: concept.entries
                    .map((e) => '${e.key}: ${e.value}')
                    .toList(),
              ),
              InfoBlock(
                title: '제조 공정',
                chips: ((spec['process_list'] as List<dynamic>?) ?? [])
                    .map((e) => '$e')
                    .toList(),
              ),
              InfoBlock(
                title: 'BOM 초안',
                lines: ingredients.map((item) {
                  final row = item as Map<String, dynamic>;
                  return '${row['role']} · ${row['name']} · ${row['ratio_range']}';
                }).toList(),
              ),
            ],
          ),
          ExpansionTile(
            tilePadding: EdgeInsets.zero,
            title: const Text('규제'),
            children: [
              Align(
                alignment: Alignment.centerLeft,
                child: StatusChip(
                  label: screening['overall_status'] as String? ?? 'not_run',
                  tone: toneFor(screening['overall_status'] as String?),
                ),
              ),
              const SizedBox(height: 8),
              ...findings.map(
                (item) => FindingTile(finding: item as Map<String, dynamic>),
              ),
            ],
          ),
          ExpansionTile(
            tilePadding: EdgeInsets.zero,
            title: const Text('공장 후보'),
            children: matches.isEmpty
                ? [
                    const Align(
                      alignment: Alignment.centerLeft,
                      child: Text('공장 후보가 없습니다.'),
                    ),
                  ]
                : matches.map((item) {
                    final match = item as Map<String, dynamic>;
                    final factory =
                        (match['factory'] as Map<String, dynamic>?) ?? {};
                    return ListTile(
                      contentPadding: EdgeInsets.zero,
                      title: Text(
                        '${factory['company_name'] ?? '공장'} · ${match['score']}점',
                      ),
                      subtitle: Text(match['reason'] as String),
                    );
                  }).toList(),
          ),
          ExpansionTile(
            tilePadding: EdgeInsets.zero,
            title: const Text('문서와 원가'),
            children: [
              Wrap(
                spacing: 8,
                runSpacing: 8,
                children: [
                  FilledButton.icon(
                    onPressed: () => widget.onCreatePdf('product_plan'),
                    icon: const Icon(Icons.picture_as_pdf_outlined),
                    label: const Text('기획안'),
                  ),
                  FilledButton.icon(
                    onPressed: () => widget.onCreatePdf('sample_brief'),
                    icon: const Icon(Icons.picture_as_pdf),
                    label: const Text('발주안'),
                  ),
                  OutlinedButton.icon(
                    onPressed: widget.onEvaluateRecipe,
                    icon: const Icon(Icons.fact_check_outlined),
                    label: const Text('레시피 평가'),
                  ),
                ],
              ),
              const SizedBox(height: 12),
              InfoBlock(
                title: '레시피 평가',
                lines: widget.evaluations.isEmpty
                    ? ['아직 평가 결과가 없습니다.']
                    : widget.evaluations.take(3).map((item) {
                        final row = item as Map<String, dynamic>;
                        return '제조성 ${row['manufacturability_score']}점 · 원가 ${row['cost_score']}점 · 표현 ${row['claim_feasibility']}';
                      }).toList(),
              ),
              InfoBlock(
                title: '원가',
                lines: [
                  '1식당 원가: ${cost['unit_cost'] ?? '-'}원',
                  '공급가 제안: ${cost['supply_price'] ?? '-'}원',
                  'VAT 포함 총액: ${cost['vat_included_total'] ?? '-'}원',
                ],
              ),
              Row(
                children: [
                  Expanded(
                    child: TextField(
                      controller: ingredient,
                      keyboardType: TextInputType.number,
                      decoration: const InputDecoration(labelText: '원료비'),
                    ),
                  ),
                  const SizedBox(width: 8),
                  Expanded(
                    child: TextField(
                      controller: packaging,
                      keyboardType: TextInputType.number,
                      decoration: const InputDecoration(labelText: '포장비'),
                    ),
                  ),
                  const SizedBox(width: 8),
                  Expanded(
                    child: TextField(
                      controller: manufacturing,
                      keyboardType: TextInputType.number,
                      decoration: const InputDecoration(labelText: '제조비'),
                    ),
                  ),
                ],
              ),
              const SizedBox(height: 8),
              SizedBox(
                width: double.infinity,
                child: OutlinedButton.icon(
                  onPressed: () => widget.onRecalculateCost({
                    'ingredient_cost': double.tryParse(ingredient.text) ?? 0,
                    'packaging_cost': double.tryParse(packaging.text) ?? 0,
                    'manufacturing_fee':
                        double.tryParse(manufacturing.text) ?? 0,
                    'sample_fee': 300000,
                    'test_fee': 250000,
                    'logistics_fee': 100000,
                  }),
                  icon: const Icon(Icons.calculate_outlined),
                  label: const Text('원가 재계산'),
                ),
              ),
            ],
          ),
        ],
      ),
    );
  }
}
