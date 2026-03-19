import 'package:dio/dio.dart';

import '../core/api_config.dart';
import '../models/subject_profile.dart';
import 'auth_service.dart';

class SubjectApiService {
  SubjectApiService._();

  static final SubjectApiService instance = SubjectApiService._();
  final Dio _dio = Dio(BaseOptions(baseUrl: ApiConfig.baseUrl));

  Future<List<SubjectProfile>> fetchSubjects({String? query}) async {
    final token = await AuthService.instance.getAccessToken();
    final response = await _dio.get<List<dynamic>>(
      '/subjects',
      queryParameters: {'q': query},
      options: Options(headers: {'Authorization': 'Bearer $token'}),
    );
    return (response.data ?? const [])
        .map((raw) => SubjectProfile.fromJson(raw as Map<String, dynamic>))
        .toList();
  }

  Future<void> createSubject(Map<String, dynamic> payload) async {
    final token = await AuthService.instance.getAccessToken();
    await _dio.post<void>(
      '/subjects',
      data: payload,
      options: Options(headers: {'Authorization': 'Bearer $token'}),
    );
  }
}
