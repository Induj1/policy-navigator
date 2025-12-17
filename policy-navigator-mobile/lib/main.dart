import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'providers/language_provider.dart';
import 'screens/home_screen.dart';
import 'screens/eligibility_screen.dart';
import 'screens/policies_screen.dart';
import 'screens/benefits_screen.dart';
import 'screens/chat_screen.dart';
import 'screens/impact_screen.dart';
import 'screens/policy_interpretation_screen.dart';
import 'screens/advocacy_screen.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MultiProvider(
      providers: [
        ChangeNotifierProvider(create: (_) => LanguageProvider()),
      ],
      child: MaterialApp(
        title: 'Policy Navigator',
        debugShowCheckedModeBanner: false,
        theme: ThemeData(
          useMaterial3: true,
          colorScheme: ColorScheme.fromSeed(
            seedColor: Colors.blue,
            brightness: Brightness.light,
          ),
          fontFamily: 'Inter',
        ),
        initialRoute: '/',
        routes: {
          '/': (context) => const HomeScreen(),
          '/eligibility': (context) => const EligibilityScreen(),
          '/policies': (context) => const PoliciesScreen(),
          '/benefits': (context) => const BenefitsScreen(),
          '/chat': (context) => const ChatScreen(),
          '/impact': (context) => const ImpactScreen(),
          '/interpretation': (context) => const PolicyInterpretationScreen(),
          '/advocacy': (context) => const AdvocacyScreen(),
        },
      ),
    );
  }
}
