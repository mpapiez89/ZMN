#ifndef RESULT_H
#define RESULT_H

#include <QDialog>
#include <QDebug>
#include "simplex.h"
#include "simplexTable.h"

namespace Ui {
class Result;
}

class Result : public QDialog
{
    Q_OBJECT

public:
    explicit Result(QString resultText="",
                    QMap<int, SimplexTableNamespace::SimplexTable> allSimplexTables = QMap<int, SimplexTableNamespace::SimplexTable>(),
                    QWidget *parent = 0);
    ~Result();
    void showResult();
    void showTable(int tableNumber);

    QMap<int, SimplexTableNamespace::SimplexTable> allSimplexTables;

private slots:


    void on_leftArrow_clicked();

    void on_rightArrow_clicked();


private:
    QString resultText;
    Ui::Result *ui;
    int numberOfTable;
    int currentTableNumber;
    void prepareTable(int tableNumber);
    void addColors(int numberOfColVars, int numberOfRowsVars);

};

#endif // RESULT_H
