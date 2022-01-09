import logging


def check_file_name(fname):
	result = None
	period = []
	filename = fname.split('.')
	if 'GoogleEarningsReport' in filename[0] and filename[1] == 'csv':
		fname_parts = filename[0].split('_')
		if len(fname_parts) == 2:
			period = get_period(fname_parts[1])
			result = ('ga', period)
		elif len(fname_parts) == 1:
			print(type(fname_parts))
			period = get_period(fname_parts[0].split('-'))
			result = ('gg', period)
		else:
			print("Filename is not ok, too many parts (sep='_')")
			return
		year = period[0]
		month = period[1]
		if year == 0 or month == 0:
			print("Don't know the period of filename.")
			return
	else:
		print("Does not appear to be a Google earnings .csv report.")
	return result


def get_period(fname_restof):
	period, month, year = None, 0, 0
	others = fname_restof.split('-')
	if len(others) == 1:
		print(f"Filename error, period is: '{period}'")
		period = (0, 0)
		return period
	try:
		year = int(others[0])
	except ValueError:
		logging.exception(msg=f"Year convert failed, {period} errored out.")
		print(f"Year convert failed, {period} errored out.")
		period = (0, 0)
		return period
	try:
		month = int(others[1])
	except Exception:
		logging.exception(msg=f'Month convert failed, {period} errored out.')
		period = (0, 0)
		return period
	period = (year, month)
	return period


def main():
	check_file_name("GoogleEarningsReport_whatever.csv")


if __name__ == '__main__':
	main()
