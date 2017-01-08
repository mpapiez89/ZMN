#include "result.h"
#include "ui_result.h"
#include "simplex.h"

Result::Result(QString text, QMap<int, SimplexTableNamespace::SimplexTable> simplexTables, QWidget *parent) :
    QDialog(parent),
    ui(new Ui::Result)
{
    ui->setupUi(this);
    this->resultText = text;

    this->numberOfTable = simplexTables.size();
    this->currentTableNumber = 1;
    ui->leftArrow->setDisabled(true);
    ui->resultTextBox->document()->setPlainText(this->resultText);
    allSimplexTables = simplexTables;
    showTable(currentTableNumber-1);
}

Result::~Result()
{
    delete ui;
}

void Result::on_leftArrow_clicked()
{
    this->currentTableNumber--;
    ui->tableNumber->setText(QString::number(this->currentTableNumber) );

    if (this->currentTableNumber < this->numberOfTable ){
        ui->rightArrow->setEnabled(true);
    }
    if (currentTableNumber <= 1){
        ui->leftArrow->setDisabled(true);
    }
    showTable(currentTableNumber-1);
}

void Result::on_rightArrow_clicked()
{
    this->currentTableNumber++;
    ui->tableNumber->setText(QString::number(this->currentTableNumber) );
    if (this->currentTableNumber > 1){
        ui->leftArrow->setEnabled(true);
    }
    if (this->currentTableNumber == this->numberOfTable){
        ui->rightArrow->setDisabled(true);
    }
    showTable(currentTableNumber-1);
}

void Result::showTable(int tableNumber){
    prepareTable(tableNumber);

    int temp = 0;
    int numberOfBaseVar;
    for (int i=1; i<= allSimplexTables[tableNumber].vars; i++ ){
        numberOfBaseVar = allSimplexTables[tableNumber].cb.size();
        ui->table->setColumnWidth(1+i,40);
        ui->table->setItem(0,1+i,new QTableWidgetItem(QString::number(allSimplexTables[tableNumber].cj[i]) ));
        ui->table->setItem(1,1+i,new QTableWidgetItem("x"+QString::number(i)));
        ui->table->setItem(numberOfBaseVar+2,1+i,new QTableWidgetItem(QString::number(allSimplexTables[tableNumber].zj[i] )));
        ui->table->setItem(numberOfBaseVar+3,1+i,new QTableWidgetItem(QString::number(allSimplexTables[tableNumber].cj_zj[i] )));

        if (allSimplexTables[tableNumber].cb.contains(i) != false){
            ui->table->setItem(2+temp,1,new QTableWidgetItem("x"+QString::number(i)));
            ui->table->setItem(2+temp,0,new QTableWidgetItem(QString::number(allSimplexTables[tableNumber].cb[i] )));
            ui->table->setItem(2+temp, allSimplexTables[tableNumber].vars+2 ,new QTableWidgetItem(QString::number(allSimplexTables[tableNumber].result[i] )));
            for(int j=1; j<= allSimplexTables[tableNumber].vars; j++ ){
                ui->table->setItem(2+temp,1+j,new QTableWidgetItem(QString::number(allSimplexTables[tableNumber].data[i][j])));
            }
            temp++;
        }
    }
    ui->table->setItem(temp+2, allSimplexTables[tableNumber].vars+2,new QTableWidgetItem(QString::number(allSimplexTables[tableNumber].zj[allSimplexTables[tableNumber].vars+1] )));
    addColors(temp, allSimplexTables[tableNumber].vars);
    if(tableNumber == numberOfTable-1){
        ui->table->item(temp+2,allSimplexTables[tableNumber].vars+2)->setBackgroundColor(Qt::red);
    }
}

void Result::prepareTable(int tableNumber){
    ui->table->setColumnCount(3+allSimplexTables[tableNumber].vars);
    ui->table->setRowCount(4+allSimplexTables[tableNumber].cb.size());

    ui->table->setItem(1,0,new QTableWidgetItem("Cb"));
    ui->table->setItem(0,1,new QTableWidgetItem("Cj"));
    ui->table->setItem(1,1,new QTableWidgetItem("Zm. bazowe"));
    ui->table->setItem(1,2+allSimplexTables[tableNumber].vars,new QTableWidgetItem("Rozwiazanie(Bi)"));
    ui->table->setItem(2+allSimplexTables[tableNumber].cb.size(),1,new QTableWidgetItem("Zj"));
    ui->table->setItem(3+allSimplexTables[tableNumber].cb.size(),1,new QTableWidgetItem("Cj-Zj"));
    ui->table->setColumnWidth(0,40);
    ui->table->setColumnWidth(1,100);
    ui->table->setColumnWidth(2+allSimplexTables[tableNumber].vars,100);
}

void Result::addColors(int numberOfColVars, int numberOfRowsVars){
    for (int row=0; row<numberOfRowsVars+3; row++){
        ui->table->item(1,row)->setBackgroundColor(Qt::gray);
    }

    for(int col=0; col<numberOfColVars+4; col++){
        ui->table->item(col,1)->setBackgroundColor(Qt::gray);
    }
}










