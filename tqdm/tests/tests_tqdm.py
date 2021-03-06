from __future__ import unicode_literals

import csv

try:
    from StringIO import StringIO
except:
    from io import StringIO

from tqdm import format_interval
from tqdm import format_meter
from tqdm import tqdm
from tqdm import trange


def test_format_interval():
    assert format_interval(60) == '01:00'
    assert format_interval(6160) == '1:42:40'
    assert format_interval(238113) == '66:08:33'


def test_format_meter():
    assert format_meter(0, 1000, 13) == \
        "|----------| 0/1000   0% [elapsed: " \
        "00:13 left: ?,  0.00 iters/sec]"
    assert format_meter(231, 1000, 392) == \
        "|##--------| 231/1000  23% [elapsed: " \
        "06:32 left: 21:44,  0.59 iters/sec]"
    assert format_meter(10000, 1000, 13) == \
        "10000 [elapsed: 00:13, 769.23 iters/sec]"


def test_nothing_fails():
    """ Just make sure we're able to iterate using tqdm """
    for i in tqdm(range(10)):
        pass


def test_iterate_over_csv_rows():
    # Create a test csv pseudo file
    test_csv_file = StringIO()
    writer = csv.writer(test_csv_file)
    for i in range(3):
        writer.writerow(['test', 'test', 'test'])
    test_csv_file.seek(0)

    # Test that nothing fails if we iterate over rows
    reader = csv.DictReader(test_csv_file, fieldnames=('row1', 'row2', 'row3'))
    for row in tqdm(reader):
        pass


def test_file_output():
    """ Tests that output to arbitrary file-like objects works """
    our_file = StringIO()
    for i in tqdm(range(3), file=our_file):
        if i == 1:
            our_file.seek(0)
            assert '0/3' in our_file.read()


def test_leave_option():
    """
    Tests that if leave=True, tqdm will leave the info
    about the last iteration on the screen
    """
    our_file = StringIO()
    for i in tqdm(range(3), file=our_file, leave=True):
        pass
    our_file.seek(0)
    assert '3/3 100%' in our_file.read()
    our_file.close()

    our_file2 = StringIO()
    for i in tqdm(range(3), file=our_file2, leave=False):
        pass
    our_file2.seek(0)
    assert '3/3 100%' not in our_file2.read()
    our_file2.close()


def test_trange():
    our_file = StringIO()
    for i in trange(3, file=our_file, leave=True):
        pass
    our_file.seek(0)
    assert '3/3 100%' in our_file.read()
    our_file.close()

    our_file2 = StringIO()
    for i in trange(3, file=our_file2, leave=False):
        pass
    our_file2.seek(0)
    assert '3/3 100%' not in our_file2.read()
    our_file2.close()


def test_min_interval():
    our_file = StringIO()
    for i in tqdm(range(3), file=our_file, mininterval=1e-10):
        pass
    our_file.seek(0)
    assert "|----------| 0/3   0% [elapsed: 00:00 left" in our_file.read()
