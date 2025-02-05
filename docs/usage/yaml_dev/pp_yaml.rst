.. _history-files:

History files
-------------
Each history tarfile, again, is date-stamped with the date of the beginning of the segment, in YYYYMMDD format.
For example, for a 5-year experiment with 6-month segments, there will be 10 history files containing the
raw model output. Each history tarfile contains a segment's worth of time (in this case 6 months).::

  19790101.nc.tar  19800101.nc.tar  19810101.nc.tar  19820101.nc.tar  19830101.nc.tar
  19790701.nc.tar  19800701.nc.tar  19810701.nc.tar  19820701.nc.tar  19830701.nc.tar
