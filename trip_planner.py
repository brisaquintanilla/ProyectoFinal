from datetime import datetime, date
import argparse
import sys


def parse_date(s: str) -> date:
    try:
        return datetime.strptime(s, "%Y-%m-%d").date()
    except ValueError:
        raise ValueError("Formato de fecha inválido. Usa YYYY-MM-DD.")


def days_inclusive(start: date, end: date) -> int:
    delta = (end - start).days
    return delta + 1


def suggest_activities(days: int) -> dict:
    pool = [
        "Museos",
        "Cafés",
        "Monumentos",
        "Parques",
        "Mercados",
        "Teatros",
        "Galerías",
        "Excursiones",
    ]
    plan = {}
    for d in range(1, days + 1):
        # seleccionar dos actividades por día (o 1 si el viaje es de 1 día)
        count = 2 if days > 1 else 1
        activities = []
        for i in range(count):
            idx = (d - 1 + i) % len(pool)
            activities.append(pool[idx])
        plan[d] = activities
    return plan


def format_plan(plan: dict) -> str:
    lines = []
    for day, acts in plan.items():
        lines.append(f"Día {day}: {', '.join(acts)}")
    return "\n".join(lines)


def main(argv=None):
    parser = argparse.ArgumentParser(description="Planificador simple de viajes")
    parser.add_argument("--start", help="Fecha de inicio YYYY-MM-DD", required=False)
    parser.add_argument("--end", help="Fecha de fin YYYY-MM-DD", required=False)
    args = parser.parse_args(argv)

    try:
        if args.start and args.end:
            start = parse_date(args.start)
            end = parse_date(args.end)
        else:
            start = parse_date(input("Fecha inicio (YYYY-MM-DD): ").strip())
            end = parse_date(input("Fecha fin (YYYY-MM-DD): ").strip())
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)

    if end < start:
        print("Error: La fecha de fin es anterior a la fecha de inicio.")
        sys.exit(1)

    days = days_inclusive(start, end)
    print(f"Has planeado {days} día(s) en el destino (desde {start} hasta {end}).")

    plan = suggest_activities(days)
    print("\nPlan sugerido:")
    print(format_plan(plan))


if __name__ == "__main__":
    main()
