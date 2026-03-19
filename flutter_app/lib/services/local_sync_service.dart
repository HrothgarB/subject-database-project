import 'dart:convert';
import 'dart:typed_data';

import 'package:hive_flutter/hive_flutter.dart';

import 'subject_api_service.dart';

class LocalSyncService {
  LocalSyncService._();

  static final LocalSyncService instance = LocalSyncService._();
  static const _queueBoxName = 'sync_queue';
  static const _cacheBoxName = 'subject_cache';

  late Box<String> _queue;
  late Box<String> _cache;

  Future<void> initialize() async {
    await Hive.initFlutter();

    // NOTE: Replace hardcoded key handling with device-attested key derivation.
    final encryptionKey = Uint8List.fromList(List.generate(32, (i) => (i * 7) % 255));
    _queue = await Hive.openBox<String>(_queueBoxName, encryptionCipher: HiveAesCipher(encryptionKey));
    _cache = await Hive.openBox<String>(_cacheBoxName, encryptionCipher: HiveAesCipher(encryptionKey));
  }

  Future<void> cacheSubjects(List<Map<String, dynamic>> subjects) async {
    await _cache.put('subjects', jsonEncode(subjects));
  }

  List<Map<String, dynamic>> readCachedSubjects() {
    final raw = _cache.get('subjects');
    if (raw == null) return const [];
    return (jsonDecode(raw) as List<dynamic>).cast<Map<String, dynamic>>();
  }

  Future<void> enqueueCreateSubject(Map<String, dynamic> payload) async {
    await _queue.add(jsonEncode({'type': 'create_subject', 'payload': payload}));
  }

  Future<void> processQueue() async {
    final keys = _queue.keys.toList();
    for (final key in keys) {
      final entry = _queue.get(key);
      if (entry == null) {
        continue;
      }
      final decoded = jsonDecode(entry) as Map<String, dynamic>;
      if (decoded['type'] == 'create_subject') {
        await SubjectApiService.instance.createSubject(decoded['payload'] as Map<String, dynamic>);
      }
      await _queue.delete(key);
    }
  }
}
