import 'package:flutter/material.dart';

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'App Prueba Flutter',
      home: HomeScreen(),
    );
  }
}

class HomeScreen extends StatefulWidget {
  @override
  _HomeScreenState createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  List<String> items = [];
  String? nullableText;
  
  // BUG 1: Null check operator en variable nullable
  String getText() {
    return nullableText!;  // ¡Esto lanza error si nullableText es null!
  }
  
  // BUG 2: Acceso a índice fuera de rango
  String getItem(int index) {
    return items[index];  // ¡Esto lanza RangeError si index >= items.length!
  }
  
  // BUG 3: setState después de dispose (simulado)
  @override
  void initState() {
    super.initState();
    Future.delayed(Duration(seconds: 5), () {
      // Si el widget ya no existe, esto causa error
      if (mounted) {
        setState(() {
          items.add("Nuevo item");
        });
      }
    });
  }
  
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('App de Prueba con Bugs'),
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Text('Items cargados: ${items.length}'),
            SizedBox(height: 20),
            ElevatedButton(
              onPressed: () {
                // BUG 4: Acceder a índice 0 cuando la lista está vacía
                final primerItem = getItem(0);
                ScaffoldMessenger.of(context).showSnackBar(
                  SnackBar(content: Text('Primer item: $primerItem')),
                );
              },
              child: Text('Mostrar primer item'),
            ),
            ElevatedButton(
              onPressed: () {
                // BUG 5: Llamar a getText() cuando nullableText es null
                final texto = getText();
                ScaffoldMessenger.of(context).showSnackBar(
                  SnackBar(content: Text('Texto: $texto')),
                );
              },
              child: Text('Mostrar texto nullable'),
            ),
          ],
        ),
      ),
    );
  }
}
