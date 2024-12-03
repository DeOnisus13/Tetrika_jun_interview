def appearance(intervals: dict[str, list[int]]) -> int:
    """Функция подсчета времени, когда ученик и учитель одновременно были на уроке."""
    lesson_start, lesson_end = intervals['lesson']
    lesson_time = set(range(lesson_start, lesson_end))  # Время начала и конца урока

    pupil_intervals_ranges = [range(intervals['pupil'][i], intervals['pupil'][i + 1]) for i in
                              range(0, len(intervals['pupil']), 2)]
    tutor_intervals_ranges = [range(intervals['tutor'][i], intervals['tutor'][i + 1]) for i in
                              range(0, len(intervals['tutor']), 2)]

    pupil_time = set().union(*pupil_intervals_ranges)  # Группа времен, когда ученик был на уроке
    tutor_time = set().union(*tutor_intervals_ranges)  # Группа времен, когда учитель был на уроке

    result_time = lesson_time & pupil_time & tutor_time

    return len(result_time)
