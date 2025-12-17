import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../services/api_service.dart';
import '../providers/language_provider.dart';
import '../l10n/app_localizations.dart';

class ImpactScreen extends StatefulWidget {
  const ImpactScreen({super.key});

  @override
  State<ImpactScreen> createState() => _ImpactScreenState();
}

class _ImpactScreenState extends State<ImpactScreen> {
  final ApiService _apiService = ApiService();
  final _formKey = GlobalKey<FormState>();
  final TextEditingController _policyNameController = TextEditingController();
  final TextEditingController _budgetController = TextEditingController();
  bool _isLoading = false;
  Map<String, dynamic>? _prediction;

  Future<void> _predictImpact() async {
    if (!_formKey.currentState!.validate()) return;

    setState(() {
      _isLoading = true;
    });

    try {
      final data = {
        'policy_name': _policyNameController.text,
        'budget': double.parse(_budgetController.text),
      };

      final result = await _apiService.predictImpact(data);

      setState(() {
        _prediction = result;
        _isLoading = false;
      });
    } catch (e) {
      setState(() {
        _isLoading = false;
      });
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Error: $e')),
      );
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
          localizations.policyImpactPredictor,
          style: const TextStyle(
            color: Color(0xFF1E40AF),
            fontWeight: FontWeight.bold,
          ),
        ),
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16),
        child: Form(
          key: _formKey,
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Container(
                padding: const EdgeInsets.all(20),
                decoration: BoxDecoration(
                  gradient: const LinearGradient(
                    colors: [Color(0xFF6366F1), Color(0xFF8B5CF6)],
                  ),
                  borderRadius: BorderRadius.circular(16),
                ),
                child: const Text(
                  'Predict how your policy will impact citizens',
                  style: TextStyle(
                    fontSize: 18,
                    color: Colors.white,
                    fontWeight: FontWeight.bold,
                  ),
                  textAlign: TextAlign.center,
                ),
              ),
              const SizedBox(height: 24),
              TextFormField(
                controller: _policyNameController,
                decoration: InputDecoration(
                  labelText: localizations.policyName,
                  border: const OutlineInputBorder(),
                  filled: true,
                  fillColor: Colors.white,
                ),
                validator: (value) {
                  if (value == null || value.isEmpty) {
                    return 'Please enter policy name';
                  }
                  return null;
                },
              ),
              const SizedBox(height: 16),
              TextFormField(
                controller: _budgetController,
                keyboardType: TextInputType.number,
                decoration: InputDecoration(
                  labelText: localizations.budget,
                  border: const OutlineInputBorder(),
                  filled: true,
                  fillColor: Colors.white,
                ),
                validator: (value) {
                  if (value == null || value.isEmpty) {
                    return 'Please enter budget';
                  }
                  return null;
                },
              ),
              const SizedBox(height: 24),
              SizedBox(
                width: double.infinity,
                height: 56,
                child: ElevatedButton(
                  onPressed: _isLoading ? null : _predictImpact,
                  style: ElevatedButton.styleFrom(
                    backgroundColor: const Color(0xFF6366F1),
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(12),
                    ),
                  ),
                  child: _isLoading
                      ? const CircularProgressIndicator(color: Colors.white)
                      : Text(
                          localizations.predictImpact,
                          style: const TextStyle(
                            fontSize: 18,
                            fontWeight: FontWeight.bold,
                            color: Colors.white,
                          ),
                        ),
                ),
              ),
              if (_prediction != null) ...[
                const SizedBox(height: 32),
                Card(
                  child: Padding(
                    padding: const EdgeInsets.all(16),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          localizations.impactPrediction,
                          style: const TextStyle(
                            fontSize: 20,
                            fontWeight: FontWeight.bold,
                          ),
                        ),
                        const SizedBox(height: 16),
                        Text('${localizations.beneficiaries}: ${_getPredictionValue('beneficiaries', 'predicted')}'),
                        const SizedBox(height: 8),
                        Text('${localizations.successRate}: ${_getSuccessRate()}%'),
                        const SizedBox(height: 8),
                        Text('${localizations.roi}: ${_getROI()}%'),
                        const SizedBox(height: 8),
                        Text('${localizations.budgetRequired}: ₹${_getPredictionValue('budget', 'total_estimated_budget')}'),
                      ],
                    ),
                  ),
                ),
              ],
            ],
          ),
        ),
      ),
    );
  }
  
  String _getPredictionValue(String category, String field) {
    try {
      if (_prediction == null) return 'N/A';
      final predictions = _prediction!['predictions'];
      if (predictions == null) return 'N/A';
      final categoryData = predictions[category];
      if (categoryData == null) return 'N/A';
      final value = categoryData[field];
      if (value == null) return 'N/A';
      return value.toString();
    } catch (e) {
      return 'N/A';
    }
  }
  
  String _getSuccessRate() {
    try {
      if (_prediction == null) return 'N/A';
      final predictions = _prediction!['predictions'];
      if (predictions == null) return 'N/A';
      final successProb = predictions['success_probability'];
      if (successProb == null) return 'N/A';
      final overall = successProb['overall_probability'];
      if (overall == null) return 'N/A';
      return (overall * 100).toStringAsFixed(1);
    } catch (e) {
      return 'N/A';
    }
  }
  
  String _getROI() {
    try {
      if (_prediction == null) return 'N/A';
      final predictions = _prediction!['predictions'];
      if (predictions == null) return 'N/A';
      final roi = predictions['roi'];
      if (roi == null) return 'N/A';
      final roiPercentage = roi['roi_percentage'];
      if (roiPercentage == null) return 'N/A';
      return roiPercentage.toStringAsFixed(2);
    } catch (e) {
      return 'N/A';
    }
  }
}
