#include "table.h"
#include <QDebug>
#include <QDragEnterEvent>
#include <QMimeData>
#include "subject.h"


table::table()
{
    setAcceptDrops(true);
    setDragDropMode(QAbstractItemView::InternalMove);
}

QVector<DataTable> table::getData()
{
    QVector<DataTable> result;
    for (int i = 0; i < model()->rowCount(); i++) {
        for (int j = 0; j < model()->columnCount(); j++){
            auto ptr = cellWidget(i, j);
            if (ptr != nullptr){
                subject *subinTable = static_cast<subject*>(ptr);
                DataTable data;
                data.row = i;
                data.col = j;
                data.id = subinTable->getID();
                data.count = subinTable->getCounter();
                result.push_back(data);
            }
        }
    }
    return result;
}


void table::setData(QVector<DataTable> &data)
{
    for (int i = 0; i < model()->rowCount(); i++) {
        for (int j = 0; j < model()->columnCount(); j++){
            auto ptr = cellWidget(i, j);
            if (ptr != nullptr){
                removeCellWidget(i,j);
            }
        }
    }
    queue_data.clear();
     for (int i = 0; i < data.size(); i++) {
         qDebug()<<"noWidget";
         subject *subinTable = new subject();
         subinTable->create(100, 100);
         subinTable->setMimeData("aplication/subjectInTable");
         subinTable->setRowCol(data[i].row, data[i].col);
         subinTable->setID(data[i].id);
         subinTable->setCounter(data[i].count);
         setCellWidget(data[i].row, data[i].col, subinTable);
         int k = 0;
         while(k < data[i].count){
         remember_queue(data[i].row, data[i].col,data[i].id);
         k++;
         }
    }

}

void table::dragEnterEvent(QDragEnterEvent *event)
{
    qDebug()<<"dragEnterEvent";
    if(event->mimeData()->hasFormat("aplication/subject")||
            event->mimeData()->hasFormat("aplication/subjectInTable")){
        event->acceptProposedAction();
        qDebug()<<"event->acceptProposedAction";
    }
    else {
        event->ignore();
    qDebug()<<" event->ignore()";
    }

}

void table::dropEvent(QDropEvent *event)
{
    qDebug()<<"dropEvent";
    QModelIndex indexCur = indexAt(event->pos());
    if(!indexCur.isValid())
        return;
    qDebug()<<"row to = "<<indexCur.row()
    << "col to = "<<indexCur.column();


    if(event->mimeData()->hasFormat("aplication/subject"))
    {
        handleSubject(event, indexCur.row(), indexCur.column());
    }
    if(event->mimeData()->hasFormat("aplication/subjectInTable"))
    {
        handleSubjectTable(event, indexCur.row(), indexCur.column());
    }


}

void table::handleSubject(QDropEvent *event, int row_to, int column_to)
{
    int max_count;
    QByteArray data = event->mimeData()
            ->data("aplication/subject");
    QDataStream in(&data, QIODevice:: ReadOnly);
    int row;
    int col;
    int ID;
    int c = 1;
    in >> row >> col >> ID;
    qDebug()<<"row from = "<<row
    << "col from = "<<col <<"id"<< ID;
    if (ID == 0) {
        max_count = 4;
    } else if (ID == 1){
        max_count = 5;
    } else {
        max_count = 3;
    }

auto ptr = cellWidget(row_to, column_to);
if (ptr == nullptr){
    qDebug()<<"noWidget";
    subject *subinTable = new subject();
    subinTable->create(100, 100);
    subinTable->setMimeData("aplication/subjectInTable");
    subinTable->setRowCol(row_to, column_to);
    subinTable->setID(ID);
    subinTable->setCounter(c);
    setCellWidget(row_to, column_to, subinTable);
    remember_queue(row_to, column_to, ID);
    if(check_remove_sub(ID, max_count)){
       History sub_to_remove = remove_sub(ID);
       auto ptrWidget = cellWidget(sub_to_remove.row, sub_to_remove.col);
       subject *sub = static_cast<subject*>(ptrWidget);
       int counter_sub = sub->getCounter();
       if (counter_sub > 1){
       sub->setCounter(counter_sub - 1);
       }
       else {
       removeCellWidget(sub_to_remove.row, sub_to_remove.col);
       }
        qDebug()<<"Стало:";
        showDebug();
    }


    }
else {
        qDebug()<<"isWidget";
        subject *subinTable = static_cast<subject*>(ptr);
        if (ID == subinTable->getID()){
        int counter = subinTable->getCounter();
        qDebug()<<"counter"<<counter;
        counter++;
        subinTable->setCounter(counter);
        remember_queue(row_to, column_to, ID);
        if(check_remove_sub(ID, max_count)){
            History sub_to_remove = remove_sub(ID);
            auto ptrWidget = cellWidget(sub_to_remove.row, sub_to_remove.col);
            subject *sub = static_cast<subject*>(ptrWidget);
            int counter_sub = sub->getCounter();
            if (counter_sub > 1){
            sub->setCounter(counter_sub - 1);
            }
            else {
            removeCellWidget(sub_to_remove.row, sub_to_remove.col);
            }
            qDebug()<<"Стало:";
            showDebug();
        }
        }
    }

}

void table::handleSubjectTable(QDropEvent *event, int row_to, int column_to)
{
    History *q_data = queue_data.data();
    QByteArray data = event->mimeData()
            ->data("aplication/subjectInTable");
    QDataStream in(&data, QIODevice:: ReadOnly);
    int row_from;
    int col_from;
    int ID_from;
    in >> row_from >> col_from >> ID_from;
    qDebug()<<"row from = "<<row_from
    << "col from = "<<col_from <<"id_from"<< ID_from;

    auto ptrFrom = cellWidget(row_from, col_from);
    subject *subFrom = static_cast<subject*>(ptrFrom);
    int counterFrom = subFrom->getCounter();
     qDebug()<<"counterFrom = "<<counterFrom;

     auto ptr_to = cellWidget(row_to, column_to);
     if (ptr_to == nullptr){
         qDebug()<<"noWidget";
         subject *subinTable = new subject();
         subinTable->create(100, 100);
         subinTable->setMimeData("aplication/subjectInTable");
         subinTable->setRowCol(row_to, column_to);
         subinTable->setID(ID_from);
         subinTable->setCounter(counterFrom);
         setCellWidget(row_to, column_to, subinTable);
         removeCellWidget(row_from, col_from);
         for(int i = 0; i < queue_data.size(); i++){
             if((queue_data.at(i).row == row_from)&&(queue_data.at(i).col == col_from)&&(queue_data.at(i).id == ID_from)){
                 q_data[i].row = row_to;
                 q_data[i].col = column_to;

             }
         }
         }
     else {
             qDebug()<<"isWidget";
             subject *subinTable = static_cast<subject*>(ptr_to);
             int ID_to = subinTable->getID();
             if (ID_from == ID_to) {
                 int counterTo = subinTable->getCounter();
                 qDebug()<<"counterTo"<<counterTo;
                 subinTable->setCounter(counterTo + counterFrom);
                 removeCellWidget(row_from, col_from);
                 for(int i = 0; i < queue_data.size(); i++){
                     if((queue_data.at(i).row == row_from)&&(queue_data.at(i).col == col_from)&&(queue_data.at(i).id == ID_from)){
                         q_data[i].row = row_to;
                         q_data[i].col = column_to;

                     }
                 }
             }

     }

     qDebug()<<"Перемещение:";
     showDebug();
}

bool table::check_remove_sub(int id, int max_count)
{
    int check_count = 0;
    QVector<DataTable> data = getData();
    for (int i = 0; i< data.size(); i++){
    if (data[i].id == id){
        check_count = check_count + data[i].count;
    }
    }
    if (check_count > max_count){
        qDebug()<<"Need to remove";
        return true;
    }
qDebug()<<"No need to remove";
return false;
}

void table::remember_queue(int row, int column, int id)
{
        History data;
        data.row = row;
        data.col = column;
        data.id = id;
        queue_data.push_back(data);
        qDebug()<<"Запомнил:";
        showDebug();
}

History table::remove_sub(int ID)
{
    History sub_to_remove;
    for(int i = 0; i<queue_data.size(); i++){
        if(queue_data.at(i).id == ID){
            sub_to_remove.id = queue_data.at(i).id;
            sub_to_remove.col = queue_data.at(i).col;
            sub_to_remove.row = queue_data.at(i).row;
                queue_data.remove(i);
                break;
            }
    }
    return sub_to_remove;
}

void table::showDebug()
{
    for(int i=0; i < queue_data.size(); i++){
    qDebug()<<queue_data.at(i).row <<";"<<queue_data.at(i).col <<";"
              <<queue_data.at(i).id;
    }
}
