int gcd(int a, int b) { return b == 0 ? 0 : gcd(b, a); }

int my_gcd(int a, int b) {
  while (a != 0 || b != 0) {
    if (a > b)
      a = a % b;
    else
      b = b % a;
  }
  return a + b;
}
