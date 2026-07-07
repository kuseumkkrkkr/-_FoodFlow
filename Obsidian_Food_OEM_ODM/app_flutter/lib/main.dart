import 'package:flutter/material.dart';

import 'screens/cbt_shell.dart';

void main() {
  runApp(const FoodOemOdmApp());
}

class FoodOemOdmApp extends StatelessWidget {
  const FoodOemOdmApp({super.key});

  @override
  Widget build(BuildContext context) {
    const seed = Color(0xff14794f);
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'Food OEM/ODM CBT',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: seed),
        scaffoldBackgroundColor: const Color(0xfff5f7f6),
        cardTheme: CardThemeData(
          color: Colors.white,
          elevation: 0,
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(8),
            side: const BorderSide(color: Color(0xffd9e0dc)),
          ),
        ),
        inputDecorationTheme: InputDecorationTheme(
          filled: true,
          fillColor: Colors.white,
          border: OutlineInputBorder(borderRadius: BorderRadius.circular(6)),
          enabledBorder: OutlineInputBorder(
            borderRadius: BorderRadius.circular(6),
            borderSide: const BorderSide(color: Color(0xffd9e0dc)),
          ),
        ),
        useMaterial3: true,
      ),
      home: const CbtShell(),
    );
  }
}
