"""Lighting cache capacity 1024 -> 4096."""


def apply(b):
    c = b.code
    c(0x2565e5, "mov edx, 0x1000", "mov edx, 0x400")  # cache capacity 0x400 -> 0x1000
