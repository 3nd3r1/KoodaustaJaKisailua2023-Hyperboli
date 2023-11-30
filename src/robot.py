from typing import TYPE_CHECKING
import time
from enum import Enum

if TYPE_CHECKING:
    from apiwrapper.websocket_wrapper import ClientContext
from apiwrapper.models import GameState, Command, ActionType, MoveActionData, ShootActionData, TurnActionData, CompassDirection, ClientContext, Coordinates
from helpers import get_own_ship_id, get_entity_coordinates


class Side(Enum):
    LEFT = 0
    RIGHT = 1


class HyperBotti:
    def __init__(self, logger):
        self._entity_id = get_own_ship_id()
        self._last_turn = -1
        self._coords = None
        self._side = None
        self._current_direction = CompassDirection.North

        self._logger = logger

    def _get_coords(self, game_state: GameState) -> Coordinates:
        return get_entity_coordinates(self._entity_id, game_state.game_map)

    def _get_side(self) -> Side:
        if not self._coords:
            return None

        if self._coords.x < 15:
            return Side.LEFT
        return Side.RIGHT

    def _turn_to_middle(self) -> Command:
        if not self._side:
            return None

        if self._side == Side.LEFT:
            return Command(ActionType.Turn, TurnActionData(CompassDirection.East))
        return Command(ActionType.Turn, TurnActionData(CompassDirection.West))

    def _turn_to_up_or_down(self) -> Command:
        if self._coords.y == 0 and self._current_direction == CompassDirection.North:
            self._current_direction = CompassDirection.West
        if self._coords.y == 29 and self._current_direction == CompassDirection.West:
            self._current_direction = CompassDirection.North

        return Command(ActionType.Turn, TurnActionData(self._current_direction))

    def _move(self):
        return Command(ActionType.Move, MoveActionData(1))

    def _shoot(self):
        return Command(ActionType.Shoot, ShootActionData(1, 1))

    def tick(self, context: ClientContext, game_state: GameState) -> Command:
        self._logger.debug("Game turn: %s, Last turn: %s", game_state.turn_number, self._last_turn)
        self._logger.debug("Tick length %s, turn rate: %s",
                           context.tick_length_ms, context.turn_rate)

        if game_state.turn_number == self._last_turn:
            return None

        self._last_turn = game_state.turn_number
        self._coords = self._get_coords(game_state)
        self._side = self._get_side()

        match game_state.turn_number % 4:
            case 0:
                return self._turn_to_middle()
            case 1:
                return self._shoot()
            case 2:
                return self._turn_to_up_or_down()
            case 3:
                return self._move()
        return None
