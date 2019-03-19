#ifndef __CPILOT_HPP__
#define __CPILOT_HPP__

class CPilot
{
public:
    CPilot(int id);
    ~CPilot();

    int getId();

private:
    int id_;
};

#endif
