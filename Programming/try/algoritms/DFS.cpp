#include <vector>

// 5. Поиск в глубину (DFS) для графа
void dfs(int v, std::vector<std::vector<int>> &adj,
         std::vector<bool> &visited) {
  // Отмечаем вершину как посещенную
  visited[v] = true;
  // Проходим по всем смежным вершинам
  for (int u : adj[v]) {
    // Если вершина еще не посещена — рекурсивно спускаемся
    if (!visited[u])
      dfs(u, adj, visited);
  }
}
