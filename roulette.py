import numpy as np

def roulette_simulation(bet_on, games=1000):
    outcomes = ['red'] * 18 + ['black'] * 18 + ['green'] * 2
    win_count = 0
    earnings = 0
    current_streak = 0
    longest_win_streak = 0
    longest_lose_streak = 0
    
    for _ in range(games):
        result = np.random.choice(outcomes)
        if result == bet_on:
            if bet_on == 'green':
                earnings += 17  # Win $17 for green
            else:
                earnings += 1  # Win $1 for red or black
            win_count += 1
            current_streak += 1
            longest_lose_streak = max(longest_lose_streak, -current_streak)
            current_streak = max(0, current_streak)  # Reset losing streak if it was a win
        else:
            earnings -= 1  # Lose $1
            current_streak -= 1
            longest_win_streak = max(longest_win_streak, current_streak)
            current_streak = min(0, current_streak)  # Reset winning streak if it was a loss

    longest_win_streak = max(longest_win_streak, current_streak)  # Check at end in case last was part of streak
    longest_lose_streak = max(longest_lose_streak, -current_streak)
    
    earnings_per_game = earnings / games
    return {
        'bet_on': bet_on,
        'total_earnings': earnings,
        'earnings_per_game': earnings_per_game,
        'longest_win_streak': longest_win_streak,
        'longest_lose_streak': longest_lose_streak,
        'win_count': win_count
    }

# Simulate betting on red/black
results_red_black = roulette_simulation('red')

# Simulate betting on green
results_green = roulette_simulation('green')

print("Results for betting on red/black:", results_red_black)
print("Results for betting on green:", results_green)
