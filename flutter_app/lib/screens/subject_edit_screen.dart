import 'package:flutter/material.dart';

import '../services/local_sync_service.dart';

class SubjectEditScreen extends StatefulWidget {
  const SubjectEditScreen({super.key});

  @override
  State<SubjectEditScreen> createState() => _SubjectEditScreenState();
}

class _SubjectEditScreenState extends State<SubjectEditScreen> {
  final _formKey = GlobalKey<FormState>();
  final _firstController = TextEditingController();
  final _lastController = TextEditingController();
  final _notesController = TextEditingController();

  Future<void> _saveOffline() async {
    if (!_formKey.currentState!.validate()) return;
    await LocalSyncService.instance.enqueueCreateSubject({
      'first_name': _firstController.text.trim(),
      'last_name': _lastController.text.trim(),
      'notes': _notesController.text.trim(),
    });
    if (mounted) {
      ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text('Saved to encrypted sync queue.')));
      Navigator.pop(context);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Create Subject')),
      body: Form(
        key: _formKey,
        child: ListView(
          padding: const EdgeInsets.all(16),
          children: [
            TextFormField(
              controller: _firstController,
              decoration: const InputDecoration(labelText: 'First Name'),
              validator: (value) => (value == null || value.isEmpty) ? 'Required' : null,
            ),
            TextFormField(
              controller: _lastController,
              decoration: const InputDecoration(labelText: 'Last Name'),
              validator: (value) => (value == null || value.isEmpty) ? 'Required' : null,
            ),
            TextFormField(controller: _notesController, decoration: const InputDecoration(labelText: 'Notes')),
            const SizedBox(height: 16),
            FilledButton.icon(onPressed: _saveOffline, icon: const Icon(Icons.save), label: const Text('Queue for Sync')),
          ],
        ),
      ),
    );
  }
}
