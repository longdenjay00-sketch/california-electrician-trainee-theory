#!/usr/bin/env python3
"""
tools/box_fill.py

California Electrical Code / NEC Article 314.16 Box Fill Volume Calculator.
Calculates required box volume in cubic inches and cubic centimeters based on:
- Conductor fill (NEC 314.16(B)(1))
- Internal clamp fill (NEC 314.16(B)(2))
- Support fitting / luminaire stud / hickey fill (NEC 314.16(B)(3))
- Device / equipment yoke fill (NEC 314.16(B)(4))
- Equipment grounding conductor fill (NEC 314.16(B)(5))
"""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any, Dict, List, Optional

# NEC Table 314.16(B) Volume Allowance Required per Conductor (cu in)
VOLUME_PER_CONDUCTOR_CU_IN: Dict[str, float] = {
    "18": 1.50,
    "16": 1.75,
    "14": 2.00,
    "12": 2.25,
    "10": 2.50,
    "8": 3.00,
    "6": 5.00,
}

# AWG ranking for determining largest conductor (larger number = smaller conductor)
AWG_ORDER: List[str] = ["18", "16", "14", "12", "10", "8", "6"]

# Standard Metal Boxes per NEC Table 314.16(A)
STANDARD_BOXES = [
    {"name": '4 x 1-1/4" Round/Octagonal', "volume_cu_in": 12.5},
    {"name": '4 x 1-1/2" Round/Octagonal', "volume_cu_in": 15.5},
    {"name": '4 x 2-1/8" Round/Octagonal', "volume_cu_in": 21.5},
    {"name": '4 x 1-1/4" Square', "volume_cu_in": 18.0},
    {"name": '4 x 1-1/2" Square', "volume_cu_in": 21.0},
    {"name": '4 x 2-1/8" Square', "volume_cu_in": 30.3},
    {"name": '4-11/16 x 1-1/2" Square', "volume_cu_in": 29.5},
    {"name": '4-11/16 x 2-1/8" Square', "volume_cu_in": 42.0},
    {"name": '3 x 2 x 2" Device Box', "volume_cu_in": 10.0},
    {"name": '3 x 2 x 2-1/2" Device Box', "volume_cu_in": 12.5},
    {"name": '3 x 2 x 3-1/2" Device Box', "volume_cu_in": 18.0},
]


def get_largest_awg(awg_list: List[str]) -> Optional[str]:
    """Returns the physically largest AWG from a list of AWG gauge strings."""
    valid = [awg for awg in awg_list if awg in VOLUME_PER_CONDUCTOR_CU_IN]
    if not valid:
        return None
    # Largest conductor has lowest index in reversed AWG_ORDER (6 is largest, 18 smallest)
    return max(valid, key=lambda a: AWG_ORDER.index(a))


def calculate_box_fill(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Computes box fill volume breakdown according to CEC 2022 / NEC 2020 Article 314.16.

    Expected input dictionary structure:
    {
      "conductors": [{"awg": "14", "count": 4}, {"awg": "12", "count": 2}],
      "has_internal_clamps": true,
      "support_fittings_count": 0,
      "devices": [{"yokes": 1, "largest_awg": "14"}],
      "ground_conductors": [{"awg": "14", "count": 2}]
    }
    """
    breakdown: List[Dict[str, Any]] = []
    total_cu_in = 0.0
    all_awgs: List[str] = []

    # 1. Conductor Fill - NEC 314.16(B)(1)
    conductors_input = data.get("conductors", [])
    for item in conductors_input:
        awg = str(item.get("awg", "14"))
        count = int(item.get("count", 0))
        if count <= 0:
            continue
        unit_vol = VOLUME_PER_CONDUCTOR_CU_IN.get(awg, 2.00)
        vol = round(count * unit_vol, 2)
        total_cu_in += vol
        all_awgs.append(awg)
        breakdown.append({
            "section": "314.16(B)(1)",
            "category": "Conductor Fill",
            "description": f"{count}x #{awg} AWG insulated conductor(s)",
            "multiplier": count,
            "unit_vol_cu_in": unit_vol,
            "total_vol_cu_in": vol,
        })

    # Find overall largest conductor for clamp and support allowances
    largest_box_awg = get_largest_awg(all_awgs) or "14"

    # 2. Internal Cable Clamps - NEC 314.16(B)(2)
    has_internal_clamps = bool(data.get("has_internal_clamps", False))
    if has_internal_clamps:
        clamp_awg = data.get("clamp_largest_awg") or largest_box_awg
        clamp_unit_vol = VOLUME_PER_CONDUCTOR_CU_IN.get(str(clamp_awg), 2.00)
        vol = clamp_unit_vol  # Single volume allowance regardless of clamp count
        total_cu_in += vol
        breakdown.append({
            "section": "314.16(B)(2)",
            "category": "Clamp Fill",
            "description": f"Internal cable clamp(s) (based on #{clamp_awg} AWG)",
            "multiplier": 1,
            "unit_vol_cu_in": clamp_unit_vol,
            "total_vol_cu_in": vol,
        })

    # 3. Support Fittings (Fixture Studs / Hickeys) - NEC 314.16(B)(3)
    support_count = int(data.get("support_fittings_count", 0))
    if support_count > 0:
        support_awg = data.get("support_largest_awg") or largest_box_awg
        support_unit_vol = VOLUME_PER_CONDUCTOR_CU_IN.get(str(support_awg), 2.00)
        vol = round(support_count * support_unit_vol, 2)
        total_cu_in += vol
        breakdown.append({
            "section": "314.16(B)(3)",
            "category": "Support Fittings",
            "description": f"{support_count} luminaire stud(s) or hickey(s) (based on #{support_awg} AWG)",
            "multiplier": support_count,
            "unit_vol_cu_in": support_unit_vol,
            "total_vol_cu_in": vol,
        })

    # 4. Device / Equipment Yokes - NEC 314.16(B)(4)
    devices_input = data.get("devices", [])
    for dev in devices_input:
        yokes = int(dev.get("yokes", 1))
        if yokes <= 0:
            continue
        dev_awg = str(dev.get("largest_awg") or largest_box_awg)
        dev_unit_vol = VOLUME_PER_CONDUCTOR_CU_IN.get(dev_awg, 2.00)
        vol = round(yokes * 2 * dev_unit_vol, 2)
        total_cu_in += vol
        breakdown.append({
            "section": "314.16(B)(4)",
            "category": "Device/Strap Fill",
            "description": f"{yokes} device yoke/strap(s) (2x allowance on #{dev_awg} AWG)",
            "multiplier": yokes * 2,
            "unit_vol_cu_in": dev_unit_vol,
            "total_vol_cu_in": vol,
        })

    # 5. Equipment Grounding Conductors - NEC 314.16(B)(5)
    grounds_input = data.get("ground_conductors", [])
    ground_awgs: List[str] = []
    total_grounds_count = 0
    for g in grounds_input:
        g_awg = str(g.get("awg", "14"))
        g_count = int(g.get("count", 0))
        total_grounds_count += g_count
        for _ in range(g_count):
            ground_awgs.append(g_awg)

    if total_grounds_count > 0:
        largest_g_awg = get_largest_awg(ground_awgs) or largest_box_awg
        g_unit_vol = VOLUME_PER_CONDUCTOR_CU_IN.get(largest_g_awg, 2.00)
        if total_grounds_count <= 4:
            g_multiplier = 1.0
        else:
            g_multiplier = 1.0 + 0.25 * (total_grounds_count - 4)

        vol = round(g_multiplier * g_unit_vol, 2)
        total_cu_in += vol
        breakdown.append({
            "section": "314.16(B)(5)",
            "category": "Grounding Fill",
            "description": (
                f"{total_grounds_count} EGC(s) (1.0 base"
                + (f" + {0.25 * (total_grounds_count - 4):.2f} extra" if total_grounds_count > 4 else "")
                + f" on #{largest_g_awg} AWG)"
            ),
            "multiplier": g_multiplier,
            "unit_vol_cu_in": g_unit_vol,
            "total_vol_cu_in": vol,
        })

    total_cu_in = round(total_cu_in, 2)
    total_cm3 = round(total_cu_in * 16.387064, 2)

    # Standard Box Selection Recommendations
    suitable_boxes = [
        box["name"] for box in STANDARD_BOXES if box["volume_cu_in"] >= total_cu_in
    ]

    return {
        "breakdown": breakdown,
        "total_cu_in": total_cu_in,
        "total_cm3": total_cm3,
        "recommended_standard_boxes": suitable_boxes,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Calculate electrical box fill volume.")
    parser.add_argument("--json", type=str, help="JSON input string")
    parser.add_argument("--file", type=str, help="JSON input file path")
    args = parser.parse_args()

    if args.json:
        data = json.loads(args.json)
    elif args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        # Read from stdin
        raw = sys.stdin.read().strip()
        data = json.loads(raw) if raw else {}

    result = calculate_box_fill(data)
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
