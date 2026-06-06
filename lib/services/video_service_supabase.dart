import 'package:supabase_flutter/supabase_flutter.dart';
import '../models/video_model.dart';
import 'supabase_service.dart';

class VideoServiceSupabase {
  // Obtener videos con paginación
  static Future<List<VideoModel>> getVideos({
    int limit = 10,
    int offset = 0,
  }) async {
    try {
      final response = await SupabaseService.client
          .from('videos')
          .select('*, profiles(*)')
          .order('created_at', ascending: false)
          .range(offset, offset + limit - 1);

      return (response as List)
          .map((video) => VideoModel.fromJson(video))
          .toList();
    } catch (e) {
      print('Error getting videos: $e');
      return [];
    }
  }

  // Subir video
  static Future<VideoModel?> uploadVideo({
    required String userId,
    required String videoUrl,
    required String description,
    required String musicTitle,
    String? thumbnailUrl,
  }) async {
    try {
      final response = await SupabaseService.client
          .from('videos')
          .insert({
            'user_id': userId,
            'video_url': videoUrl,
            'thumbnail_url': thumbnailUrl,
            'description': description,
            'music_title': musicTitle,
          })
          .select()
          .single();

      return VideoModel.fromJson(response);
    } catch (e) {
      print('Error uploading video: $e');
      return null;
    }
  }

  // Dar like
  static Future<void> likeVideo(String videoId, String userId) async {
    try {
      await SupabaseService.client
          .from('likes')
          .insert({
            'user_id': userId,
            'video_id': videoId,
          });
    } catch (e) {
      print('Error liking video: $e');
    }
  }

  // Quitar like
  static Future<void> unlikeVideo(String videoId, String userId) async {
    try {
      await SupabaseService.client
          .from('likes')
          .delete()
          .match({'user_id': userId, 'video_id': videoId});
    } catch (e) {
      print('Error unliking video: $e');
    }
  }

  // Verificar si dio like
  static Future<bool> isVideoLiked(String videoId, String userId) async {
    try {
      final response = await SupabaseService.client
          .from('likes')
          .select()
          .match({'user_id': userId, 'video_id': videoId});

      return (response as List).isNotEmpty;
    } catch (e) {
      return false;
    }
  }

  // Obtener videos de un usuario
  static Future<List<VideoModel>> getUserVideos(String userId) async {
    try {
      final response = await SupabaseService.client
          .from('videos')
          .select('*, profiles(*)')
          .eq('user_id', userId)
          .order('created_at', ascending: false);

      return (response as List)
          .map((video) => VideoModel.fromJson(video))
          .toList();
    } catch (e) {
      print('Error getting user videos: $e');
      return [];
    }
  }

  // Incrementar contador de compartidos
  static Future<void> incrementShares(String videoId) async {
    try {
      await SupabaseService.client.rpc('increment_shares', params: {
        'video_id': videoId,
      });
    } catch (e) {
      print('Error incrementing shares: $e');
    }
  }
}