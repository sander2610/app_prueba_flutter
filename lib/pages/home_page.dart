import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../providers/video_provider.dart';
import '../widgets/home/home_video_renderer.dart';

class HomePage extends StatefulWidget {
  const HomePage({super.key});

  @override
  State<HomePage> createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  late PageController _pageController;
  int _currentPage = 0;

  @override
  void initState() {
    super.initState();
    _pageController = PageController();
    // Cargar videos al iniciar
    WidgetsBinding.instance.addPostFrameCallback((_) {
      context.read<VideoProvider>().loadVideos();
    });
  }

  @override
  void dispose() {
    _pageController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final videoProvider = context.watch<VideoProvider>();
    
    if (videoProvider.isLoading && videoProvider.videos.isEmpty) {
      return const Scaffold(
        body: Center(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              CircularProgressIndicator(),
              SizedBox(height: 20),
              Text(
                'Cargando videos...',
                style: TextStyle(color: Colors.white),
              ),
            ],
          ),
        ),
      );
    }
    
    if (videoProvider.error != null) {
      return Scaffold(
        body: Center(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              const Icon(Icons.error_outline, color: Colors.red, size: 60),
              const SizedBox(height: 20),
              Text(
                'Error: ${videoProvider.error}',
                style: const TextStyle(color: Colors.white),
                textAlign: TextAlign.center,
              ),
              const SizedBox(height: 20),
              ElevatedButton(
                onPressed: () => videoProvider.refreshVideos(),
                child: const Text('Reintentar'),
              ),
            ],
          ),
        ),
      );
    }
    
    if (videoProvider.videos.isEmpty) {
      return const Scaffold(
        body: Center(
          child: Text(
            'No hay videos disponibles',
            style: TextStyle(color: Colors.white),
          ),
        ),
      );
    }
    
    return Scaffold(
      body: Stack(
        children: [
          PageView.builder(
            controller: _pageController,
            scrollDirection: Axis.vertical,
            itemCount: videoProvider.videos.length,
            onPageChanged: (int page) {
              setState(() {
                _currentPage = page;
              });
            },
            itemBuilder: (context, index) {
              final video = videoProvider.videos[index];
              return HomeVideoRenderer(
                videoData: video,
                isActive: _currentPage == index,
                onLikePressed: () {
                  videoProvider.toggleLike(video.id, index);
                },
              );
            },
          ),
          _buildHeader(),
        ],
      ),
    );
  }

  Widget _buildHeader() {
    return Positioned(
      top: 40,
      left: 0,
      right: 0,
      child: Padding(
        padding: const EdgeInsets.symmetric(horizontal: 16),
        child: Row(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            Row(
              children: [
                const Text(
                  'Para Ti',
                  style: TextStyle(
                    color: Colors.white,
                    fontSize: 20,
                    fontWeight: FontWeight.bold,
                  ),
                ),
                const SizedBox(width: 20),
                Text(
                  'Siguiendo',
                  style: TextStyle(
                    color: Colors.grey[400],
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
      ),
    );
  }
}