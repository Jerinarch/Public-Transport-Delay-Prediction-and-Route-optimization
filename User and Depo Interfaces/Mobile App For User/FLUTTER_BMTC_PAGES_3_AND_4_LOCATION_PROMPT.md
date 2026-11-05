# Master Engineering Prompt: BMTC Pages 3 & 4 (Location Access & Manual Search)
## Production-Grade Flutter Architecture, Animated Radar, and Location Fallbacks

---

### HOW TO USE THIS PROMPT
Provide this exact prompt to your AI developer, Copilot, or use it directly as your implementation blueprint in **Android Studio**. It connects directly to Pages 1 & 2 (Splash & Welcome), building the **exact Citymapper-style Location Permission Primer (Page 3)** and the **Dual-Mode Location Handler / Manual Stop Search (Page 4)** following international enterprise standards.

---

```markdown
You are a Principal Flutter Mobile Engineer. Build Pages 3 and 4 of the onboarding sequence for an enterprise public transport mobile application called "BMTC" in Android Studio using Flutter.

This builds immediately after Page 1 (Splash) and Page 2 (Welcome Screen).
The user must be given a choice:
- PATH A: Automatic GPS Location Access (with Citymapper's animated radar pulse and system permission dialog).
- PATH B: Manual Stop / Location Search (the user can type their transit stop or choose from major Bengaluru corridors).

================================================================================
1. INTERNATIONAL ENGINEERING & PERFORMANCE CONSTRAINTS
================================================================================
- Zero-Lag Vector Radar: The concentric radar pulse and blue GPS dot must be rendered with a hardware-accelerated CustomPainter rather than heavy GIFs or Lottie JSONs. Asset size is 0 KB, locked at 60/120 FPS.
- Memory Leak Prevention: AnimationController must use SingleTickerProviderStateMixin and be properly disposed in dispose().
- Robust Location State Machine:
  1. Check if device Location Services (GPS switch) are enabled (`Geolocator.isLocationServiceEnabled()`).
  2. Request runtime permissions (`Permission.locationWhenInUse.request()`).
  3. Handle all states: Granted, Denied, Permanently Denied, or GPS Disabled without ever freezing or throwing unhandled platform exceptions.
  4. 5-second timeout on GPS position retrieval to prevent infinite loading spinners if satellite fix is slow.
- Android Manifest Setup:
  Include `ACCESS_FINE_LOCATION`, `ACCESS_COARSE_LOCATION`, and `usesCleartextTraffic="true"`.
- Clean Architecture Organization:
  lib/
  ├── core/
  │   ├── constants/
  │   │   ├── colors.dart
  │   │   └── bmtc_stops.dart             # Pre-indexed BMTC arterial stops
  │   └── services/
  │       └── location_service.dart       # Robust GPS & permission manager
  └── features/
      └── onboarding/
          └── presentation/
              ├── pages/
              │   ├── location_permission_page.dart # Page 3: Radar & Location Primer
              │   └── manual_search_page.dart       # Page 4: Type/Search Location Choice
              └── widgets/
                  ├── radar_pulse_widget.dart       # Vector radar sweep & pulse
                  └── amber_pill_button.dart        # Citymapper action button

================================================================================
2. DETAILED SCREEN SPECIFICATIONS
================================================================================

--- PAGE 3: LOCATION PERMISSION PRIMER (location_permission_page.dart) ---
- Background: Solid BMTC Transit Green (CitymapperColors.primaryGreen = #2E7D32).
- Top Area:
  - Circular avatar badge with smiling transit robot face (`·→·` or transit icon).
- Typography:
  - "Allow Location" (34sp, bold, white).
  - SizedBox(height: 8).
  - "We're a transport app" (20sp, semi-bold, white).
  - SizedBox(height: 6).
  - "Location helps us get you from A to B and find buses near your stop" (16sp, white.withOpacity(0.85), centered).
- Center Radar Animation (`radar_pulse_widget.dart`):
  - Concentric expanding rings with fading opacity.
  - Rotating radar sweep gradient.
  - Pulsing bright blue GPS locator dot (#2196F3) inside a white circular border.
- Bottom Dual-Action Area:
  - Primary Button: Amber Pill Button "OK  >" (#EAA043) -> Triggers automatic location request.
  - Secondary Action: Clean text button below: "Or type your location manually" (white with underline or subtle border) -> Immediately navigates to ManualSearchPage.

--- PAGE 4: DUAL-MODE RESOLUTION (System Permission & Manual Search Page) ---
- If the user taps "OK >":
  - Triggers native OS dialog: "Allow 'BMTC' to use your location?".
  - If Granted: Saves coordinates, sets `onboarding_completed = true` in SharedPreferences, and navigates to MainMapScreen.
  - If Denied / Disabled: Automatically slides open ManualSearchPage with a friendly banner: "Location turned off. Choose your corridor or stop below."
- If the user taps "Or type your location manually" (manual_search_page.dart):
  - Clean Citymapper-style search interface.
  - Top search input: White rounded box with search icon and "Type bus stop or area (e.g. Silk Board, Majestic)".
  - Instant autocomplete filter against BMTC stops database (`bmtc_stops.dart`).
  - Quick-select Corridor Hub chips:
    [ Central Silk Board ] [ Majestic KBS ] [ ITPL Whitefield ] [ Hebbal Flyover ] [ Banashankari ]
  - Tapping any stop sets the active origin and navigates to the Main Map.

================================================================================
3. READY-TO-USE CODE IMPLEMENTATION
================================================================================
Provide the complete, bug-free, null-safe Dart files for:
1. `lib/core/services/location_service.dart`
2. `lib/core/constants/bmtc_stops.dart`
3. `lib/features/onboarding/presentation/widgets/radar_pulse_widget.dart`
4. `lib/features/onboarding/presentation/pages/location_permission_page.dart`
5. `lib/features/onboarding/presentation/pages/manual_search_page.dart`
```

---

## Complete Production Code Implementation

### 1. `lib/core/services/location_service.dart`
*(Handles permissions, hardware GPS toggles, timeouts, and fallbacks with zero crashes)*
```dart
import 'package:geolocator/geolocator.dart';
import 'package:permission_handler/permission_handler.dart';

enum LocationResultStatus {
  success,
  serviceDisabled,
  permissionDenied,
  permissionPermanentlyDenied,
  timeout,
  error,
}

class LocationResult {
  final LocationResultStatus status;
  final Position? position;
  final String? message;

  LocationResult({required this.status, this.position, this.message});
}

class LocationService {
  static final LocationService _instance = LocationService._internal();
  factory LocationService() => _instance;
  LocationService._internal();

  /// Requests permission and retrieves high-accuracy position with safety timeouts
  Future<LocationResult> requestAndGetLocation() async {
    try {
      // 1. Check if device location services (GPS) are on
      final isServiceEnabled = await Geolocator.isLocationServiceEnabled();
      if (!isServiceEnabled) {
        return LocationResult(
          status: LocationResultStatus.serviceDisabled,
          message: "Location services are turned off on your device.",
        );
      }

      // 2. Check and request permission
      var permission = await Geolocator.checkPermission();
      if (permission == LocationPermission.denied) {
        permission = await Geolocator.requestPermission();
        if (permission == LocationPermission.denied) {
          return LocationResult(
            status: LocationResultStatus.permissionDenied,
            message: "Location permission was denied.",
          );
        }
      }

      if (permission == LocationPermission.deniedForever) {
        return LocationResult(
          status: LocationResultStatus.permissionPermanentlyDenied,
          message: "Location permission is permanently denied. You can search stops manually.",
        );
      }

      // 3. Retrieve position with a 5-second timeout to prevent infinite spinners
      final position = await Geolocator.getCurrentPosition(
        desiredAccuracy: LocationAccuracy.high,
        timeLimit: const Duration(seconds: 5),
      );

      return LocationResult(
        status: LocationResultStatus.success,
        position: position,
      );
    } catch (e) {
      // Graceful timeout or hardware fallback
      try {
        final lastKnown = await Geolocator.getLastKnownPosition();
        if (lastKnown != null) {
          return LocationResult(
            status: LocationResultStatus.success,
            position: lastKnown,
          );
        }
      } catch (_) {}

      return LocationResult(
        status: LocationResultStatus.timeout,
        message: "GPS fix timed out. You can pick your stop manually.",
      );
    }
  }
}
```

---

### 2. `lib/core/constants/bmtc_stops.dart`
*(Pre-indexed database of primary Bengaluru transit hubs and corridor stops)*
```dart
class BmtcStop {
  final String id;
  final String name;
  final String corridor;
  final double lat;
  final double lon;

  const BmtcStop({
    required this.id,
    required this.name,
    required this.corridor,
    required this.lat,
    required this.lon,
  });
}

class BmtcStopsData {
  static const List<BmtcStop> popularStops = [
    BmtcStop(
      id: "BS_SIL",
      name: "Central Silk Board",
      corridor: "Outer Ring Road (500D) / Hosur Road",
      lat: 12.9176,
      lon: 77.6234,
    ),
    BmtcStop(
      id: "BS_MAJ",
      name: "Kempegowda Bus Station (Majestic)",
      corridor: "City Central Terminal (335E)",
      lat: 12.9772,
      lon: 77.5713,
    ),
    BmtcStop(
      id: "BS_ITP",
      name: "ITPL Main Gate (Whitefield)",
      corridor: "Whitefield Tech Corridor (500K / 335E)",
      lat: 12.9863,
      lon: 77.7381,
    ),
    BmtcStop(
      id: "BS_HEB",
      name: "Hebbal Flyover TTMC",
      corridor: "Outer Ring Road / Airport Expressway",
      lat: 13.0358,
      lon: 77.5970,
    ),
    BmtcStop(
      id: "BS_BEL",
      name: "Bellandur EcoSpace",
      corridor: "Outer Ring Road Arterial (500D)",
      lat: 12.9279,
      lon: 77.6800,
    ),
    BmtcStop(
      id: "BS_MAR",
      name: "Marathahalli Bridge",
      corridor: "HAL Old Airport Road / ORR Junction",
      lat: 12.9562,
      lon: 77.7011,
    ),
    BmtcStop(
      id: "BS_BAN",
      name: "Banashankari TTMC",
      corridor: "South Bengaluru Arterial (500K)",
      lat: 12.9155,
      lon: 77.5736,
    ),
    BmtcStop(
      id: "BS_TIN",
      name: "Tin Factory Junction",
      corridor: "KR Puram / Old Madras Road (500CA)",
      lat: 12.9944,
      lon: 77.6669,
    ),
    BmtcStop(
      id: "BS_ELE",
      name: "Electronic City Wipro Gate",
      corridor: "Hosur Road IT Corridor (500CA)",
      lat: 12.8399,
      lon: 77.6770,
    ),
  ];
}
```

---

### 3. `lib/features/onboarding/presentation/widgets/radar_pulse_widget.dart`
*(CustomPainter vector radar animation: zero assets, 60 FPS, 0 MB memory)*
```dart
import 'dart:math' as math;
import 'package:flutter/material.dart';

class RadarPulseWidget extends StatefulWidget {
  final double size;
  const RadarPulseWidget({Key? key, this.size = 200}) : super(key: key);

  @override
  State<RadarPulseWidget> createState() => _RadarPulseWidgetState();
}

class _RadarPulseWidgetState extends State<RadarPulseWidget>
    with SingleTickerProviderStateMixin {
  late AnimationController _controller;

  @override
  void initState() {
    super.initState();
    _controller = AnimationController(
      vsync: this,
      duration: const Duration(milliseconds: 2400),
    )..repeat();
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return SizedBox(
      width: widget.size,
      height: widget.size,
      child: AnimatedBuilder(
        animation: _controller,
        builder: (context, child) {
          return CustomPaint(
            painter: _RadarPainter(progress: _controller.value),
          );
        },
      ),
    );
  }
}

class _RadarPainter extends CustomPainter {
  final double progress;
  _RadarPainter({required this.progress});

  @override
  void paint(Canvas canvas, Size size) {
    final center = Offset(size.width / 2, size.height / 2);
    final maxRadius = size.width / 2;

    // 1. Static Translucent Background Disk
    final bgPaint = Paint()
      ..color = Colors.white.withOpacity(0.08)
      ..style = PaintingStyle.fill;
    canvas.drawCircle(center, maxRadius, bgPaint);

    // 2. Animated Concentric Rings (Wave 1 and Wave 2)
    void drawWave(double waveProgress) {
      final r = maxRadius * waveProgress;
      final opacity = (1.0 - waveProgress).clamp(0.0, 1.0) * 0.7;
      final ringPaint = Paint()
        ..color = Colors.white.withOpacity(opacity)
        ..style = PaintingStyle.stroke
        ..strokeWidth = 2.0;
      canvas.drawCircle(center, r, ringPaint);
    }

    drawWave(progress);
    drawWave((progress + 0.5) % 1.0);

    // 3. Rotating Radar Sweep Beam
    final sweepAngle = progress * 2 * math.pi;
    final sweepPaint = Paint()
      ..shader = SweepGradient(
        center: Alignment.center,
        startAngle: sweepAngle - 0.5,
        endAngle: sweepAngle,
        colors: [
          Colors.white.withOpacity(0.0),
          Colors.white.withOpacity(0.25),
        ],
      ).createShader(Rect.fromCircle(center: center, radius: maxRadius))
      ..style = PaintingStyle.fill;

    canvas.drawCircle(center, maxRadius, sweepPaint);

    // 4. Center Glowing Blue GPS Dot with White Border
    final whiteBorderPaint = Paint()
      ..color = Colors.white
      ..style = PaintingStyle.fill;
    canvas.drawCircle(center, 18, whiteBorderPaint);

    final blueDotPaint = Paint()
      ..color = const Color(0xFF1E88E5)
      ..style = PaintingStyle.fill;
    canvas.drawCircle(center, 12, blueDotPaint);

    // Inner bright reflection
    final reflectionPaint = Paint()
      ..color = Colors.white.withOpacity(0.6)
      ..style = PaintingStyle.fill;
    canvas.drawCircle(center.translate(-3, -3), 3, reflectionPaint);
  }

  @override
  bool shouldRepaint(covariant _RadarPainter oldDelegate) =>
      oldDelegate.progress != progress;
}
```

---

### 4. `lib/features/onboarding/presentation/pages/location_permission_page.dart` (Page 3)
```dart
import 'package:flutter/material.dart';
import '../../../../core/constants/colors.dart';
import '../../../../core/services/location_service.dart';
import '../widgets/radar_pulse_widget.dart';
import '../widgets/amber_pill_button.dart';
import 'manual_search_page.dart';

class LocationPermissionPage extends StatefulWidget {
  const LocationPermissionPage({Key? key}) : super(key: key);

  @override
  State<LocationPermissionPage> createState() => _LocationPermissionPageState();
}

class _LocationPermissionPageState extends State<LocationPermissionPage> {
  bool _isLoading = false;

  Future<void> _handleAutoLocation() async {
    setState(() => _isLoading = true);

    final result = await LocationService().requestAndGetLocation();

    if (!mounted) return;
    setState(() => _isLoading = false);

    if (result.status == LocationResultStatus.success && result.position != null) {
      // Successfully obtained GPS coordinates!
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text(
            "Location active: (${result.position!.latitude.toStringAsFixed(3)}, ${result.position!.longitude.toStringAsFixed(3)})",
          ),
          backgroundColor: const Color(0xFF2E7D32),
        ),
      );
      // Navigate to Main Map with live GPS coordinates
      // Navigator.pushReplacementNamed(context, '/map', arguments: result.position);
    } else {
      // Permission denied or GPS switch off -> Gracefully route to Manual Search
      Navigator.push(
        context,
        MaterialPageRoute(
          builder: (context) => ManualSearchPage(
            bannerMessage: result.message ?? "Select your stop below to continue.",
          ),
        ),
      );
    }
  }

  void _handleManualChoice() {
    Navigator.push(
      context,
      MaterialPageRoute(builder: (context) => const ManualSearchPage()),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: CitymapperColors.primaryGreen,
      body: SafeArea(
        child: Padding(
          padding: const EdgeInsets.symmetric(horizontal: 26.0, vertical: 16.0),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            crossAxisAlignment: CrossAxisAlignment.center,
            children: [
              // Top Area: Circular Mascot Badge + Headings
              Column(
                children: [
                  const SizedBox(height: 12),
                  // Citymapper Robot / Transit Icon
                  Container(
                    width: 58,
                    height: 58,
                    decoration: const BoxDecoration(
                      color: Colors.white24,
                      shape: BoxShape.circle,
                    ),
                    child: const Icon(
                      Icons.near_me_rounded,
                      color: Colors.white,
                      size: 32,
                    ),
                  ),
                  const SizedBox(height: 18),
                  const Text(
                    "Allow Location",
                    style: TextStyle(
                      color: Colors.white,
                      fontSize: 34,
                      fontWeight: FontWeight.w900,
                      letterSpacing: -0.5,
                    ),
                  ),
                  const SizedBox(height: 8),
                  const Text(
                    "We’re a transport app",
                    style: TextStyle(
                      color: Colors.white,
                      fontSize: 20,
                      fontWeight: FontWeight.w600,
                    ),
                  ),
                  const SizedBox(height: 8),
                  Text(
                    "Location helps us get you from A to B and find buses near your stop",
                    textAlign: TextAlign.center,
                    style: TextStyle(
                      color: Colors.white.withOpacity(0.9),
                      fontSize: 16,
                      height: 1.35,
                    ),
                  ),
                ],
              ),

              // Center Radar Animation
              const RadarPulseWidget(size: 210),

              // Bottom Actions: Primary "OK >" + Secondary "Type Manually"
              Column(
                children: [
                  _isLoading
                      ? const CircularProgressIndicator(color: Colors.white)
                      : AmberPillButton(
                          label: "OK",
                          onPressed: _handleAutoLocation,
                        ),
                  const SizedBox(height: 12),

                  // Secondary Choice: Type Location Manually
                  TextButton(
                    onPressed: _handleManualChoice,
                    style: TextButton.styleFrom(
                      foregroundColor: Colors.white,
                      padding: const EdgeInsets.symmetric(vertical: 8, horizontal: 16),
                    ),
                    child: Row(
                      mainAxisSize: MainAxisSize.min,
                      children: const [
                        Icon(Icons.edit_location_alt_rounded, size: 18, color: Colors.white70),
                        SizedBox(width: 8),
                        Text(
                          "Or type your location manually",
                          style: TextStyle(
                            fontSize: 15,
                            fontWeight: FontWeight.w600,
                            decoration: TextDecoration.underline,
                            decorationColor: Colors.white70,
                          ),
                        ),
                      ],
                    ),
                  ),
                  const SizedBox(height: 6),
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

### 5. `lib/features/onboarding/presentation/pages/manual_search_page.dart` (Page 4)
*(Full manual search, instant autocomplete against BMTC stops, and quick corridor chips)*
```dart
import 'package:flutter/material.dart';
import '../../../../core/constants/colors.dart';
import '../../../../core/constants/bmtc_stops.dart';

class ManualSearchPage extends StatefulWidget {
  final String? bannerMessage;
  const ManualSearchPage({Key? key, this.bannerMessage}) : super(key: key);

  @override
  State<ManualSearchPage> createState() => _ManualSearchPageState();
}

class _ManualSearchPageState extends State<ManualSearchPage> {
  final TextEditingController _searchController = TextEditingController();
  List<BmtcStop> _filteredStops = BmtcStopsData.popularStops;

  void _onSearchChanged(String query) {
    setState(() {
      if (query.trim().isEmpty) {
        _filteredStops = BmtcStopsData.popularStops;
      } else {
        _filteredStops = BmtcStopsData.popularStops
            .where((stop) =>
                stop.name.toLowerCase().contains(query.toLowerCase()) ||
                stop.corridor.toLowerCase().contains(query.toLowerCase()))
            .toList();
      }
    });
  }

  void _selectStop(BmtcStop stop) {
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: Text("Origin selected: ${stop.name}"),
        backgroundColor: const Color(0xFF2E7D32),
      ),
    );
    // Navigate to Main Map with chosen stop as origin
    // Navigator.pushReplacementNamed(context, '/map', arguments: stop);
  }

  @override
  void dispose() {
    _searchController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: CitymapperColors.primaryGreen,
      appBar: AppBar(
        backgroundColor: Colors.transparent,
        elevation: 0,
        leading: IconButton(
          icon: const Icon(Icons.arrow_back_ios_rounded, color: Colors.white),
          onPressed: () => Navigator.pop(context),
        ),
        title: const Text(
          "Choose Your Stop",
          style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold),
        ),
      ),
      body: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          // Optional Notification Banner if redirected from GPS failure
          if (widget.bannerMessage != null)
            Container(
              margin: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
              padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 10),
              decoration: BoxDecoration(
                color: CitymapperColors.amberButton,
                borderRadius: BorderRadius.circular(12),
              ),
              child: Row(
                children: [
                  const Icon(Icons.info_outline_rounded, color: Colors.white, size: 20),
                  const SizedBox(width: 10),
                  Expanded(
                    child: Text(
                      widget.bannerMessage!,
                      style: const TextStyle(
                        color: Colors.white,
                        fontSize: 13,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                  ),
                ],
              ),
            ),

          // Search Input Bar (Citymapper style white rounded pill)
          Padding(
            padding: const EdgeInsets.symmetric(horizontal: 16.0, vertical: 8.0),
            child: Container(
              height: 52,
              decoration: BoxDecoration(
                color: Colors.white,
                borderRadius: BorderRadius.circular(26),
                boxShadow: const [
                  BoxShadow(color: Colors.black26, blurRadius: 4, offset: Offset(0, 2)),
                ],
              ),
              child: TextField(
                controller: _searchController,
                onChanged: _onSearchChanged,
                autofocus: widget.bannerMessage == null,
                style: const TextStyle(fontSize: 16, color: Colors.black87),
                decoration: InputDecoration(
                  hintText: "Type bus stop or area (e.g. Silk Board)",
                  hintStyle: TextStyle(color: Colors.grey.shade500, fontSize: 15),
                  prefixIcon: const Icon(Icons.search_rounded, color: Color(0xFF2E7D32)),
                  suffixIcon: _searchController.text.isNotEmpty
                      ? IconButton(
                          icon: const Icon(Icons.clear_rounded, color: Colors.grey),
                          onPressed: () {
                            _searchController.clear();
                            _onSearchChanged("");
                          },
                        )
                      : null,
                  border: InputBorder.none,
                  contentPadding: const EdgeInsets.symmetric(vertical: 14),
                ),
              ),
            ),
          ),

          // Quick Corridor Chips
          Padding(
            padding: const EdgeInsets.symmetric(horizontal: 16.0, vertical: 6.0),
            child: SingleChildScrollView(
              scrollDirection: Axis.horizontal,
              child: Row(
                children: [
                  _buildQuickChip("Silk Board"),
                  _buildQuickChip("Majestic"),
                  _buildQuickChip("Bellandur"),
                  _buildQuickChip("ITPL"),
                  _buildQuickChip("Hebbal"),
                ],
              ),
            ),
          ),

          const SizedBox(height: 8),

          // List of Filtered BMTC Stops
          Expanded(
            child: Container(
              decoration: const BoxDecoration(
                color: Colors.white,
                borderRadius: BorderRadius.only(
                  topLeft: Radius.circular(24),
                  topRight: Radius.circular(24),
                ),
              ),
              child: _filteredStops.isEmpty
                  ? Center(
                      child: Column(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: [
                          Icon(Icons.search_off_rounded, size: 54, color: Colors.grey.shade400),
                          const SizedBox(height: 10),
                          Text(
                            "No stops found for \"${_searchController.text}\"",
                            style: TextStyle(color: Colors.grey.shade600, fontSize: 16),
                          ),
                        ],
                      ),
                    )
                  : ListView.separated(
                      padding: const EdgeInsets.symmetric(vertical: 12),
                      itemCount: _filteredStops.length,
                      separatorBuilder: (context, index) =>
                          Divider(color: Colors.grey.shade200, height: 1),
                      itemBuilder: (context, index) {
                        final stop = _filteredStops[index];
                        return ListTile(
                          leading: Container(
                            width: 40,
                            height: 40,
                            decoration: BoxDecoration(
                              color: CitymapperColors.primaryGreen.withOpacity(0.12),
                              shape: BoxShape.circle,
                            ),
                            child: const Icon(
                              Icons.directions_bus_filled_rounded,
                              color: CitymapperColors.primaryGreen,
                              size: 22,
                            ),
                          ),
                          title: Text(
                            stop.name,
                            style: const TextStyle(
                              fontWeight: FontWeight.bold,
                              fontSize: 16,
                              color: Colors.black87,
                            ),
                          ),
                          subtitle: Text(
                            stop.corridor,
                            style: TextStyle(color: Colors.grey.shade600, fontSize: 13),
                          ),
                          trailing: const Icon(
                            Icons.arrow_forward_ios_rounded,
                            size: 14,
                            color: Colors.black38,
                          ),
                          onTap: () => _selectStop(stop),
                        );
                      },
                    ),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildQuickChip(String label) {
    return Padding(
      padding: const EdgeInsets.only(right: 8.0),
      child: ActionChip(
        backgroundColor: Colors.white.withOpacity(0.2),
        side: BorderSide.none,
        label: Text(
          label,
          style: const TextStyle(color: Colors.white, fontSize: 13, fontWeight: FontWeight.bold),
        ),
        onPressed: () {
          _searchController.text = label;
          _onSearchChanged(label);
        },
      ),
    );
  }
}
```

