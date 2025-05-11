import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'package:flutter_markdown/flutter_markdown.dart';

void main() => runApp(FlightWeatherApp());

class FlightWeatherApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Aviation Weather',
      debugShowCheckedModeBanner: false,
      home: FlightScreen(),
    );
  }
}

class FlightScreen extends StatefulWidget {
  @override
  _FlightScreenState createState() => _FlightScreenState();
}

class _FlightScreenState extends State<FlightScreen> {
  final _flightController = TextEditingController();
  final _offsetController = TextEditingController(text: '0');
  String? summary;
  List<String>? waypoints;
  bool loading = false;

  Future<void> fetchFlightData() async {
    setState(() {
      loading = true;
      summary = null;
      waypoints = null;
    });

    try {
      final response = await http.post(
        Uri.parse("http://127.0.0.1:5000/analyze-flight"),
        headers: {"Content-Type": "application/json"},
        body: jsonEncode({
          "flight_number": _flightController.text.trim(),
          "forecast_offset": int.tryParse(_offsetController.text.trim()) ?? 0
        }),
      );

      final data = jsonDecode(response.body);
      setState(() {
        summary = data['summary'];
        waypoints = List<String>.from(data['waypoints']);
      });
    } catch (e) {
      setState(() => summary = 'Error: $e');
    } finally {
      setState(() => loading = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    final width = MediaQuery.of(context).size.width;
    final isMobile = width < 600;

    return Scaffold(
      appBar: AppBar(
        title: Text('Aviation Weather',
            style: TextStyle(fontWeight: FontWeight.bold, color: Colors.white)),
        centerTitle: true,
        backgroundColor: Colors.blue,
      ),
      body: Stack(
        children: [
          Container(
            decoration: BoxDecoration(
              image: DecorationImage(
                image: AssetImage("assets/images/backpic.png"), // Your background image
                fit: BoxFit.cover,
              ),
            ),
          ),
          SingleChildScrollView(
            padding: const EdgeInsets.all(16.0),
            child: Center(
              child: ConstrainedBox(
                constraints: BoxConstraints(maxWidth: 700),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.stretch,
                  children: [
                    TextField(
                      controller: _flightController,
                      decoration: InputDecoration(
                        labelText: 'Enter Flight Number (e.g., BA112)',
                        border: OutlineInputBorder(),
                        filled: true,
                        fillColor: Colors.white
                      ),
                      style: TextStyle(fontSize: isMobile ? 16 : 18),
                    ),
                    const SizedBox(height: 16),
                    TextField(
                      controller: _offsetController,
                      decoration: InputDecoration(
                        labelText: 'Forecast Offset (hours)',
                        border: OutlineInputBorder(),
                        filled: true,
                        fillColor: Colors.white
                      ),
                      keyboardType: TextInputType.number,
                      style: TextStyle(fontSize: isMobile ? 16 : 18),
                    ),
                    const SizedBox(height: 16),
                    ElevatedButton(
                      onPressed: fetchFlightData,
                      style: ElevatedButton.styleFrom(
                        padding: EdgeInsets.symmetric(
                          vertical: isMobile ? 12 : 16,
                          horizontal: isMobile ? 20 : 30,
                        ),
                      ),
                      child: Text('Analyze Flight',
                          style: TextStyle(fontSize: isMobile ? 16 : 18)),
                    ),
                    const SizedBox(height: 24),
                    if (loading)
                      Center(child: CircularProgressIndicator()),
                    if (waypoints != null) ...[
                      Text('Flight Route:',
                          style: TextStyle(
                              fontWeight: FontWeight.bold, fontSize: 18)),
                      const SizedBox(height: 8),
                      ...waypoints!.map((wp) => Padding(
                        padding: const EdgeInsets.symmetric(vertical: 4.0),
                        child: Text('• $wp'),
                      )),
                    ],
                    if (summary != null) ...[
                      const SizedBox(height: 24),
                      Text('Weather Safety Briefing:',
                          style: TextStyle(
                              fontWeight: FontWeight.bold, fontSize: 18)),
                      const SizedBox(height: 8),
                      Container(
                        padding: EdgeInsets.all(12),
                        decoration: BoxDecoration(
                          color: Colors.grey[200]?.withValues(alpha: 0.85),
                          borderRadius: BorderRadius.circular(8),
                        ),
                        child: MarkdownBody(
                          data: summary!,
                          styleSheet: MarkdownStyleSheet(
                            p: TextStyle(fontSize: 16, height: 1.4),
                            strong: TextStyle(fontWeight: FontWeight.bold),
                          ),
                        ),
                      ),
                    ]
                  ],
                ),
              ),
            ),
          ),
        ],
      ),
    );
  }
}
