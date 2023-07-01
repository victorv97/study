#ifndef SUBJECT1_H
#define SUBJECT1_H

#include <QWidget>
#include <QDrag>
#include <QMimeData>


namespace Ui {
class subject;
}

class subject : public QWidget
{
    Q_OBJECT

public:
    explicit subject(QWidget *parent = nullptr);
    ~subject();
    void create(int w, int h);

    void setCounter(int value);
    int getCounter();
    void disableCounter();
    void setMimeData(QString data);
    void setRowCol(int, int);
    void setID(int ID);
    int getID();

    QDrag *makeDrag();

protected:
    //Drag
    virtual void mousePressEvent(QMouseEvent *event) override;
    virtual void mouseMoveEvent(QMouseEvent *event) override;
    //paint
    virtual void paintEvent(QPaintEvent *event) override;

    virtual void mouseReleaseEvent(QMouseEvent *e) override;

private:
    Ui::subject *ui;
    QPoint m_dragStart;
    QPixmap m_pixmap;
    QString m_mimeData;
    int m_row;
    int m_col;
    int m_ID;
};

#endif // SUBJECT1_H
