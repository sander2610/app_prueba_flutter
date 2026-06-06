import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'providers/video_provider.dart';
import 'bottom_nav_bar.dart';

void main() {
  runApp(const TikTokApp());
}

class TikTokApp extends StatelessWidget {
  const TikTokApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MultiProvider(
      providers: [
        ChangeNotifierProvider(create: (_) => VideoProvider()),
      ],
      child: MaterialApp(
        title: 'TikTok Clone',
        theme: ThemeData(
          brightness: Brightness.dark,
          scaffoldBackgroundColor: Colors.black,
          fontFamily: 'Roboto',
          useMaterial3: true,
        ),
        home: BottomNavigation(), // Quitamos el const
        debugShowCheckedModeBanner: false,
      ),
    );
  }
}
