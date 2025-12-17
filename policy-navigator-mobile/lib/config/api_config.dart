class ApiConfig {
  static const String baseUrl = 'http://localhost:8000';
  
  // Endpoints
  static const String healthCheck = '/health';
  static const String eligibilityCheck = '/api/eligibility/check';
  static const String policiesSample = '/api/policies/sample';
  static const String citizensStatus = '/api/citizens/status';
  static const String chatMessage = '/api/chat/message';
  static const String translateText = '/api/translate/text';
  static const String languages = '/api/translate/languages';
  static const String impactPredict = '/api/impact/predict';
  static const String impactQuickPredict = '/api/impact/quick-predict';
  
  // API Timeout
  static const Duration timeout = Duration(seconds: 30);
}
