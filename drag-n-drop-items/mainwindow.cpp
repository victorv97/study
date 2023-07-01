#include "mainwindow.h"
#include "ui_mainwindow.h"
#include <QDebug>
#include <QFileDialog>


MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
    , ui(new Ui::MainWindow)
{
    ui->setupUi(this);
    connect(ui->save, SIGNAL(triggered()), this, SLOT(saveClick()));
    connect(ui->load, SIGNAL(triggered()), this, SLOT(loadClick()));

}

MainWindow::~MainWindow()
{
    delete ui;
}

void MainWindow::create()
{
    my_widget.create();
    setCentralWidget(&my_widget);
}

void MainWindow::saveClick()
{
    qDebug()<<"Save";
    QString filename = QFileDialog::getSaveFileName(this, "Save data to file", my_filename, "(*.txt)");
    if (filename.isEmpty())
        return;
    qDebug()<<"filename"<<filename;
    QFile file(filename);
    if (file.open(QIODevice::WriteOnly)) {


        QTextStream stream(&file);
        QVector<DataTable> data = my_widget.getDataTable();
        for (int i = 0; i< data.size(); i++){
        qDebug()<<"save"<< data[i].id<<";"
                    << data[i].count<<";"
                    << data[i].row<<";"
                    << data[i].col;
        stream << data[i].id<<";"
               << data[i].count<<";"
               << data[i].row<<";"
               << data[i].col<<"\n";
                }
        file.close();
    } else
        qDebug()<<"Can't open file"<<filename;
}

void MainWindow::loadClick()
{
    qDebug()<<"Load";
    QString filename = QFileDialog::getOpenFileName(this, "Load data from file", my_filename, "(*.txt)");
    if (filename.isEmpty())
        return;
    qDebug()<<"filename"<<filename;
    QFile file(filename);
    QVector<DataTable> data;

    if (file.open(QIODevice::ReadOnly)) {
        while(!file.atEnd()) {
            QString line = QString::fromUtf8(file.readLine());
            qDebug()<<"line = "<< line;
            QStringList tokens = line.split(";");
            auto tokenVektor = tokens.toVector();
            if (tokenVektor.size() != 4) {
                qDebug()<<"error = "<<tokenVektor.size();
                continue;
            }
            DataTable dataTable;
            dataTable.id = tokenVektor[0].toInt();
            dataTable.count = tokenVektor[1].toInt();
            dataTable.row = tokenVektor[2].toInt();
            dataTable.col = tokenVektor[3].toInt();
            data.push_back(dataTable);
        }
        file.close();
    }
    my_widget.setDataTable(data);


}

