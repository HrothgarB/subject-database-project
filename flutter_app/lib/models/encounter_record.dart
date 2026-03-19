class EncounterRecord {
  EncounterRecord({
    required this.id,
    required this.subjectId,
    required this.officerId,
    required this.summary,
    required this.encounteredAt,
    this.location,
  });

  final int id;
  final int subjectId;
  final int officerId;
  final String? location;
  final String summary;
  final DateTime encounteredAt;

  factory EncounterRecord.fromJson(Map<String, dynamic> json) => EncounterRecord(
        id: json['id'] as int,
        subjectId: json['subject_id'] as int,
        officerId: json['officer_id'] as int,
        location: json['location'] as String?,
        summary: json['summary'] as String,
        encounteredAt: DateTime.parse(json['encountered_at'] as String),
      );
}
