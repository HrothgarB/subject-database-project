import 'package:flutter/material.dart';

import '../screens/encounter_screen.dart';
import '../screens/login_screen.dart';
import '../screens/subject_detail_screen.dart';
import '../screens/subject_edit_screen.dart';
import '../screens/subject_list_screen.dart';

class AppRouter {
  static const login = '/login';
  static const subjects = '/subjects';
  static const subjectDetail = '/subject-detail';
  static const subjectEdit = '/subject-edit';
  static const encounterCreate = '/encounter-create';

  static final Map<String, WidgetBuilder> routes = {
    login: (_) => const LoginScreen(),
    subjects: (_) => const SubjectListScreen(),
    subjectDetail: (_) => const SubjectDetailScreen(),
    subjectEdit: (_) => const SubjectEditScreen(),
    encounterCreate: (_) => const EncounterScreen(),
  };
}
