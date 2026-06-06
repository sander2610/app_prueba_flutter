import 'package:flutter/material.dart';

LinearGradient get audioDiscGradient => LinearGradient(
  colors: [
    Colors.grey[800]!,
    Colors.grey[900]!,
    Colors.grey[900]!,
    Colors.grey[800]!
  ], 
  stops: const [
    0.0,
    0.4,
    0.6,
    1.0
  ], 
  begin: Alignment.bottomLeft, 
  end: Alignment.topRight
);

Widget audioSpinner() {
  return Container(
    width: 50.0,
    height: 50.0,
    decoration: BoxDecoration(
      gradient: audioDiscGradient,
      shape: BoxShape.circle,
      image: const DecorationImage(
        image: AssetImage("assets/images/avatar.png"),
        fit: BoxFit.cover,
      ),
    ),
  );
}

// Versión mejorada con borde y animación
class AudioSpinnerIcon extends StatelessWidget {
  final double size;
  final String? imageUrl;
  
  const AudioSpinnerIcon({super.key, this.size = 50, this.imageUrl});

  @override
  Widget build(BuildContext context) {
    return Container(
      width: size,
      height: size,
      decoration: BoxDecoration(
        gradient: audioDiscGradient,
        shape: BoxShape.circle,
        border: Border.all(color: Colors.white, width: 2),
        image: imageUrl != null 
          ? DecorationImage(
              image: NetworkImage(imageUrl!),
              fit: BoxFit.cover,
            )
          : const DecorationImage(
              image: AssetImage("assets/images/avatar.png"),
              fit: BoxFit.cover,
            ),
      ),
    );
  }
}