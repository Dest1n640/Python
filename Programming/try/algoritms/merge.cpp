#include <vector>
// 4. Сортировка слиянием (Merge Sort)
// Слияние двух отсортированных частей
void merge(std::vector<int> &arr, int l, int m, int r) {
  // Создаем временные векторы для левой и правой частей
  std::vector<int> L(arr.begin() + l, arr.begin() + m + 1);
  std::vector<int> R(arr.begin() + m + 1, arr.begin() + r + 1);
  int i = 0, j = 0; // указатели для L и R
  int k = l;        // указатель для результирующего массива
  // Пока обе части не закончились
  while (i < L.size() && j < R.size())
    // Берем меньший элемент и добавляем в arr
    arr[k++] = (L[i] < R[j]) ? L[i++] : R[j++];
  // Копируем оставшиеся элементы левой части
  while (i < L.size())
    arr[k++] = L[i++];
  // Копируем оставшиеся элементы правой части
  while (j < R.size())
    arr[k++] = R[j++];
}

void mergeSort(std::vector<int> &arr, int l, int r) {
  // Если диапазон состоит из одного элемента — выход
  if (l >= r)
    return;
  // Ищем середину
  int m = (l + r) / 2;
  // Сортируем левую половину
  mergeSort(arr, l, m);
  // Сортируем правую половину
  mergeSort(arr, m + 1, r);
  // Сливаем отсортированные части
  merge(arr, l, m, r);
}
