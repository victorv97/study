#include "gamewidget.h"
#include "ui_gamewidget.h"
#include <QDebug>
gameWidget::gameWidget(QWidget *parent) :
    QWidget(parent),
    ui(new Ui::gameWidget)
{
    ui->setupUi(this);
}

gameWidget::~gameWidget()
{
    delete ui;
}

void gameWidget::create()
{

    ui->horizontalLayout_2->addWidget(&m_table);
//    ui->horizontalLayout_2->setSizeConstraint(QLayout::SetMinimumSize);
//    ui->verticalLayout;
    my_sub1.create(75, 75);
    my_sub1.setID(0);
    ui->verticalLayout->addWidget(&my_sub1);
    my_sub1.disableCounter();
    my_sub1.setMimeData("aplication/subject");
    my_sub1.setRowCol(-1, -1);
    my_sub2.create(75, 75);
    my_sub2.setID(1);
    ui->verticalLayout->addWidget(&my_sub2);
    my_sub2.disableCounter();
    my_sub2.setMimeData("aplication/subject");
    my_sub2.setRowCol(-1, -1);
    my_sub3.create(75, 75);
    my_sub3.setID(2);
    ui->verticalLayout->addWidget(&my_sub3);
    my_sub3.disableCounter();
    my_sub3.setMimeData("aplication/subject");
    my_sub3.setRowCol(-1, -1);

    m_table.setColumnCount(3);
    m_table.setRowCount(3);
//    m_table.horizontalHeader()->setSectionResizeMode(QHeaderView::Stretch);
//    m_table.verticalHeader()->setSectionResizeMode(QHeaderView::Stretch);
    m_table.setRowHeight(0,100);
    m_table.setRowHeight(1,100);
    m_table.setRowHeight(2,100);
    m_table.setColumnWidth(0,100);
    m_table.setColumnWidth(1,100);
    m_table.setColumnWidth(2,100);
    this->adjustSize();
}

QVector<DataTable> gameWidget::getDataTable()
{
    return m_table.getData();
}

void gameWidget::setDataTable(QVector<DataTable> &data)
{
    m_table.setData(data);
}


