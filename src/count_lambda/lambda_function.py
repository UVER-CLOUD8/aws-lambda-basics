import json
import logging
import time
from typing import Dict, Any, List

logger = logging.getLogger()
logger.setLevel(logging.INFO)

DEFAULT_N = 100_000
MAX_N = 5_000_000  # 事故防止（Lambdaで極端に重い処理を避ける）

def _parse_event(event: Dict[str, Any]) -> int:
    """
    eventから上限nを取り出す。なければDEFAULT。
    文字列で来ても数値に変換して扱う。
    """
    raw = event.get("n", event.get("limit", DEFAULT_N))  # n優先、なければlimit互換
    try:
        n = int(raw)
    except (TypeError, ValueError):
        n = DEFAULT_N

    if n < 2:
        return 1  # 1以下なら素数0なので、後段の処理を簡略化
    return min(n, MAX_N)

def _count_primes_sieve(n: int) -> int:
    """
    エラトステネスの篩（簡易版）で2..nの素数個数を数える。
    書籍サンプルと差を出すため、実装の形（配列・ステップ）を変えている。
    """
    # sieve[i] == 1 なら「候補」、0なら「合成数」
    sieve = bytearray(b"\x01") * (n + 1)
    sieve[0:2] = b"\x00\x00"

    # 偶数をまとめて落とす（2だけ残す）
    for x in range(4, n + 1, 2):
        sieve[x] = 0

    # 奇数のみ走査
    p = 3
    while p * p <= n:
        if sieve[p]:
            step = 2 * p
            start = p * p
            for x in range(start, n + 1, step):
                sieve[x] = 0
        p += 2

    return int(sum(sieve))

def lambda_handler(event, context):
    t0 = time.perf_counter()

    n = _parse_event(event if isinstance(event, dict) else {})
    prime_count = 0 if n <= 1 else _count_primes_sieve(n)

    elapsed_ms = (time.perf_counter() - t0) * 1000.0

    # CloudWatchで比較しやすいようにログを整形
    logger.info(
        json.dumps(
            {
                "metric": "prime_count",
                "n": n,
                "count": prime_count,
                "elapsed_ms": round(elapsed_ms, 3),
                "memory_limit_mb": getattr(context, "memory_limit_in_mb", None),
                "request_id": getattr(context, "aws_request_id", None),
            },
            ensure_ascii=False,
        )
    )

    return {
        "n": n,
        "prime_count": prime_count,
        "elapsed_ms": round(elapsed_ms, 3),
        "note": "Try changing Lambda memory_size to observe CPU scaling.",
    }
