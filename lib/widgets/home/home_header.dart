import 'package:flutter/material.dart';
import '../../resources/dimen.dart';

class HomeHeader extends StatelessWidget {
  const HomeHeader({super.key});

  @override
  Widget build(BuildContext context) {
    return Container(
      height: Dimen.headerHeight,
      padding: const EdgeInsets.symmetric(horizontal: 16),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          Row(
            children: const [
              Text(
                'Para Ti',
                style: TextStyle(
                  color: Colors.white,
                  fontSize: 20,
                  fontWeight: FontWeight.bold,
                ),
              ),
              SizedBox(width: 20),
              Text(
                'Siguiendo',
                style: TextStyle(
                  color: Colors.grey,
                  fontSize: 18,
                ),
              ),
            ],
          ),
          Row(
            children: const [
              Icon(Icons.search, color: Colors.white, size: 27),
              SizedBox(width: 20),
              Icon(Icons.person_outline, color: Colors.white, size: 27),
            ],
          ),
        ],
      ),
    );
  }
}