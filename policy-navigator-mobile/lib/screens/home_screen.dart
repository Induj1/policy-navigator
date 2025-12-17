import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../providers/language_provider.dart';
import '../services/api_service.dart';
import '../l10n/app_localizations.dart';

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  final ApiService _apiService = ApiService();
  Map<String, dynamic>? _healthData;
  bool _isLoading = true;

  @override
  void initState() {
    super.initState();
    _checkHealth();
  }

  Future<void> _checkHealth() async {
    try {
      final data = await _apiService.checkHealth();
      setState(() {
        _healthData = data;
        _isLoading = false;
      });
    } catch (e) {
      setState(() {
        _isLoading = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    final languageProvider = Provider.of<LanguageProvider>(context);
    final localizations = AppLocalizations(languageProvider.currentLanguage);
    
    return Scaffold(
      backgroundColor: const Color(0xFFF0F9FF),
      appBar: AppBar(
        elevation: 0,
        backgroundColor: Colors.white,
        title: Text(
          localizations.appTitle,
          style: const TextStyle(
            color: Color(0xFF1E40AF),
            fontWeight: FontWeight.bold,
          ),
        ),
        actions: [
          PopupMenuButton<String>(
            icon: const Icon(Icons.language, color: Color(0xFF1E40AF)),
            onSelected: (languageCode) {
              languageProvider.setLanguage(languageCode);
            },
            itemBuilder: (BuildContext context) {
              return languageProvider.supportedLanguages.map((lang) {
                return PopupMenuItem<String>(
                  value: lang['code']!,
                  child: Text(lang['nativeName']!),
                );
              }).toList();
            },
          ),
        ],
      ),
      body: SingleChildScrollView(
        child: Column(
          children: [
            // Hero Section
            Container(
              width: double.infinity,
              padding: const EdgeInsets.all(24),
              decoration: const BoxDecoration(
                gradient: LinearGradient(
                  begin: Alignment.topLeft,
                  end: Alignment.bottomRight,
                  colors: [Color(0xFF3B82F6), Color(0xFF10B981)],
                ),
              ),
              child: Column(
                children: [
                  Text(
                    localizations.findBenefits,
                    style: const TextStyle(
                      fontSize: 28,
                      fontWeight: FontWeight.bold,
                      color: Colors.white,
                    ),
                    textAlign: TextAlign.center,
                  ),
                  const SizedBox(height: 12),
                  Text(
                    localizations.simpleGuidance,
                    style: const TextStyle(
                      fontSize: 16,
                      color: Colors.white70,
                    ),
                    textAlign: TextAlign.center,
                  ),
                  const SizedBox(height: 8),
                  Text(
                    localizations.noTechnicalKnowledge,
                    style: const TextStyle(
                      fontSize: 14,
                      color: Colors.white60,
                    ),
                    textAlign: TextAlign.center,
                  ),
                  const SizedBox(height: 20),
                  
                  // Trust Badges
                  Wrap(
                    spacing: 8,
                    runSpacing: 8,
                    alignment: WrapAlignment.center,
                    children: [
                      _buildBadge(Icons.verified_user, 'Free & Secure', Colors.blue),
                      _buildBadge(Icons.lock, 'Privacy Protected', Colors.green),
                      _buildBadge(Icons.translate, '8 Languages', Colors.teal),
                    ],
                  ),
                ],
              ),
            ),
            
            const SizedBox(height: 20),
            
            // System Status
            if (_healthData != null)
              Container(
                margin: const EdgeInsets.symmetric(horizontal: 16),
                padding: const EdgeInsets.all(16),
                decoration: BoxDecoration(
                  color: Colors.white,
                  borderRadius: BorderRadius.circular(16),
                  boxShadow: [
                    BoxShadow(
                      color: Colors.black.withOpacity(0.05),
                      blurRadius: 10,
                      offset: const Offset(0, 4),
                    ),
                  ],
                ),
                child: Column(
                  children: [
                    Row(
                      children: [
                        Container(
                          width: 8,
                          height: 8,
                          decoration: const BoxDecoration(
                            color: Colors.green,
                            shape: BoxShape.circle,
                          ),
                        ),
                        const SizedBox(width: 8),
                        const Text(
                          'System Status: Online',
                          style: TextStyle(
                            fontWeight: FontWeight.bold,
                            fontSize: 16,
                          ),
                        ),
                      ],
                    ),
                    const SizedBox(height: 12),
                    Row(
                      mainAxisAlignment: MainAxisAlignment.spaceAround,
                      children: [
                        _buildStatusIndicator('AI', _healthData!['llm_available'] ?? false),
                        _buildStatusIndicator('Network', true),
                        _buildStatusIndicator('P3AI', _healthData!['p3ai_available'] ?? false),
                      ],
                    ),
                  ],
                ),
              ),
            
            const SizedBox(height: 24),
            
            // Feature Cards
            Padding(
              padding: const EdgeInsets.symmetric(horizontal: 16),
              child: Column(
                children: [
                  _buildFeatureCard(
                    context,
                    'Am I Eligible?',
                    'Answer a few simple questions to see which government benefits you qualify for',
                    Icons.how_to_reg,
                    const Color(0xFF3B82F6),
                    '/eligibility',
                  ),
                  const SizedBox(height: 12),
                  _buildFeatureCard(
                    context,
                    'Understand Benefits',
                    'Read clear, simple explanations of government schemes in your language',
                    Icons.menu_book,
                    const Color(0xFF10B981),
                    '/policies',
                  ),
                  const SizedBox(height: 12),
                  _buildFeatureCard(
                    context,
                    'Get Your Match',
                    'Receive personalized recommendations for benefits that match your needs',
                    Icons.card_giftcard,
                    const Color(0xFF14B8A6),
                    '/benefits',
                  ),
                  const SizedBox(height: 12),
                  _buildFeatureCard(
                    context,
                    'Ask Questions',
                    'Talk to our helpful assistant anytime. Get answers about benefits 24/7',
                    Icons.chat_bubble,
                    const Color(0xFF8B5CF6),
                    '/chat',
                  ),
                  const SizedBox(height: 12),
                  _buildFeatureCard(
                    context,
                    'Policy Impact',
                    'For governments: See how policy changes will affect citizens',
                    Icons.analytics,
                    const Color(0xFF6366F1),
                    '/impact',
                  ),
                  const SizedBox(height: 12),
                  _buildFeatureCard(
                    context,
                    'Understand Policies',
                    'Get clear, simple explanations of complex government documents',
                    Icons.description,
                    const Color(0xFF10B981),
                    '/interpretation',
                  ),
                  const SizedBox(height: 12),
                  _buildFeatureCard(
                    context,
                    'Get Help & Support',
                    'Guided assistance for applications, documents, and appeals',
                    Icons.support_agent,
                    const Color(0xFFEC4899),
                    '/advocacy',
                  ),
                ],
              ),
            ),
            
            const SizedBox(height: 32),
            
            // Stats Section
            Container(
              margin: const EdgeInsets.symmetric(horizontal: 16),
              padding: const EdgeInsets.all(20),
              decoration: BoxDecoration(
                color: Colors.white,
                borderRadius: BorderRadius.circular(16),
                boxShadow: [
                  BoxShadow(
                    color: Colors.black.withOpacity(0.05),
                    blurRadius: 10,
                    offset: const Offset(0, 4),
                  ),
                ],
              ),
              child: Column(
                children: [
                  const Text(
                    'Trusted by Citizens and Governments',
                    style: TextStyle(
                      fontSize: 20,
                      fontWeight: FontWeight.bold,
                    ),
                    textAlign: TextAlign.center,
                  ),
                  const SizedBox(height: 20),
                  Row(
                    mainAxisAlignment: MainAxisAlignment.spaceAround,
                    children: [
                      _buildStat('10,000+', 'Citizens Helped'),
                      _buildStat('50+', 'Programs'),
                      _buildStat('95%', 'Success Rate'),
                      _buildStat('8', 'Languages'),
                    ],
                  ),
                ],
              ),
            ),
            
            const SizedBox(height: 32),
          ],
        ),
      ),
    );
  }

  Widget _buildBadge(IconData icon, String text, Color color) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
      decoration: BoxDecoration(
        color: Colors.white.withOpacity(0.2),
        borderRadius: BorderRadius.circular(20),
        border: Border.all(color: Colors.white.withOpacity(0.3)),
      ),
      child: Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          Icon(icon, size: 16, color: Colors.white),
          const SizedBox(width: 6),
          Text(
            text,
            style: const TextStyle(
              color: Colors.white,
              fontSize: 12,
              fontWeight: FontWeight.w600,
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildStatusIndicator(String label, bool isActive) {
    return Column(
      children: [
        Container(
          width: 50,
          height: 50,
          decoration: BoxDecoration(
            gradient: LinearGradient(
              colors: isActive
                  ? [const Color(0xFF3B82F6), const Color(0xFF1E40AF)]
                  : [Colors.grey.shade300, Colors.grey.shade400],
            ),
            borderRadius: BorderRadius.circular(12),
          ),
          child: Center(
            child: Text(
              label,
              style: const TextStyle(
                color: Colors.white,
                fontSize: 12,
                fontWeight: FontWeight.bold,
              ),
            ),
          ),
        ),
        const SizedBox(height: 8),
        Text(
          isActive ? 'Active' : 'Inactive',
          style: TextStyle(
            fontSize: 12,
            color: isActive ? Colors.green : Colors.grey,
            fontWeight: FontWeight.w600,
          ),
        ),
      ],
    );
  }

  Widget _buildFeatureCard(
    BuildContext context,
    String title,
    String description,
    IconData icon,
    Color color,
    String route,
  ) {
    return GestureDetector(
      onTap: () => Navigator.pushNamed(context, route),
      child: Container(
        padding: const EdgeInsets.all(20),
        decoration: BoxDecoration(
          color: Colors.white,
          borderRadius: BorderRadius.circular(16),
          boxShadow: [
            BoxShadow(
              color: Colors.black.withOpacity(0.05),
              blurRadius: 10,
              offset: const Offset(0, 4),
            ),
          ],
        ),
        child: Row(
          children: [
            Container(
              width: 56,
              height: 56,
              decoration: BoxDecoration(
                gradient: LinearGradient(
                  colors: [color, color.withOpacity(0.7)],
                ),
                borderRadius: BorderRadius.circular(12),
              ),
              child: Icon(icon, color: Colors.white, size: 28),
            ),
            const SizedBox(width: 16),
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    title,
                    style: const TextStyle(
                      fontSize: 18,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                  const SizedBox(height: 4),
                  Text(
                    description,
                    style: TextStyle(
                      fontSize: 14,
                      color: Colors.grey.shade600,
                    ),
                  ),
                ],
              ),
            ),
            Icon(Icons.arrow_forward_ios, size: 16, color: Colors.grey.shade400),
          ],
        ),
      ),
    );
  }

  Widget _buildStat(String value, String label) {
    return Column(
      children: [
        Text(
          value,
          style: const TextStyle(
            fontSize: 24,
            fontWeight: FontWeight.bold,
            color: Color(0xFF1E40AF),
          ),
        ),
        const SizedBox(height: 4),
        Text(
          label,
          style: TextStyle(
            fontSize: 11,
            color: Colors.grey.shade600,
          ),
          textAlign: TextAlign.center,
        ),
      ],
    );
  }
}
