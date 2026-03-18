import 'package:flutter/material.dart';

import '../core/app_router.dart';
import '../models/subject_profile.dart';
import '../services/subject_api_service.dart';

class SubjectListScreen extends StatefulWidget {
  const SubjectListScreen({super.key});

  @override
  State<SubjectListScreen> createState() => _SubjectListScreenState();
}

class _SubjectListScreenState extends State<SubjectListScreen> {
  final _searchController = TextEditingController();
  late Future<List<SubjectProfile>> _future;

  @override
  void initState() {
    super.initState();
    _future = SubjectApiService.instance.fetchSubjects();
  }

  void _search() {
    setState(() {
      _future = SubjectApiService.instance.fetchSubjects(query: _searchController.text.trim());
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Subjects')),
      floatingActionButton: FloatingActionButton.extended(
        onPressed: () => Navigator.pushNamed(context, AppRouter.subjectEdit),
        label: const Text('Create'),
        icon: const Icon(Icons.add),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          children: [
            Row(
              children: [
                Expanded(
                  child: TextField(
                    controller: _searchController,
                    decoration: const InputDecoration(labelText: 'Search by name or alias'),
                  ),
                ),
                IconButton(onPressed: _search, icon: const Icon(Icons.search)),
              ],
            ),
            const SizedBox(height: 8),
            Expanded(
              child: FutureBuilder<List<SubjectProfile>>(
                future: _future,
                builder: (context, snapshot) {
                  if (!snapshot.hasData) return const Center(child: CircularProgressIndicator());
                  final items = snapshot.data!;
                  if (items.isEmpty) return const Center(child: Text('No matches'));
                  return ListView.builder(
                    itemCount: items.length,
                    itemBuilder: (context, index) {
                      final subject = items[index];
                      return Card(
                        child: ListTile(
                          title: Text('${subject.firstName} ${subject.lastName}'),
                          subtitle: Text('Case: ${subject.caseNumber ?? '-'}'),
                          onTap: () => Navigator.pushNamed(context, AppRouter.subjectDetail, arguments: subject),
                        ),
                      );
                    },
                  );
                },
              ),
            ),
          ],
        ),
      ),
    );
  }
}
