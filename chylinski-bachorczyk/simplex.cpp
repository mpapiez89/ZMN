#include "simplex.h"
#include "ui_simplex.h"
#include "result.h"

simplex::simplex(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::simplex)
{
    ui->setupUi(this);

    this->maximalizeFunc = true;
}

simplex::~simplex()
{
    delete ui;
}

void simplex::on_calculateButton_clicked()
{
//    connect(calculateButton, SIGNAL( showResultSignal() ), SLOT( showResultSlot() ) );
    QMap<int, double> functionData;
    QVector<Inequality> inequalities;

    functionData = getValuesFromString(ui->lineEdit ->text());
    inequalities = getInequalities(ui->inequalitiesText->toPlainText());
    QString result = getResult(functionData, inequalities);
    qDebug() << "\n\nRESULT: ";
    qDebug() << result;

}

void simplex::showResults(QString resultText, QMap<int, SimplexTableNamespace::SimplexTable>allTables){
    Result *result = new Result(resultText, allTables, this);

    result ->show();
}

void simplex::on_maxRadio_clicked()
{
    this->maximalizeFunc = true;
}

void simplex::on_minRadio_clicked()
{
    this->maximalizeFunc = false;
}

QString simplex::getResult(QMap<int, double> functionData, QVector<Inequality> inequalities){
    if (functionData.empty() || inequalities.empty()) return "";

    if(!validateInputs(functionData, inequalities)){
        showError("Variables names must start from 1 and be a continuous numbers!");
        return "zle inputy";
    }

    if(!this->maximalizeFunc){
        foreach (int key, functionData.keys()) {
            functionData[key] *= -1.0;
        }
    }

    //create simplex table
    SimplexTableNamespace::SimplexTable table = createSimplexTable(functionData, inequalities);
    setOptimalityIndicator(&table);

    QMap<int, SimplexTableNamespace::SimplexTable> allTables = getAllSimplexTables(&table);

    if (allTables.empty()){
        return "Couldn't find the result.";
    }

    QString result;
    for (int i = 1; i <= table.vars; i++) {
        if (!table.result.contains(i)){
            continue;
        }
        result.append("x(");
        result.append(QString::number(i));
        result.append(") = ");
        result.append(QString::number(table.result[i]));
        result.append("    ");
    }
    showResults(result, allTables);
    return result;    
}

bool simplex::validateInputs(QMap<int, double> functionData, QVector<Inequality> inequalities){
    QList<int> funcKeys = functionData.keys();

    for (int i = 1; i <= funcKeys.size(); i++) {
        if (!funcKeys.contains(i)){
            return false;
        }
    }

    foreach (Inequality ineq, inequalities) {
        foreach (int key, ineq.varsData.keys()) {
            //qDebug() << key;
            if (!funcKeys.contains(key)){
                return false;
            }
        }
    }

    return true;
}

SimplexTableNamespace::SimplexTable simplex::createSimplexTable(QMap<int, double> functionData, QVector<Inequality> inequalities){
    SimplexTableNamespace::SimplexTable table;
    table.vars = functionData.size() + inequalities.size(); //przyjalem ze ile jest nierownosci tyle jest zmiennych dodatkowych

    for (int i = 1; i <= table.vars; i++) {
        if (i <= functionData.size()){
            table.cj[i] = functionData[i];
        } else {
            table.cj[i] = 0;
            table.cb[i] = 0;
            table.result[i] = inequalities[i-functionData.size()-1].result;
            for (int varId = 1; varId <= table.vars; varId++) {
                double tmp = 0;
                if(i == varId) tmp = 1;
                if (inequalities[i-functionData.size()-1].varsData.contains(varId)){
                    tmp = inequalities[i-functionData.size()-1].varsData[varId];
                }
                table.data[i][varId] = tmp;
            }
        }
    }

    return table;
}

void simplex::setOptimalityIndicator(SimplexTableNamespace::SimplexTable* table){
    for (int varId = 1; varId <= table->vars + 1; varId++) { // +1 do obliczenia zj dla result
        double tmp = 0;
        for (int cbId = 1; cbId <= table->vars; cbId++) {
            if (!table->cb.contains(cbId)){
                continue;
            }
            if (varId == (table->vars+1)){
                tmp += table->result[cbId] * table->cb[cbId];
                continue;
            }
            tmp += table->data[cbId][varId] * table->cb[cbId];
        }
        table->zj[varId] = tmp;

        if (varId != (table->vars+1)){
            table->cj_zj[varId] = table->cj[varId] - table->zj[varId];
        }
    }
}

QMap<int, SimplexTableNamespace::SimplexTable> simplex::getAllSimplexTables(SimplexTableNamespace::SimplexTable* table){
    QMap<int, SimplexTableNamespace::SimplexTable> tables;
    tables[0] = *table;

    int i = 1;
    while (!checkOptimality(table)){
        if (tables.size() >= 100){
            showError("Function is not convergent!");
            return QMap<int, SimplexTableNamespace::SimplexTable>();
        }
        calculateSimplexTable(table);
        tables[i] = *table;
        i++;
    }

    return tables;
}

bool simplex::checkOptimality(SimplexTableNamespace::SimplexTable* table){
    foreach (double cj_zj, table->cj_zj) {
        if (cj_zj > 0){
            return false;
        }
    }

    return true;
}

void simplex::calculateSimplexTable(SimplexTableNamespace::SimplexTable* table){
    int switchIndex = switchOutputVarWithInputVar(table);
    updateSimplexTable(table, switchIndex);
    setOptimalityIndicator(table);

}

void simplex::updateSimplexTable(SimplexTableNamespace::SimplexTable* table, int switchIndex){
    double tmp = table->data[switchIndex][switchIndex];
    for (int varId = 1; varId <= table->vars; varId++) {
        table->data[switchIndex][varId] = table->data[switchIndex][varId] / tmp;
    }
    table->result[switchIndex] = table->result[switchIndex] / tmp;

    for (int cbId = 1; cbId <= table->vars + 1; cbId++) { // +1 do obliczenia zj dla result
        if (!table->cb.contains(cbId) || cbId == switchIndex){
            continue;
        }
        tmp = table->data[cbId][switchIndex];
        for (int varId = 1; varId <= table->vars; varId++) {
            table->data[cbId][varId] = table->data[cbId][varId] - (table->data[switchIndex][varId] * tmp);
        }
        table->result[cbId] = table->result[cbId] - (table->result[switchIndex] * tmp);
        //qDebug() << table->result[cbId];
    }
}

int simplex::switchOutputVarWithInputVar(SimplexTableNamespace::SimplexTable* table){
    int maxIndex = 1;
    double maxValue = table->cj_zj[1];

    for(int i=2; i <= table->vars; i++){
        if (table->cj_zj[i] > maxValue){
            maxIndex = i;
            maxValue = table->cj_zj[i];
        }
    }

    int minIndex;
    double minValue = INFINITY;
    for (int cbId = 1; cbId <= table->vars; cbId++) {
        if (!table->cb.contains(cbId)){
            continue;
        }

        double tmp = table->result[cbId] / table->data[cbId][maxIndex];

        if (tmp < minValue && tmp >= 0){
            minValue = tmp;
            minIndex = cbId;
        }
    }

    table->cb[maxIndex] = table->cj[maxIndex];
    table->result[maxIndex] = table->result[minIndex];
    for (int varId = 1; varId <= table->vars; varId++) {
        table->data[maxIndex][varId] = table->data[minIndex][varId];
    }
    table->data.remove(minIndex);
    table->cb.remove(minIndex);
    table->result.remove(minIndex);

    return maxIndex;
}

QMap<int, double> simplex::getValuesFromString(QString text){
    QString clearText = clearString(text); // remove spaces, * and make ,=>.
    QStringList splitedText = splitString(clearText);
    return convertListToMap(splitedText);
    //qDebug() << splitedText;
}

QString simplex::clearString(QString text){
    text = text.simplified();
    text.replace( " ", "" );
    text.replace( "*", "" );
    text.replace( ",", "." );
    text.replace( "X", "x" );
    return text;
}

QStringList simplex::splitString(QString text){
    text.replace("-", "+-");
    if (text[0] == '+'){
       text = text.remove(0,1);
    }
    QRegExp rx("\\+");
    QStringList splitedString = text.split(rx);

    return splitedString;
}

void simplex::showError(QString text){
    QMessageBox error;
    error.setText(text);
    error.exec();
}

QMap<int, double> simplex::convertListToMap(QStringList splitedText){
    QRegExp xFactorRx("^\\-?[0-9]+(\\.[0-9]+){0,1}$");
    QRegExp xNameRx("^\\([0-9]+\\)$");
    QMap<int, double> map;

    foreach(QString el, splitedText){
        QStringList splitOnX = el.split("x");       
        if (splitOnX[0] == "-"){
            splitOnX[0] = "-1";
        } else if (splitOnX[0] == ""){
            splitOnX[0] = "1";
        }
        if (splitOnX.length() != 2 ||
            splitOnX[0].contains(xFactorRx) == false ||
            splitOnX[1].contains(xNameRx) == false){
            showError("Ooops, something went wrong. Please correct your functions.");

            return QMap<int, double>();
        } else{ // zwalidowane, baby!
            splitOnX[1].replace("(", "");
            splitOnX[1].replace(")", "");
//            qDebug() << "good!";
        }

        if (map.count(splitOnX[1].toDouble()) == 1){ //wywala pikny blad jak wpisze sie dwa takie same numerki x
            showError("Ooops, something went wrong. Please correct your functions. (variables can't repeat)");
            return QMap<int, double>();
        }

        //qDebug() <<splitOnX[0];
        //qDebug() <<splitOnX[0];

        map[splitOnX[1].toDouble()] = splitOnX[0].toDouble();
    }
    return map;
}

QVector<simplex::Inequality> simplex::getInequalities(QString text){
    QRegExp resultRx("^[0-9]+$");
    QStringList rows = text.split("\n");
    QVector<Inequality> inequalities;

    foreach(QString row, rows){
        Inequality item;
        row = clearString(row);
        QStringList splitOnSign = row.split(">=");
        item.greaterThan = true;
        if (splitOnSign.length() < 2){
            splitOnSign = row.split("<=");
            item.greaterThan = false;
        }
        if (!splitOnSign[1].contains(resultRx)){
            showError("Inequalities are not set correctly!");
            return QVector<simplex::Inequality>();
        }
        item.result = splitOnSign[1].toDouble();

        item.varsData = getValuesFromString(splitOnSign[0]);
        if(item.greaterThan){
            item.result *= -1;
            foreach (int key, item.varsData.keys()) {
                item.varsData[key] *= -1;
            }
        }

        inequalities.push_back(item);
    }

    return inequalities;
}
