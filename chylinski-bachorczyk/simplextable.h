#ifndef SIMPLEXTABLE_H
#define SIMPLEXTABLE_H
namespace SimplexTableNamespace {


struct SimplexTable {
    QMap<int, double> cj;
    int vars;
    QMap<int, QMap<int, double>> data;
    QMap<int, double> cb;
    QMap<int, double> result;
    QMap<int, double> zj;
    QMap<int, double> cj_zj;
};
}

#endif // SIMPLEXTABLE_H
