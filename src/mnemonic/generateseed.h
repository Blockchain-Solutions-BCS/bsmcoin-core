// Copyright (c) 2019 The VEIL developers
// Distributed under the MIT software license, see the accompanying
// file COPYING or http://www.opensource.org/licenses/mit-license.php.

#ifndef BSMCOIN_GENERATESEED_H
#define BSMCOIN_GENERATESEED_H

#include <uint256.h>

namespace bsmcoin {
uint512 GenerateNewMnemonicSeed(std::string& mnemonic, const std::string& strLanguage);
}

#endif //BSMCOIN_GENERATESEED_H
