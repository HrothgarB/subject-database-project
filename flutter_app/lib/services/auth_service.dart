import 'package:dio/dio.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';

class AuthService {
  AuthService._();

  static final AuthService instance = AuthService._();
  static const _storage = FlutterSecureStorage();
  final Dio _dio = Dio(BaseOptions(baseUrl: 'https://internal-api.example/api'));

  Future<void> login(String email, String password) async {
    final response = await _dio.post<Map<String, dynamic>>(
      '/auth/login',
      data: {'email': email, 'password': password},
    );
    final accessToken = response.data?['access_token'] as String?;
    if (accessToken != null) {
      await _storage.write(key: 'access_token', value: accessToken);
    }
  }

  Future<String?> getAccessToken() => _storage.read(key: 'access_token');
}
