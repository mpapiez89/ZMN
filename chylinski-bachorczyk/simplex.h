#ifndef SIMPLEX_H
#define SIMPLEX_H

#include "result.h"
#include "simplextable.h"
#include <QMainWindow>
#include <QDebug>
#include <QMessageBox>
#include <QVector>


namespace Ui {
class simplex;

}

class simplex : public QMainWindow
{
    Q_OBJECT

public:
    explicit simplex(QWidget *parent = 0);
    ~simplex();

    struct Inequality {
        double result;
        bool greaterThan;
        QMap<int, double> varsData;
    };

//    struct SimplexTable {
//        QMap<int, double> cj;
//        int vars;
//        QMap<int, QMap<int, double>> data;
//        QMap<int, double> cb;
//        QMap<int, double> result;
//        QMap<int, double> zj;
//        QMap<int, double> cj_zj;
//    };

signals:
    void showResultSignal();

private slots:
    void on_calculateButton_clicked();

    void on_maxRadio_clicked();

    void on_minRadio_clicked();

private:
    Ui::simplex *ui;
    QMap<int, double> getValuesFromString(QString text);
    QString clearString(QString text);
    QStringList splitString (QString text);
    QMap<int, double> convertListToMap (QStringList splitedText);
    void showError(QString text);
    QVector<simplex::Inequality> getInequalities(QString text);
    QString getResult(QMap<int, double> functionData, QVector<Inequality> inequalities);
    bool validateInputs(QMap<int, double> functionData, QVector<Inequality> inequalities);
    SimplexTableNamespace::SimplexTable createSimplexTable(QMap<int, double> functionData, QVector<Inequality> inequalities);
    void setOptimalityIndicator(SimplexTableNamespace::SimplexTable* table);
    QMap<int, SimplexTableNamespace::SimplexTable> getAllSimplexTables(SimplexTableNamespace::SimplexTable* table);
    bool checkOptimality(SimplexTableNamespace::SimplexTable* table);
    void calculateSimplexTable(SimplexTableNamespace::SimplexTable* table);
    int switchOutputVarWithInputVar(SimplexTableNamespace::SimplexTable* table);
    void updateSimplexTable(SimplexTableNamespace::SimplexTable* table, int switchIndex);

    void showResults(QString resultText, QMap<int, SimplexTableNamespace::SimplexTable> allTables);


    bool maximalizeFunc;
};

#endif // SIMPLEX_H
