// Copyright (c) 2019 The BsmCoin Core developers
// Distributed under the MIT software license, see the accompanying
// file COPYING or http://www.opensource.org/licenses/mit-license.php.

#ifndef BSMCOINLISTWIDGET_H
#define BSMCOINLISTWIDGET_H

#include <QFrame>
#include <QLabel>
#include <QListWidget>
#include <QLineEdit>
#include <QPushButton>
#include <QString>
#include <QStringList>
#include <QVBoxLayout>
#include <QWidget>

typedef std::function<bool(QString)> ValidatorFunc;

class BsmCoinListWidget : public QWidget
{
    Q_OBJECT
public:
    explicit BsmCoinListWidget(QWidget *parent, QString title, ValidatorFunc validator);

    QStringList getEntries();

private:
    QListWidget* listWidget;
    QLineEdit* addInput;
    QPushButton* removeBtn;
    QLabel* warningLbl;

    ValidatorFunc validatorFunc;

private Q_SLOTS:
    void onInsert();
    void onRemove();
    void onSelect(QListWidgetItem*);
};

#endif // BSMCOINLISTWIDGET_H
