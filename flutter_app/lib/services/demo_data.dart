import '../models/encounter_record.dart';
import '../models/subject_profile.dart';

class DemoData {
  DemoData._();

  static final List<SubjectProfile> _subjects = <SubjectProfile>[
    SubjectProfile(
      id: 1,
      firstName: 'Avery',
      middleName: 'J',
      lastName: 'Cole',
      alias: 'Northline',
      phone: '(312) 555-0134',
      address: '1448 W Division St',
      notes: 'Known associate in a recurring property-theft investigation.',
      caseNumber: 'CASE-2048',
      intelNumber: 'INT-7781',
      restrictedSsn: '***-**-1084',
      dob: DateTime(1991, 4, 12),
    ),
    SubjectProfile(
      id: 2,
      firstName: 'Marina',
      middleName: null,
      lastName: 'Vega',
      alias: 'Blue Harbor',
      phone: '(312) 555-0192',
      address: '820 S Michigan Ave',
      notes: 'Frequent contact point for field interviews. Low confidence risk flag.',
      caseNumber: 'CASE-2210',
      intelNumber: 'INT-8823',
      restrictedSsn: '***-**-4472',
      dob: DateTime(1987, 9, 3),
    ),
    SubjectProfile(
      id: 3,
      firstName: 'Darius',
      middleName: 'K',
      lastName: 'Nguyen',
      alias: 'Signal',
      phone: '(312) 555-0177',
      address: '53 N Wells St',
      notes: 'Subject profile used for encounter workflow and offline sync preview.',
      caseNumber: 'CASE-2294',
      intelNumber: 'INT-9014',
      restrictedSsn: '***-**-2208',
      dob: DateTime(1995, 1, 28),
    ),
  ];

  static final Map<int, List<EncounterRecord>> _encounters = <int, List<EncounterRecord>>{
    1: <EncounterRecord>[
      EncounterRecord(
        id: 101,
        subjectId: 1,
        officerId: 44,
        location: 'Warehouse district',
        summary: 'Observed leaving a storage lot with two unidentified individuals.',
        encounteredAt: DateTime(2026, 2, 24, 18, 30),
      ),
      EncounterRecord(
        id: 102,
        subjectId: 1,
        officerId: 44,
        location: 'Central station lobby',
        summary: 'Voluntary interview scheduled for follow-up next week.',
        encounteredAt: DateTime(2026, 3, 4, 9, 15),
      ),
    ],
    2: <EncounterRecord>[
      EncounterRecord(
        id: 201,
        subjectId: 2,
        officerId: 19,
        location: 'South end of the transit platform',
        summary: 'Identity confirmed against internal records during a pass-through check.',
        encounteredAt: DateTime(2026, 3, 9, 13, 5),
      ),
    ],
    3: <EncounterRecord>[
      EncounterRecord(
        id: 301,
        subjectId: 3,
        officerId: 12,
        location: 'Field office',
        summary: 'Encounter entry created to demonstrate the offline-first workflow.',
        encounteredAt: DateTime(2026, 3, 12, 16, 45),
      ),
    ],
  };

  static List<SubjectProfile> get subjects => List<SubjectProfile>.unmodifiable(_subjects);

  static SubjectProfile? subjectById(int subjectId) {
    for (final subject in _subjects) {
      if (subject.id == subjectId) {
        return subject;
      }
    }
    return null;
  }

  static List<SubjectProfile> searchSubjects({
    String? query,
    String? caseNumber,
    String? intelNumber,
  }) {
    final normalizedQuery = query?.trim().toLowerCase();
    final normalizedCase = caseNumber?.trim().toLowerCase();
    final normalizedIntel = intelNumber?.trim().toLowerCase();

    return _subjects.where((subject) {
      final matchesQuery = normalizedQuery == null ||
          normalizedQuery.isEmpty ||
          [
            subject.firstName,
            subject.middleName ?? '',
            subject.lastName,
            subject.alias ?? '',
          ].any((value) => value.toLowerCase().contains(normalizedQuery));

      final matchesCase = normalizedCase == null ||
          normalizedCase.isEmpty ||
          (subject.caseNumber ?? '').toLowerCase().contains(normalizedCase);

      final matchesIntel = normalizedIntel == null ||
          normalizedIntel.isEmpty ||
          (subject.intelNumber ?? '').toLowerCase().contains(normalizedIntel);

      return matchesQuery && matchesCase && matchesIntel;
    }).toList(growable: false);
  }

  static List<EncounterRecord> encountersFor(int subjectId) =>
      List<EncounterRecord>.unmodifiable(_encounters[subjectId] ?? const <EncounterRecord>[]);

  static SubjectProfile createSubject(Map<String, dynamic> payload) {
    final nextId = _subjects.isEmpty ? 1 : _subjects.map((subject) => subject.id).reduce((a, b) => a > b ? a : b) + 1;
    final newSubject = SubjectProfile(
      id: nextId,
      firstName: payload['first_name'] as String? ?? '',
      middleName: payload['middle_name'] as String?,
      lastName: payload['last_name'] as String? ?? '',
      alias: payload['alias'] as String?,
      phone: payload['phone'] as String?,
      address: payload['address'] as String?,
      notes: payload['notes'] as String?,
      caseNumber: payload['case_number'] as String?,
      intelNumber: payload['intel_number'] as String?,
      restrictedSsn: payload['restricted_ssn'] as String?,
      dob: payload['dob'] == null ? null : DateTime.tryParse(payload['dob'] as String),
    );
    _subjects.insert(0, newSubject);
    return newSubject;
  }

  static SubjectProfile updateSubject(int subjectId, Map<String, dynamic> payload) {
    final index = _subjects.indexWhere((subject) => subject.id == subjectId);
    if (index < 0) {
      throw StateError('Subject not found');
    }

    final current = _subjects[index];
    final updated = SubjectProfile(
      id: current.id,
      firstName: payload['first_name'] as String? ?? current.firstName,
      middleName: payload['middle_name'] as String? ?? current.middleName,
      lastName: payload['last_name'] as String? ?? current.lastName,
      alias: payload['alias'] as String? ?? current.alias,
      phone: payload['phone'] as String? ?? current.phone,
      address: payload['address'] as String? ?? current.address,
      notes: payload['notes'] as String? ?? current.notes,
      caseNumber: payload['case_number'] as String? ?? current.caseNumber,
      intelNumber: payload['intel_number'] as String? ?? current.intelNumber,
      restrictedSsn: payload['restricted_ssn'] as String? ?? current.restrictedSsn,
      dob: payload['dob'] == null ? current.dob : DateTime.tryParse(payload['dob'] as String),
    );
    _subjects[index] = updated;
    return updated;
  }

  static EncounterRecord createEncounter(int subjectId, Map<String, dynamic> payload) {
    final encounters = _encounters.putIfAbsent(subjectId, () => <EncounterRecord>[]);
    final nextId = encounters.isEmpty ? subjectId * 100 + 1 : encounters.map((encounter) => encounter.id).reduce((a, b) => a > b ? a : b) + 1;
    final encounter = EncounterRecord(
      id: nextId,
      subjectId: subjectId,
      officerId: 1,
      location: payload['location'] as String?,
      summary: payload['summary'] as String? ?? '',
      encounteredAt: DateTime.tryParse(payload['encountered_at'] as String? ?? '') ?? DateTime.now(),
    );
    encounters.insert(0, encounter);
    return encounter;
  }
}
