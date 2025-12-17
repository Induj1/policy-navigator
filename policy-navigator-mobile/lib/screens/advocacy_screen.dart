import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../providers/language_provider.dart';

class AdvocacyScreen extends StatefulWidget {
  const AdvocacyScreen({super.key});

  @override
  State<AdvocacyScreen> createState() => _AdvocacyScreenState();
}

class _AdvocacyScreenState extends State<AdvocacyScreen> {
  final List<Map<String, dynamic>> _helpCategories = [
    {
      'title': 'Application Help',
      'icon': Icons.file_copy,
      'color': const Color(0xFF3B82F6),
      'description': 'Step-by-step guidance for filling applications',
      'steps': [
        'Gather required documents (ID proof, address proof, income certificate)',
        'Fill application form accurately with correct details',
        'Submit to correct office or online portal',
        'Track application status using reference number',
      ]
    },
    {
      'title': 'Document Assistance',
      'icon': Icons.folder_open,
      'color': const Color(0xFF10B981),
      'description': 'Help with required documents and verification',
      'steps': [
        'Identify required documents for your specific scheme',
        'Get document templates and sample formats',
        'Verify document authenticity through official channels',
        'Submit for processing at designated centers',
      ]
    },
    {
      'title': 'Appeals Process',
      'icon': Icons.gavel,
      'color': const Color(0xFFF59E0B),
      'description': 'Guide for filing appeals if rejected',
      'steps': [
        'Understand rejection reason from official notice',
        'Gather supporting evidence and documentation',
        'File appeal with proper format within deadline',
        'Follow up on appeal status regularly',
      ]
    },
    {
      'title': 'Contact Support',
      'icon': Icons.support_agent,
      'color': const Color(0xFF8B5CF6),
      'description': 'Connect with officials and support staff',
      'steps': [
        'Find relevant office contacts and helpline numbers',
        'Schedule appointments through online booking',
        'Prepare questions and required documents',
        'Get personalized guidance from officials',
      ]
    },
  ];

  @override
  Widget build(BuildContext context) {
    final languageProvider = Provider.of<LanguageProvider>(context);
    
    return Scaffold(
      backgroundColor: const Color(0xFFF0F9FF),
      appBar: AppBar(
        elevation: 0,
        backgroundColor: Colors.white,
        leading: IconButton(
          icon: const Icon(Icons.arrow_back, color: Color(0xFF1E40AF)),
          onPressed: () => Navigator.pop(context),
        ),
        title: const Text(
          'Citizen Advocacy',
          style: TextStyle(
            color: Color(0xFF1E40AF),
            fontWeight: FontWeight.bold,
          ),
        ),
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Container(
              padding: const EdgeInsets.all(20),
              decoration: BoxDecoration(
                gradient: const LinearGradient(
                  colors: [Color(0xFFEC4899), Color(0xFFF43F5E)],
                ),
                borderRadius: BorderRadius.circular(16),
              ),
              child: Row(
                children: [
                  Container(
                    padding: const EdgeInsets.all(12),
                    decoration: BoxDecoration(
                      color: Colors.white.withOpacity(0.2),
                      borderRadius: BorderRadius.circular(12),
                    ),
                    child: const Icon(Icons.shield, color: Colors.white, size: 32),
                  ),
                  const SizedBox(width: 16),
                  const Expanded(
                    child: Text(
                      'We\'re Here to Help You Succeed',
                      style: TextStyle(
                        fontSize: 16,
                        color: Colors.white,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                  ),
                ],
              ),
            ),
            const SizedBox(height: 24),
            const Text(
              'How Can We Assist You?',
              style: TextStyle(
                fontSize: 20,
                fontWeight: FontWeight.bold,
                color: Color(0xFF1E40AF),
              ),
            ),
            const SizedBox(height: 16),
            ..._helpCategories.map((category) => Padding(
              padding: const EdgeInsets.only(bottom: 16),
              child: _buildHelpCard(category),
            )),
          ],
        ),
      ),
    );
  }

  Widget _buildHelpCard(Map<String, dynamic> category) {
    return Card(
      elevation: 2,
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(16),
      ),
      child: ExpansionTile(
        leading: Container(
          padding: const EdgeInsets.all(12),
          decoration: BoxDecoration(
            color: (category['color'] as Color).withOpacity(0.1),
            borderRadius: BorderRadius.circular(12),
          ),
          child: Icon(
            category['icon'] as IconData,
            color: category['color'] as Color,
            size: 28,
          ),
        ),
        title: Text(
          category['title'] as String,
          style: const TextStyle(
            fontSize: 18,
            fontWeight: FontWeight.bold,
          ),
        ),
        subtitle: Padding(
          padding: const EdgeInsets.only(top: 4),
          child: Text(
            category['description'] as String,
            style: TextStyle(
              fontSize: 14,
              color: Colors.grey[600],
            ),
          ),
        ),
        children: [
          Padding(
            padding: const EdgeInsets.all(16),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                const Text(
                  'Steps to Follow:',
                  style: TextStyle(
                    fontSize: 16,
                    fontWeight: FontWeight.w600,
                  ),
                ),
                const SizedBox(height: 12),
                ...(category['steps'] as List<String>).asMap().entries.map(
                  (entry) => Padding(
                    padding: const EdgeInsets.only(bottom: 12),
                    child: Row(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Container(
                          width: 28,
                          height: 28,
                          decoration: BoxDecoration(
                            color: category['color'] as Color,
                            shape: BoxShape.circle,
                          ),
                          child: Center(
                            child: Text(
                              '${entry.key + 1}',
                              style: const TextStyle(
                                color: Colors.white,
                                fontWeight: FontWeight.bold,
                                fontSize: 14,
                              ),
                            ),
                          ),
                        ),
                        const SizedBox(width: 12),
                        Expanded(
                          child: Text(
                            entry.value,
                            style: const TextStyle(fontSize: 15, height: 1.4),
                          ),
                        ),
                      ],
                    ),
                  ),
                ),
                const SizedBox(height: 8),
                SizedBox(
                  width: double.infinity,
                  child: ElevatedButton.icon(
                    onPressed: () {
                      // Navigate to chat with pre-filled question
                      Navigator.pushNamed(context, '/chat');
                    },
                    icon: const Icon(Icons.chat, color: Colors.white),
                    label: const Text(
                      'Get Personalized Help',
                      style: TextStyle(color: Colors.white),
                    ),
                    style: ElevatedButton.styleFrom(
                      backgroundColor: category['color'] as Color,
                      padding: const EdgeInsets.symmetric(vertical: 12),
                      shape: RoundedRectangleBorder(
                        borderRadius: BorderRadius.circular(8),
                      ),
                    ),
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
