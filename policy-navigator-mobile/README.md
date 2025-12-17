# Policy Navigator Mobile App

A Flutter mobile application for discovering government benefits and schemes. This app connects to the Policy Navigator backend API to provide citizens with easy access to eligibility checks, policy information, and personalized benefit recommendations.

## Features

### For Citizens
- **Eligibility Checker**: Answer simple questions to discover which government benefits you qualify for
- **Policy Browser**: Read clear explanations of government schemes in your preferred language
- **Benefit Matcher**: Get personalized recommendations based on your profile
- **24/7 Chat Assistant**: Ask questions about benefits and application processes anytime
- **Multi-language Support**: Available in 8 Indian languages (English, Hindi, Marathi, Tamil, Telugu, Kannada, Gujarati, Bengali)

### For Government Officials
- **Policy Impact Predictor**: Analyze how policy changes will affect citizens
- **Real-time Analytics**: View adoption rates and success metrics
- **Transparent Reporting**: Generate impact reports for stakeholders

## Tech Stack

- **Framework**: Flutter 3.0+
- **State Management**: Provider
- **HTTP Client**: Dio
- **Local Storage**: SharedPreferences
- **Backend API**: FastAPI (localhost:8000)

## Project Structure

```
lib/
├── config/
│   └── api_config.dart          # API endpoints and configuration
├── providers/
│   └── language_provider.dart   # Language state management
├── screens/
│   ├── home_screen.dart         # Main dashboard
│   ├── eligibility_screen.dart  # Eligibility checker
│   ├── policies_screen.dart     # Policy browser
│   ├── benefits_screen.dart     # Benefits list
│   ├── chat_screen.dart         # AI chat assistant
│   └── impact_screen.dart       # Impact predictor
├── services/
│   └── api_service.dart         # API integration layer
└── main.dart                    # App entry point
```

## Getting Started

### Prerequisites

1. **Flutter SDK** (3.0 or higher)
   ```bash
   flutter --version
   ```

2. **Backend API Running**
   - Make sure the Policy Navigator backend is running on `http://localhost:8000`
   - See the main project README for backend setup instructions

### Installation

1. **Clone the repository** (if not already done)
   ```bash
   cd policy-navigator-mobile
   ```

2. **Install dependencies**
   ```bash
   flutter pub get
   ```

3. **Run the app**
   
   For Android:
   ```bash
   flutter run
   ```
   
   For iOS (macOS only):
   ```bash
   flutter run -d ios
   ```
   
   For Web:
   ```bash
   flutter run -d chrome
   ```

### Configuration

To connect to a different backend server, edit `lib/config/api_config.dart`:

```dart
class ApiConfig {
  static const String baseUrl = 'http://your-server-url:8000';
  // ...
}
```

For Android emulator to access localhost, use: `http://10.0.2.2:8000`
For iOS simulator to access localhost, use: `http://localhost:8000`

## Building for Production

### Android APK
```bash
flutter build apk --release
```

### Android App Bundle (for Play Store)
```bash
flutter build appbundle --release
```

### iOS (macOS only)
```bash
flutter build ios --release
```

## Key Dependencies

```yaml
dependencies:
  flutter:
    sdk: flutter
  provider: ^6.1.1              # State management
  dio: ^5.4.0                   # HTTP client
  shared_preferences: ^2.2.2    # Local storage
  google_fonts: ^6.1.0          # Typography
  flutter_svg: ^2.0.9           # SVG support
```

## Features Overview

### Home Screen
- System health status indicator
- Quick access to all features
- Statistics dashboard
- Trust badges (Free, Secure, Privacy Protected)

### Eligibility Screen
- Step-by-step form with validation
- Age, income, location, and category inputs
- Real-time eligibility results
- List of matching government schemes

### Policies Screen
- Browse all available government policies
- Search and filter capabilities
- Detailed policy information

### Benefits Screen
- View all benefit programs
- Category-wise organization
- Benefit details and requirements

### Chat Screen
- Real-time AI-powered chat
- Natural language understanding
- Context-aware responses
- Multi-language support

### Impact Screen
- Policy impact prediction tool
- Budget analysis
- Beneficiary estimates
- Success rate forecasting
- ROI calculations

## API Integration

The app communicates with the backend via REST API:

- **Health Check**: `GET /health`
- **Eligibility**: `POST /api/eligibility/check`
- **Policies**: `GET /api/policies`
- **Benefits**: `GET /api/benefits`
- **Chat**: `POST /api/chat`
- **Translation**: `POST /api/translate/text`
- **Impact**: `POST /api/impact/predict`

## Multi-language Support

The app supports 8 languages with automatic translation:
- English (en)
- Hindi (हिंदी) - hi
- Marathi (मराठी) - mr
- Tamil (தமிழ்) - ta
- Telugu (తెలుగు) - te
- Kannada (ಕನ್ನಡ) - kn
- Gujarati (ગુજરાતી) - gu
- Bengali (বাংলা) - bn

Translations are cached locally for better performance.

## Design System

### Color Palette
- **Primary Blue**: #3B82F6
- **Success Green**: #10B981
- **Teal**: #14B8A6
- **Purple**: #8B5CF6
- **Indigo**: #6366F1
- **Background**: #F0F9FF (Light Blue)

### Typography
- Headlines: Bold, 24-28px
- Body: Regular, 14-16px
- Captions: Regular, 12px

### Components
- Rounded corners (12-16px radius)
- Gradient backgrounds for emphasis
- Glass-morphism effects
- Smooth animations and transitions

## Troubleshooting

### Cannot connect to backend
- Ensure backend is running on localhost:8000
- For Android emulator, use `http://10.0.2.2:8000` instead of localhost
- Check firewall settings

### Build errors
```bash
flutter clean
flutter pub get
flutter run
```

### Hot reload not working
- Restart the app
- Check for syntax errors
- Ensure you're modifying Dart files (not native code)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is part of the Policy Navigator platform.

## Support

For issues and questions:
- GitHub Issues: [Create an issue]
- Email: support@policynavigator.com

---

**Made with ❤️ for citizens and governments**
