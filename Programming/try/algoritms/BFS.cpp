#include <queue>
#include <vector>
// 6. Поиск в ширину (BFS) для графа
void bfs(int start, std::vector<std::vector<int>> &adj) {
  std::queue<int> q;                            // Очередь вершин
  std::vector<bool> visited(adj.size(), false); // Массив посещенных
  visited[start] = true;                        // Отмечаем стартовую вершину
  q.push(start);                                // Добавляем ее в очередь
  // Пока очередь не пуста
  while (!q.empty()) {
    int v = q.front();
    q.pop();               // Берем следующий элемент
    for (int u : adj[v]) { // Для каждой смежной вершины
      if (!visited[u]) {   // Если не посещена
        visited[u] = true; // Отмечаем
        q.push(u);         // И добавляем в очередь
      }
    }
  }
}
