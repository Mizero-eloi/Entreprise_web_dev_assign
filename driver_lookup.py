"""
Kigali food-delivery driver lookup.

The app used to scan a list of 10,000 drivers on every customer request
(O(N)). This file builds a dictionary keyed by driver_id (the mapping loop)
so each request is an O(1) hash lookup, then reports the timing difference.
"""
from time import perf_counter

from maps import generate_drivers, sample_requests


def find_driver_slow(drivers, driver_id):
    """O(N): walk the list until the id matches, or fall off the end."""
    for driver in drivers:
        if driver["driver_id"] == driver_id:
            return driver
    return None


def build_driver_index(drivers):
    """Mapping loop: pay O(N) once so later lookups are O(1)."""
    by_id = {}
    for driver in drivers:
        by_id[driver["driver_id"]] = driver
    return by_id


def find_driver_fast(by_id, driver_id):
    """O(1): one hash-table access. Missing ids return None immediately."""
    return by_id.get(driver_id)


def same_results(drivers, by_id, requests):
    """Confirm both methods agree on every request (found or missing)."""
    for driver_id in requests:
        slow = find_driver_slow(drivers, driver_id)
        fast = find_driver_fast(by_id, driver_id)
        if slow is not fast:
            return False
    return True


def time_lookups(lookup, requests):
    """Run every request through lookup() and return elapsed seconds."""
    start = perf_counter()
    for driver_id in requests:
        lookup(driver_id)
    return perf_counter() - start


def format_seconds(seconds):
    if seconds >= 1:
        return f"{seconds:.3f} s"
    if seconds >= 0.001:
        return f"{seconds * 1_000:.3f} ms"
    return f"{seconds * 1_000_000:.1f} µs"


def print_metrics(n_drivers, n_requests, index_seconds, slow_seconds, fast_seconds):
    speedup = slow_seconds / fast_seconds if fast_seconds else float("inf")
    per_slow = slow_seconds / n_requests
    per_fast = fast_seconds / n_requests

    print()
    print("=" * 60)
    print("  TIME IMPROVEMENT METRICS")
    print("=" * 60)
    print(f"  Drivers in the raw list          {n_drivers:>12,}")
    print(f"  Customer lookup requests         {n_requests:>12,}")
    print()
    print(f"  Mapping loop (build index once)  {format_seconds(index_seconds):>12}")
    print(f"  O(N) sequential scan             {format_seconds(slow_seconds):>12}")
    print(f"  O(1) dictionary query            {format_seconds(fast_seconds):>12}")
    print()
    print(f"  Average time per O(N) request    {format_seconds(per_slow):>12}")
    print(f"  Average time per O(1) request    {format_seconds(per_fast):>12}")
    print(f"  Speedup                          {speedup:>11.0f}x")
    print("=" * 60)
    print()
    print("  Why this happens")
    print("  - O(N): each request may inspect every driver (worst case: missing id).")
    print("  - O(1): Python hashes the id and jumps to that slot.")
    print("  - The mapping loop is paid once. After that, every request is instant.")
    print()


def print_wwdc_pitch():
    print("=" * 60)
    print("  WWDC 2027 PITCH  —  “Find the rider. Instantly.”")
    print("=" * 60)
    print(
        """
  [Cold open — a map of Kigali, 10,000 dots]
  Every lunch rush, a customer taps “Find my driver.”
  Today that tap walks a list. Driver 1… driver 2… driver 10,000.
  If the id is missing, we still walk all the way to the end.
  That is O(N). On a city scale, that is latency you can feel.

  [Cut to one line of Python]
      by_id[driver["driver_id"]] = driver
  That is the whole product change. One mapping loop.
  We pay the walk once. Then the city is a dictionary.

  [Live demo]
  Same 10,000 drivers. Same 10,000 requests.
  Sequential scan: seconds.
  Dictionary query: milliseconds.
  The customer never sees a spinner. The rider is just… there.

  [Close]
  Apple Maps already knows where you are.
  This is how a delivery network knows who is coming —
  not by searching the city, but by naming it.
  Identity should be O(1). Everything else can wait.
"""
    )


def main():
    drivers = generate_drivers()
    requests = sample_requests(drivers)

    start = perf_counter()
    by_id = build_driver_index(drivers)
    index_seconds = perf_counter() - start

    if not same_results(drivers, by_id, requests[:200]):
        raise SystemExit("Slow and fast lookups disagreed — aborting.")

    slow_seconds = time_lookups(lambda i: find_driver_slow(drivers, i), requests)
    fast_seconds = time_lookups(lambda i: find_driver_fast(by_id, i), requests)

    demo_id = requests[0]
    demo_driver = find_driver_fast(by_id, demo_id)
    print(f"Loaded {len(drivers):,} drivers. Example lookup {demo_id}: {demo_driver['name']}")
    print_metrics(len(drivers), len(requests), index_seconds, slow_seconds, fast_seconds)
    print_wwdc_pitch()


if __name__ == "__main__":
    main()
