import 'package:flutter/material.dart';

class VideoControlAction extends StatelessWidget {
  final IconData icon;
  final String label;
  final double size;
  final VoidCallback? onTap;
  
  const VideoControlAction({
    super.key,
    required this.icon,
    required this.label,
    this.size = 30,
    this.onTap,
  });

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: onTap,
      child: Container(
        margin: const EdgeInsets.only(bottom: 20),
        child: Column(
          children: [
            Icon(
              icon,
              color: Colors.white,
              size: size,
            ),
            const SizedBox(height: 5),
            Text(
              label,
              style: const TextStyle(color: Colors.white, fontSize: 11),
            ),
          ],
        ),
      ),
    );
  }
}