# Script to compare fees when using Wasabi & Whirlpool by @6102bitcoin

from pylab import *
import numpy as np
import math

mix_amount_range = np.arange(0.001, 1.001, 0.001)

# Fixed Parameter: Anonset Per Round
wasabi_anonset_per_round = 100.0
whirlpool_anonset_per_round = 5.0

# Fixed Parameter: Pool Size
wasabi_pool_size = 0.1 #BTC
whirlpool_pool_size = 0.005 #BTC

# Initialise Results Lists
results_mix_amount = []
results_wasabi_coordinator_fee = []
results_whirlpool_coordinator_fee = []
results_wasabi_anonset = []
results_whirlpool_anonset = []
results_wasabi_utxos = []
results_whirlpool_utxos = []

for index, mix_amount in np.ndenumerate(mix_amount_range):

    # Rounds
    wasabi_rounds = math.ceil(mix_amount / wasabi_pool_size) # Rounds Up
    whirlpool_rounds = math.ceil(mix_amount / whirlpool_pool_size) # Rounds Up

    # Anonset [This is a bad metric and Anonset doesn't scale like this]
    wasabi_anonset = wasabi_anonset_per_round * wasabi_rounds
    whirlpool_anonset = whirlpool_anonset_per_round * whirlpool_rounds

    # Fee Structure
    wasabi_coordinator_fee = mix_amount * 0.003/100 * wasabi_anonset
    whirlpool_coordinator_fee = whirlpool_pool_size * 0.05 # 5% of Pool Size

    # UTXO's
    wasabi_utxos = wasabi_rounds
    whirlpool_utxos = whirlpool_rounds

    results_mix_amount.append(mix_amount)

    if wasabi_pool_size <= mix_amount:
        results_wasabi_coordinator_fee.append(100 * wasabi_coordinator_fee / mix_amount) # Percentage of Amount Mixed
        results_wasabi_anonset.append(wasabi_anonset)
        results_wasabi_utxos.append(wasabi_rounds)
    else:
        results_wasabi_coordinator_fee.append(None)
        results_wasabi_anonset.append(None)
        results_wasabi_utxos.append(None)

    if whirlpool_pool_size <= mix_amount:
        results_whirlpool_coordinator_fee.append((100 * whirlpool_coordinator_fee / mix_amount)) # Percentage of Amount Mixed
        results_whirlpool_anonset.append(whirlpool_anonset)
        results_whirlpool_utxos.append(whirlpool_rounds)
    else:
        results_whirlpool_coordinator_fee.append(None)
        results_whirlpool_anonset.append(None)
        results_whirlpool_utxos.append(None)

# Plot Figures
plt.suptitle('CoinJoin Coordinator Fee Comparison \n (Whirlpool Pool Size: ' + str(whirlpool_pool_size) + ")")

subplot(2,1,1)
plt.ylabel('Fee (% of Mix Amount)')
plt.xlabel('Amount being mixed (BTC)')
plt.plot(results_mix_amount, results_wasabi_coordinator_fee)
plt.plot(results_mix_amount, results_whirlpool_coordinator_fee)
plt.legend(['Wasabi', 'Whirlpool'])

subplot(2,1,2)
plt.ylabel('UTXO\'s')
plt.xlabel('Amount being mixed (BTC)')
plt.plot(results_mix_amount, results_wasabi_utxos)
plt.plot(results_mix_amount, results_whirlpool_utxos)
plt.legend(['Wasabi', 'Whirlpool'])

subplots_adjust(left=.12, bottom=.11, right=.9, top=.88, wspace=.2, hspace=.5) # Adjust vertical spacing
plt.show()
