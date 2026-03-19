import '../models/picked_photo.dart';
import 'photo_picker_stub.dart' if (dart.library.html) 'photo_picker_web.dart';

Future<PickedPhoto?> pickPhotoFromLibrary() => pickPhotoFromLibraryImpl();

Future<PickedPhoto?> pickPhotoFromCamera() => pickPhotoFromCameraImpl();
