import 'package:flutter/material.dart';
import '../services/supabase_service.dart';

class VideoModel {
  final String id;
  final String userId;
  final String videoUrl;
  final String? thumbnailUrl;
  final String description;
  final String musicTitle;
  final int likesCount;
  final int commentsCount;
  final int sharesCount;
  final String username;
  final String avatarUrl;
  bool isLiked;

  VideoModel({
    required this.id,
    required this.userId,
    required this.videoUrl,
    this.thumbnailUrl,
    required this.description,
    required this.musicTitle,
    required this.likesCount,
    required this.commentsCount,
    required this.sharesCount,
    required this.username,
    required this.avatarUrl,
    this.isLiked = false,
  });

  factory VideoModel.fromJson(Map<String, dynamic> json) {
    final profile = json['profiles'] as Map<String, dynamic>;
    return VideoModel(
      id: json['id'],
      userId: json['user_id'],
      videoUrl: json['video_url'],
      thumbnailUrl: json['thumbnail_url'],
      description: json['description'] ?? '',
      musicTitle: json['music_title'] ?? 'Original Sound',
      likesCount: json['likes_count'] ?? 0,
      commentsCount: json['comments_count'] ?? 0,
      sharesCount: json['shares_count'] ?? 0,
      username: profile['username'],
      avatarUrl: profile['avatar_url'] ?? 'https://ui-avatars.com/api/?name=${profile['username']}&background=random',
    );
  }
}

class VideoProvider extends ChangeNotifier {
  List<VideoModel> _videos = [];
  bool _isLoading = false;
  String? _error;

  List<VideoModel> get videos => _videos;
  bool get isLoading => _isLoading;
  String? get error => _error;

  Future<void> loadVideos() async {
    if (_isLoading) return;
    
    _isLoading = true;
    _error = null;
    notifyListeners();

    try {
      print('🔄 Cargando videos desde Supabase...');
      
      final response = await SupabaseService.client
          .from('videos')
          .select('*, profiles(*)')
          .order('created_at', ascending: false);

      print('✅ Respuesta recibida: ${response.length} videos');
      
      _videos = (response as List)
          .map((video) => VideoModel.fromJson(video))
          .toList();
          
      print('📹 Videos cargados: ${_videos.length}');
      for (var video in _videos) {
        print('   - ${video.username}: ${video.description}');
      }
      
    } catch (e) {
      _error = 'Error loading videos: $e';
      print('❌ Error: $e');
    } finally {
      _isLoading = false;
      notifyListeners();
    }
  }

  Future<void> refreshVideos() async {
    await loadVideos();
  }

  Future<void> toggleLike(String videoId, int index) async {
    try {
      final video = _videos[index];
      
      if (video.isLiked) {
        // Quitar like
        await SupabaseService.client
            .from('likes')
            .delete()
            .match({'video_id': videoId});
        
        _videos[index].likesCount--;
        _videos[index].isLiked = false;
      } else {
        // Dar like
        await SupabaseService.client
            .from('likes')
            .insert({
              'video_id': videoId,
              'user_id': video.userId, // Usamos el ID del creador como ejemplo
            });
        
        _videos[index].likesCount++;
        _videos[index].isLiked = true;
      }
      
      notifyListeners();
    } catch (e) {
      print('Error toggling like: $e');
    }
  }
}