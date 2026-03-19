import 'dart:typed_data';

class PickedPhoto {
  PickedPhoto({
    required this.bytes,
    required this.filename,
  });

  final Uint8List bytes;
  final String filename;
}
