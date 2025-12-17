import 'package:dio/dio.dart';
import '../config/api_config.dart';

class ApiService {
  final Dio _dio;
  
  ApiService() : _dio = Dio(BaseOptions(
    baseUrl: ApiConfig.baseUrl,
    connectTimeout: ApiConfig.timeout,
    receiveTimeout: ApiConfig.timeout,
    headers: {
      'Content-Type': 'application/json',
      'Accept': 'application/json',
    },
  ));
  
  // Health Check
  Future<Map<String, dynamic>> checkHealth() async {
    try {
      final response = await _dio.get(ApiConfig.healthCheck);
      return response.data;
    } catch (e) {
      throw Exception('Failed to check health: $e');
    }
  }
  
  // Check Eligibility
  Future<Map<String, dynamic>> checkEligibility(Map<String, dynamic> data) async {
    try {
      // Use the new simple-check endpoint that uses OpenAI directly
      final requestData = {
        'age': data['age'],
        'income': data['income'],
        'location': data['location'],
        'category': data['category'],
      };
      
      final response = await _dio.post('${ApiConfig.baseUrl}/api/eligibility/simple-check', data: requestData);
      
      print('Backend response: ${response.data}');
      
      // Transform the response - keep field names that match the UI
      final schemes = response.data['schemes'] as List<dynamic>;
      final results = schemes.map((scheme) {
        print('Processing scheme: $scheme');
        return {
          'name': scheme['name'] ?? 'Unknown Scheme',
          'description': scheme['description'] ?? 'No description',
          'eligible': true,
          'confidence': scheme['confidence'] ?? 0.0,
          'eligibility_match': scheme['eligibility_match'] ?? '',
          'how_to_apply': scheme['how_to_apply'] ?? '',
        };
      }).toList();
      
      print('Transformed results: $results');
      
      return {
        'results': results,
        'total_checked': schemes.length,
        'llm_used': response.data['llm_used'] ?? false,
      };
    } catch (e) {
      print('Eligibility check error: $e');
      throw Exception('Failed to check eligibility: $e');
    }
  }
  
  // Get Policies
  Future<List<dynamic>> getPolicies() async {
    try {
      final response = await _dio.get(ApiConfig.policiesSample);
      return response.data;
    } catch (e) {
      throw Exception('Failed to fetch policies: $e');
    }
  }
  
  // Get Benefits (uses citizens status endpoint)
  Future<List<dynamic>> getBenefits() async {
    try {
      final response = await _dio.get(ApiConfig.citizensStatus);
      // Return empty list for now as this endpoint returns status
      return [];
    } catch (e) {
      throw Exception('Failed to fetch benefits: $e');
    }
  }
  
  // Chat
  Future<Map<String, dynamic>> sendChatMessage(String message) async {
    try {
      final response = await _dio.post(ApiConfig.chatMessage, data: {
        'message': message,
      });
      return response.data;
    } catch (e) {
      throw Exception('Failed to send message: $e');
    }
  }
  
  // Translate Text
  Future<String> translateText(String text, String targetLanguage) async {
    try {
      final response = await _dio.post(ApiConfig.translateText, data: {
        'text': text,
        'target_language': targetLanguage,
      });
      return response.data['translated_text'];
    } catch (e) {
      throw Exception('Failed to translate: $e');
    }
  }
  
  // Get Supported Languages
  Future<List<dynamic>> getSupportedLanguages() async {
    try {
      final response = await _dio.get(ApiConfig.languages);
      return response.data;
    } catch (e) {
      throw Exception('Failed to fetch languages: $e');
    }
  }
  
  // Predict Impact
  Future<Map<String, dynamic>> predictImpact(Map<String, dynamic> data) async {
    try {
      // Use quick-predict endpoint for simple predictions
      final requestData = {
        'policy_name': data['policy_name'] ?? '',
        'num_eligibility_rules': 3,
        'category': 'welfare_schemes',
        'benefit_value': data['budget'] ?? 25000,
      };
      final response = await _dio.post(ApiConfig.impactQuickPredict, data: requestData);
      return response.data;
    } catch (e) {
      throw Exception('Failed to predict impact: $e');
    }
  }

  // Interpret Policy - Simplify complex policy text
  Future<Map<String, dynamic>> interpretPolicy(String policyText) async {
    try {
      final response = await _dio.post(
        '/api/policies/simplify',
        data: {'policy_text': policyText},
      );
      
      return response.data;
    } catch (e) {
      print('Policy interpretation error: $e');
      throw Exception('Failed to interpret policy: $e');
    }
  }
}
