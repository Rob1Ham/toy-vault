"""Intentionally vulnerable, offline teaching fixture. Never use for real funds."""

from dataclasses import dataclass


@dataclass(frozen=True)
class SpendRequest:
    vault_id: str
    destination: str
    amount_sats: int
    fee_sats: int
    approvals: tuple[str, ...]
    request_id: str


class ToyVaultLedger:
    def __init__(self):
        self.vaults: dict[str, dict] = {}
        self.credits: dict[str, int] = {}
        self.fees_sats = 0
        self.receipts: list[dict] = []

    def add_vault(self, vault_id: str, owner: str, signers: set[str], balance_sats: int):
        if balance_sats < 0 or not owner or not vault_id or vault_id in self.vaults:
            raise ValueError("invalid vault")
        self.vaults[vault_id] = {"owner": owner, "signers": set(signers), "balance": balance_sats}

    @staticmethod
    def _check_request(request: SpendRequest):
        if request.amount_sats <= 0 or request.fee_sats < 0 or not request.destination or not request.request_id:
            raise ValueError("invalid spend request")

    def preview(self, request: SpendRequest) -> dict:
        self._check_request(request)
        vault = self.vaults[request.vault_id]
        total = request.amount_sats + request.fee_sats
        if vault["balance"] < total:
            raise ValueError("insufficient balance for amount and fee")
        return {"total_debit_sats": total, "remaining_sats": vault["balance"] - total}

    def submit(self, actor_id: str, request: SpendRequest) -> dict:
        self._check_request(request)
        vault = self.vaults[request.vault_id]
        if not actor_id:
            raise ValueError("unknown actor")
        if len(request.approvals) < 2 or any(name not in vault["signers"] for name in request.approvals):
            raise ValueError("two permitted approvals required")
        if vault["balance"] < request.amount_sats:
            raise ValueError("insufficient balance")

        vault["balance"] -= request.amount_sats + request.fee_sats
        self.credits[request.destination] = self.credits.get(request.destination, 0) + request.amount_sats
        self.fees_sats += request.fee_sats
        receipt = {"request_id": request.request_id, "actor": actor_id,
                   "remaining_sats": vault["balance"]}
        self.receipts.append(receipt)
        return receipt
