#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include "gamewidget.h"

QT_BEGIN_NAMESPACE
namespace Ui { class MainWindow; }
QT_END_NAMESPACE

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    MainWindow(QWidget *parent = nullptr);
    ~MainWindow();
    void create();

public slots:
    void saveClick();
    void loadClick();

private:
    QString my_filename = "last_save.txt";
    Ui::MainWindow *ui;
    gameWidget my_widget;
};
#endif // MAINWINDOW_H
