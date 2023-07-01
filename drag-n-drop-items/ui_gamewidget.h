/********************************************************************************
** Form generated from reading UI file 'gamewidget.ui'
**
** Created by: Qt User Interface Compiler version 5.9.9
**
** WARNING! All changes made in this file will be lost when recompiling UI file!
********************************************************************************/

#ifndef UI_GAMEWIDGET_H
#define UI_GAMEWIDGET_H

#include <QtCore/QVariant>
#include <QtWidgets/QAction>
#include <QtWidgets/QApplication>
#include <QtWidgets/QButtonGroup>
#include <QtWidgets/QHBoxLayout>
#include <QtWidgets/QHeaderView>
#include <QtWidgets/QVBoxLayout>
#include <QtWidgets/QWidget>

QT_BEGIN_NAMESPACE

class Ui_gameWidget
{
public:
    QHBoxLayout *horizontalLayout;
    QHBoxLayout *horizontalLayout_2;
    QVBoxLayout *verticalLayout;

    void setupUi(QWidget *gameWidget)
    {
        if (gameWidget->objectName().isEmpty())
            gameWidget->setObjectName(QStringLiteral("gameWidget"));
        gameWidget->resize(400, 300);
        QSizePolicy sizePolicy(QSizePolicy::Minimum, QSizePolicy::Minimum);
        sizePolicy.setHorizontalStretch(0);
        sizePolicy.setVerticalStretch(0);
        sizePolicy.setHeightForWidth(gameWidget->sizePolicy().hasHeightForWidth());
        gameWidget->setSizePolicy(sizePolicy);
        gameWidget->setFocusPolicy(Qt::NoFocus);
        horizontalLayout = new QHBoxLayout(gameWidget);
        horizontalLayout->setObjectName(QStringLiteral("horizontalLayout"));
        horizontalLayout_2 = new QHBoxLayout();
        horizontalLayout_2->setObjectName(QStringLiteral("horizontalLayout_2"));
        horizontalLayout_2->setSizeConstraint(QLayout::SetMinimumSize);

        horizontalLayout->addLayout(horizontalLayout_2);

        verticalLayout = new QVBoxLayout();
        verticalLayout->setObjectName(QStringLiteral("verticalLayout"));

        horizontalLayout->addLayout(verticalLayout);


        retranslateUi(gameWidget);

        QMetaObject::connectSlotsByName(gameWidget);
    } // setupUi

    void retranslateUi(QWidget *gameWidget)
    {
        gameWidget->setWindowTitle(QApplication::translate("gameWidget", "Form", Q_NULLPTR));
    } // retranslateUi

};

namespace Ui {
    class gameWidget: public Ui_gameWidget {};
} // namespace Ui

QT_END_NAMESPACE

#endif // UI_GAMEWIDGET_H
