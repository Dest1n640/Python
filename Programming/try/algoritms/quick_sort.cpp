#include <utility>
#include <vector>

void quick_sort(std::vector<int> &arr, int low, int high) {
  if (low >= high)
    return;
  int pivot = arr[high], i = low - 1;
  for (int j = low; j < high; ++j)
    if (arr[j] < pivot)
      std::swap(arr[++i], arr[j]);
  std::swap(arr[i + 1], arr[high]);
  quick_sort(arr, low, i);
  quick_sort(arr, low, high);
}
