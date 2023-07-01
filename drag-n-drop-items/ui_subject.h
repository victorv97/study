/********************************************************************************
** Form generated from reading UI file 'subject.ui'
**
** Created by: Qt User Interface Compiler version 5.9.9
**
** WARNING! All changes made in this file will be lost when recompiling UI file!
********************************************************************************/

#ifndef UI_SUBJECT_H
#define UI_SUBJECT_H

#include <QtCore/QVariant>
#include <QtWidgets/QAction>
#include <QtWidgets/QApplication>
#include <QtWidgets/QButtonGroup>
#include <QtWidgets/QHeaderView>
#include <QtWidgets/QLabel>
#include <QtWidgets/QVBoxLayout>
#include <QtWidgets/QWidget>

QT_BEGIN_NAMESPACE

class Ui_subject
{
public:
    QVBoxLayout *verticalLayout;
    QLabel *counter;

    void setupUi(QWidget *subject)
    {
        if (subject->objectName().isEmpty())
            subject->setObjectName(QStringLiteral("subject"));
        subject->resize(400, 300);
        verticalLayout = new QVBoxLayout(subject);
        verticalLayout->setObjectName(QStringLiteral("verticalLayout"));
        verticalLayout->setContentsMargins(9, -1, -1, -1);
        counter = new QLabel(subject);
        counter->setObjectName(QStringLiteral("counter"));
        counter->setEnabled(true);
        QSizePolicy sizePolicy(QSizePolicy::Preferred, QSizePolicy::Preferred);
        sizePolicy.setHorizontalStretch(0);
        sizePolicy.setVerticalStretch(0);
        sizePolicy.setHeightForWidth(counter->sizePolicy().hasHeightForWidth());
        counter->setSizePolicy(sizePolicy);
        QFont font;
        font.setFamily(QStringLiteral("Arial Black"));
        font.setPointSize(16);
        font.setBold(false);
        font.setItalic(false);
        font.setWeight(50);
        counter->setFont(font);
        counter->setLayoutDirection(Qt::LeftToRight);
        counter->setStyleSheet(QStringLiteral(""));
        counter->setAlignment(Qt::AlignCenter);

        verticalLayout->addWidget(counter);


        retranslateUi(subject);

        QMetaObject::connectSlotsByName(subject);
    } // setupUi

    void retranslateUi(QWidget *subject)
    {
        subject->setWindowTitle(QApplication::translate("subject", "Form", Q_NULLPTR));
        counter->setText(QApplication::translate("subject", "1234", Q_NULLPTR));
    } // retranslateUi

};

namespace Ui {
    class subject: public Ui_subject {};
} // namespace Ui

QT_END_NAMESPACE

#endif // UI_SUBJECT_H
