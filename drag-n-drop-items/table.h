#ifndef TABLE_H
#define TABLE_H

#include <QTableWidget>


struct DataTable{
    int id;
    int count;
    int row;
    int col;
};

struct History{
    int id;
    int row;
    int col;
};

class table :public QTableWidget
{
public:
    table();
    QVector<DataTable> getData();
    void setData(QVector<DataTable> &data);
protected:
    virtual void dragEnterEvent(QDragEnterEvent* event) override;
    virtual void dropEvent(QDropEvent *event) override;
private:
    void handleSubject(QDropEvent *event, int row_to, int column_to);
    void handleSubjectTable(QDropEvent *event, int row_to, int column_to);
    bool check_remove_sub(int id, int max_count);
    void remember_queue(int row, int column, int id);
    QVector<History> queue_data;
    History remove_sub(int ID);
    void showDebug(void);


};

#endif // TABLE_H
