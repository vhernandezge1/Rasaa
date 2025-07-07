from typing import Any, Text, Dict, List
from rasa_sdk import Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
import re

class ValidateReservationForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_reservation_form"

    def validate_nombre_personnes(
        self, slot_value: Any, dispatcher: CollectingDispatcher,
        tracker: Tracker, domain: DomainDict
    ) -> Dict[Text, Any]:
        try:
            nombre = int(slot_value)
            if 1 <= nombre <= 10:
                return {"nombre_personnes": nombre}
            dispatcher.utter_message(text="Veuillez entrer un nombre entre 1 et 10.")
        except ValueError:
            dispatcher.utter_message(text="Entrez un nombre valide svp.")
        return {"nombre_personnes": None}

    def validate_heure(
        self, slot_value: Any, dispatcher: CollectingDispatcher,
        tracker: Tracker, domain: DomainDict
    ) -> Dict[Text, Any]:
        pattern = r'(\d{1,2})[h:]?(\d{0,2})'
        match = re.match(pattern, slot_value.lower())
        if match:
            heure = int(match.group(1))
            minute = int(match.group(2)) if match.group(2) else 0
            if 18 <= heure <= 23 and 0 <= minute <= 59:
                return {"heure": f"{heure}h{minute:02d}" if minute > 0 else f"{heure}h"}
            dispatcher.utter_message(text="Réservations possibles entre 18h et 23h.")
        else:
            dispatcher.utter_message(text="Format d'heure incorrect (ex : 19h30).")
        return {"heure": None}
