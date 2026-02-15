from app.db.db import *

class TicketRepository:
    def __init__(self) -> None:
        pass

    def add_ticket(self, ticket: Ticket):
        tickets[ticket.id] = ticket.model_dump()
        return True

    def remove_ticket(self, ticket_id: str):
        del tickets[ticket_id]
        return True

    def get_ticket(self, ticket_id: str):
        return tickets[ticket_id]

    def get_all_tickets(self):
        return tickets