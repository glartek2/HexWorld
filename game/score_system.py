def bonus_points(map_grid, player, bonus_name, bonus_value):
    for row, col in player.tiles:
        tile = map_grid[row][col]
        if tile.terrain.name == bonus_name or tile.bonus.name == bonus_name:
            player.score += bonus_value

def update_score(map_grid, player):
    player.score += len(player.tiles)

    def apply_bonus(civ):
        if civ:
            species_bonus_name, species_bonus_value = civ.species.bonus_score()
            bonus_points(map_grid, player, species_bonus_name, species_bonus_value)

            ability_bonus_name, ability_bonus_value = civ.ability.bonus_score_on_tile()
            bonus_points(map_grid, player, ability_bonus_name, ability_bonus_value)

    apply_bonus(player.current_civ)
    apply_bonus(player.old_civ)
