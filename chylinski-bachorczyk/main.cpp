#include "simplex.h"
#include <QApplication>

int main(int argc, char *argv[])
{
    QApplication a(argc, argv);
    simplex w;
    w.show();

    return a.exec();
}
