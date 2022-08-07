import pytest

from stores.ciando import get_dates


@pytest.fixture()
def fpath():
    fnames = [
        'Q1-2022-0_somename',
        'Q2-2022-0_somename',
        'Q3-2022-0_somename',
        'Q4-2022-0_somename',
    ]
    yield iter(fnames)


def test_dates_from_filename_q1(fpath):
    fname = next(fpath)
    assert get_dates(fname) == {'10': '2021-10-15', '11': '2021-11-15', '12': '2021-12-15',
                                '01': '2022-01-15', '02': '2022-02-15', '03': '2022-03-15'}


def test_dates_from_filename_q2(fpath):
    next(fpath)
    fname = next(fpath)
    assert get_dates(fname) == {'01': '2022-01-15', '02': '2022-02-15', '03': '2022-03-15',
                                '04': '2022-04-15', '05': '2022-05-15', '06': '2022-06-15'}


def test_dates_from_filename_q3(fpath):
    next(fpath)
    next(fpath)
    fname = next(fpath)
    assert get_dates(fname) == {'04': '2022-04-15', '05': '2022-05-15', '06': '2022-06-15',
                                '07': '2022-07-15', '08': '2022-08-15', '09': '2022-09-15'}


def test_dates_from_filename_q4(fpath):
    next(fpath)
    next(fpath)
    next(fpath)
    fname = next(fpath)
    assert get_dates(fname) == {'07': '2022-07-15', '08': '2022-08-15', '09': '2022-09-15',
                                '10': '2022-10-15', '11': '2022-11-15', '12': '2022-12-15'}
