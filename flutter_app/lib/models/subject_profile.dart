class SubjectProfile {
  SubjectProfile({
    required this.id,
    required this.firstName,
    required this.lastName,
    this.middleName,
    this.alias,
    this.phone,
    this.address,
    this.notes,
    this.caseNumber,
    this.intelNumber,
    this.dob,
  });

  final int id;
  final String firstName;
  final String? middleName;
  final String lastName;
  final String? alias;
  final String? phone;
  final String? address;
  final String? notes;
  final String? caseNumber;
  final String? intelNumber;
  final DateTime? dob;

  factory SubjectProfile.fromJson(Map<String, dynamic> json) => SubjectProfile(
        id: json['id'] as int,
        firstName: json['first_name'] as String,
        middleName: json['middle_name'] as String?,
        lastName: json['last_name'] as String,
        alias: json['alias'] as String?,
        phone: json['phone'] as String?,
        address: json['address'] as String?,
        notes: json['notes'] as String?,
        caseNumber: json['case_number'] as String?,
        intelNumber: json['intel_number'] as String?,
        dob: json['dob'] != null ? DateTime.parse(json['dob'] as String) : null,
      );

  Map<String, dynamic> toJson() => {
        'id': id,
        'first_name': firstName,
        'middle_name': middleName,
        'last_name': lastName,
        'alias': alias,
        'phone': phone,
        'address': address,
        'notes': notes,
        'case_number': caseNumber,
        'intel_number': intelNumber,
        'dob': dob?.toIso8601String(),
      };
}
