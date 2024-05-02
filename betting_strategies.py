import numpy as np
import matplotlib.pyplot as plt
from tabulate import tabulate

def martingale(bet, win, unit):
    if win:
        return unit * 5
    else:
        return bet * 2

def fibonacci(bet, win, sequence):
    if win:
        if len(sequence) > 2:
            sequence.pop()
            sequence.pop()
        else:
            sequence = [1, 1]
        return sequence[-1] * bet
    else:
        if len(sequence) < 2:
            sequence.append(1)
        else:
            sequence.append(sequence[-1] + sequence[-2])
        return sequence[-1] * bet

def paroli(bet, win, consecutive_wins, unit):
    if win:
        consecutive_wins += 1
        if consecutive_wins == 3:
            return unit * 5, 0
        else:
            return bet * 2, consecutive_wins
    else:
        return bet, 0

def d_alembert(bet, win, unit):
    if win:
        return max(bet - unit, unit)
    else:
        return bet + unit

def roulette_simulation(bet_on, strategy, games=1000, starting_bankroll=10000, profit_goal=100):
    outcomes = ['red'] * 18 + ['black'] * 18 + ['green'] * 2
    bankroll = starting_bankroll
    unit = starting_bankroll // 100  # Unit is 1% of bankroll
    bet = 5 * unit # Base bet is 5 units 
    consecutive_wins = 0
    fibonacci_sequence = [1, 1]
    successes = 0
    games_played = 0
    bankruptcies = 0

    while games > 0:
        result = np.random.choice(outcomes)
        win = (result == bet_on)
        if strategy == 'martingale':
            bet = martingale(bet, win, unit)
        elif strategy == 'fibonacci':
            bet = fibonacci(bet, win, fibonacci_sequence)
        elif strategy == 'paroli':
            bet, consecutive_wins = paroli(bet, win, consecutive_wins, unit)
        elif strategy == 'd_alembert':
            bet = d_alembert(bet, win, unit)

        if win:
            bankroll += bet
        else:
            bankroll -= bet

        games_played += 1

        if bankroll >= starting_bankroll + profit_goal: # Reached profit goal, walk away
            successes += 1
            games -= 1
            bankroll = starting_bankroll
            bet = 5 * unit
            consecutive_wins = 0
            fibonacci_sequence = [1, 1]
        elif bankroll < bet: # Bankroll is less than bet size
            bet = max(bankroll, 0) # All in
            if bet == 0: # Bankrupt, walk away
                bankruptcies += 1
                games -= 1
                bankroll = starting_bankroll
                bet = 5 * unit
                consecutive_wins = 0
                fibonacci_sequence = [1, 1]

    return {
        'strategy': strategy,
        'successes': successes,
        'games_played_per_success': games_played / successes if successes > 0 else np.inf,
        'bankruptcies': bankruptcies
    }

# Simulate betting strategies
strategies = ['martingale', 'fibonacci', 'paroli', 'd_alembert', 'constant_bet']
profit_goals = [100, 500, 1000, 5000]
results = {}

for profit_goal in profit_goals:
    results[profit_goal] = {}
    for strategy in strategies:
        results[profit_goal][strategy] = roulette_simulation('red', strategy, profit_goal=profit_goal)

# Print results
for profit_goal, profit_goal_results in results.items():
    print(f"\nResults for profit goal {profit_goal}:\n")
    table_data = []
    headers = ['Strategy', 'Successes', 'Games Played Per Success', 'Bankruptcies']
    for strategy, result in profit_goal_results.items():
        table_data.append([
            strategy,
            result['successes'],
            round(result['games_played_per_success'], 2),
            result['bankruptcies']
        ])
    print(tabulate(table_data, headers, tablefmt='grid'))

for profit_goal in profit_goals:
    fig, ax = plt.subplots(figsize=(10, 6))
    x = np.arange(len(strategies))
    bar_width = 0.35

    successes = [results[profit_goal][strategy]['successes'] for strategy in strategies]
    bankruptcies = [results[profit_goal][strategy]['bankruptcies'] for strategy in strategies]

    ax.bar(x - bar_width/2, successes, bar_width, label='Successes')
    ax.bar(x + bar_width/2, bankruptcies, bar_width, label='Bankruptcies')

    ax.set_xticks(x)
    ax.set_xticklabels(strategies)
    ax.set_ylabel('Count')
    ax.set_title(f'Betting Strategy Comparison (Profit Goal: {profit_goal})')
    ax.legend()

    plt.tight_layout()
    plt.show()
