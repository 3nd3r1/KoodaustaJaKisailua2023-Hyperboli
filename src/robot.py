from typing import TYPE_CHECKING
import time

if TYPE_CHECKING:
    from apiwrapper.websocket_wrapper import ClientContext
from apiwrapper.models import GameState, Command, ActionType, MoveActionData, ShootActionData, TurnActionData, CompassDirection, ClientContext


class HyperBotti:
    def __init__(self, logger):
        self._last_turn = -1
        self._logger = logger

    def _turn_to_east(self) -> Command:
        return Command(ActionType.Turn, TurnActionData(CompassDirection.East))

    def _turn_to_north(self) -> Command:
        return Command(ActionType.Turn, TurnActionData(CompassDirection.North))

    def _move(self):
        return Command(ActionType.Move, MoveActionData(1))

    def _shoot(self):
        return Command(ActionType.Shoot, ShootActionData(1, 1))

    def tick(self, context: ClientContext, game_state: GameState) -> Command:
        self._logger.debug("Game turn: %s, Last turn: %s", game_state.turn_number, self._last_turn)

        if game_state.turn_number == self._last_turn:
            return None
        self._last_turn = game_state.turn_number

        match game_state.turn_number % 4:
            case 0:
                return self._turn_to_east()
            case 1:
                return self._shoot()
            case 2:
                return self._turn_to_north()
            case 3:
                return self._move()
        return None
