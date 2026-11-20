from dataclasses import dataclass
from enum import IntEnum


class StudentType(IntEnum):
    REGULAR = 1
    STAFF_CHILD = 2
    SCHOLARSHIP = 3


@dataclass(frozen=True)
class Course:
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
}


def tuition_fee(courses, kind, summer=False, discount=0, extras=()):
    hours = sum(course.hours for course in courses)
    total = hours * RATE_PER_HOUR * FEE_SHARE[kind]
    if total > LARGE_FEE_THRESHOLD:
        total -= LARGE_FEE_REDUCTION
    if summer:
        total += SUMMER_SURCHARGE
    return total - discount + sum(extras)


def fee_report(courses, kind, summer=False, discount=0):
    fee = tuition_fee(courses, kind, summer, discount)
    lines = []
    if kind in FEE_LABEL:
        lines.append(f"{FEE_LABEL[kind]}: {fee}")
    if fee > LARGE_FEE_THRESHOLD:
        lines.append("High fee")
    return "\n".join(lines)


def process_all(students):
    fees = {}
    for student in students:
        if student["type"] == StudentType.REGULAR:
            fee = tuition_fee(student["courses"], StudentType.REGULAR, student["summer"])
        if student["type"] == StudentType.STAFF_CHILD:
            fee = tuition_fee(student["courses"], StudentType.STAFF_CHILD, student["summer"])
        fees[student["name"]] = fee
    return fees


def print_fees(students):
    for name, fee in process_all(students).items():
        print(name, fee)
