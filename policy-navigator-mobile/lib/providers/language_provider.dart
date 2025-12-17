import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';
import '../services/api_service.dart';

class LanguageProvider extends ChangeNotifier {
  String _currentLanguage = 'en';
  final Map<String, String> _translations = {};
  bool _isLoading = false;
  final ApiService _apiService = ApiService();
  
  String get currentLanguage => _currentLanguage;
  bool get isLoading => _isLoading;
  
  final List<Map<String, String>> supportedLanguages = [
    {'code': 'en', 'name': 'English', 'nativeName': 'English'},
    {'code': 'hi', 'name': 'Hindi', 'nativeName': 'हिंदी'},
    {'code': 'mr', 'name': 'Marathi', 'nativeName': 'मराठी'},
    {'code': 'ta', 'name': 'Tamil', 'nativeName': 'தமிழ்'},
    {'code': 'te', 'name': 'Telugu', 'nativeName': 'తెలుగు'},
    {'code': 'kn', 'name': 'Kannada', 'nativeName': 'ಕನ್ನಡ'},
    {'code': 'gu', 'name': 'Gujarati', 'nativeName': 'ગુજરાતી'},
    {'code': 'bn', 'name': 'Bengali', 'nativeName': 'বাংলা'},
  ];
  
  LanguageProvider() {
    _loadLanguagePreference();
  }
  
  Future<void> _loadLanguagePreference() async {
    final prefs = await SharedPreferences.getInstance();
    _currentLanguage = prefs.getString('language') ?? 'en';
    notifyListeners();
  }
  
  Future<void> setLanguage(String languageCode) async {
    _currentLanguage = languageCode;
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString('language', languageCode);
    _translations.clear();
    notifyListeners();
  }
  
  Future<String> translateText(String text) async {
    if (_currentLanguage == 'en') return text;
    
    final cacheKey = '$text-$_currentLanguage';
    if (_translations.containsKey(cacheKey)) {
      return _translations[cacheKey]!;
    }
    
    try {
      _isLoading = true;
      notifyListeners();
      
      final translated = await _apiService.translateText(text, _currentLanguage);
      _translations[cacheKey] = translated;
      
      _isLoading = false;
      notifyListeners();
      
      return translated;
    } catch (e) {
      _isLoading = false;
      notifyListeners();
      return text;
    }
  }
}
