import 'package:flutter/material.dart';

class EncounterScreen extends StatefulWidget {
  const EncounterScreen({super.key});

  @override
  State<EncounterScreen> createState() => _EncounterScreenState();
}

class _EncounterScreenState extends State<EncounterScreen> {
  final _summaryController = TextEditingController();

  @override
  Widget build(BuildContext context) {
    final subjectId = ModalRoute.of(context)?.settings.arguments as int?;
    return Scaffold(
      appBar: AppBar(title: const Text('Encounter Entry')),
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          children: [
            Text('Subject ID: ${subjectId ?? '-'}'),
            TextField(
              controller: _summaryController,
              maxLines: 4,
              decoration: const InputDecoration(labelText: 'Encounter Summary'),
            ),
            const SizedBox(height: 16),
            FilledButton(
              onPressed: () {
                ScaffoldMessenger.of(context).showSnackBar(
                  const SnackBar(content: Text('Encounter endpoint wiring can be added to API service.')),
                );
              },
              child: const Text('Submit'),
            ),
          ],
        ),
      ),
    );
  }
}
