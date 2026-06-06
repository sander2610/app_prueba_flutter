import 'package:supabase_flutter/supabase_flutter.dart';
import 'supabase_service.dart';

class AuthService {
  static final supabase = SupabaseService.client;

  static Future<AuthResponse> signUpWithEmail({
    required String email,
    required String password,
    required String username,
  }) async {
    try {
      final response = await supabase.auth.signUp(
        email: email,
        password: password,
        data: {
          'username': username,
          'full_name': username,
        },
      );
      
      // Crear perfil después del registro
      if (response.user != null) {
        await SupabaseService.profiles.insert({
          'id': response.user?.id,
          'username': username,
          'full_name': username,
          'avatar_url': 'https://ui-avatars.com/api/?name=$username&background=random',
        });
      }
      
      return response;
    } catch (e) {
      throw Exception('Error signing up: $e');
    }
  }

  static Future<AuthResponse> signInWithEmail({
    required String email,
    required String password,
  }) async {
    try {
      return await supabase.auth.signInWithPassword(
        email: email,
        password: password,
      );
    } catch (e) {
      throw Exception('Error signing in: $e');
    }
  }

  static Future<void> signOut() async {
    await supabase.auth.signOut();
  }

  static User? get currentUser => supabase.auth.currentUser;
}