from __future__ import annotations

from .publickey import PublicKey
from .core.http import AsyncHTTPClient
from .core.types import RPCResponse
from .transaction import Transaction

ENDPOINTS = (
    "https://api.mainnet-beta.solana.com",
    "https://api.devnet.solana.com",
    "https://api.testnet.solana.com",
)


class AsyncClient:
    def __init__(self, endpoint: str, local: bool = False):
        if not local and endpoint not in ENDPOINTS:
            raise ValueError(
                "Invalid cluster RPC endpoint provided"
                " (Refer to https://docs.solana.com/cluster/rpc-endpoints)."
                " Use the argument local to use a local development endpoint."
            )
        self.http = AsyncHTTPClient(endpoint)
        self.endpoint = endpoint

    async def refresh_http(self) -> None:
        await self.http.refresh()

    async def get_account_info(self, public_key: PublicKey | str) -> RPCResponse:
        data = self.http.build_data(
            method="getAccountInfo", params=[public_key]
        )
        res = await self.http.send(data)
        return res

    async def get_balance(self, public_key: PublicKey | str) -> RPCResponse:
        data = self.http.build_data(
            method="getBalance", params=[public_key]
        )
        res = await self.http.send(data)
        return res

    async def get_block(self, slot: int) -> RPCResponse:
        data = self.http.build_data(
            method="getBlock", params=[slot]
        )
        res = await self.http.send(data)
        return res

    async def get_block_height(self) -> RPCResponse:
        data = self.http.build_data(
            method="getBlockHeight", params=[None]
        )
        res = await self.http.send(data)
        return res

    async def get_block_production(self) -> RPCResponse:
        data = self.http.build_data(
            method="getBlockProduction", params=[None]
        )
        res = await self.http.send(data)
        return res

    async def get_block_commitment(self, block: int) -> RPCResponse:
        data = self.http.build_data(
            method="getBlockCommitment", params=[block]
        )
        res = await self.http.send(data)
        return res

    async def get_blocks(self, start_slot: int, end_slot: int | None = None
                   ) -> RPCResponse:
        params = [start_slot]
        if end_slot:
            params.append(end_slot)

        data = self.http.build_data(
            method="getBlocks", params=params
        )
        res = await self.http.send(data)
        return res

    async def get_blocks_with_limit(self, start_slot: int, limit: int
                              ) -> RPCResponse:

        data = self.http.build_data(
            method="getBlocksWithLimit", params=[start_slot, limit]
        )
        res = await self.http.send(data)
        return res

    async def get_block_time(self, block: int) -> RPCResponse:

        data = self.http.build_data(
            method="getBlockTime", params=[block]
        )
        res = await self.http.send(data)
        return res

    async def get_cluster_nodes(self) -> RPCResponse:

        data = self.http.build_data(
            method="getClusterNodes", params=[None]
        )
        res = await self.http.send(data)
        return res

    async def get_epoch_info(self) -> RPCResponse:

        data = self.http.build_data(
            method="getEpochInfo", params=[None]
        )
        res = await self.http.send(data)
        return res

    async def get_epoch_schedule(self) -> RPCResponse:

        data = self.http.build_data(
            method="getEpochSchedule", params=[None]
        )
        res = await self.http.send(data)
        return res

    async def get_fee_for_message(self, message: str) -> RPCResponse:

        data = self.http.build_data(
            method="getFeeForMessage", params=[message]
        )
        res = await self.http.send(data)
        return res

    # Going to be deprecated
    async def get_fees(self) -> RPCResponse:

        data = self.http.build_data(
            method="getFees", params=[None]
        )
        res = await self.http.send(data)
        return res

    async def get_first_available_block(self) -> RPCResponse:

        data = self.http.build_data(
            method="getFirstAvailableBlock", params=[None]
        )
        res = await self.http.send(data)
        return res

    async def get_supply(self) -> RPCResponse:
        data = self.http.build_data(
            method="getSupply", params=[None]
        )
        res = await self.http.send(data)
        return res

    async def get_identity(self) -> RPCResponse:
        data = self.http.build_data(
            method="getIdentity", params=[None]
        )
        res = await self.http.send(data)
        return res

    async def get_transaction(self, signature: str) -> RPCResponse:
        data = self.http.build_data(
            method="getTransaction", params=[signature]
        )
        res = await self.http.send(data)
        return res

    # Will switch to getFeeForMessage (latest)
    async def get_recent_blockhash(self) -> RPCResponse:
        data = self.http.build_data(
            method="getRecentBlockhash", params=[None]
        )
        res = await self.http.send(data)
        return res

    async def get_token_accounts_by_owner(self, public_key: str | PublicKey,
                                    **kwargs) -> RPCResponse:
        if "mint_id" not in kwargs and "program_id" not in kwargs:
            raise ValueError(
                "You must pass either mint_id or program_id keyword argument")

        mint_id = kwargs.get("mint_id")
        program_id = kwargs.get("program_id")
        # Who doesn't like JSON?
        encoding = kwargs.get("encoding", "jsonParsed")

        data = self.http.build_data(
            method="getTokenAccountsByOwner",
            params=[
                str(public_key),
                {"mint": mint_id} if mint_id else {"programId": program_id},
                {"encoding": encoding}
            ]
        )
        res = await self.http.send(data)
        return res

    async def request_airdrop(self, public_key: PublicKey | str, lamports: int
                        ) -> RPCResponse:

        data = self.http.build_data(
            method="requestAirdrop",
            params=[public_key, lamports]
        )
        res = await self.http.send(data)
        return res

    async def send_transaction(self, transaction: Transaction,
                         recent_blockhash: str | None = None
                         ) -> RPCResponse:

        if recent_blockhash is None:
            blockhash_resp = self.get_recent_blockhash()
            recent_blockhash = blockhash_resp["result"]["value"]["blockhash"]

        transaction.recent_blockhash = recent_blockhash
        transaction.sign()

        data = self.http.build_data(
            method="sendTransaction",
            params=[transaction.serialize(), {"encoding": "base64"}]
        )
        res = await self.http.send(data)
        return res