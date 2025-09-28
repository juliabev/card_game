import itertools

def get_players():
    """
    Returns a list of all 8 players, represented as 3-bit binary strings.
    """
    return [f'{i:03b}' for i in range(8)]

def play_game(player1: str, player2: str) -> tuple[int, int]:
    """
    This is a placeholder for your game logic.

    Args:
        player1: The first player.
        player2: The second player.

    Returns:
        A tuple containing the scores for player1 and player2.
    """
    # Replace this with your actual game logic.
    # For now, it returns a dummy score.
    score1 = sum(int(bit) for bit in player1)
    score2 = sum(int(bit) for bit in player2)
    if score1 > score2:
        return (1, 0)
    elif score2 > score1:
        return (0, 1)
    else:
        return (0, 0)

def run_tournament(players: list[str]) -> dict:
    """
    Plays a tournament where every player plays against every other player.

    Args:
        players: A list of players.

    Returns:
        A dictionary containing the results of the tournament.
    """
    scores = {player: 0 for player in players}
    results = {}

    for player1, player2 in itertools.combinations(players, 2):
        score1, score2 = play_game(player1, player2)
        scores[player1] += score1
        scores[player2] += score2
        results[f'{player1}_vs_{player2}'] = (score1, score2)

    return scores, results

if __name__ == '__main__':
    players = get_players()
    final_scores, game_results = run_tournament(players)

    print("--- Game Results ---")
    for game, result in game_results.items():
        print(f'{game}: {result}')

    print("\n--- Final Scores ---")
    for player, score in sorted(final_scores.items(), key=lambda item: item[1], reverse=True):
        print(f'{player}: {score}')