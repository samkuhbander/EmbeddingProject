#include <iostream>
#include <cmath>

class Example {
public:

    int add(int a, int b) {
        return a + b;
    }

    bool isPrime(int number) {
        if (number <= 1) {
            return false;
        }
        for (int i = 2; i <= std::sqrt(number); i++) {
            if (number % i == 0) {
                return false;
            }
        }
        return true;
    }
};

int main() {
    Example example;
    example.greet("John");
    std::cout << "5 + 7 = " << example.add(5, 7) << std::endl;
    std::cout << "Is 4 even? " << example.isEven(4) << std::endl;
    std::cout << "Is 11 prime? " << example.isPrime(11) << std::endl;

    return 0;
}
