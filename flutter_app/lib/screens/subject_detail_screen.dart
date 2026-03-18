import 'package:flutter/material.dart';

import '../core/app_router.dart';
import '../models/subject_profile.dart';

class SubjectDetailScreen extends StatelessWidget {
  const SubjectDetailScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final subject = ModalRoute.of(context)?.settings.arguments as SubjectProfile?;
    if (subject == null) {
      return const Scaffold(body: Center(child: Text('Subject missing')));
    }

    return Scaffold(
      appBar: AppBar(title: Text('${subject.firstName} ${subject.lastName}')),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          Text('Alias: ${subject.alias ?? '-'}'),
          Text('Case #: ${subject.caseNumber ?? '-'}'),
          Text('Intel #: ${subject.intelNumber ?? '-'}'),
          Text('Phone: ${subject.phone ?? '-'}'),
          Text('Address: ${subject.address ?? '-'}'),
          const SizedBox(height: 12),
          Text(subject.notes ?? 'No notes.'),
          const SizedBox(height: 20),
          FilledButton.icon(
            onPressed: () => Navigator.pushNamed(context, AppRouter.encounterCreate, arguments: subject.id),
            icon: const Icon(Icons.history),
            label: const Text('Add Encounter'),
          ),
        ],
      ),
    );
  }
}
