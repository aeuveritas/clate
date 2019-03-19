#include <iostream>
#include "cpilot.hpp"

CPilot::CPilot(int id)
: id_{id}
{
    std::cout << "construct CPilot" << std::endl;
}

CPilot::~CPilot()
{
    std::cout << "destruct CPilot" << std::endl;
}

int CPilot::getId()
{
    return id_;
}

