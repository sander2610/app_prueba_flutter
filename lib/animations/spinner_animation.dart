import 'package:flutter/material.dart';
import 'dart:math' as math;
import '../resources/dimen.dart';

class SpinnerAnimation extends StatefulWidget {
  final Widget body;
  
  const SpinnerAnimation({super.key, required this.body});

  @override
  SpinnerAnimationState createState() => SpinnerAnimationState();
}

class SpinnerAnimationState extends State<SpinnerAnimation>
    with SingleTickerProviderStateMixin {
  late AnimationController _controller;

  @override
  void initState() {
    super.initState();
    _controller = AnimationController(
      duration: const Duration(seconds: Dimen.five),
      vsync: this,
    )..repeat();
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return AnimatedBuilder(
      animation: _controller,
      child: widget.body,
      builder: (BuildContext context, Widget? child) {
        return Transform.rotate(
          angle: _controller.value * 2.0 * math.pi,
          child: child,
        );
      },
    );
  }
}