import 'package:flutter_test/flutter_test.dart';

import 'package:food_oem_odm_cbt/main.dart';

void main() {
  testWidgets('CBT app renders request workspace', (WidgetTester tester) async {
    await tester.pumpWidget(const FoodOemOdmApp());
    await tester.pump();

    expect(find.text('제품 만들기 요청'), findsOneWidget);
    expect(find.text('홈'), findsOneWidget);

    await tester.tap(find.text('요청'));
    await tester.pumpAndSettle();
    expect(find.text('새 요청'), findsAtLeastNWidgets(1));

    await tester.tap(find.text('아이디어'));
    await tester.pumpAndSettle();
    expect(find.text('DeepSeek 모델'), findsOneWidget);
  });
}
