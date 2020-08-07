// Copyright (c) 2019 The BsmCoin Core developers
// Distributed under the MIT software license, see the accompanying
// file COPYING or http://www.opensource.org/licenses/mit-license.php.

#ifndef BSMCOINPUSHBUTTON_H
#define BSMCOINPUSHBUTTON_H

#include <QIcon>
#include <QPushButton>
#include <QPainter>
#include <QString>
#include <QWidget>

class BsmCoinPushButton : public QPushButton
{
    Q_OBJECT

public:
    BsmCoinPushButton(QString label);
    void paintEvent(QPaintEvent*);
    void setBadge(int nValue);

private:
    QIcon getBadgeIcon(int nValue);
};

#endif // BSMCOINPUSHBUTTON_H
