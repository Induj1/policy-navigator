import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../services/api_service.dart';
import '../providers/language_provider.dart';
import '../l10n/app_localizations.dart';

class PoliciesScreen extends StatefulWidget {
  const PoliciesScreen({super.key});

  @override
  State<PoliciesScreen> createState() => _PoliciesScreenState();
}

class _PoliciesScreenState extends State<PoliciesScreen> {
  final ApiService _apiService = ApiService();
  List<dynamic>? _policies;
  bool _isLoading = true;

  @override
  void initState() {
    super.initState();
    _loadPolicies();
  }

  Future<void> _loadPolicies() async {
    try {
      final policies = await _apiService.getPolicies();
      setState(() {
        _policies = policies;
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
        leading: IconButton(
          icon: const Icon(Icons.arrow_back, color: Color(0xFF1E40AF)),
          onPressed: () => Navigator.pop(context),
        ),
        title: Text(
          localizations.governmentPolicies,
          style: const TextStyle(
            color: Color(0xFF1E40AF),
            fontWeight: FontWeight.bold,
          ),
        ),
      ),
      body: _isLoading
          ? const Center(child: CircularProgressIndicator())
          : ListView.builder(
              padding: const EdgeInsets.all(16),
              itemCount: _policies?.length ?? 0,
              itemBuilder: (context, index) {
                final policy = _policies![index];
                return Card(
                  margin: const EdgeInsets.only(bottom: 12),
                  child: ListTile(
                    leading: const Icon(Icons.policy, color: Color(0xFF3B82F6)),
                    title: Text(
                      policy['name'] ?? 'Policy',
                      style: const TextStyle(fontWeight: FontWeight.bold),
                    ),
                    subtitle: Text(policy['description'] ?? ''),
                    onTap: () {},
                  ),
                );
              },
            ),
    );
  }
}
