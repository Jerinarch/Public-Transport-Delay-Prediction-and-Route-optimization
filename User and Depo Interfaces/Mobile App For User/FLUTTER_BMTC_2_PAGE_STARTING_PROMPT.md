# Master Engineering Prompt: BMTC 2-Page Starting Animation Flow in Flutter
## Production-Grade Architecture, Hero Animation, and Zero-Jank Performance

---

### HOW TO USE THIS PROMPT
Provide this exact prompt to your AI developer, copilot, or use it directly as your implementation blueprint in **Android Studio**. It is engineered to build the **exact 2-page animated opening sequence** from Citymapper (customized for **BMTC**) following international Flutter standards.

---

```markdown
You are a Principal Flutter Mobile Engineer. Build the starting 2-page onboarding sequence for an enterprise public transport mobile application called "BMTC" in Android Studio using Flutter.

The app must strictly replicate the iconic, playful visual identity and animations of Citymapper seen in the reference designs:
- PAGE 1: The Iconic Splash Screen (Solid transit green with the center animated circular emblem and bottom logo).
- PAGE 2: The Welcome Hero Screen (Hero-transitioned top circular badge, "BMTC" bold title, "The ultimate transport app" subtitle, playful white line-art doodle illustration of a bus and commuter over the city skyline, and the signature amber pill button "Start >").

================================================================================
1. INTERNATIONAL ENGINEERING & PERFORMANCE CONSTRAINTS
================================================================================
- Zero-Lag 60/120 FPS Guarantee: Use lightweight CustomPainter and native vector curves for the illustrations rather than heavy PNGs/videos. This ensures asset size is virtually 0 KB, APK size remains minimal, and cold-start latency is <400ms.
- Memory Leak Prevention: All AnimationControllers must use `SingleTickerProviderStateMixin` and be strictly disposed in `dispose()`.
- Smooth Hero Animation: The center circular logo on Page 1 must seamlessly Hero-animate to the top circular badge on Page 2 during page transition.
- Responsive Viewport Scaling: Must fit perfectly on all screen sizes and aspect ratios (from compact 4.7-inch screens to tall 6.8-inch modern devices) without any `RenderFlex overflow` warnings.
- Clean Architecture Directory Organization:
  lib/
  ├── core/
  │   ├── constants/
  │   │   ├── colors.dart         # BMTC & Citymapper hex palette
  │   │   └── strings.dart        # Internationalized string keys
  │   └── theme/
  │       └── app_theme.dart      # Material 3 typography & theme definition
  └── features/
      └── onboarding/
          ├── presentation/
          │   ├── pages/
          │   │   ├── splash_page.dart    # Page 1: Animated Splash
          │   │   └── welcome_page.dart   # Page 2: Welcome Hero & Doodle
          │   └── widgets/
          │       ├── bmtc_logo_badge.dart      # Shared Hero-animated circular emblem
          │       ├── city_skyline_doodle.dart  # Lightweight vector line-art painter
          │       └── amber_pill_button.dart    # Signature Citymapper-style button
          └── logic/
              └── navigation_cubit.dart or state controllers

================================================================================
2. DETAILED SCREEN-BY-SCREEN SPECIFICATIONS
================================================================================

--- PAGE 1: SPLASH SCREEN (splash_page.dart) ---
- Background: Full-bleed solid transit green (CitymapperColors.primaryGreen = #2E7D32).
- Center Emblem:
  - White circular border (width: 3.5, diameter: 110dp).
  - Inside: Playful white transit icon (smiling arrow face `·→·` or stylized electric bus glyph).
  - Entrance Animation: ScaleTransition (0.8 -> 1.0) with an ElasticOut or EaseInOut curve over 800ms.
  - Tagged with `Hero(tag: 'bmtc_emblem', child: ...)` for the seamless Page 1 -> Page 2 transition.
- Bottom Branding:
  - Row with mini logo arrow and bold sans-serif text: "BMTC" (fontSize: 22, fontWeight: FontWeight.w800, color: Colors.white).
  - Positioned 40dp above the bottom safe area.
- Flow Transition:
  - After 1.5 seconds, automatically triggers a smooth Hero page route transition to WelcomePage:
    Navigator.of(context).pushReplacement(
      PageRouteBuilder(
        transitionDuration: const Duration(milliseconds: 700),
        pageBuilder: (_, __, ___) => const WelcomePage(),
        transitionsBuilder: (_, animation, __, child) => FadeTransition(opacity: animation, child: child),
      ),
    );

--- PAGE 2: WELCOME HERO SCREEN (welcome_page.dart) ---
- Background: Identical solid green (#2E7D32).
- Top Area:
  - Hero target: `Hero(tag: 'bmtc_emblem')` renders the circular badge now scaled down to diameter 52dp at the top center.
- Header Typography:
  - "BMTC" (fontSize: 38, fontWeight: FontWeight.w900, color: Colors.white, letterSpacing: -0.5).
  - SizedBox(height: 6).
  - "The ultimate transport app" (fontSize: 18, fontWeight: FontWeight.w600, color: Colors.white.withOpacity(0.95)).
- Center Illustration (City Skyline & Bus Doodle):
  - Must replicate the playful Citymapper doodle line-art.
  - Draw with CustomPainter (CitySkylineDoodlePainter):
    • Tilted double-decker / electric BMTC bus with cartoon wheels and smiling driver.
    • Flying commuter with helmet / jetpack emitting a curved smoke trail.
    • Subtle silhouette of Bengaluru tech park / city skyline in the background with 20% opacity.
  - Runs in pure vector arithmetic (0 KB storage, instant rendering).
- Bottom Action Area:
  - Amber Pill Button (`amber_pill_button.dart`):
    • Background: #EAA043 (Citymapper golden amber).
    • Dimensions: double.infinity width, height: 56dp, borderRadius: 28dp.
    • Text: "Start" (fontSize: 20, fontWeight: FontWeight.bold, color: Colors.white).
    • Trailing Icon: Chevron right `>` (Icons.chevron_right_rounded, size: 24).
    • OnPressed: Triggers smooth push to location permission / main map screen.

================================================================================
3. READY-TO-USE CODE IMPLEMENTATION
================================================================================
Provide the complete, bug-free, null-safe Dart files for:
1. `lib/core/constants/colors.dart`
2. `lib/features/onboarding/presentation/widgets/bmtc_logo_badge.dart`
3. `lib/features/onboarding/presentation/widgets/city_skyline_doodle.dart`
4. `lib/features/onboarding/presentation/widgets/amber_pill_button.dart`
5. `lib/features/onboarding/presentation/pages/splash_page.dart`
6. `lib/features/onboarding/presentation/pages/welcome_page.dart`
7. `lib/main.dart`
```

---

## 4. Complete Code Implementation (Ready to Copy into Android Studio)

### 1. `lib/core/constants/colors.dart`
```dart
import 'package:flutter/material.dart';

class CitymapperColors {
  // Signature Citymapper / BMTC Solid Green
  static const Color primaryGreen = Color(0xFF2E7D32);
  static const Color lightGreen = Color(0xFF388E3C);
  
  // Signature Action Amber/Orange Pill Button
  static const Color amberButton = Color(0xFFEAA043);
  static const Color amberButtonPressed = Color(0xFFD68A2E);
  
  // Contrast Elements
  static const Color textWhite = Colors.white;
  static const Color doodleLine = Colors.white;
}
```

---

### 2. `lib/features/onboarding/presentation/widgets/bmtc_logo_badge.dart`
```dart
import 'package:flutter/material.dart';

class BmtcLogoBadge extends StatelessWidget {
  final double size;
  final bool isMini;

  const BmtcLogoBadge({
    Key? key,
    required this.size,
    this.isMini = false,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Hero(
      tag: 'bmtc_emblem',
      child: Material(
        color: Colors.transparent,
        child: Container(
          width: size,
          height: size,
          decoration: BoxDecoration(
            shape: BoxShape.circle,
            color: isMini ? Colors.white.withOpacity(0.2) : Colors.transparent,
            border: Border.all(
              color: Colors.white,
              width: isMini ? 2.5 : 3.8,
            ),
          ),
          child: Center(
            child: isMini
                ? const Text(
                    "·→·",
                    style: TextStyle(
                      color: Colors.white,
                      fontSize: 22,
                      fontWeight: FontWeight.bold,
                      letterSpacing: -1.0,
                    ),
                  )
                : Column(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      const Text(
                        "·→·",
                        style: TextStyle(
                          color: Colors.white,
                          fontSize: 42,
                          fontWeight: FontWeight.w900,
                          letterSpacing: -2.0,
                        ),
                      ),
                      Container(
                        width: 38,
                        height: 3,
                        decoration: BoxDecoration(
                          color: Colors.white,
                          borderRadius: BorderRadius.circular(2),
                        ),
                      ),
                    ],
                  ),
          ),
        ),
      ),
    );
  }
}
```

---

### 3. `lib/features/onboarding/presentation/widgets/city_skyline_doodle.dart`
*(Zero-asset, vector-based line art painter that consumes 0 KB storage and never lags)*
```dart
import 'dart:math' as math;
import 'package:flutter/material.dart';

class CitySkylineDoodle extends StatelessWidget {
  const CitySkylineDoodle({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return SizedBox(
      height: 240,
      width: double.infinity,
      child: CustomPaint(
        painter: _CitymapperDoodlePainter(),
      ),
    );
  }
}

class _CitymapperDoodlePainter extends CustomPainter {
  @override
  void paint(Canvas canvas, Size size) {
    final w = size.width;
    final h = size.height;

    // 1. Subtle Bengaluru Skyline Silhouette (20% Opacity)
    final skylinePaint = Paint()
      ..color = Colors.white.withOpacity(0.18)
      ..style = PaintingStyle.fill;

    final skylinePath = Path();
    skylinePath.moveTo(0, h);
    skylinePath.lineTo(0, h * 0.75);
    skylinePath.lineTo(w * 0.15, h * 0.75);
    skylinePath.lineTo(w * 0.15, h * 0.60);
    skylinePath.lineTo(w * 0.28, h * 0.60);
    skylinePath.lineTo(w * 0.28, h * 0.78);
    skylinePath.lineTo(w * 0.45, h * 0.78);
    skylinePath.lineTo(w * 0.45, h * 0.50); // Tall tower
    skylinePath.lineTo(w * 0.58, h * 0.50);
    skylinePath.lineTo(w * 0.58, h * 0.70);
    skylinePath.lineTo(w * 0.75, h * 0.70);
    skylinePath.lineTo(w * 0.75, h * 0.58);
    skylinePath.lineTo(w * 0.88, h * 0.58);
    skylinePath.lineTo(w * 0.88, h * 0.82);
    skylinePath.lineTo(w, h * 0.82);
    skylinePath.lineTo(w, h);
    skylinePath.close();
    canvas.drawPath(skylinePath, skylinePaint);

    // 2. Playful Doodle Line-Art Paint
    final linePaint = Paint()
      ..color = Colors.white
      ..style = PaintingStyle.stroke
      ..strokeWidth = 2.4
      ..strokeCap = StrokeCap.round
      ..strokeJoin = StrokeJoin.round;

    // 3. Smoke Trail from Jetpack Commuter
    final smokePath = Path();
    smokePath.moveTo(w * 0.35, h * 0.72);
    smokePath.cubicTo(
      w * 0.50, h * 0.80,
      w * 0.65, h * 0.65,
      w * 0.72, h * 0.42,
    );
    final smokePaint = Paint()
      ..color = Colors.white.withOpacity(0.6)
      ..style = PaintingStyle.stroke
      ..strokeWidth = 14.0
      ..strokeCap = StrokeCap.round;
    canvas.drawPath(smokePath, smokePaint);

    // 4. Tilted BMTC Electric Bus
    canvas.save();
    canvas.translate(w * 0.36, h * 0.58);
    canvas.rotate(-15 * math.pi / 180); // 15-degree playful tilt

    final busRect = RRect.fromRectAndRadius(
      const Rect.fromLTWH(-65, -45, 130, 90),
      const Radius.circular(16),
    );
    canvas.drawRRect(busRect, linePaint);

    // Bus Windows
    canvas.drawRRect(
      RRect.fromRectAndRadius(const Rect.fromLTWH(-55, -35, 32, 28), const Radius.circular(6)),
      linePaint,
    );
    canvas.drawRRect(
      RRect.fromRectAndRadius(const Rect.fromLTWH(-16, -35, 32, 28), const Radius.circular(6)),
      linePaint,
    );
    canvas.drawRRect(
      RRect.fromRectAndRadius(const Rect.fromLTWH(23, -35, 32, 28), const Radius.circular(6)),
      linePaint,
    );

    // Bus Wheels
    canvas.drawCircle(const Offset(-38, 48), 12, linePaint);
    canvas.drawCircle(const Offset(38, 48), 12, linePaint);
    canvas.restore();

    // 5. Jetpack Commuter Flying Doodle
    canvas.save();
    canvas.translate(w * 0.76, h * 0.32);
    canvas.rotate(22 * math.pi / 180);

    // Head / Helmet
    canvas.drawCircle(const Offset(0, -18), 16, linePaint);
    // Smile in helmet
    final visorPath = Path();
    visorPath.arcTo(
      Rect.fromCircle(center: const Offset(0, -18), radius: 10),
      0.2,
      2.7,
      false,
    );
    canvas.drawPath(visorPath, linePaint);

    // Body & Jetpack
    canvas.drawRRect(
      RRect.fromRectAndRadius(const Rect.fromLTWH(-12, -2, 24, 30), const Radius.circular(8)),
      linePaint,
    );
    canvas.drawRRect(
      RRect.fromRectAndRadius(const Rect.fromLTWH(-18, 2, 8, 22), const Radius.circular(4)),
      linePaint,
    );
    canvas.restore();
  }

  @override
  bool shouldRepaint(covariant CustomPainter oldDelegate) => false;
}
```

---

### 4. `lib/features/onboarding/presentation/widgets/amber_pill_button.dart`
```dart
import 'package:flutter/material.dart';
import '../../../../core/constants/colors.dart';

class AmberPillButton extends StatelessWidget {
  final String label;
  final VoidCallback onPressed;

  const AmberPillButton({
    Key? key,
    required this.label,
    required this.onPressed,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return SizedBox(
      width: double.infinity,
      height: 56,
      child: ElevatedButton(
        style: ElevatedButton.styleFrom(
          backgroundColor: CitymapperColors.amberButton,
          elevation: 3,
          shadowColor: Colors.black38,
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(28),
          ),
        ),
        onPressed: onPressed,
        child: Row(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Text(
              label,
              style: const TextStyle(
                color: Colors.white,
                fontSize: 20,
                fontWeight: FontWeight.bold,
                letterSpacing: 0.3,
              ),
            ),
            const SizedBox(width: 8),
            const Icon(
              Icons.chevron_right_rounded,
              color: Colors.white,
              size: 26,
            ),
          ],
        ),
      ),
    );
  }
}
```

---

### 5. `lib/features/onboarding/presentation/pages/splash_page.dart` (Page 1)
```dart
import 'dart:async';
import 'package:flutter/material.dart';
import '../../../../core/constants/colors.dart';
import '../widgets/bmtc_logo_badge.dart';
import 'welcome_page.dart';

class SplashPage extends StatefulWidget {
  const SplashPage({Key? key}) : super(key: key);

  @override
  State<SplashPage> createState() => _SplashPageState();
}

class _SplashPageState extends State<SplashPage> with SingleTickerProviderStateMixin {
  late AnimationController _animController;
  late Animation<double> _scaleAnimation;

  @override
  void initState() {
    super.initState();
    _animController = AnimationController(
      vsync: this,
      duration: const Duration(milliseconds: 700),
    );

    _scaleAnimation = CurvedAnimation(
      parent: _animController,
      curve: Curves.easeOutBack,
    );

    _animController.forward();

    // Auto navigate after 1.5 seconds with a smooth fade/hero transition
    Timer(const Duration(milliseconds: 1500), () {
      if (mounted) {
        Navigator.of(context).pushReplacement(
          PageRouteBuilder(
            transitionDuration: const Duration(milliseconds: 600),
            pageBuilder: (_, __, ___) => const WelcomePage(),
            transitionsBuilder: (_, animation, __, child) {
              return FadeTransition(opacity: animation, child: child);
            },
          ),
        );
      }
    });
  }

  @override
  void dispose() {
    _animController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: CitymapperColors.primaryGreen,
      body: SafeArea(
        child: Stack(
          alignment: Alignment.center,
          children: [
            // Center Animated Hero Emblem
            Center(
              child: ScaleTransition(
                scale: _scaleAnimation,
                child: const BmtcLogoBadge(size: 110, isMini: false),
              ),
            ),

            // Bottom Branding
            Positioned(
              bottom: 30,
              child: Row(
                mainAxisSize: MainAxisSize.min,
                children: const [
                  Text(
                    "·→· ",
                    style: TextStyle(
                      color: Colors.white,
                      fontSize: 22,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                  Text(
                    "BMTC",
                    style: TextStyle(
                      color: Colors.white,
                      fontSize: 22,
                      fontWeight: FontWeight.w800,
                      letterSpacing: -0.5,
                    ),
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}
```

---

### 6. `lib/features/onboarding/presentation/pages/welcome_page.dart` (Page 2)
```dart
import 'package:flutter/material.dart';
import '../../../../core/constants/colors.dart';
import '../widgets/bmtc_logo_badge.dart';
import '../widgets/city_skyline_doodle.dart';
import '../widgets/amber_pill_button.dart';

class WelcomePage extends StatelessWidget {
  const WelcomePage({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: CitymapperColors.primaryGreen,
      body: SafeArea(
        child: Padding(
          padding: const EdgeInsets.symmetric(horizontal: 24.0, vertical: 16.0),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            crossAxisAlignment: CrossAxisAlignment.center,
            children: [
              // Top Area: Hero Badge + Titles
              Column(
                children: [
                  const SizedBox(height: 12),
                  // Scaled down Hero badge from Page 1
                  const BmtcLogoBadge(size: 56, isMini: true),
                  const SizedBox(height: 18),
                  const Text(
                    "BMTC",
                    style: TextStyle(
                      color: Colors.white,
                      fontSize: 38,
                      fontWeight: FontWeight.w900,
                      letterSpacing: -0.5,
                    ),
                  ),
                  const SizedBox(height: 6),
                  Text(
                    "The ultimate transport app",
                    style: TextStyle(
                      color: Colors.white.withOpacity(0.95),
                      fontSize: 18,
                      fontWeight: FontWeight.w600,
                    ),
                  ),
                ],
              ),

              // Center Citymapper-Style Line-Art Doodle
              const CitySkylineDoodle(),

              // Bottom Citymapper Amber "Start >" Action Button
              Column(
                children: [
                  AmberPillButton(
                    label: "Start",
                    onPressed: () {
                      // Navigate to Location Permission or Main Map
                      ScaffoldMessenger.of(context).showSnackBar(
                        const SnackBar(
                          content: Text("Starting BMTC SmartCommute..."),
                          duration: Duration(seconds: 1),
                        ),
                      );
                    },
                  ),
                  const SizedBox(height: 10),
                ],
              ),
            ],
          ),
        ),
      ),
    );
  }
}
```

---

### 7. `lib/main.dart`
```dart
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'features/onboarding/presentation/pages/splash_page.dart';

void main() {
  WidgetsFlutterBinding.ensureInitialized();
  
  // Immersive UI & Status Bar
  SystemChrome.setSystemUIOverlayStyle(
    const SystemUiOverlayStyle(
      statusBarColor: Colors.transparent,
      statusBarIconBrightness: Brightness.light,
      systemNavigationBarColor: Color(0xFF2E7D32),
      systemNavigationBarIconBrightness: Brightness.light,
    ),
  );
  
  runApp(const BmtcApp());
}

class BmtcApp extends StatelessWidget {
  const BmtcApp({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'BMTC',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        fontFamily: 'Roboto',
        useMaterial3: true,
      ),
      home: const SplashPage(),
    );
  }
}
```

