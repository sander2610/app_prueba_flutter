import 'package:flutter/material.dart';
import 'package:tiktok_flutter/resources/assets.dart';
import 'package:tiktok_flutter/resources/dimen.dart';
import 'pages/home_page.dart';

class BottomNavigation extends StatefulWidget {
  @override
  State<StatefulWidget> createState() => _BottomNavigation();
}

class _BottomNavigation extends State<BottomNavigation> {
  int _currentIndex = 0;
  
  final List<Widget> _pages = [
    const HomePage(),
    const Center(child: Text('Discover', style: TextStyle(color: Colors.white))),
    const Center(child: Text('Create', style: TextStyle(color: Colors.white))),
    const Center(child: Text('Inbox', style: TextStyle(color: Colors.white))),
    const Center(child: Text('Profile', style: TextStyle(color: Colors.white))),
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: _pages[_currentIndex],
      bottomNavigationBar: Column(
        mainAxisSize: MainAxisSize.min,
        children: <Widget>[
          Divider(
            height: 2,
            color: Colors.grey[700],
          ),
          Container(
            height: 60,
            color: Colors.transparent,
            child: Padding(
              padding: const EdgeInsets.only(top: 7),
              child: Row(
                crossAxisAlignment: CrossAxisAlignment.center,
                mainAxisSize: MainAxisSize.max,
                mainAxisAlignment: MainAxisAlignment.center,
                children: <Widget>[
                  _buildNavItem(
                    icon: AppIcons.home,
                    label: "Home",
                    index: 0,
                  ),
                  _buildNavItem(
                    icon: AppIcons.search,
                    label: "Discover",
                    index: 1,
                  ),
                  _buildCreateButton(),
                  _buildNavItem(
                    icon: AppIcons.messages,
                    label: "Inbox",
                    index: 3,
                  ),
                  _buildNavItem(
                    icon: AppIcons.profile,
                    label: "Me",
                    index: 4,
                  ),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }
  
  Widget _buildNavItem({
    required IconData icon,
    required String label,
    required int index,
  }) {
    return Expanded(
      flex: 1,
      child: GestureDetector(
        onTap: () {
          setState(() {
            _currentIndex = index;
          });
        },
        child: Column(
          children: <Widget>[
            Icon(
              icon,
              color: _currentIndex == index ? Colors.white : Colors.grey[500],
              size: Dimen.iconSize,
            ),
            Padding(
              padding: EdgeInsets.only(top: Dimen.textSpacing),
              child: Text(
                label,
                style: TextStyle(
                  fontSize: Dimen.bottomNavigationTextSize,
                  color: _currentIndex == index ? Colors.white : Colors.grey[500],
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
  
  Widget _buildCreateButton() {
    return Expanded(
      flex: 1,
      child: GestureDetector(
        onTap: () {
          setState(() {
            _currentIndex = 2;
          });
        },
        child: Column(
          children: <Widget>[
            Container(
              width: 45.0,
              height: 32.0,
              child: Stack(children: [
                Container(
                  margin: const EdgeInsets.only(left: 10.0),
                  width: 100,
                  decoration: BoxDecoration(
                    color: const Color.fromARGB(255, 250, 45, 108),
                    borderRadius: BorderRadius.circular(Dimen.createButtonBorder),
                  ),
                ),
                Container(
                  margin: const EdgeInsets.only(right: 10.0),
                  width: 200,
                  decoration: BoxDecoration(
                    color: const Color.fromARGB(255, 32, 211, 234),
                    borderRadius: BorderRadius.circular(Dimen.createButtonBorder),
                  ),
                ),
                Center(
                  child: Container(
                    height: double.infinity,
                    width: 38,
                    decoration: BoxDecoration(
                      color: Colors.white,
                      borderRadius: BorderRadius.circular(Dimen.createButtonBorder),
                    ),
                    child: const Icon(
                      Icons.add,
                      size: 20.0,
                    ),
                  ),
                ),
              ]),
            ),
          ],
        ),
      ),
    );
  }
}
