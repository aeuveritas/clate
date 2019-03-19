#include <iostream>
#include "cpilot.hpp"

int main(int argc, char **argv) {
    auto cp1 = CPilot{1};
    CPilot cp2{2};

    std::cout << cp1.getId() << std::endl;
    std::cout << cp2.getId() << std::endl;

    return 0;
}
