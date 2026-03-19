class ApiConfig {
  ApiConfig._();

  static const baseUrl = String.fromEnvironment(
    'SUBJECT_API_BASE_URL',
    defaultValue: 'http://10.0.2.2:8000/api',
  );

  static const deviceId = String.fromEnvironment(
    'SUBJECT_DEVICE_ID',
    defaultValue: 'flutter-mobile',
  );
}
