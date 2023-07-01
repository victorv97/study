#ifndef GAMEWIDGET_H
#define GAMEWIDGET_H

#include <QWidget>
#include "subject.h"
#include <QPushButton>
#include "table.h"

namespace Ui {
class gameWidget;
}

class gameWidget : public QWidget
{
    Q_OBJECT

public:
    explicit gameWidget(QWidget *parent = nullptr);
    ~gameWidget();
    void create();
    QVector<DataTable> getDataTable();
    void setDataTable(QVector<DataTable> &);

private:
    Ui::gameWidget *ui;
    subject my_sub1;
    subject my_sub2;
    subject my_sub3;

    table m_table;
};

#endif // GAMEWIDGET_H
