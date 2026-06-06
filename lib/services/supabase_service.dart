import 'package:supabase_flutter/supabase_flutter.dart';

class SupabaseService {
  static final SupabaseClient client = Supabase.instance.client;
  
  // Reemplaza con tus credenciales de Supabase
  static const String supabaseUrl = 'https://TU_PROYECTO.supabase.co';
  static const String supabaseAnonKey = 'TU_ANON_KEY';
  
  static Future<void> initialize() async {
    await Supabase.initialize(
      url: supabaseUrl,
      anonKey: supabaseAnonKey,
    );
  }
  
  // Colecciones
  static var profiles = client.from('profiles');
  static var videos = client.from('videos');
  static var likes = client.from('likes');
  static var comments = client.from('comments');
  static var follows = client.from('follows');
  static var hashtags = client.from('hashtags');
}