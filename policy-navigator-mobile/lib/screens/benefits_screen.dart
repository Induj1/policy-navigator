import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../services/api_service.dart';
import '../providers/language_provider.dart';
import '../l10n/app_localizations.dart';

class BenefitsScreen extends StatefulWidget {
  const BenefitsScreen({super.key});

  @override
  State<BenefitsScreen> createState() => _BenefitsScreenState();
}

class _BenefitsScreenState extends State<BenefitsScreen> {
  final ApiService _apiService = ApiService();
  List<dynamic>? _benefits;
  bool _isLoading = true;

  @override
  void initState() {
    super.initState();
    _loadBenefits();
  }

  Future<void> _loadBenefits() async {
    try {
      // Use sample data for benefits - could be enhanced with real API call
      final benefits = [
        {
          'name': 'Pradhan Mantri Jan Dhan Yojana',
          'description': 'Financial inclusion program providing zero balance bank accounts with RuPay debit card and insurance coverage',
          'benefit_amount': '₹10,000 overdraft facility',
          'category': 'Financial Inclusion'
        },
        {
          'name': 'Ayushman Bharat - PMJAY',
          'description': 'Health insurance coverage of ₹5 lakh per family per year for secondary and tertiary care hospitalization',
          'benefit_amount': '₹5,00,000 per family/year',
          'category': 'Healthcare'
        },
        {
          'name': 'PM Kisan Samman Nidhi',
          'description': 'Direct income support of ₹6,000 per year to small and marginal farmers',
          'benefit_amount': '₹6,000 per year',
          'category': 'Agriculture'
        },
        {
          'name': 'Pradhan Mantri Awas Yojana',
          'description': 'Affordable housing scheme providing financial assistance for building/purchasing a house',
          'benefit_amount': 'Up to ₹2.67 lakh subsidy',
          'category': 'Housing'
        },
        {
          'name': 'Atal Pension Yojana',
          'description': 'Pension scheme guaranteeing minimum pension after 60 years of age',
          'benefit_amount': '₹1,000-5,000 per month',
          'category': 'Social Security'
        },
      ];
      
      setState(() {
        _benefits = benefits;
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
          localizations.availableBenefits,
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
              itemCount: _benefits?.length ?? 0,
              itemBuilder: (context, index) {
                final benefit = _benefits![index];
                return Card(
                  margin: const EdgeInsets.only(bottom: 12),
                  elevation: 2,
                  child: Padding(
                    padding: const EdgeInsets.all(16),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Row(
                          children: [
                            Container(
                              padding: const EdgeInsets.all(8),
                              decoration: BoxDecoration(
                                color: const Color(0xFF10B981).withOpacity(0.1),
                                borderRadius: BorderRadius.circular(8),
                              ),
                              child: const Icon(
                                Icons.card_giftcard,
                                color: Color(0xFF10B981),
                              ),
                            ),
                            const SizedBox(width: 12),
                            Expanded(
                              child: Text(
                                benefit['name'] ?? 'Benefit',
                                style: const TextStyle(
                                  fontWeight: FontWeight.bold,
                                  fontSize: 16,
                                ),
                              ),
                            ),
                          ],
                        ),
                        const SizedBox(height: 12),
                        Text(
                          benefit['description'] ?? '',
                          style: TextStyle(
                            color: Colors.grey.shade700,
                            fontSize: 14,
                          ),
                        ),
                        const SizedBox(height: 8),
                        Row(
                          children: [
                            Container(
                              padding: const EdgeInsets.symmetric(
                                horizontal: 12,
                                vertical: 6,
                              ),
                              decoration: BoxDecoration(
                                color: const Color(0xFF3B82F6).withOpacity(0.1),
                                borderRadius: BorderRadius.circular(12),
                              ),
                              child: Text(
                                benefit['benefit_amount'] ?? '',
                                style: const TextStyle(
                                  color: Color(0xFF3B82F6),
                                  fontWeight: FontWeight.bold,
                                  fontSize: 12,
                                ),
                              ),
                            ),
                            const SizedBox(width: 8),
                            Container(
                              padding: const EdgeInsets.symmetric(
                                horizontal: 12,
                                vertical: 6,
                              ),
                              decoration: BoxDecoration(
                                color: const Color(0xFF8B5CF6).withOpacity(0.1),
                                borderRadius: BorderRadius.circular(12),
                              ),
                              child: Text(
                                benefit['category'] ?? '',
                                style: const TextStyle(
                                  color: Color(0xFF8B5CF6),
                                  fontWeight: FontWeight.w500,
                                  fontSize: 12,
                                ),
                              ),
                            ),
                          ],
                        ),
                      ],
                    ),
                  ),
                );
              },
            ),
    );
  }
}
