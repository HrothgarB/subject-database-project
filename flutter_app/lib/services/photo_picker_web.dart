import 'dart:async';
import 'dart:html' as html;
import 'dart:typed_data';

import '../models/picked_photo.dart';

Future<PickedPhoto?> pickPhotoFromLibraryImpl() => _pickPhoto(capture: false);

Future<PickedPhoto?> pickPhotoFromCameraImpl() => _pickPhoto(capture: true);

Future<PickedPhoto?> _pickPhoto({required bool capture}) async {
  final completer = Completer<PickedPhoto?>();
  final input = html.FileUploadInputElement()..accept = 'image/*';
  if (capture) {
    input.setAttribute('capture', 'environment');
  }

  input.onChange.first.then((_) async {
    final files = input.files;
    if (files == null || files.isEmpty) {
      if (!completer.isCompleted) {
        completer.complete(null);
      }
      return;
    }

    final file = files.first;
    final reader = html.FileReader();
    reader.readAsArrayBuffer(file);
    await reader.onLoadEnd.first;

    final result = reader.result;
    if (result is ByteBuffer) {
      if (!completer.isCompleted) {
        completer.complete(
          PickedPhoto(
            bytes: Uint8List.view(result),
            filename: file.name.isNotEmpty ? file.name : 'photo.jpg',
          ),
        );
      }
      return;
    }

    if (!completer.isCompleted) {
      completer.complete(null);
    }
  }).catchError((_) {
    if (!completer.isCompleted) {
      completer.complete(null);
    }
  });

  input.click();
  return completer.future;
}
