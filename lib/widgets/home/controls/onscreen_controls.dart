import 'package:flutter/material.dart';
import '../../../providers/video_provider.dart';

class OnscreenControls extends StatelessWidget {
  final VideoModel videoData;
  final VoidCallback onLikePressed;
  
  const OnscreenControls({
    super.key,
    required this.videoData,
    required this.onLikePressed,
  });

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        const SizedBox(height: 20),
        // Like button
        GestureDetector(
          onTap: onLikePressed,
          child: Column(
            children: [
              Icon(
                videoData.isLiked ? Icons.favorite : Icons.favorite_border,
                color: videoData.isLiked ? Colors.red : Colors.white,
                size: 45,
              ),
              const SizedBox(height: 4),
              Text(
                videoData.likesCount.toString(),
                style: const TextStyle(color: Colors.white, fontSize: 12),
              ),
            ],
          ),
        ),
        const SizedBox(height: 20),
        // Comment button
        const Column(
          children: [
            Icon(Icons.comment, color: Colors.white, size: 45),
            SizedBox(height: 4),
            Text('0', style: TextStyle(color: Colors.white, fontSize: 12)),
          ],
        ),
        const SizedBox(height: 20),
        // Share button
        const Column(
          children: [
            Icon(Icons.share, color: Colors.white, size: 45),
            SizedBox(height: 4),
            Text('0', style: TextStyle(color: Colors.white, fontSize: 12)),
          ],
        ),
      ],
    );
  }
}