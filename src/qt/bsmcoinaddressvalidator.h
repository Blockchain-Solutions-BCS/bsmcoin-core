// Copyright (c) 2011-2014 The Bitcoin Core developers
// Distributed under the MIT software license, see the accompanying
// file COPYING or http://www.opensource.org/licenses/mit-license.php.

#ifndef BSMCOIN_QT_BSMCOINADDRESSVALIDATOR_H
#define BSMCOIN_QT_BSMCOINADDRESSVALIDATOR_H

#include <QValidator>

/** Base58 entry widget validator, checks for valid characters and
 * removes some whitespace.
 */
class BsmCoinAddressEntryValidator : public QValidator
{
    Q_OBJECT

public:
    explicit BsmCoinAddressEntryValidator(QObject *parent);

    State validate(QString &input, int &pos) const;
};

/** BsmCoin address widget validator, checks for a valid bsmcoin address.
 */
class BsmCoinAddressCheckValidator : public QValidator
{
    Q_OBJECT

public:
    explicit BsmCoinAddressCheckValidator(QObject *parent);

    State validate(QString &input, int &pos) const;
};

#endif // BSMCOIN_QT_BSMCOINADDRESSVALIDATOR_H
