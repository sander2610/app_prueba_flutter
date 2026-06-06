// FlutterFix UI Framework - Proyecto Individual
// Sociedad: FlutterFix
// Objetivo: Framework de UI autónomo con IA

import 'package:flutter/material.dart';

void main() {
  runApp(FlutterFixApp());
}

class FlutterFixApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'FlutterFix UI Framework',
      theme: ThemeData.dark(),
      home: FlutterFixHome(),
    );
  }
}

class FlutterFixHome extends StatefulWidget {
  @override
  _FlutterFixHomeState createState() => _FlutterFixHomeState();
}

class _FlutterFixHomeState extends State<FlutterFixHome> {
  List<Widget> componentes = [];
  int contador = 0;

  void agregarComponente() {
    setState(() {
      componentes.add(
        Card(
          child: ListTile(
            title: Text('Componente ${componentes.length + 1}'),
            subtitle: Text('Generado por IA autónoma'),
            leading: Icon(Icons.widgets, color: Colors.blue),
          ),
        )
      );
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('FlutterFix UI Framework v1.0'),
        backgroundColor: Colors.deepPurple,
      ),
      body: Column(
        children: [
          Container(
            padding: EdgeInsets.all(20),
            color: Colors.deepPurple[50],
            child: Column(
              children: [
                Text(
                  'Framework de UI Autónomo',
                  style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
                ),
                SizedBox(height: 10),
                Text(
                  'Componentes generados: ${componentes.length}',
                  style: TextStyle(fontSize: 18),
                ),
                SizedBox(height: 10),
                ElevatedButton.icon(
                  onPressed: agregarComponente,
                  icon: Icon(Icons.add),
                  label: Text('Generar Componente IA'),
                  style: ElevatedButton.styleFrom(
                    backgroundColor: Colors.deepPurple,
                    padding: EdgeInsets.symmetric(horizontal: 30, vertical: 15),
                  ),
                ),
              ],
            ),
          ),
          Expanded(
            child: ListView.builder(
              itemCount: componentes.length,
              itemBuilder: (context, index) => componentes[index],
            ),
          ),
        ],
      ),
    );
  }
}
