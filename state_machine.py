import logging

from globals import Events, States


class StateMachine:
    # Dict of states with list of next states per event
    STATE_TRANSITIONS = {
        States.IDLE:    {Events.SET_READY: States.READY,
                         Events.ENTER_ERROR: States.ERROR},
        States.READY:   {Events.START: States.RUNNING,
                         Events.ENTER_ERROR: States.ERROR},
        States.RUNNING: {Events.STOP: States.STOPPED,
                         Events.ENTER_ERROR: States.ERROR},
        States.STOPPED: {Events.SET_READY: States.READY,
                         Events.ENTER_ERROR: States.ERROR},
        States.ERROR:   {Events.QUIT_ERROR: States.IDLE,
                         Events.ENTER_ERROR: States.ERROR},
    }

    def __init__(self):
        self._current_state = States.IDLE

    def update(self, new_event: Events) -> bool:
        state_changed = False
        if new_event in self.STATE_TRANSITIONS[self._current_state]:
            new_state = self.STATE_TRANSITIONS[self._current_state][new_event]
            if new_state != self._current_state:
                state_changed = True
                logging.info(f'State changed from {self._current_state.name} to {new_state.name}')
                self._current_state = new_state
        else:
            logging.error(f'Received invalid event: {new_event.name}')
        return state_changed

    def get_current_state(self) -> States:
        return self._current_state
