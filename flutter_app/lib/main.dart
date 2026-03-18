import 'package:flutter/material.dart';

import 'core/app_router.dart';
import 'services/local_sync_service.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await LocalSyncService.instance.initialize();
  runApp(const SubjectMobileApp());
}

class SubjectMobileApp extends StatelessWidget {
  const SubjectMobileApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Subject DB',
      theme: ThemeData(useMaterial3: true, colorSchemeSeed: Colors.indigo),
      initialRoute: AppRouter.login,
      routes: AppRouter.routes,
    );
  }
}
