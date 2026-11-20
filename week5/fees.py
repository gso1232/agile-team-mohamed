"""Tuition fees for the Student Services App (refactored from legacy_fees.py)."""

from dataclasses import dataclass
from enum import IntEnum


class StudentType(IntEnum):
    """Kinds of student; the numbers match the old type codes 1/2/3."""

    REGULAR = 1
    STAFF_CHILD = 2
    SCHOLARSHIP = 3


@dataclass(frozen=True)
class Course:
    """A course the student is registered for."""

    hours: int


RATE_PER_HOUR = 350
LARGE_FEE_THRESHOLD = 6000
LARGE_FEE_REDUCTION = 200
SUMMER_SURCHARGE = 150

# Share of the full hourly rate each type of student pays.
FEE_SHARE = {
    StudentType.REGULAR: 1.0,
    StudentType.STAFF_CHILD: 0.5,
    StudentType.SCHOLARSHIP: 0.0,
}

FEE_LABEL = {
    StudentType.REGULAR: "Student fee",
    StudentType.STAFF_CHILD: "Staff child fee",
    StudentType.SCHOLARSHIP: "Scholarship fee",
}


def tuition_fee(courses, kind, summer=False, discount=0, extras=()):
    """Return the fee for one student's courses."""
    hours = sum(course.hours for course in courses)
    total = hours * RATE_PER_HOUR * FEE_SHARE[kind]
    if total > LARGE_FEE_THRESHOLD:
        total -= LARGE_FEE_REDUCTION
    if summer:
        total += SUMMER_SURCHARGE
    return total - discount + sum(extras)


def fee_report(courses, kind, summer=False, discount=0):
    """Return the fee as printable text, flagging high fees."""
    fee = tuition_fee(courses, kind, summer, discount)
    lines = [f"{FEE_LABEL[kind]}: {fee}"]
    if fee > LARGE_FEE_THRESHOLD:
        lines.append("High fee")
    return "\n".join(lines)


def process_all(students):
    """Return {name: fee} for every student, whatever their type."""
    return {
        student["name"]: tuition_fee(
            student["courses"], StudentType(student["type"]), student["summer"]
        )
        for student in students
    }


def print_fees(students):
    """Print one line per student with their fee."""
    for name, fee in process_all(students).items():
        print(name, fee)
