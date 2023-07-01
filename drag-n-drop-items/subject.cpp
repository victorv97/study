#include "subject.h"
#include "ui_subject.h"
#include <QPixmap>
#include <QVariant>
#include <QtDebug>
#include <QSize>
#include <QMouseEvent>
#include <QMimeData>
#include <QPainter>

subject::subject(QWidget *parent) :
    QWidget(parent),
    ui(new Ui::subject)
{
    ui->setupUi(this);

}

subject::~subject()
{
    delete ui;
}

void subject::create(int w, int h)
{
    this->setMinimumSize(QSize(w, h));
    this->setMaximumSize(QSize(w, h));
    this->resize(w, h);
    qDebug() << "subject size" << this->size();
    setCounter(0);
}

void subject::setCounter(int value)
{
    QVariant var(value);
    ui->counter->setText(var.toString());
}

int subject::getCounter()
{
    QVariant var(ui->counter->text());
    return var.toInt();
}

void subject::disableCounter()
{
    ui->counter->setVisible(false);
}

void subject::setMimeData(QString data)
{
    m_mimeData = data;
}

void subject::setRowCol(int row, int col)
{
    m_row = row;
    m_col = col;
}

void subject::setID(int ID)
{
    m_ID = ID;
    if (m_ID == 0) {
        m_pixmap.load(".\\images\\circle.png");
    }
    else if(m_ID == 1){
        m_pixmap.load(".\\images\\triangle.png");
    }
    else if(m_ID == 2){
        m_pixmap.load(".\\images\\square.png");
    }
    else {
        m_pixmap.load("");
    }

}

int subject::getID()
{
    return m_ID;
}




void subject::mousePressEvent(QMouseEvent *event)
{
    qDebug() <<"mousePressEvent";
    m_dragStart = event->pos();
    QWidget::mousePressEvent(event);

}

void subject::mouseMoveEvent(QMouseEvent *event)
{
    qDebug() <<"mouseMoveEvent";
    if((event->buttons() & Qt::LeftButton)
            && QApplication::startDragDistance() <=
            (event->pos() - m_dragStart).manhattanLength())
    {
        makeDrag()->exec(Qt::MoveAction);
    }
    QWidget::mouseMoveEvent(event);
}

void subject::paintEvent(QPaintEvent *event)
{
    qDebug() <<"paintEvent";
    QPainter painter(this);
    if (!m_pixmap.isNull())
    {
        QSize widgetSize = size();
        QPixmap scaledPixmap = m_pixmap.scaled(widgetSize, Qt::KeepAspectRatio);
        QPoint center((widgetSize.width()-scaledPixmap.width())/2,
                      (widgetSize.height()-scaledPixmap.height())/2);
        painter.drawPixmap(center, scaledPixmap);
       // painter.drawText(rect(), Qt::AlignRight | Qt::AlignBottom, m_text);
    }
    QWidget::paintEvent(event);
}

QDrag *subject::makeDrag()
{
    QDrag *drag = new QDrag(this);
    QByteArray itemData;
    QDataStream stream(&itemData, QIODevice::WriteOnly);
    stream<< m_row << m_col << m_ID;
    QMimeData *mimeData = new QMimeData;
    mimeData->setData(m_mimeData, itemData);
    drag->setMimeData(mimeData);
    drag->setPixmap(m_pixmap.scaled(size(), Qt::KeepAspectRatio));
    return drag;
}

void subject::mouseReleaseEvent(QMouseEvent *e)
{
    qDebug()<<"mouseReleaseEvent";
    QWidget:: mouseReleaseEvent(e);
}

