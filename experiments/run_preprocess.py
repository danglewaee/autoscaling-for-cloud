from __future__ import annotations

import argparse
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.data.preprocess import preprocess_trace


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Azure trace preprocessing.")
    parser.add_argument("--input", required=True, help="Raw trace path.")
    parser.add_argument("--output", required=True, help="Processed CSV path.")
    parser.add_argument("--top-k-apps", type=int, default=10)
    parser.add_argument("--min-invocations", type=int, default=1000)
    parser.add_argument("--bucket-seconds", type=int, default=60)
    parser.add_argument("--utilization-target", type=float, default=1.0)
    parser.add_argument("--nrows", type=int, default=None)
    args = parser.parse_args()

    frame = preprocess_trace(
        input_path=args.input,
        output_path=args.output,
        top_k_apps=args.top_k_apps,
        min_invocations=args.min_invocations,
        bucket_seconds=args.bucket_seconds,
        utilization_target=args.utilization_target,
        nrows=args.nrows,
    )
    print(frame.head(10).to_string(index=False))


if __name__ == "__main__":
    main()
