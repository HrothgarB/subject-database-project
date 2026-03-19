import '../models/picked_photo.dart';

Future<PickedPhoto?> pickPhotoFromLibraryImpl() async {
  throw UnsupportedError('Photo picking is only available in the web preview in this build.');
}

Future<PickedPhoto?> pickPhotoFromCameraImpl() async {
  throw UnsupportedError('Camera capture is only available in the web preview in this build.');
}
