import 'package:flutter/material.dart';
import '../../providers/video_provider.dart';
import 'controls/onscreen_controls.dart';

class HomeVideoRenderer extends StatelessWidget {
  final VideoModel videoData;
  final bool isActive;
  final VoidCallback onLikePressed;
  
  const HomeVideoRenderer({
    super.key,
    required this.videoData,
    required this.isActive,
    required this.onLikePressed,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      color: Colors.black,
      child: Stack(
        fit: StackFit.expand,
        children: [
          // Video placeholder (luego agregaremos reproducción real)
          Container(
            color: Colors.grey[900],
            child: Center(
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Icon(
                    isActive ? Icons.play_circle_filled : Icons.play_circle_outline,
                    color: Colors.white,
                    size: 64,
                  ),
                  const SizedBox(height: 16),
                  Text(
                    isActive ? '▶️ Reproduciendo' : '⏸️ Pausado',
                    style: const TextStyle(color: Colors.white, fontSize: 16),
                  ),
                  const SizedBox(height: 8),
                  Text(
                    videoData.description,
                    style: const TextStyle(color: Colors.white70, fontSize: 14),
                    textAlign: TextAlign.center,
                  ),
                ],
              ),
            ),
          ),
          
          // Gradient overlay
          Container(
            decoration: BoxDecoration(
              gradient: LinearGradient(
                begin: Alignment.topCenter,
                end: Alignment.bottomCenter,
                colors: [
                  Colors.black.withOpacity(0.3),
                  Colors.transparent,
                  Colors.transparent,
                  Colors.black.withOpacity(0.5),
                ],
              ),
            ),
          ),
          
          // Right side controls
          Positioned(
            right: 16,
            bottom: 100,
            child: OnscreenControls(
              videoData: videoData,
              onLikePressed: onLikePressed,
            ),
          ),
          
          // Bottom info
          Positioned(
            left: 16,
            bottom: 100,
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Row(
                  children: [
                    Text(
                      '@${videoData.username}',
                      style: const TextStyle(
                        color: Colors.white,
                        fontSize: 16,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                    const SizedBox(width: 8),
                    Container(
                      padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 2),
                      decoration: BoxDecoration(
                        border: Border.all(color: Colors.white),
                        borderRadius: BorderRadius.circular(4),
                      ),
                      child: const Text(
                        'Follow',
                        style: TextStyle(color: Colors.white, fontSize: 12),
                      ),
                    ),
                  ],
                ),
                const SizedBox(height: 8),
                Text(
                  videoData.description,
                  style: const TextStyle(color: Colors.white, fontSize: 14),
                ),
                const SizedBox(height: 8),
                Row(
                  children: [
                    const Icon(Icons.music_note, color: Colors.white, size: 14),
                    const SizedBox(width: 4),
                    Text(
                      videoData.musicTitle,
                      style: const TextStyle(color: Colors.white70, fontSize: 12),
                    ),
                  ],
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}